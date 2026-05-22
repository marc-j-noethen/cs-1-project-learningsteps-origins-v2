param(
    [string]$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$requiredFiles = @(
    "README.md",
    ".gitignore",
    ".gitattributes",
    ".env.example",
    "SECURITY.md",
    ".github/dependabot.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/codeql.yml",
    "app/api/main.py",
    "app/.env.example",
    "docs/architecture/target-architecture.md",
    "docs/architecture/port-matrix.md",
    "docs/operations/deployment-runbook.md",
    "docs/operations/github-publishing.md",
    "evidence/verification-summary.md",
    "reports/final-project-report.md"
)

$publicSafeIgnore = @(
    ".git",
    "Project-Dev",
    "Project-Info",
    "app/venv",
    "evidence/raw"
)

$problems = New-Object System.Collections.Generic.List[string]

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "== $Title ==" -ForegroundColor Cyan
}

function Add-Problem {
    param([string]$Message)
    $null = $problems.Add($Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Test-RelativePath {
    param([string]$RelativePath)
    Test-Path -LiteralPath (Join-Path $Root $RelativePath)
}

Write-Section "Required Files"
foreach ($relativePath in $requiredFiles) {
    if (Test-RelativePath -RelativePath $relativePath) {
        Write-Host "[PASS] $relativePath" -ForegroundColor Green
    } else {
        Add-Problem "Missing required file: $relativePath"
    }
}

Write-Section "Unexpected Local-Only Files"
$forbiddenFiles = Get-ChildItem -LiteralPath $Root -Recurse -Force -File |
    Where-Object {
        $full = $_.FullName
        foreach ($segment in $publicSafeIgnore) {
            if ($full -like "*$segment*") { return $false }
        }

        $_.Name -eq ".env" -or
        $_.Extension -in @(".pem", ".key", ".p12", ".pfx", ".crt")
    }

if ($forbiddenFiles) {
    foreach ($file in $forbiddenFiles) {
        Add-Problem "Unexpected sensitive file present: $($file.FullName)"
    }
} else {
    Write-Host "[PASS] No unexpected .env files or key material detected." -ForegroundColor Green
}

Write-Section "TODO Scan"
$rg = Get-Command rg -ErrorAction SilentlyContinue
$todoMatches = $null
$useFallback = $true
if ($rg) {
    try {
        $todoMatches = & $rg.Source --hidden -n -F `
            -e "TODO" `
            -e "[Draft" `
            -e "[In Progress" `
            $Root `
            -g "!Project-Dev/**" `
            -g "!Project-Info/**" `
            -g "!.git/**" `
            -g "!scripts/repo-readiness-check.ps1"
        if ($LASTEXITCODE -eq 0 -and $todoMatches) {
            Add-Problem "Found unfinished markers:`n$todoMatches"
            $useFallback = $false
        } elseif ($LASTEXITCODE -le 1) {
            Write-Host "[PASS] No unfinished TODO or draft markers found in the public surface." -ForegroundColor Green
            $useFallback = $false
        } else {
            $todoMatches = $null
        }
    } catch {
        $todoMatches = $null
    }
}

if ($useFallback) {
    $fallbackMatches = Get-ChildItem -LiteralPath $Root -Recurse -Force -File |
        Where-Object {
            $_.FullName -notlike "*Project-Dev*" -and
            $_.FullName -notlike "*Project-Info*" -and
            $_.FullName -notlike "*.git*" -and
            $_.FullName -notlike "*scripts\\repo-readiness-check.ps1"
        } |
        Select-String -SimpleMatch -Pattern "TODO", "[Draft", "[In Progress"

    if ($fallbackMatches) {
        $formattedMatches = $fallbackMatches | ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line.Trim() }
        Add-Problem "Found unfinished markers:`n$($formattedMatches -join [Environment]::NewLine)"
    } else {
        Write-Host "[PASS] No unfinished TODO or draft markers found in the public surface." -ForegroundColor Green
    }
}

Write-Section "Python Compile Check"
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if ($python) {
    & $python.Source --version *> $null
    if ($LASTEXITCODE -eq 0) {
        Push-Location $Root
        try {
            & $python.Source -m compileall app/api app/tests app/test_api.py | Out-Host
            if ($LASTEXITCODE -ne 0) {
                Add-Problem "Python compile check failed."
            } else {
                Write-Host "[PASS] Python sources compiled successfully." -ForegroundColor Green
            }
        } finally {
            Pop-Location
        }
    } else {
        Write-Host "[WARN] Python launcher exists but no runnable interpreter was found. Skipping compile check." -ForegroundColor Yellow
    }
} else {
    Write-Host "[WARN] Python executable not found, skipping compile check." -ForegroundColor Yellow
}

Write-Section "Summary"
if ($problems.Count -gt 0) {
    Write-Host "$($problems.Count) issue(s) detected." -ForegroundColor Red
    exit 1
}

Write-Host "Repository looks ready for git initialization and GitHub publishing." -ForegroundColor Green
