const state = {
    authenticated: false,
    csrfToken: null,
    workshops: [],
    selectedId: null,
    query: "",
    category: "",
};

const elements = {
    authGate: document.querySelector("#authGate"),
    breadcrumbs: document.querySelector("#breadcrumbs"),
    categoryCount: document.querySelector("#categoryCount"),
    categoryFilters: document.querySelector("#categoryFilters"),
    closeDialogButton: document.querySelector("#closeDialogButton"),
    copyWorkshopButton: document.querySelector("#copyWorkshopButton"),
    createWorkshopButton: document.querySelector("#createWorkshopButton"),
    dashboardView: document.querySelector("#dashboardView"),
    descriptionText: document.querySelector("#descriptionText"),
    dialog: document.querySelector("#workshopDialog"),
    dialogTitle: document.querySelector("#dialogTitle"),
    editWorkshopButton: document.querySelector("#editWorkshopButton"),
    formMessage: document.querySelector("#formMessage"),
    globalSearch: document.querySelector("#globalSearch"),
    heroSummary: document.querySelector("#heroSummary"),
    heroTitle: document.querySelector("#heroTitle"),
    loginForm: document.querySelector("#loginForm"),
    loginMessage: document.querySelector("#loginMessage"),
    logoutButton: document.querySelector("#logoutButton"),
    metaCategory: document.querySelector("#metaCategory"),
    metaDifficulty: document.querySelector("#metaDifficulty"),
    metaDuration: document.querySelector("#metaDuration"),
    metaSlug: document.querySelector("#metaSlug"),
    metaStatus: document.querySelector("#metaStatus"),
    metaUpdated: document.querySelector("#metaUpdated"),
    objectivesList: document.querySelector("#objectivesList"),
    quickCreateButton: document.querySelector("#quickCreateButton"),
    quickDeleteButton: document.querySelector("#quickDeleteButton"),
    sidebarWorkshopGroups: document.querySelector("#sidebarWorkshopGroups"),
    stackChips: document.querySelector("#stackChips"),
    statCategories: document.querySelector("#statCategories"),
    statDraft: document.querySelector("#statDraft"),
    statPublished: document.querySelector("#statPublished"),
    statReview: document.querySelector("#statReview"),
    statTotal: document.querySelector("#statTotal"),
    statusMessage: document.querySelector("#statusMessage"),
    themeToggle: document.querySelector("#themeToggle"),
    workshopBadges: document.querySelector("#workshopBadges"),
    workshopCategory: document.querySelector("#workshopCategory"),
    workshopCount: document.querySelector("#workshopCount"),
    workshopDescriptionInput: document.querySelector("#workshopDescriptionInput"),
    workshopDifficulty: document.querySelector("#workshopDifficulty"),
    workshopDuration: document.querySelector("#workshopDuration"),
    workshopForm: document.querySelector("#workshopForm"),
    workshopId: document.querySelector("#workshopId"),
    workshopObjectives: document.querySelector("#workshopObjectives"),
    workshopPublished: document.querySelector("#workshopPublished"),
    workshopStack: document.querySelector("#workshopStack"),
    workshopStatus: document.querySelector("#workshopStatus"),
    workshopSummary: document.querySelector("#workshopSummary"),
    workshopSummaryInput: document.querySelector("#workshopSummaryInput"),
    workshopTitle: document.querySelector("#workshopTitle"),
    deliveryList: document.querySelector("#deliveryList"),
    cancelDialogButton: document.querySelector("#cancelDialogButton"),
};

function createNode(tagName, className, textContent) {
    const node = document.createElement(tagName);
    if (className) {
        node.className = className;
    }
    if (typeof textContent === "string") {
        node.textContent = textContent;
    }
    return node;
}

function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("swb-theme", theme);
    elements.themeToggle.textContent = theme === "dark" ? "Light mode" : "Dark mode";
}

function initTheme() {
    const savedTheme = localStorage.getItem("swb-theme") || "dark";
    setTheme(savedTheme);
}

function formatDate(value) {
    if (!value) {
        return "-";
    }
    return new Intl.DateTimeFormat("de-DE", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(new Date(value));
}

function setStatusMessage(message, isError = false) {
    elements.statusMessage.textContent = message || "";
    elements.statusMessage.style.color = isError ? "var(--danger)" : "var(--muted)";
}

function setFormMessage(message, isError = false) {
    elements.formMessage.textContent = message || "";
    elements.formMessage.style.color = isError ? "var(--danger)" : "var(--muted)";
}

function setLoginMessage(message, isError = false) {
    elements.loginMessage.textContent = message || "";
    elements.loginMessage.style.color = isError ? "var(--danger)" : "var(--muted)";
}

async function httpRequest(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
        const error = new Error(payload.detail || "Request failed.");
        error.status = response.status;
        throw error;
    }
    return payload;
}

function getSelectedWorkshop() {
    return state.workshops.find((workshop) => workshop.id === state.selectedId) || null;
}

function buildBadge(text, variant = "") {
    const badge = createNode("span", `badge ${variant}`.trim(), text);
    return badge;
}

function renderBadges(workshop) {
    elements.workshopBadges.replaceChildren();
    if (!workshop) {
        return;
    }
    const statusVariant = workshop.status === "published"
        ? "badge-success"
        : workshop.status === "review"
            ? "badge-warning"
            : "badge-danger";
    elements.workshopBadges.append(
        buildBadge(workshop.category),
        buildBadge(workshop.status, statusVariant),
        buildBadge(workshop.difficulty),
        buildBadge(workshop.published ? "visible" : "private"),
    );
}

function renderObjectives(workshop) {
    elements.objectivesList.replaceChildren();
    if (!workshop) {
        return;
    }
    workshop.objectives.forEach((objective) => {
        elements.objectivesList.append(createNode("li", "", objective));
    });
}

function renderStack(workshop) {
    elements.stackChips.replaceChildren();
    if (!workshop) {
        return;
    }
    workshop.stack.forEach((item) => {
        elements.stackChips.append(createNode("span", "chip", item));
    });
}

function renderDeliveryNotes(workshop) {
    elements.deliveryList.replaceChildren();
    if (!workshop) {
        return;
    }
    const notes = [
        `Geplante Dauer: ${workshop.duration_hours} Stunden`,
        `Workflow-Status: ${workshop.status}`,
        workshop.published
            ? "Workshop ist fuer deine Library sichtbar."
            : "Workshop bleibt intern, bis du ihn veroeffentlichst.",
        `Letzte Aktualisierung: ${formatDate(workshop.updated_at)}`,
    ];
    notes.forEach((item) => {
        elements.deliveryList.append(createNode("li", "", item));
    });
}

function renderMeta(workshop) {
    elements.metaStatus.textContent = workshop ? workshop.status : "-";
    elements.metaDifficulty.textContent = workshop ? workshop.difficulty : "-";
    elements.metaDuration.textContent = workshop ? `${workshop.duration_hours} h` : "-";
    elements.metaCategory.textContent = workshop ? workshop.category : "-";
    elements.metaSlug.textContent = workshop ? workshop.slug : "-";
    elements.metaUpdated.textContent = workshop ? formatDate(workshop.updated_at) : "-";
}

function renderHero(workshop) {
    if (!workshop) {
        elements.heroTitle.textContent = "Workshop auswaehlen";
        elements.heroSummary.textContent = "Waehle links einen Workshop aus oder lege direkt einen neuen Themenbaustein an.";
        elements.breadcrumbs.textContent = "Home / Workshops";
        elements.workshopSummary.textContent = "Noch kein Workshop ausgewaehlt.";
        elements.descriptionText.textContent = "Sobald ein Workshop aktiv ist, erscheinen hier die ausformulierten Inhalte.";
        elements.editWorkshopButton.disabled = true;
        elements.copyWorkshopButton.disabled = true;
        elements.quickDeleteButton.disabled = true;
        renderBadges(null);
        renderMeta(null);
        renderObjectives(null);
        renderStack(null);
        renderDeliveryNotes(null);
        return;
    }

    elements.heroTitle.textContent = workshop.title;
    elements.heroSummary.textContent = workshop.summary;
    elements.breadcrumbs.textContent = `Home / Workshops / ${workshop.category} / ${workshop.title}`;
    elements.workshopSummary.textContent = workshop.summary;
    elements.descriptionText.textContent = workshop.description;
    elements.editWorkshopButton.disabled = false;
    elements.copyWorkshopButton.disabled = false;
    elements.quickDeleteButton.disabled = false;
    renderBadges(workshop);
    renderMeta(workshop);
    renderObjectives(workshop);
    renderStack(workshop);
    renderDeliveryNotes(workshop);
}

function renderCategoryFilters(workshops) {
    const categories = Array.from(new Set(workshops.map((workshop) => workshop.category))).sort();
    elements.categoryCount.textContent = String(categories.length);
    elements.categoryFilters.replaceChildren();

    const createFilter = (label, value) => {
        const button = createNode("button", "filter-button", label);
        button.type = "button";
        if (state.category === value) {
            button.classList.add("is-active");
        }
        button.addEventListener("click", () => {
            state.category = value;
            loadDashboard();
        });
        return button;
    };

    elements.categoryFilters.append(createFilter("Alle Themen", ""));
    categories.forEach((category) => {
        elements.categoryFilters.append(createFilter(category, category));
    });
}

function renderSidebar(workshops) {
    elements.workshopCount.textContent = String(workshops.length);
    elements.sidebarWorkshopGroups.replaceChildren();

    const groups = new Map();
    workshops.forEach((workshop) => {
        if (!groups.has(workshop.category)) {
            groups.set(workshop.category, []);
        }
        groups.get(workshop.category).push(workshop);
    });

    if (!workshops.length) {
        const empty = createNode("p", "lead-text", "Noch keine Workshops gefunden. Passe den Filter an oder lege direkt einen neuen Workshop an.");
        elements.sidebarWorkshopGroups.append(empty);
        return;
    }

    groups.forEach((items, category) => {
        const wrapper = createNode("section", "workshop-group");
        const heading = createNode("h3", "", category);
        wrapper.append(heading);

        items.forEach((workshop) => {
            const button = createNode("button", "workshop-link");
            button.type = "button";
            if (workshop.id === state.selectedId) {
                button.classList.add("is-active");
            }

            const copy = createNode("span", "workshop-link-copy");
            copy.append(
                createNode("span", "workshop-link-title", workshop.title),
                createNode("small", "", workshop.summary),
            );

            const pill = buildBadge(workshop.status);
            button.append(copy, pill);
            button.addEventListener("click", () => {
                state.selectedId = workshop.id;
                renderAll();
            });
            wrapper.append(button);
        });

        elements.sidebarWorkshopGroups.append(wrapper);
    });
}

function renderStats(snapshot) {
    elements.statTotal.textContent = String(snapshot.stats.total);
    elements.statCategories.textContent = String(snapshot.stats.categories);
    elements.statPublished.textContent = String(snapshot.stats.published);
    elements.statReview.textContent = String(snapshot.stats.review);
    elements.statDraft.textContent = String(snapshot.stats.draft);
}

function renderAll() {
    renderCategoryFilters(state.workshops);
    renderSidebar(state.workshops);
    renderHero(getSelectedWorkshop());
}

function parseObjectives(value) {
    return value
        .split("\n")
        .map((item) => item.trim())
        .filter(Boolean);
}

function parseStack(value) {
    return value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean);
}

function openDialog(mode, workshop = null) {
    elements.workshopForm.dataset.mode = mode;
    elements.dialogTitle.textContent = mode === "edit" ? "Workshop bearbeiten" : "Workshop anlegen";
    setFormMessage("");

    if (workshop) {
        elements.workshopId.value = workshop.id;
        elements.workshopTitle.value = workshop.title;
        elements.workshopCategory.value = workshop.category;
        elements.workshopStatus.value = workshop.status;
        elements.workshopDifficulty.value = workshop.difficulty;
        elements.workshopDuration.value = String(workshop.duration_hours);
        elements.workshopPublished.checked = workshop.published;
        elements.workshopSummaryInput.value = workshop.summary;
        elements.workshopDescriptionInput.value = workshop.description;
        elements.workshopObjectives.value = workshop.objectives.join("\n");
        elements.workshopStack.value = workshop.stack.join(", ");
    } else {
        elements.workshopForm.reset();
        elements.workshopId.value = "";
        elements.workshopPublished.checked = false;
    }

    elements.dialog.showModal();
}

function closeDialog() {
    elements.dialog.close();
}

async function refreshSession() {
    const session = await httpRequest("/api/auth/session", { method: "GET" });
    state.authenticated = session.authenticated;
    state.csrfToken = session.csrfToken;
    elements.authGate.hidden = session.authenticated;
    elements.dashboardView.hidden = !session.authenticated;
    elements.logoutButton.hidden = !session.authenticated;
}

async function loadDashboard() {
    if (!state.authenticated) {
        return;
    }
    const params = new URLSearchParams();
    if (state.query) {
        params.set("q", state.query);
    }
    if (state.category) {
        params.set("category", state.category);
    }

    const snapshot = await httpRequest(`/api/workshops?${params.toString()}`, { method: "GET" });
    state.workshops = snapshot.workshops;
    renderStats(snapshot);

    if (!state.workshops.some((workshop) => workshop.id === state.selectedId)) {
        state.selectedId = snapshot.selectedId;
    }

    renderAll();
}

async function submitLogin(event) {
    event.preventDefault();
    setLoginMessage("Authentifizierung laeuft...");
    try {
        await httpRequest("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({
                username: document.querySelector("#loginUsername").value,
                password: document.querySelector("#loginPassword").value,
            }),
        });
        await refreshSession();
        await loadDashboard();
        setLoginMessage("Login erfolgreich.");
    } catch (error) {
        setLoginMessage(error.message, true);
    }
}

async function submitWorkshop(event) {
    event.preventDefault();
    setFormMessage("Workshop wird gespeichert...");

    const workshop = {
        title: elements.workshopTitle.value,
        category: elements.workshopCategory.value,
        status: elements.workshopStatus.value,
        difficulty: elements.workshopDifficulty.value,
        duration_hours: Number(elements.workshopDuration.value),
        summary: elements.workshopSummaryInput.value,
        description: elements.workshopDescriptionInput.value,
        objectives: parseObjectives(elements.workshopObjectives.value),
        stack: parseStack(elements.workshopStack.value),
        published: elements.workshopPublished.checked,
    };

    const mode = elements.workshopForm.dataset.mode;
    const workshopId = elements.workshopId.value;
    const url = mode === "edit" ? `/api/workshops/${workshopId}` : "/api/workshops";
    const method = mode === "edit" ? "PUT" : "POST";

    try {
        const payload = await httpRequest(url, {
            method,
            headers: { "X-CSRF-Token": state.csrfToken || "" },
            body: JSON.stringify(workshop),
        });
        closeDialog();
        state.selectedId = payload.workshop.id;
        setStatusMessage(payload.detail);
        await loadDashboard();
    } catch (error) {
        setFormMessage(error.message, true);
    }
}

async function handleDelete() {
    const selected = getSelectedWorkshop();
    if (!selected) {
        return;
    }

    const confirmed = window.confirm(`Workshop "${selected.title}" wirklich loeschen?`);
    if (!confirmed) {
        return;
    }

    try {
        const payload = await httpRequest(`/api/workshops/${selected.id}`, {
            method: "DELETE",
            headers: { "X-CSRF-Token": state.csrfToken || "" },
        });
        state.selectedId = null;
        setStatusMessage(payload.detail);
        await loadDashboard();
    } catch (error) {
        setStatusMessage(error.message, true);
    }
}

async function handleLogout() {
    try {
        await httpRequest("/api/auth/logout", {
            method: "POST",
            headers: { "X-CSRF-Token": state.csrfToken || "" },
        });
        state.authenticated = false;
        state.csrfToken = null;
        state.workshops = [];
        state.selectedId = null;
        elements.authGate.hidden = false;
        elements.dashboardView.hidden = true;
        elements.logoutButton.hidden = true;
        setStatusMessage("");
        setLoginMessage("Abgemeldet.");
    } catch (error) {
        setStatusMessage(error.message, true);
    }
}

async function copyBriefing() {
    const workshop = getSelectedWorkshop();
    if (!workshop) {
        return;
    }

    const markdown = [
        `# ${workshop.title}`,
        "",
        `- Kategorie: ${workshop.category}`,
        `- Status: ${workshop.status}`,
        `- Schwierigkeit: ${workshop.difficulty}`,
        `- Dauer: ${workshop.duration_hours} Stunden`,
        "",
        workshop.summary,
        "",
        "## Lernziele",
        ...workshop.objectives.map((objective) => `- ${objective}`),
        "",
        "## Beschreibung",
        workshop.description,
        "",
        "## Stack",
        ...workshop.stack.map((item) => `- ${item}`),
    ].join("\n");

    await navigator.clipboard.writeText(markdown);
    setStatusMessage("Workshop-Briefing in die Zwischenablage kopiert.");
}

function wireEvents() {
    elements.themeToggle.addEventListener("click", () => {
        const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        setTheme(nextTheme);
    });

    elements.loginForm.addEventListener("submit", submitLogin);
    elements.workshopForm.addEventListener("submit", submitWorkshop);

    [elements.createWorkshopButton, elements.quickCreateButton].forEach((button) => {
        button.addEventListener("click", () => openDialog("create"));
    });

    elements.editWorkshopButton.addEventListener("click", () => {
        const workshop = getSelectedWorkshop();
        if (workshop) {
            openDialog("edit", workshop);
        }
    });

    elements.copyWorkshopButton.addEventListener("click", () => {
        copyBriefing().catch((error) => setStatusMessage(error.message, true));
    });

    elements.quickDeleteButton.addEventListener("click", () => {
        handleDelete().catch((error) => setStatusMessage(error.message, true));
    });

    elements.logoutButton.addEventListener("click", () => {
        handleLogout().catch((error) => setStatusMessage(error.message, true));
    });

    elements.globalSearch.addEventListener("input", async (event) => {
        state.query = event.target.value.trim();
        await loadDashboard();
    });

    elements.closeDialogButton.addEventListener("click", closeDialog);
    elements.cancelDialogButton.addEventListener("click", closeDialog);
}

async function init() {
    initTheme();
    wireEvents();

    try {
        await refreshSession();
        if (state.authenticated) {
            await loadDashboard();
        }
    } catch (error) {
        setLoginMessage(error.message, true);
    }
}

init();
