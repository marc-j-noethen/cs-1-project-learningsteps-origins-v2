# Deployment Runbook

## Goal

Provision and validate a secure 2-tier Azure deployment for the portfolio workload:

- internet-accessible FastAPI application tier
- private PostgreSQL tier
- least-privilege network controls

## Preconditions

- Azure subscription with rights to create networking and virtual machines
- SSH key pair available for administrative access
- A repository URL or deployment artifact for the application bundle in `app/`
- A secret handling plan for database credentials and `SESSION_SECRET`

## Build Order

### 1. Create the resource group and network

```bash
az group create -n rg-learningsteps-dev -l westeurope

az network vnet create \
  -g rg-learningsteps-dev \
  -n vnet-learningsteps \
  --address-prefix 10.10.0.0/16 \
  --subnet-name snet-public-api \
  --subnet-prefixes 10.10.1.0/24

az network vnet subnet create \
  -g rg-learningsteps-dev \
  --vnet-name vnet-learningsteps \
  -n snet-private-db \
  --address-prefixes 10.10.2.0/24
```

### 2. Define and attach the NSGs

```bash
az network nsg create -g rg-learningsteps-dev -n nsg-db

az network nsg rule create \
  -g rg-learningsteps-dev \
  --nsg-name nsg-db \
  -n allow-postgres-from-api-subnet \
  --priority 100 \
  --access Allow \
  --protocol Tcp \
  --direction Inbound \
  --source-address-prefixes 10.10.1.0/24 \
  --source-port-ranges "*" \
  --destination-address-prefixes "*" \
  --destination-port-ranges 5432

az network vnet subnet update \
  -g rg-learningsteps-dev \
  --vnet-name vnet-learningsteps \
  -n snet-private-db \
  --network-security-group nsg-db
```

> During the original implementation, the effective API ingress rule ended up living on a NIC-bound NSG rather than the intended subnet NSG. Keep that possibility in mind during validation.

### 3. Provision the virtual machines

```bash
az network public-ip create \
  -g rg-learningsteps-dev \
  -n pip-api-vm \
  --sku Standard \
  --allocation-method Static

az vm create \
  -g rg-learningsteps-dev \
  -n vm-api-learningsteps \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --vnet-name vnet-learningsteps \
  --subnet snet-public-api \
  --public-ip-address pip-api-vm

az vm create \
  -g rg-learningsteps-dev \
  -n vm-db-learningsteps \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --vnet-name vnet-learningsteps \
  --subnet snet-private-db \
  --public-ip-address ""
```

### 4. Configure PostgreSQL on the DB VM

```bash
az vm run-command invoke \
  -g rg-learningsteps-dev \
  -n vm-db-learningsteps \
  --command-id RunShellScript \
  --scripts \
"set -e" \
"sudo apt-get update -y" \
"sudo DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib" \
"PGVER=\$(ls /etc/postgresql | head -n1)" \
"CONF=/etc/postgresql/\$PGVER/main/postgresql.conf" \
"HBA=/etc/postgresql/\$PGVER/main/pg_hba.conf" \
"sudo sed -i \"s|^#\\?listen_addresses =.*|listen_addresses = '*'|\" \$CONF" \
"grep -q \"host learning_journal postgres 10.10.1.0/24 md5\" \$HBA || echo \"host learning_journal postgres 10.10.1.0/24 md5\" | sudo tee -a \$HBA" \
"sudo systemctl restart postgresql" \
"sudo systemctl is-active postgresql"
```

Create the database and user credentials separately so the public runbook does not embed real secrets.

### 5. Validate internal DB reachability from the API tier

```bash
az vm run-command invoke \
  -g rg-learningsteps-dev \
  -n vm-api-learningsteps \
  --command-id RunShellScript \
  --scripts \
"set -e" \
"sudo apt-get update -y" \
"sudo DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-client" \
"PGPASSWORD=<db_password> psql -h 10.10.2.4 -U postgres -d learning_journal -c '\\conninfo'"
```

### 6. Deploy the application as a systemd service

```bash
az vm run-command invoke \
  -g rg-learningsteps-dev \
  -n vm-api-learningsteps \
  --command-id RunShellScript \
  --scripts \
"set -e" \
"sudo apt-get update -y" \
"sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git python3-venv python3-pip" \
"if [ ! -d /opt/learningsteps-origins/.git ]; then sudo git clone <your-repo-url> /opt/learningsteps-origins; fi" \
"cd /opt/learningsteps-origins/app && sudo python3 -m venv venv && sudo /opt/learningsteps-origins/app/venv/bin/pip install -r api/requirements.txt" \
"cat <<'EOF' | sudo tee /opt/learningsteps-origins/app/.env >/dev/null
APP_ENV=production
SWB_APP_NAME=SWB | Second-Workshop-Brain
DATABASE_URL=postgresql://postgres:<db_password>@10.10.2.4:5432/learning_journal
SWB_ADMIN_USERNAME=swb-admin
SWB_ADMIN_PASSWORD_HASH=<hashed_admin_password>
SESSION_SECRET=<long_random_secret>
SWB_ALLOWED_HOSTS=<public_host_or_ip>
SWB_SESSION_HTTPS_ONLY=false
SWB_SEED_DEMO_DATA=false
SWB_ENABLE_DOCS=false
EOF" \
"cat <<'EOF' | sudo tee /etc/systemd/system/learningsteps-api.service >/dev/null
[Unit]
Description=LearningSteps Origins FastAPI service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/learningsteps-origins/app/api
EnvironmentFile=/opt/learningsteps-origins/app/.env
ExecStart=/opt/learningsteps-origins/app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 80
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF" \
"sudo systemctl daemon-reload" \
"sudo systemctl enable --now learningsteps-api" \
"sudo systemctl is-active learningsteps-api"
```

### 7. Validate the effective policy path

```bash
az network watcher test-ip-flow \
  -g rg-learningsteps-dev \
  --vm vm-api-learningsteps \
  --direction Inbound \
  --protocol TCP \
  --local 10.10.1.4:80 \
  --remote 8.8.8.8:50000 \
  -o table
```

If traffic is denied while the app is healthy, inspect the NIC security group:

```bash
az network nic show \
  -g rg-learningsteps-dev \
  -n vm-api-learningstepsVMNic \
  --query "networkSecurityGroup.id" -o tsv
```

Then correct the effective NSG rather than only the intended subnet NSG.

### 8. Restrict SSH to an approved source

```bash
az network nsg rule update \
  -g rg-learningsteps-dev \
  --nsg-name vm-api-learningstepsNSG \
  -n default-allow-ssh \
  --source-address-prefixes <your-admin-ip>/32
```

## Verification Checklist

- `curl -I http://<public-endpoint>/docs` returns a successful HTTP response when docs are enabled for validation
- `test-ip-flow` shows `Allow` for intended HTTP and approved SSH traffic
- `test-ip-flow` shows `Deny` for unapproved SSH sources
- PostgreSQL is reachable from the API VM but not from the public internet
- Data persists after restarting the API service

## Operational Notes

- Keep the public repo free from real IP allowlists, secrets, and personal access details.
- If you move beyond the learning phase, add HTTPS, Key Vault, Bastion/JIT, and centralized logging before treating the workload as production-ready.
