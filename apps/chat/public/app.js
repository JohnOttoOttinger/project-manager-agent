(() => {
  "use strict";

  const DEFAULT_CONFIG = {
    name: "Project Manager",
    subtitle:
      "Turn meetings, documents, and project ideas into clear next actions.",
    welcomeMessage:
      "Hello! I’m your Project Manager. Add a meeting transcript or tell me what you’re working on, and I’ll help turn it into decisions, plans, and safe next actions.",
    primaryColour: "#6D4AFF",
    examplePrompts: [
      "Turn these meeting notes into decisions and action items",
      "Build a practical project plan from this document",
      "Show me the highest-priority work in my local project",
    ],
  };
  const DEFAULT_AGENTS = [
    {
      id: "project-manager",
      name: "Project Manager",
      description:
        "Plans projects, analyses meetings, and turns decisions into safe next actions.",
      status: "active",
      examplePrompts: DEFAULT_CONFIG.examplePrompts,
    },
    {
      id: "sales",
      name: "Sales",
      description: "Researches prospects, drafts replies, and turns calls into proposals.",
      status: "active",
      examplePrompts: [
        "Draft a reply to this enquiry that just came in",
        "Turn these call notes into a recap and a proposal",
        "Write a cold email to this person",
      ],
    },
    {
      id: "marketing",
      name: "Marketing",
      description: "Plans campaigns and creates grounded content from supplied or researched evidence.",
      status: "active",
      examplePrompts: [
        "Turn these customer notes into three grounded content themes",
        "Build a practical campaign plan from this brief",
        "Review this draft and identify unsupported claims",
      ],
    },
    {
      id: "investment",
      name: "Investment",
      description: "Reviews grants, funding evidence, and business updates without making financial decisions.",
      status: "active",
      examplePrompts: [
        "Compare these two funding opportunities from the supplied documents",
        "Turn this grant brief into eligibility questions and deadlines",
        "Draft a factual investor update from these notes",
      ],
    },
    {
      id: "bookkeeping",
      name: "Bookkeeping",
      description: "Prepares coding-review suggestions and questions for the user to complete in their accounting system.",
      status: "active",
      examplePrompts: [
        "Review these transactions and suggest coding categories with confidence",
        "List the questions I should take to my bookkeeper from this statement",
        "Summarise the unpaid invoices in this document",
      ],
    },
  ];
  const STORAGE_KEY = "ai-solopreneur-chat-session";
  const MAX_DOCUMENTS = 3;
  const LARGE_PASTE_THRESHOLD = 4_000;

  const elements = {
    agentPanel: document.querySelector(".agent-panel"),
    agentInitials: document.querySelector("#agent-initials"),
    agentList: document.querySelector("#agent-list"),
    agentName: document.querySelector("#agent-name"),
    agentSubtitle: document.querySelector("#agent-subtitle"),
    attachmentMenu: document.querySelector("#attachment-menu"),
    attachmentMenuButton: document.querySelector("#attachment-menu-button"),
    characterCount: document.querySelector("#character-count"),
    conversation: document.querySelector("#conversation"),
    conversationAgentName: document.querySelector("#conversation-agent-name"),
    conversationTitleText: document.querySelector("#conversation-title-text"),
    documentList: document.querySelector("#document-list"),
    documentStatus: document.querySelector("#document-status"),
    fileInput: document.querySelector("#file-input"),
    form: document.querySelector("#chat-form"),
    historyButton: document.querySelector("#history-button"),
    historyClose: document.querySelector("#history-close"),
    historyList: document.querySelector("#history-list"),
    historyMore: document.querySelector("#history-more"),
    historyNew: document.querySelector("#history-new"),
    historySearchForm: document.querySelector("#history-search-form"),
    historySearchInput: document.querySelector("#history-search-input"),
    historyStatus: document.querySelector("#history-status"),
    input: document.querySelector("#message-input"),
    mobileAgentInitials: document.querySelector("#mobile-agent-initials"),
    pasteButton: document.querySelector("#paste-button"),
    pasteCancel: document.querySelector("#paste-cancel"),
    pasteDialog: document.querySelector("#paste-dialog"),
    pastedName: document.querySelector("#pasted-name"),
    pastedText: document.querySelector("#pasted-text"),
    pasteForm: document.querySelector("#paste-form"),
    prospectAddCancel: document.querySelector("#prospect-add-cancel"),
    prospectAddCompany: document.querySelector("#prospect-add-company"),
    prospectAddDialog: document.querySelector("#prospect-add-dialog"),
    prospectAddForm: document.querySelector("#prospect-add-form"),
    prospectAddList: document.querySelector("#prospect-add-list"),
    prospectAddStatus: document.querySelector("#prospect-add-status"),
    prospectDialog: document.querySelector("#prospect-dialog"),
    prospectDialogBody: document.querySelector("#prospect-dialog-body"),
    prospectDialogClose: document.querySelector("#prospect-dialog-close"),
    prospectDialogSubtitle: document.querySelector("#prospect-dialog-subtitle"),
    prospectDialogTitle: document.querySelector("#prospect-dialog-title"),
    profileAgentName: document.querySelector("#profile-agent-name"),
    profileAvatar: document.querySelector("#profile-avatar"),
    profileAvatarButton: document.querySelector("#profile-avatar-button"),
    profileAvatarInitials: document.querySelector("#profile-avatar-initials"),
    profileBoundaries: document.querySelector("#profile-boundaries"),
    profileBusinessName: document.querySelector("#profile-business-name"),
    profileCancel: document.querySelector("#profile-cancel"),
    profileDialog: document.querySelector("#profile-dialog"),
    profileForm: document.querySelector("#profile-form"),
    profileOffer: document.querySelector("#profile-offer"),
    profilePrice: document.querySelector("#profile-price"),
    profileSample1: document.querySelector("#profile-sample-1"),
    profileSample2: document.querySelector("#profile-sample-2"),
    profileSave: document.querySelector("#profile-save"),
    profileStatus: document.querySelector("#profile-status"),
    profileVoice: document.querySelector("#profile-voice"),
    profileWho: document.querySelector("#profile-who"),
    requestStatus: document.querySelector("#request-status"),
    resetButton: document.querySelector("#reset-button"),
    sendButton: document.querySelector("#send-button"),
    sendButtonLabel: document.querySelector("#send-button-label"),
    suggestionList: document.querySelector("#suggestion-list"),
    suggestions: document.querySelector("#suggestions"),
    uploadButton: document.querySelector("#upload-button"),
    brandBar: document.querySelector("#brand-bar"),
    brandToggle: document.querySelector("#brand-toggle"),
    brandNote: document.querySelector("#brand-note"),
    quickActions: document.querySelector("#quick-actions"),
    quickActionsSection: document.querySelector("#quick-actions-section"),
    pipelinePanel: document.querySelector("#pipeline-panel"),
    pipelineBadge: document.querySelector("#pipeline-badge"),
    pipelineContent: document.querySelector("#pipeline-content"),
    stageTitle: document.querySelector("#stage-title"),
    stageBrandLabel: document.querySelector("#stage-brand-label"),
    sectionTabs: document.querySelector("#section-tabs"),
    stageBody: document.querySelector("#stage-body"),
    chatToggle: document.querySelector("#chat-toggle"),
    chatDrawer: document.querySelector("#chat-drawer"),
    chatScrim: document.querySelector("#chat-scrim"),
    drawerClose: document.querySelector("#drawer-close"),
    pipelineNavButton: document.querySelector("#pipeline-nav-button"),
    sidebarBrand: document.querySelector("#sidebar-brand"),
    sidebarBrandToggle: document.querySelector("#sidebar-brand-toggle"),
  };

  const BRAND_STORAGE_KEY = "ai-solopreneur-active-brand";

  let sessionId = loadOrCreateSession();
  let requestInProgress = false;
  let documentRequestInProgress = false;
  let loadingMessage = null;
  let agents = DEFAULT_AGENTS;
  let activeAgentId = "project-manager";
  let uploadedDocuments = [];
  let sessionDocuments = [];
  let profile = null;
  let pendingAvatarDataUrl = "";
  let conversations = [];
  let nextConversationCursor = null;
  let currentMessages = [];
  let nextMessageBefore = null;
  let activeConversationTitle = "New conversation";
  let pendingRefreshTimer = null;
  let articleRefreshTimer = null;
  // Stage state: the centre shows a per-agent dashboard ("agent" view)
  // or the cross-brand Content Pipeline board ("pipeline" view). Chat
  // lives in the slide-over drawer.
  let activeView = "agent";
  let activeTabId = "";
  let chatDrawerOpen = false;
  const narrowLayout = window.matchMedia("(max-width: 50rem)");

  function cleanText(value, fallback, maximumLength) {
    if (typeof value !== "string") {
      return fallback;
    }
    const cleaned = value.trim();
    return cleaned.length > 0 ? cleaned.slice(0, maximumLength) : fallback;
  }

  function loadConfig() {
    const supplied =
      typeof window.AGENT_CONFIG === "object" && window.AGENT_CONFIG !== null
        ? window.AGENT_CONFIG
        : {};
    const prompts = Array.isArray(supplied.examplePrompts)
      ? supplied.examplePrompts
          .filter((prompt) => typeof prompt === "string" && prompt.trim())
          .slice(0, 6)
          .map((prompt) => prompt.trim().slice(0, 180))
      : DEFAULT_CONFIG.examplePrompts;
    const suppliedColour = cleanText(
      supplied.primaryColour,
      DEFAULT_CONFIG.primaryColour,
      40,
    );

    return {
      name: cleanText(supplied.name, DEFAULT_CONFIG.name, 60),
      subtitle: cleanText(
        supplied.subtitle,
        DEFAULT_CONFIG.subtitle,
        160,
      ),
      welcomeMessage: cleanText(
        supplied.welcomeMessage,
        DEFAULT_CONFIG.welcomeMessage,
        800,
      ),
      primaryColour:
        window.CSS?.supports("color", suppliedColour)
          ? suppliedColour
          : DEFAULT_CONFIG.primaryColour,
      examplePrompts:
        prompts.length > 0 ? prompts : DEFAULT_CONFIG.examplePrompts,
      brands: Array.isArray(supplied.brands)
        ? supplied.brands
            .filter(
              (brand) =>
                brand &&
                typeof brand.id === "string" &&
                typeof brand.label === "string",
            )
            .slice(0, 4)
            .map((brand) => ({
              id: brand.id.trim().slice(0, 40),
              label: brand.label.trim().slice(0, 40),
              colour:
                typeof brand.colour === "string" &&
                window.CSS?.supports("color", brand.colour.trim())
                  ? brand.colour.trim()
                  : DEFAULT_CONFIG.primaryColour,
            }))
        : [],
      brandExamplePrompts:
        typeof supplied.brandExamplePrompts === "object" &&
        supplied.brandExamplePrompts !== null
          ? supplied.brandExamplePrompts
          : {},
      welcomeMessages:
        typeof supplied.welcomeMessages === "object" &&
        supplied.welcomeMessages !== null
          ? supplied.welcomeMessages
          : {},
      quickActions: Array.isArray(supplied.quickActions)
        ? supplied.quickActions
            .filter(
              (action) =>
                action &&
                typeof action.label === "string" &&
                typeof action.prompt === "string",
            )
            .slice(0, 6)
            .map((action) => ({
              icon: cleanText(action.icon, "", 4),
              label: action.label.trim().slice(0, 40),
              prompt: action.prompt.trim().slice(0, 500),
            }))
        : [],
    };
  }

  const config = loadConfig();

  function activeAgent() {
    return (
      agents.find(
        (agent) => agent.id === activeAgentId && agent.status === "active",
      ) ?? agents.find((agent) => agent.status === "active")
    );
  }

  function displayAgentName() {
    // A name saved through the settings form wins over both the registry and
    // agent.config.js, so renaming the agent needs no file editing.
    const saved = profile?.agentName ?? "";
    if (saved.length > 0) {
      return saved;
    }
    return activeAgentId === "project-manager"
      ? config.name
      : activeAgent()?.name ?? config.name;
  }

  function getInitials(name) {
    return name
      .split(/\s+/)
      .slice(0, 2)
      .map((part) => part.charAt(0))
      .join("")
      .toUpperCase();
  }

  function createSessionId() {
    return window.crypto.randomUUID();
  }

  function storeSession(value) {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch {
      // The chat still works when private browsing blocks local storage.
    }
  }

  function loadOrCreateSession() {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      if (
        stored &&
        /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
          stored,
        )
      ) {
        return stored;
      }
    } catch {
      // Fall through to a fresh session.
    }

    const freshSession = createSessionId();
    storeSession(freshSession);
    return freshSession;
  }

  function welcomeMessageFor(agentId) {
    const message = config.welcomeMessages[agentId];
    return typeof message === "string" && message.trim()
      ? message.trim().slice(0, 800)
      : config.welcomeMessage;
  }

  function applyAgentIdentity() {
    const name = displayAgentName();
    const description =
      activeAgentId === "project-manager"
        ? config.subtitle
        : activeAgent()?.description ?? config.subtitle;
    document.title = `${name} · Local agent`;
    document.documentElement.style.setProperty(
      "--brand-primary",
      activeBrand()?.colour ?? config.primaryColour,
    );
    elements.agentName.textContent = name;
    elements.agentSubtitle.textContent = description;
    elements.conversationAgentName.textContent = name;
    elements.conversationTitleText.textContent = activeConversationTitle;
    elements.input.setAttribute("aria-label", `Message ${name}`);
    // "the Project Manager" reads well; "the Coombe Studio" does not, so drop
    // the article once the learner has named the agent themselves.
    elements.input.placeholder =
      (profile?.agentName ?? "").length > 0
        ? `What should ${name} do?`
        : `What should the ${name} do?`;

    const initials = getInitials(name);
    elements.agentInitials.textContent = initials;
    elements.mobileAgentInitials.textContent = initials;
    applySavedAvatar();
  }

  function applySavedAvatar() {
    const avatar = profile?.avatarDataUrl ?? "";
    for (const mark of [elements.agentInitials, elements.mobileAgentInitials]) {
      if (avatar.length > 0) {
        mark.style.backgroundImage = `url("${avatar}")`;
        mark.classList.add("brand__mark--photo");
      } else {
        mark.style.removeProperty("background-image");
        mark.classList.remove("brand__mark--photo");
      }
    }
  }

  function scrollConversation() {
    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    elements.conversation.scrollTo({
      top: elements.conversation.scrollHeight,
      behavior: reduceMotion ? "auto" : "smooth",
    });
  }

  function createAvatar(kind) {
    const avatar = document.createElement("span");
    avatar.className = `message__avatar message__avatar--${kind}`;
    avatar.setAttribute("aria-hidden", "true");
    avatar.textContent =
      kind === "agent" ? getInitials(displayAgentName()) : "You";
    return avatar;
  }

  function documentMetadata(documentItem) {
    const pageText =
      typeof documentItem.pageCount === "number"
        ? ` · ${documentItem.pageCount} pages`
        : "";
    const expiryText = documentItem.expired ? " · Expired" : "";
    return `${documentItem.wordCount.toLocaleString()} words${pageText}${expiryText}`;
  }

  function documentTypeLabel(documentItem) {
    if (documentItem.type === "pasted-text") {
      return "TEXT";
    }
    return String(documentItem.type || "FILE").toUpperCase().slice(0, 5);
  }

  function createSentAttachment(documentItem) {
    const attachment = document.createElement("div");
    attachment.className = "sent-attachment";
    attachment.classList.toggle(
      "sent-attachment--expired",
      documentItem.expired === true,
    );
    attachment.setAttribute(
      "aria-label",
      `Attached ${documentItem.name}, ${documentMetadata(documentItem)}`,
    );

    const preview = document.createElement("span");
    preview.className = `sent-attachment__preview sent-attachment__preview--${documentItem.type}`;
    preview.setAttribute("aria-hidden", "true");

    const pageFold = document.createElement("span");
    pageFold.className = "sent-attachment__fold";

    const previewLines = document.createElement("span");
    previewLines.className = "sent-attachment__lines";
    for (let index = 0; index < 3; index += 1) {
      previewLines.append(document.createElement("span"));
    }

    const type = document.createElement("span");
    type.className = "sent-attachment__type";
    type.textContent = documentTypeLabel(documentItem);
    preview.append(pageFold, previewLines, type);

    const details = document.createElement("span");
    details.className = "sent-attachment__details";

    const name = document.createElement("span");
    name.className = "sent-attachment__name";
    name.textContent = documentItem.name;
    name.title = documentItem.name;

    const metadata = document.createElement("span");
    metadata.className = "sent-attachment__meta";
    metadata.textContent = documentMetadata(documentItem);

    details.append(name, metadata);
    attachment.append(preview, details);
    return attachment;
  }

  function appendSafeMessageText(element, text) {
    const localDownload = /\/api\/seo-article\/download\/[A-Za-z0-9_-]{40,60}\.md/g;
    let offset = 0;
    for (const match of text.matchAll(localDownload)) {
      const index = match.index ?? 0;
      element.append(document.createTextNode(text.slice(offset, index)));
      const link = document.createElement("a");
      link.className = "message__download";
      link.href = match[0];
      link.download = "";
      link.textContent = "Download the article (.md)";
      element.append(link);
      offset = index + match[0].length;
    }
    element.append(document.createTextNode(text.slice(offset)));
  }

  function addMessage(kind, text, attachments = [], options = {}) {
    const wrapper = document.createElement("article");
    wrapper.className = `message message--${kind}`;
    if (["pending", "failed", "interrupted"].includes(options.status)) {
      wrapper.classList.add(`message--${options.status}`);
    }
    if (options.id) {
      wrapper.dataset.messageId = options.id;
    }

    const body = document.createElement("div");
    body.className = "message__body";

    const label = document.createElement("p");
    label.className = "message__label";
    label.textContent = kind === "agent" ? displayAgentName() : "You";

    const copy = document.createElement("p");
    copy.className = "message__copy";
    appendSafeMessageText(copy, text);

    body.append(label);
    if (kind === "user" && attachments.length > 0) {
      const attachmentList = document.createElement("div");
      attachmentList.className = "message__attachments";
      attachmentList.setAttribute("aria-label", "Sent attachments");
      for (const documentItem of attachments) {
        attachmentList.append(createSentAttachment(documentItem));
      }
      body.append(attachmentList);
    }
    body.append(copy);
    if (["pending", "failed", "interrupted"].includes(options.status)) {
      const status = document.createElement("p");
      status.className = "message__status";
      status.textContent =
        options.status === "pending"
          ? "Reply in progress…"
          : options.status === "interrupted"
          ? "Reply interrupted — send this again as a new message."
          : "Reply failed — send this again to retry.";
      body.append(status);
    }
    if (
      kind === "agent" &&
      text.trim().length > 0 &&
      !["pending", "failed", "interrupted"].includes(options.status)
    ) {
      const actions = document.createElement("div");
      actions.className = "message__actions";
      const copyButton = document.createElement("button");
      copyButton.className = "message-copy-button";
      copyButton.type = "button";
      copyButton.textContent = "Copy";
      copyButton.addEventListener("click", () => {
        void copyTextToClipboard(text).then((copied) => {
          copyButton.textContent = copied ? "Copied ✓" : "Copy failed";
          copyButton.classList.toggle("message-copy-button--copied", copied);
          window.setTimeout(() => {
            copyButton.textContent = "Copy";
            copyButton.classList.remove("message-copy-button--copied");
          }, 1800);
        });
      });
      actions.append(copyButton);
      body.append(actions);
    }
    wrapper.append(createAvatar(kind), body);
    elements.conversation.append(wrapper);
    if (options.scroll !== false) {
      scrollConversation();
    }
    return wrapper;
  }

  function shortArticleText(value, maximum = 180) {
    if (typeof value !== "string") return "";
    const cleaned = value.replace(/\s+/g, " ").trim();
    return cleaned.length <= maximum
      ? cleaned
      : `${cleaned.slice(0, maximum - 1).trimEnd()}…`;
  }

  function articleStatusText(job) {
    const stages = {
      queued: "Your article is waiting to start.",
      preparing_research: "Checking the research and reliable sources…",
      drafting: "Writing and checking the draft…",
      repairing: "Improving the evidence and wording…",
      ready_for_review: "Your article is ready.",
    };
    return stages[job?.stage] ?? "Writing and checking your article…";
  }

  function appendArticleContext(panel, brief) {
    const who = shortArticleText(brief?.context?.who?.value);
    const offer = shortArticleText(brief?.context?.offer?.value);
    if (!who && !offer) return;
    const context = document.createElement("div");
    context.className = "article-panel__context";
    if (who) {
      const line = document.createElement("p");
      line.textContent = `Who you help: ${who}`;
      context.append(line);
    }
    if (offer) {
      const line = document.createElement("p");
      line.textContent = `What you sell: ${offer}`;
      context.append(line);
    }
    const edit = document.createElement("button");
    edit.type = "button";
    edit.className = "article-panel__text-button";
    edit.textContent = "Edit My Business";
    edit.addEventListener("click", () => void openProfileDialog());
    context.append(edit);
    panel.append(context);
  }

  function renderArticlePanel(payload) {
    const previousPanel = elements.conversation.querySelector(".article-panel");
    const brief = payload?.brief;
    if (!brief) {
      previousPanel?.remove();
      return;
    }
    const shouldReveal =
      previousPanel?.dataset.briefId !== brief.briefId ||
      previousPanel?.dataset.status !== brief.status;
    previousPanel?.remove();

    const panel = document.createElement("section");
    panel.className = "article-panel";
    panel.dataset.briefId = brief.briefId;
    panel.dataset.status = brief.status;

    const eyebrow = document.createElement("p");
    eyebrow.className = "article-panel__eyebrow";
    eyebrow.textContent = brief.research?.source === "paid"
      ? "Article ideas from live search data"
      : "Article ideas from website research";

    const title = document.createElement("h3");
    title.className = "article-panel__title";

    if (brief.status === "writing") {
      title.textContent = "Writing your article";
      const selected = document.createElement("p");
      selected.className = "article-panel__selected";
      selected.textContent = brief.selection?.title ?? "Your selected article";
      const progress = document.createElement("p");
      progress.className = "article-panel__progress";
      progress.textContent = articleStatusText(payload.job);
      panel.append(eyebrow, title, selected, progress);
    } else if (brief.status === "complete" && payload.article) {
      title.textContent = "Your article is ready";
      const selected = document.createElement("p");
      selected.className = "article-panel__selected";
      selected.textContent = brief.selection?.title ?? "SEO article";
      const download = document.createElement("a");
      download.className = "article-panel__primary";
      download.href = payload.article.downloadUrl;
      download.download = "";
      download.textContent = "Download article";
      panel.append(eyebrow, title, selected, download);
    } else if (brief.status === "failed") {
      title.textContent = "This draft needs attention";
      const detail = document.createElement("p");
      detail.className = "article-panel__progress";
      detail.textContent = payload.job?.errorMessage ??
        "The article could not be completed. Ask the agent what is needed next.";
      panel.append(eyebrow, title, detail);
    } else if (brief.status === "needs_details") {
      title.textContent = "One quick detail before I write";
      const detail = document.createElement("p");
      detail.className = "article-panel__progress";
      const labels = {
        who: "who you help",
        offer: "what you sell",
        price: "what the article can say about price",
        boundaries: "what the article must not promise",
      };
      const missing = (brief.missingFields ?? []).map((field) => labels[field] ?? field);
      detail.textContent = missing.length > 0
        ? `Tell the agent ${missing.join(" and ")}.`
        : "Reply to the short question in the chat.";
      panel.append(eyebrow, title, detail);
      appendArticleContext(panel, brief);
    } else {
      title.textContent = "Choose what to write";
      const intro = document.createElement("p");
      intro.className = "article-panel__intro";
      intro.textContent = "Pick one idea. You can change the details before anything is written.";
      panel.append(eyebrow, title, intro);
      appendArticleContext(panel, brief);

      const choices = document.createElement("div");
      choices.className = "article-panel__choices";
      for (const opportunity of brief.opportunities ?? []) {
        const card = document.createElement("article");
        card.className = "article-choice";
        const number = document.createElement("span");
        number.className = "article-choice__number";
        number.textContent = String(opportunity.number);
        const content = document.createElement("div");
        const heading = document.createElement("h4");
        heading.textContent = opportunity.title;
        const reason = document.createElement("p");
        reason.textContent = opportunity.reason;
        const facts = document.createElement("p");
        facts.className = "article-choice__facts";
        const interest = Number.isFinite(opportunity.searchVolume)
          ? `About ${Number(opportunity.searchVolume).toLocaleString()} searches a month`
          : "Search interest not measured";
        facts.textContent = `${interest} · ${opportunity.competition} competition`;
        const choose = document.createElement("button");
        choose.type = "button";
        choose.className = "article-panel__primary";
        choose.textContent = "Write this article";
        choose.addEventListener("click", () => {
          void sendMessage(
            `Write article option ${opportunity.number} for ${brief.domain}.`,
            true,
          );
        });
        content.append(heading, reason, facts, choose);
        card.append(number, content);
        choices.append(card);
      }
      panel.append(choices);

      const actions = document.createElement("div");
      actions.className = "article-panel__actions";
      const best = document.createElement("button");
      best.type = "button";
      best.className = "article-panel__secondary";
      best.textContent = "Choose the best one for me";
      best.addEventListener("click", () => {
        void sendMessage(`Choose the best article for ${brief.domain} and write it.`, true);
      });
      const custom = document.createElement("button");
      custom.type = "button";
      custom.className = "article-panel__text-button";
      custom.textContent = "Use another topic";
      custom.addEventListener("click", () => {
        elements.input.value = `Write an article for ${brief.domain} about `;
        updateCharacterCount();
        resizeInput();
        elements.input.focus();
      });
      actions.append(best, custom);
      panel.append(actions);
    }

    elements.conversation.append(panel);
    if (shouldReveal) {
      window.requestAnimationFrame(() => {
        panel.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
    if (brief.status === "writing") {
      articleRefreshTimer = window.setTimeout(() => {
        void refreshArticlePanel();
      }, 4_000);
    }
  }

  async function refreshArticlePanel() {
    if (articleRefreshTimer !== null) {
      window.clearTimeout(articleRefreshTimer);
      articleRefreshTimer = null;
    }
    const expectedSessionId = sessionId;
    try {
      const response = await fetch(
        `/api/seo-article/briefs?sessionId=${encodeURIComponent(expectedSessionId)}`,
        { headers: { Accept: "application/json" } },
      );
      if (response.status === 404) {
        elements.conversation.querySelector(".article-panel")?.remove();
        return;
      }
      const body = await parseResponse(response, "The article plan could not be loaded.");
      if (sessionId !== expectedSessionId) return;
      renderArticlePanel(body);
    } catch {
      // The normal chat stays usable when the optional article panel is offline.
    }
  }

  function addLoadingMessage() {
    const wrapper = document.createElement("article");
    wrapper.className = "message message--agent";

    const body = document.createElement("div");
    body.className = "message__body";

    const label = document.createElement("p");
    label.className = "message__label";
    label.textContent = displayAgentName();

    const dots = document.createElement("span");
    dots.className = "thinking-dots";
    dots.setAttribute("aria-hidden", "true");
    for (let index = 0; index < 3; index += 1) {
      dots.append(document.createElement("span"));
    }

    const accessibleText = document.createElement("span");
    accessibleText.className = "visually-hidden";
    accessibleText.textContent = `${displayAgentName()} is thinking`;

    body.append(label, dots, accessibleText);
    wrapper.append(createAvatar("agent"), body);
    elements.conversation.append(wrapper);
    scrollConversation();
    return wrapper;
  }

  function addError(message, retryRequest) {
    const alert = document.createElement("div");
    alert.className = "chat-error";
    alert.setAttribute("role", "alert");

    const icon = document.createElement("span");
    icon.className = "chat-error__icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = "!";

    const content = document.createElement("div");
    const title = document.createElement("p");
    title.className = "chat-error__title";
    title.textContent = "That didn’t work";
    const detail = document.createElement("p");
    detail.className = "chat-error__detail";
    detail.textContent = message;
    content.append(title, detail);

    if (retryRequest) {
      const retry = document.createElement("button");
      retry.className = "retry-button";
      retry.type = "button";
      retry.textContent = "Try again";
      retry.addEventListener("click", () => {
        alert.remove();
        void sendMessage(retryRequest.message, true, retryRequest.documents);
      });
      content.append(retry);
    }

    alert.append(icon, content);
    elements.conversation.append(alert);
    scrollConversation();
  }

  function friendlyError(errorBody, fallback) {
    if (
      typeof errorBody === "object" &&
      errorBody !== null &&
      typeof errorBody.error === "object" &&
      errorBody.error !== null &&
      typeof errorBody.error.message === "string"
    ) {
      return errorBody.error.message;
    }
    return fallback;
  }

  async function parseResponse(response, fallback) {
    let body = null;
    try {
      body = await response.json();
    } catch {
      // Use the stable fallback below.
    }
    if (!response.ok) {
      throw new Error(friendlyError(body, fallback));
    }
    return body;
  }

  async function loadAgents() {
    try {
      const response = await fetch("/api/agents", {
        headers: { Accept: "application/json" },
      });
      const body = await parseResponse(
        response,
        "The local agent list could not be loaded.",
      );
      if (
        body &&
        Array.isArray(body.agents) &&
        body.agents.some((agent) => agent?.status === "active")
      ) {
        agents = body.agents;
        activeAgentId =
          agents.find((agent) => agent.id === activeAgentId)?.status === "active"
            ? activeAgentId
            : agents.find((agent) => agent.status === "active").id;
      }
    } catch {
      agents = DEFAULT_AGENTS;
    }
  }

  function relativeTime(value) {
    const timestamp = Date.parse(value);
    if (!Number.isFinite(timestamp)) {
      return "Saved locally";
    }
    const seconds = Math.round((timestamp - Date.now()) / 1_000);
    const formatter = new Intl.RelativeTimeFormat(undefined, { numeric: "auto" });
    if (Math.abs(seconds) < 60) {
      return formatter.format(seconds, "second");
    }
    const minutes = Math.round(seconds / 60);
    if (Math.abs(minutes) < 60) {
      return formatter.format(minutes, "minute");
    }
    const hours = Math.round(minutes / 60);
    if (Math.abs(hours) < 24) {
      return formatter.format(hours, "hour");
    }
    return formatter.format(Math.round(hours / 24), "day");
  }

  function syncHistoryPanelAccess() {
    elements.agentPanel.inert =
      narrowLayout.matches &&
      !elements.agentPanel.classList.contains("agent-panel--open");
  }

  function setHistoryOpen(isOpen) {
    elements.agentPanel.classList.toggle("agent-panel--open", isOpen);
    elements.historyButton.setAttribute("aria-expanded", String(isOpen));
    syncHistoryPanelAccess();
    if (isOpen) {
      elements.historySearchInput.focus();
    } else if (document.activeElement === elements.historyClose) {
      elements.historyButton.focus();
    }
  }

  function renderHistoryList(items = conversations, isSearch = false) {
    elements.historyList.replaceChildren();
    if (items.length === 0) {
      elements.historyStatus.textContent = isSearch
        ? "No saved chats match that search."
        : "No saved chats yet.";
      return;
    }
    elements.historyStatus.textContent = isSearch
      ? `${items.length} matching message${items.length === 1 ? "" : "s"}`
      : "Saved on this computer";
    for (const item of items) {
      if (isSearch) {
        const result = document.createElement("button");
        result.className = "history-result";
        result.type = "button";

        const title = document.createElement("span");
        title.className = "history-result__title";
        title.textContent = item.conversationTitle;
        const snippet = document.createElement("span");
        snippet.className = "history-result__snippet";
        snippet.textContent = item.snippet;
        result.append(title, snippet);
        result.addEventListener("click", () => {
          void loadConversation(item.conversationId, item.messageId);
        });
        elements.historyList.append(result);
        continue;
      }

      const wrapper = document.createElement("div");
      wrapper.className = "history-item";
      wrapper.classList.toggle("history-item--active", item.id === sessionId);
      wrapper.setAttribute("role", "listitem");

      const open = document.createElement("button");
      open.className = "history-item__open";
      open.type = "button";
      open.setAttribute("aria-current", item.id === sessionId ? "true" : "false");
      const title = document.createElement("span");
      title.className = "history-item__title";
      title.textContent = item.title;
      const meta = document.createElement("span");
      meta.className = "history-item__meta";
      meta.textContent = `${relativeTime(item.updatedAt)} · ${item.messageCount} message${item.messageCount === 1 ? "" : "s"}`;
      open.append(title, meta);
      open.addEventListener("click", () => {
        void loadConversation(item.id);
      });

      const actions = document.createElement("span");
      actions.className = "history-item__actions";
      const rename = document.createElement("button");
      rename.className = "history-item__action";
      rename.type = "button";
      rename.textContent = "✎";
      rename.setAttribute("aria-label", `Rename ${item.title}`);
      rename.addEventListener("click", () => {
        void renameConversation(item);
      });
      const remove = document.createElement("button");
      remove.className = "history-item__action";
      remove.type = "button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Delete ${item.title}`);
      remove.addEventListener("click", () => {
        void deleteConversation(item);
      });
      actions.append(rename, remove);
      wrapper.append(open, actions);
      elements.historyList.append(wrapper);
    }
  }

  async function loadConversationList({ append = false } = {}) {
    const cursor = append && nextConversationCursor
      ? `&cursor=${encodeURIComponent(nextConversationCursor)}`
      : "";
    const response = await fetch(`/api/conversations?limit=50${cursor}`, {
      headers: { Accept: "application/json" },
    });
    const body = await parseResponse(response, "Saved chats could not be loaded.");
    const received = Array.isArray(body?.conversations) ? body.conversations : [];
    conversations = append ? [...conversations, ...received] : received;
    nextConversationCursor = body?.nextCursor ?? null;
    elements.historyMore.hidden = !nextConversationCursor;
    renderHistoryList();
    return conversations;
  }

  function discardPendingDocuments(previousSessionId) {
    const documents = sessionDocuments;
    uploadedDocuments = [];
    sessionDocuments = [];
    renderDocuments();
    for (const documentItem of documents) {
      void fetch(
        `/api/documents/${encodeURIComponent(documentItem.id)}?sessionId=${encodeURIComponent(previousSessionId)}`,
        { method: "DELETE" },
      );
    }
  }

  function renderStoredConversation(targetMessageId) {
    if (pendingRefreshTimer !== null) {
      window.clearTimeout(pendingRefreshTimer);
      pendingRefreshTimer = null;
    }
    if (articleRefreshTimer !== null) {
      window.clearTimeout(articleRefreshTimer);
      articleRefreshTimer = null;
    }
    elements.conversation.replaceChildren();
    if (nextMessageBefore) {
      const older = document.createElement("button");
      older.className = "load-older";
      older.type = "button";
      older.textContent = "Load earlier messages";
      older.addEventListener("click", () => {
        void loadOlderMessages();
      });
      elements.conversation.append(older);
    }
    if (currentMessages.length === 0) {
      addMessage("agent", welcomeMessageFor(activeAgentId), [], {
        scroll: false,
      });
      elements.suggestions.hidden = false;
    } else {
      elements.suggestions.hidden = true;
      for (const message of currentMessages) {
        addMessage(
          message.role === "assistant" ? "agent" : "user",
          message.content,
          message.attachments ?? [],
          {
            id: message.id,
            status: message.status,
            scroll: false,
          },
        );
      }
    }
    const target = targetMessageId
      ? elements.conversation.querySelector(
          `[data-message-id="${CSS.escape(targetMessageId)}"]`,
        )
      : null;
    if (target) {
      target.classList.add("message--target");
      target.scrollIntoView({ block: "center" });
      elements.conversation.focus();
    } else {
      elements.conversation.scrollTop = elements.conversation.scrollHeight;
    }
    if (currentMessages.some((message) => message.status === "pending")) {
      const expectedSessionId = sessionId;
      pendingRefreshTimer = window.setTimeout(() => {
        if (sessionId === expectedSessionId && !requestInProgress) {
          void loadConversation(sessionId, undefined, true).catch(() => {});
        }
      }, 1_500);
    }
    if (currentMessages.length > 0) {
      void refreshArticlePanel();
    }
  }

  async function loadConversation(id, targetMessageId, allowBusy = false) {
    if (!allowBusy && (requestInProgress || documentRequestInProgress)) {
      return;
    }
    const response = await fetch(
      `/api/conversations/${encodeURIComponent(id)}?limit=100`,
      { headers: { Accept: "application/json" } },
    );
    const body = await parseResponse(response, "That saved chat could not be loaded.");
    const previousSessionId = sessionId;
    if (previousSessionId !== id && sessionDocuments.length > 0) {
      discardPendingDocuments(previousSessionId);
    }
    sessionId = body.conversation.id;
    storeSession(sessionId);
    activeConversationTitle = body.conversation.title;
    const availableAgent = agents.find(
      (agent) => agent.id === body.conversation.agentId && agent.status === "active",
    );
    if (availableAgent) {
      activeAgentId = availableAgent.id;
    }
    currentMessages = Array.isArray(body.messages) ? body.messages : [];
    nextMessageBefore = body.nextBefore ?? null;
    elements.input.value = "";
    updateCharacterCount();
    resizeInput();
    applyAgentIdentity();
    renderAgentList();
    renderSuggestions();
    if (activeView === "agent") {
      activeTabId = "";
      renderStage();
    }
    renderStoredConversation(targetMessageId);
    renderHistoryList();
    setHistoryOpen(false);
    elements.input.focus();
  }

  async function loadOlderMessages() {
    if (!nextMessageBefore) {
      return;
    }
    const response = await fetch(
      `/api/conversations/${encodeURIComponent(sessionId)}?limit=100&before=${encodeURIComponent(nextMessageBefore)}`,
      { headers: { Accept: "application/json" } },
    );
    const body = await parseResponse(response, "Earlier messages could not be loaded.");
    currentMessages = [...(body.messages ?? []), ...currentMessages];
    nextMessageBefore = body.nextBefore ?? null;
    renderStoredConversation();
    elements.conversation.scrollTop = 0;
  }

  async function createConversation(agentId = activeAgentId) {
    if (requestInProgress || documentRequestInProgress) {
      return;
    }
    const previousSessionId = sessionId;
    if (sessionDocuments.length > 0) {
      discardPendingDocuments(previousSessionId);
    }
    const response = await fetch("/api/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ agentId }),
    });
    const body = await parseResponse(response, "A new chat could not be created.");
    await loadConversationList();
    await loadConversation(body.conversation.id);
    elements.requestStatus.textContent = "New conversation started";
  }

  async function renameConversation(conversation) {
    const supplied = window.prompt("Rename this conversation", conversation.title);
    if (supplied === null) {
      return;
    }
    const title = supplied.replace(/\s+/g, " ").trim();
    if (!title || title.length > 80) {
      elements.historyStatus.textContent = "Use a title from 1 to 80 characters.";
      return;
    }
    const response = await fetch(
      `/api/conversations/${encodeURIComponent(conversation.id)}`,
      {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      },
    );
    await parseResponse(response, "That chat could not be renamed.");
    if (conversation.id === sessionId) {
      activeConversationTitle = title;
      elements.conversationTitleText.textContent = title;
    }
    await loadConversationList();
  }

  async function deleteConversation(conversation) {
    if (!window.confirm(`Permanently delete “${conversation.title}” from this computer?`)) {
      return;
    }
    const response = await fetch(
      `/api/conversations/${encodeURIComponent(conversation.id)}`,
      { method: "DELETE" },
    );
    if (!response.ok) {
      await parseResponse(response, "That chat could not be deleted.");
    }
    const deletedCurrent = conversation.id === sessionId;
    await loadConversationList();
    if (deletedCurrent) {
      const replacement = conversations.find(
        (candidate) => candidate.agentId === activeAgentId,
      ) ?? conversations[0];
      if (replacement) {
        await loadConversation(replacement.id);
      } else {
        await createConversation(activeAgentId);
      }
    }
  }

  async function searchConversations(query) {
    const cleaned = query.trim();
    if (!cleaned) {
      renderHistoryList();
      elements.historyMore.hidden = !nextConversationCursor;
      return;
    }
    const response = await fetch(
      `/api/conversations/search?q=${encodeURIComponent(cleaned)}&limit=50`,
      { headers: { Accept: "application/json" } },
    );
    const body = await parseResponse(response, "Saved chats could not be searched.");
    elements.historyMore.hidden = true;
    renderHistoryList(Array.isArray(body.results) ? body.results : [], true);
  }

  function renderAgentList() {
    elements.agentList.replaceChildren();
    for (const agent of agents) {
      const button = document.createElement("button");
      button.className = "agent-button";
      button.type = "button";
      button.disabled =
        agent.status !== "active" ||
        requestInProgress ||
        documentRequestInProgress;
      button.setAttribute("role", "listitem");
      button.setAttribute(
        "aria-pressed",
        String(agent.id === activeAgentId),
      );

      const name = document.createElement("span");
      name.className = "agent-button__name";
      name.textContent = agent.name;

      const status = document.createElement("span");
      status.className = "agent-button__status";
      status.textContent =
        agent.status === "active"
          ? agent.id === activeAgentId
            ? "Active"
            : "Available"
          : "Coming soon";

      const description = document.createElement("span");
      description.className = "agent-button__description";
      description.textContent = agent.description;

      button.append(name, status, description);
      if (agent.status === "active") {
        button.addEventListener("click", () => {
          if (agent.id === activeAgentId && activeView === "agent") {
            return;
          }
          const isSameAgent = agent.id === activeAgentId;
          activeAgentId = agent.id;
          activeView = "agent";
          activeTabId = "";
          applyAgentIdentity();
          renderAgentList();
          renderSuggestions();
          renderStage();
          if (!isSameAgent) {
            void createConversation(agent.id);
          }
        });
      }

      // A cog cannot live inside the chip button, so the chip becomes a row
      // holding the selector button and its own settings control.
      const row = document.createElement("div");
      row.className = "agent-row";
      row.append(button);

      if (agent.status === "active") {
        const settings = document.createElement("button");
        settings.className = "agent-settings";
        settings.type = "button";
        settings.disabled = requestInProgress || documentRequestInProgress;
        settings.title = `Edit what ${agent.name} knows about you`;
        settings.innerHTML =
          '<svg viewBox="0 0 24 24" aria-hidden="true">' +
          '<circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="1.7" />' +
          '<path d="M12 2.6v2.2M12 19.2v2.2M21.4 12h-2.2M4.8 12H2.6m14.7-6.6-1.6 1.6M8.1 15.9l-1.6 1.6m10.8 0-1.6-1.6M8.1 8.1 6.5 6.5" ' +
          'fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="1.7" />' +
          "</svg>";
        const label = document.createElement("span");
        label.className = "visually-hidden";
        label.textContent = `Edit what ${agent.name} knows about you`;
        settings.append(label);
        settings.addEventListener("click", () => {
          void openProfileDialog();
        });
        row.append(settings);
      }

      elements.agentList.append(row);
    }
  }

  async function copyTextToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      const helper = document.createElement("textarea");
      helper.value = text;
      helper.setAttribute("readonly", "");
      helper.style.position = "fixed";
      helper.style.opacity = "0";
      document.body.append(helper);
      helper.select();
      let copied = false;
      try {
        copied = document.execCommand("copy");
      } catch {
        copied = false;
      }
      helper.remove();
      return copied;
    }
  }

  function activeBrand() {
    if (config.brands.length === 0) {
      return null;
    }
    const storedId = window.localStorage.getItem(BRAND_STORAGE_KEY);
    return (
      config.brands.find((brand) => brand.id === storedId) ?? config.brands[0]
    );
  }

  function setActiveBrand(brandId) {
    window.localStorage.setItem(BRAND_STORAGE_KEY, brandId);
    renderBrandBar();
    renderQuickActions();
    renderSuggestions();
    renderPipeline(lastPipelinePayload);
    renderStage();
  }

  function buildBrandToggle(container, current) {
    container.replaceChildren();
    for (const brand of config.brands) {
      const option = document.createElement("button");
      option.className = "brand-toggle__option";
      option.type = "button";
      option.setAttribute("role", "radio");
      option.setAttribute(
        "aria-checked",
        brand.id === current.id ? "true" : "false",
      );
      option.style.setProperty("--dot-colour", brand.colour);

      const dot = document.createElement("span");
      dot.className = "brand-toggle__dot";
      dot.setAttribute("aria-hidden", "true");

      const label = document.createElement("span");
      label.textContent = brand.label;

      option.append(dot, label);
      option.addEventListener("click", () => {
        if (brand.id !== activeBrand()?.id) {
          setActiveBrand(brand.id);
        }
      });
      container.append(option);
    }
  }

  function renderBrandBar() {
    if (config.brands.length === 0) {
      return;
    }
    const current = activeBrand();
    document.documentElement.style.setProperty(
      "--brand-primary",
      current.colour,
    );
    // The primary switch lives at the top of the sidebar's agent nav;
    // the drawer keeps its own copy so brand is switchable mid-chat.
    if (elements.sidebarBrand) {
      elements.sidebarBrand.hidden = false;
      buildBrandToggle(elements.sidebarBrandToggle, current);
    }
    elements.brandBar.hidden = false;
    buildBrandToggle(elements.brandToggle, current);
    elements.brandNote.textContent = `Acting for ${current.label} — pages and posts target this brand's site and voice.`;
  }

  function renderQuickActions() {
    if (config.quickActions.length === 0) {
      return;
    }
    const current = activeBrand();
    elements.quickActionsSection.hidden = false;
    elements.quickActions.replaceChildren();
    for (const action of config.quickActions) {
      const chip = document.createElement("button");
      chip.className = "quick-action";
      chip.type = "button";
      if (action.icon) {
        const icon = document.createElement("span");
        icon.className = "quick-action__icon";
        icon.setAttribute("aria-hidden", "true");
        icon.textContent = action.icon;
        chip.append(icon);
      }
      const label = document.createElement("span");
      label.textContent = action.label;
      chip.append(label);
      chip.addEventListener("click", () => {
        const prompt = action.prompt.replaceAll(
          "{brand}",
          current ? current.label : "the business",
        );
        elements.input.value = prompt;
        elements.input.dispatchEvent(new Event("input"));
        elements.input.focus();
      });
      elements.quickActions.append(chip);
    }
  }

  let lastPipelinePayload = null;

  function pipelineGroup(title, items, emptyText, current) {
    const group = document.createElement("div");
    group.className = "pipeline-group";
    const heading = document.createElement("p");
    heading.className = "pipeline-group__title";
    heading.textContent = title;
    group.append(heading);
    if (items.length === 0) {
      const empty = document.createElement("p");
      empty.className = "pipeline-empty";
      empty.textContent = emptyText;
      group.append(empty);
      return group;
    }
    for (const item of items) {
      const row = document.createElement("div");
      row.className = "pipeline-item";
      if (
        current &&
        item.brand !== "general" &&
        item.brand !== current.id
      ) {
        row.classList.add("pipeline-item--dimmed");
      }
      const dot = document.createElement("span");
      dot.className = `pipeline-item__brand pipeline-item__brand--${item.brand}`;
      dot.setAttribute("aria-hidden", "true");
      dot.title = item.brand;
      const title2 = document.createElement("span");
      title2.className = "pipeline-item__title";
      title2.textContent = item.title;
      title2.title = item.title;
      row.append(dot, title2);
      if (item.url) {
        const open = document.createElement("a");
        open.href = item.url;
        open.target = "_blank";
        open.rel = "noreferrer";
        open.textContent = "Review";
        row.append(open);
      }
      group.append(row);
    }
    return group;
  }

  function renderPipeline(payload) {
    if (!payload) {
      return;
    }
    lastPipelinePayload = payload;
    const current = activeBrand();
    elements.pipelinePanel.hidden = false;
    elements.pipelineBadge.hidden = payload.sample !== true;
    elements.pipelineContent.replaceChildren(
      pipelineGroup(
        "Next pages",
        payload.nextPages ?? [],
        "Backlog is clear.",
        current,
      ),
      pipelineGroup(
        "Awaiting your review",
        payload.awaitingReview ?? [],
        "Nothing waiting.",
        current,
      ),
      pipelineGroup(
        "Outreach to send",
        payload.outreach ?? [],
        "Nothing drafted.",
        current,
      ),
    );
  }

  async function loadPipeline() {
    try {
      const response = await fetch("/api/pipeline");
      if (!response.ok) {
        return;
      }
      renderPipeline(await response.json());
    } catch {
      // The pipeline card is optional; the chat works without it.
    }
  }

  // ---- Stage: per-agent dashboards, section tabs, pipeline board ----

  const SECTION_TABS = {
    "business-development": [
      { id: "bd-pipeline", label: "Pipeline" },
      { id: "bd-outreach", label: "Outreach" },
      { id: "bd-lists", label: "Lists" },
    ],
    marketing: [
      { id: "mk-overview", label: "Overview" },
      { id: "mk-campaigns", label: "Campaigns" },
      { id: "mk-content", label: "Content" },
    ],
  };
  const DEFAULT_TABS = [{ id: "overview", label: "Overview" }];

  function tabsForCurrentView() {
    if (activeView === "pipeline") {
      return [{ id: "board", label: "Board" }];
    }
    return SECTION_TABS[activeAgentId] ?? DEFAULT_TABS;
  }

  function setChatDrawerOpen(isOpen) {
    chatDrawerOpen = isOpen;
    elements.chatDrawer.classList.toggle("chat-drawer--open", isOpen);
    elements.chatScrim.hidden = !isOpen;
    elements.chatToggle.setAttribute("aria-expanded", String(isOpen));
    if (isOpen) {
      window.setTimeout(() => elements.input.focus(), 180);
    }
  }

  function openChatWithPrompt(prompt) {
    setChatDrawerOpen(true);
    if (typeof prompt === "string" && prompt.trim()) {
      elements.input.value = prompt;
      elements.input.dispatchEvent(new Event("input"));
    }
  }

  function dashLabel(text) {
    const label = document.createElement("p");
    label.className = "dash-section-label";
    label.textContent = text;
    return label;
  }

  function statCard(value, label) {
    const card = document.createElement("div");
    card.className = "stat-card";
    const number = document.createElement("p");
    number.className = "stat-card__value";
    number.textContent = String(value);
    const caption = document.createElement("p");
    caption.className = "stat-card__label";
    caption.textContent = label;
    card.append(number, caption);
    return card;
  }

  function stageChip(status) {
    const chip = document.createElement("span");
    chip.className = `stage-chip stage-chip--${status}`;
    chip.textContent = status.replaceAll("_", " ");
    return chip;
  }

  function dashCard() {
    const card = document.createElement("div");
    card.className = "dash-card";
    return card;
  }

  function dashEmpty(text) {
    const empty = document.createElement("p");
    empty.className = "dash-empty";
    empty.textContent = text;
    return empty;
  }

  function dashNote(text) {
    const note = document.createElement("p");
    note.className = "dash-note";
    note.textContent = text;
    return note;
  }

  function renderStageTabs() {
    const tabs = tabsForCurrentView();
    if (!tabs.some((tab) => tab.id === activeTabId)) {
      activeTabId = tabs[0].id;
    }
    elements.sectionTabs.replaceChildren();
    for (const tab of tabs) {
      const button = document.createElement("button");
      button.className = "stage-tab";
      button.type = "button";
      button.setAttribute("role", "tab");
      button.setAttribute(
        "aria-selected",
        String(tab.id === activeTabId),
      );
      button.textContent = tab.label;
      button.addEventListener("click", () => {
        if (tab.id !== activeTabId) {
          activeTabId = tab.id;
          renderStage();
        }
      });
      elements.sectionTabs.append(button);
    }
  }

  async function fetchJson(url, init) {
    const response = await fetch(url, init);
    if (!response.ok) {
      let message = `Request failed (${response.status})`;
      try {
        const payload = await response.json();
        if (payload?.error?.message) {
          message = payload.error.message;
        }
      } catch {
        // Keep the status-code message when the body is not JSON.
      }
      throw new Error(message);
    }
    return response.json();
  }

  // ---- BD board ----------------------------------------------------------
  // Eight columns, one per stored prospect status. `opened` is labelled
  // "Clicked" because with Gmail one-to-one drafts there is no open pixel —
  // the signal is a guide-page click read from GA4. The stored status keeps
  // its name so nothing downstream has to change.
  const BD_COLUMNS = [
    { status: "imported", label: "Imported" },
    { status: "needs_review", label: "Needs review" },
    { status: "enriched", label: "Enriched" },
    { status: "emailed", label: "Emailed" },
    { status: "opened", label: "Clicked" },
    { status: "followed_up", label: "Followed up" },
    { status: "replied", label: "Replied" },
    { status: "closed", label: "Closed" },
  ];

  let bdDraggedProspectId = null;
  // Set by renderBdPipelineTab so the dialogs can refresh the board they
  // were opened from without re-rendering the whole stage.
  let bdReload = () => {};

  function bdSubtitleFor(prospect) {
    switch (prospect.status) {
      case "needs_review":
        return prospect.flagReason || "Flagged by enrichment";
      case "emailed":
        return prospect.sentDate
          ? `Sent ${prospect.sentDate}`
          : prospect.draftedAt
            ? `Drafted ${bdShortDate(prospect.draftedAt)} — not sent yet`
            : "Draft prepared";
      case "opened":
        return prospect.clickedAt
          ? `Clicked ${bdShortDate(prospect.clickedAt)}`
          : "Clicked the guide page";
      case "followed_up":
        return prospect.followUpSent
          ? `Followed up ${prospect.followUpSent}`
          : "Follow-up sent";
      case "closed":
        return prospect.closeReason || "Closed";
      default:
        return prospect.contactEmail || prospect.website || "";
    }
  }

  function bdShortDate(value) {
    if (typeof value !== "string" || value === "") {
      return "";
    }
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return value;
    }
    return date.toLocaleDateString(undefined, { day: "numeric", month: "short" });
  }

  function bdCard(prospect) {
    const card = document.createElement("article");
    card.className = "bd-card";
    card.draggable = true;
    card.tabIndex = 0;
    card.dataset.prospectId = prospect.prospectId;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", `${prospect.company} — open details`);

    const company = document.createElement("p");
    company.className = "bd-card__company";
    company.textContent = prospect.company ?? "";
    card.append(company);

    const meta = document.createElement("p");
    meta.className = "bd-card__meta";
    meta.textContent = prospect.region || prospect.listName || "";
    if (meta.textContent !== "") {
      card.append(meta);
    }

    const chips = document.createElement("div");
    chips.className = "bd-card__chips";
    if (prospect.tier) {
      const tier = document.createElement("span");
      tier.className = "stage-chip stage-chip--tier";
      tier.textContent = `Priority ${prospect.tier}`;
      chips.append(tier);
    }
    if (prospect.status === "needs_review") {
      const flag = document.createElement("span");
      flag.className = "stage-chip stage-chip--flag";
      flag.textContent = "Check contact";
      chips.append(flag);
    }
    if (prospect.contactEmail === "" && prospect.status !== "imported") {
      const noEmail = document.createElement("span");
      noEmail.className = "stage-chip stage-chip--flag";
      noEmail.textContent = "No email";
      chips.append(noEmail);
    }
    if (chips.childElementCount > 0) {
      card.append(chips);
    }

    const subtitle = bdSubtitleFor(prospect);
    if (subtitle !== "") {
      const detail = document.createElement("p");
      detail.className = "bd-card__detail";
      detail.textContent = subtitle;
      detail.title = subtitle;
      card.append(detail);
    }

    card.addEventListener("dragstart", (event) => {
      bdDraggedProspectId = prospect.prospectId;
      card.classList.add("bd-card--dragging");
      event.dataTransfer.effectAllowed = "move";
      // Firefox will not start a drag without payload on the transfer.
      event.dataTransfer.setData("text/plain", prospect.prospectId);
    });
    card.addEventListener("dragend", () => {
      bdDraggedProspectId = null;
      card.classList.remove("bd-card--dragging");
    });
    card.addEventListener("click", () => {
      openProspectDialog(prospect.prospectId);
    });
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openProspectDialog(prospect.prospectId);
      }
    });
    return card;
  }

  function bdColumn(column, prospects, onMoved) {
    const element = document.createElement("section");
    element.className = "bd-col";
    element.dataset.status = column.status;

    const heading = document.createElement("h3");
    heading.className = "bd-col__title";
    const name = document.createElement("span");
    name.textContent = column.label;
    const count = document.createElement("span");
    count.className = "bd-col__count";
    count.textContent = String(prospects.length);
    heading.append(name, count);
    element.append(heading);

    const drop = document.createElement("div");
    drop.className = "bd-col__drop";
    for (const prospect of prospects) {
      drop.append(bdCard(prospect));
    }
    if (prospects.length === 0) {
      const empty = document.createElement("p");
      empty.className = "bd-col__empty";
      empty.textContent = "—";
      drop.append(empty);
    }
    element.append(drop);

    element.addEventListener("dragover", (event) => {
      if (bdDraggedProspectId === null) {
        return;
      }
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      element.classList.add("bd-col--over");
    });
    element.addEventListener("dragleave", () => {
      element.classList.remove("bd-col--over");
    });
    element.addEventListener("drop", (event) => {
      event.preventDefault();
      element.classList.remove("bd-col--over");
      const prospectId = bdDraggedProspectId
        ?? event.dataTransfer.getData("text/plain");
      bdDraggedProspectId = null;
      if (!prospectId) {
        return;
      }
      void moveProspect(prospectId, column.status, onMoved);
    });
    return element;
  }

  async function moveProspect(prospectId, status, onMoved) {
    try {
      const payload = await fetchJson("/api/prospects/status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prospectId, status }),
      });
      onMoved(payload);
    } catch {
      onMoved(null, "That card could not be moved. Reload and try again.");
    }
  }

  function renderBdPipelineTab(body) {
    body.append(dashLabel("Prospect pipeline"));

    const actions = document.createElement("div");
    actions.className = "bd-actions";
    const addButton = document.createElement("button");
    addButton.className = "secondary-button";
    addButton.type = "button";
    addButton.textContent = "Add a prospect";
    addButton.addEventListener("click", () => openAddProspectDialog());
    const importButton = document.createElement("button");
    importButton.className = "secondary-button";
    importButton.type = "button";
    importButton.textContent = "Import a list";
    importButton.addEventListener("click", () => {
      openChatWithPrompt(
        "I want to import a prospect list. Here are the rows:",
      );
    });
    const findButton = document.createElement("button");
    findButton.className = "secondary-button";
    findButton.type = "button";
    findButton.textContent = "Find prospects";
    findButton.addEventListener("click", () => {
      openChatWithPrompt(
        "Find me candidate prospects for this brand and propose them for import: ",
      );
    });
    actions.append(addButton, importButton, findButton);
    body.append(actions);

    const status = document.createElement("p");
    status.className = "bd-board__status";
    status.setAttribute("role", "status");
    body.append(status);

    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading the prospect store…"));
    body.append(holder);

    const load = () => {
      const brand = activeBrand()?.id ?? "oddtoe";
      void fetchJson(
        `/api/prospects?brand=${encodeURIComponent(brand)}&limit=500`,
      )
        .then((payload) => {
          holder.replaceChildren();
          const prospects = Array.isArray(payload.prospects)
            ? payload.prospects
            : [];
          if (prospects.length === 0) {
            holder.append(
              dashEmpty(
                "No prospects on this brand's board yet. Add one, import a list, or ask the agent to find some.",
              ),
            );
            return;
          }
          const board = document.createElement("div");
          board.className = "bd-board";
          const onMoved = (payload, message) => {
            if (message) {
              status.textContent = message;
              return;
            }
            status.textContent = `${payload.prospect.company} moved to ${payload.prospect.status.replaceAll("_", " ")}.`;
            load();
          };
          for (const column of BD_COLUMNS) {
            const inColumn = prospects
              .filter((prospect) => prospect.status === column.status)
              .sort((first, second) => {
                const firstTier =
                  first.tier === "" ? 99 : Number(first.tier) || 98;
                const secondTier =
                  second.tier === "" ? 99 : Number(second.tier) || 98;
                if (firstTier !== secondTier) {
                  return firstTier - secondTier;
                }
                return (first.company ?? "").localeCompare(second.company ?? "");
              });
            board.append(bdColumn(column, inColumn, onMoved));
          }
          holder.append(board);
          holder.append(
            dashNote(
              "Drag a card to move it. Clicked is a guide-page click read from GA4, not an email open — Datalabs has no click data until its GA4 property is connected.",
            ),
          );
        })
        .catch(() => {
          holder.replaceChildren(
            dashEmpty(
              "The prospect store is not reachable. Restart the local app and reload.",
            ),
          );
        });
    };
    bdReload = load;
    load();
  }

  // ---- BD dialogs --------------------------------------------------------

  const BD_EVENT_LABELS = {
    imported: "Imported",
    enriched: "Enriched",
    flagged: "Flagged",
    emailed: "Emailed",
    opened: "Opened",
    clicked: "Clicked",
    followed_up: "Followed up",
    replied: "Replied",
    status_change: "Moved",
  };

  function bdDetailRow(label, value) {
    const row = document.createElement("div");
    row.className = "prospect-detail__row";
    const name = document.createElement("dt");
    name.textContent = label;
    const detail = document.createElement("dd");
    detail.textContent = value === "" ? "—" : value;
    if (value === "") {
      detail.classList.add("prospect-detail__empty");
    }
    row.append(name, detail);
    return row;
  }

  function openProspectDialog(prospectId) {
    const dialog = elements.prospectDialog;
    if (!dialog) {
      return;
    }
    elements.prospectDialogTitle.textContent = "Loading…";
    elements.prospectDialogSubtitle.textContent = "";
    elements.prospectDialogBody.replaceChildren();
    dialog.showModal();

    void fetchJson(
      `/api/prospects/events?prospectId=${encodeURIComponent(prospectId)}`,
    )
      .then((payload) => {
        const prospect = payload.prospect;
        elements.prospectDialogTitle.textContent = prospect.company;
        elements.prospectDialogSubtitle.textContent = [
          prospect.listName,
          prospect.region,
        ]
          .filter((part) => part !== "")
          .join(" · ");

        const body = document.createElement("div");

        const chips = document.createElement("div");
        chips.className = "bd-card__chips";
        chips.append(stageChip(prospect.status));
        if (prospect.tier) {
          const tier = document.createElement("span");
          tier.className = "stage-chip stage-chip--tier";
          tier.textContent = `Priority ${prospect.tier}`;
          chips.append(tier);
        }
        body.append(chips);

        if (prospect.status === "needs_review") {
          const warning = document.createElement("p");
          warning.className = "prospect-detail__warning";
          warning.textContent = prospect.flagReason
            ? `Enrichment flagged this contact: ${prospect.flagReason}. Confirm it before drafting anything.`
            : "Enrichment flagged this contact. Confirm it before drafting anything.";
          body.append(warning);
        }

        const list = document.createElement("dl");
        list.className = "prospect-detail";
        list.append(
          bdDetailRow("Contact", prospect.contactName),
          bdDetailRow("Email", prospect.contactEmail),
          bdDetailRow("Website", prospect.website),
          bdDetailRow("LinkedIn", prospect.linkedinUrl || prospect.linkedinCompanyUrl),
          bdDetailRow("Source", prospect.source),
          bdDetailRow("Confidence", prospect.confidence),
          bdDetailRow("Hook", prospect.hook),
          bdDetailRow("Hook evidence", prospect.hookEvidence),
          bdDetailRow("Draft prepared", bdShortDate(prospect.draftedAt)),
          bdDetailRow("Sent", prospect.sentDate),
          bdDetailRow("Clicked", bdShortDate(prospect.clickedAt)),
          bdDetailRow("Follow-up due", prospect.followUpDue),
          bdDetailRow("Closed because", prospect.closeReason),
          bdDetailRow("Notes", prospect.notes),
        );
        body.append(list);

        const timelineLabel = document.createElement("p");
        timelineLabel.className = "section-label";
        timelineLabel.textContent = "Timeline";
        body.append(timelineLabel);

        const events = Array.isArray(payload.events) ? payload.events : [];
        if (events.length === 0) {
          const empty = document.createElement("p");
          empty.className = "prospect-detail__empty";
          empty.textContent = "Nothing recorded yet.";
          body.append(empty);
        } else {
          const timeline = document.createElement("ul");
          timeline.className = "prospect-timeline";
          for (const event of events) {
            const item = document.createElement("li");
            const when = document.createElement("span");
            when.className = "prospect-timeline__when";
            when.textContent = bdShortDate(event.occurredAt);
            const what = document.createElement("span");
            what.textContent = `${BD_EVENT_LABELS[event.eventType] ?? event.eventType} — ${event.detail}`;
            item.append(when, what);
            timeline.append(item);
          }
          body.append(timeline);
        }

        // Dragging is the fast path, but it is mouse-only and unusable on a
        // phone across eight columns. This is the same write, reachable from
        // the keyboard.
        const moveLabel = document.createElement("p");
        moveLabel.className = "section-label";
        moveLabel.textContent = "Move to";
        const moveRow = document.createElement("div");
        moveRow.className = "prospect-move";
        const select = document.createElement("select");
        select.className = "prospect-move__select";
        select.setAttribute("aria-label", `Move ${prospect.company} to another column`);
        for (const column of BD_COLUMNS) {
          const option = document.createElement("option");
          option.value = column.status;
          option.textContent = column.label;
          option.selected = column.status === prospect.status;
          select.append(option);
        }
        const reason = document.createElement("input");
        reason.className = "prospect-move__reason";
        reason.maxLength = 120;
        reason.placeholder = "Why closed?";
        reason.setAttribute("aria-label", "Reason for closing");
        reason.value = prospect.closeReason;
        reason.hidden = select.value !== "closed";
        select.addEventListener("change", () => {
          reason.hidden = select.value !== "closed";
        });
        const apply = document.createElement("button");
        apply.className = "secondary-button";
        apply.type = "button";
        apply.textContent = "Move";
        const moveStatus = document.createElement("p");
        moveStatus.className = "prospect-add__status";
        moveStatus.setAttribute("role", "status");
        apply.addEventListener("click", () => {
          if (select.value === prospect.status) {
            moveStatus.textContent = "Already in that column.";
            return;
          }
          moveStatus.textContent = "Moving…";
          void fetchJson("/api/prospects/status", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              prospectId: prospect.prospectId,
              status: select.value,
              closeReason: select.value === "closed" ? reason.value : "",
            }),
          })
            .then(() => {
              dialog.close();
              bdReload();
            })
            .catch((error) => {
              moveStatus.textContent =
                error.message ?? "That card could not be moved.";
            });
        });
        moveRow.append(select, reason, apply);
        body.append(moveLabel, moveRow, moveStatus);

        const ask = document.createElement("button");
        ask.className = "secondary-button";
        ask.type = "button";
        ask.textContent = "Work on this in chat";
        ask.addEventListener("click", () => {
          dialog.close();
          openChatWithPrompt(
            `Tell me where ${prospect.company} stands and what the next move is.`,
          );
        });
        body.append(ask);

        elements.prospectDialogBody.replaceChildren(body);
      })
      .catch((error) => {
        elements.prospectDialogTitle.textContent = "Could not open that card";
        elements.prospectDialogBody.replaceChildren(
          dashEmpty(error.message ?? "The prospect store is not reachable."),
        );
      });
  }

  function openAddProspectDialog() {
    const dialog = elements.prospectAddDialog;
    if (!dialog) {
      return;
    }
    elements.prospectAddForm.reset();
    elements.prospectAddList.value = "Manual additions";
    elements.prospectAddStatus.textContent = "";
    dialog.showModal();
    window.setTimeout(() => elements.prospectAddCompany.focus(), 60);
  }

  async function submitAddProspect(event) {
    event.preventDefault();
    const brand = activeBrand()?.id ?? "oddtoe";
    const form = new FormData(elements.prospectAddForm);
    const payload = { brand };
    for (const [key, value] of form.entries()) {
      if (typeof value === "string" && value.trim() !== "") {
        payload[key] = value.trim();
      }
    }
    elements.prospectAddStatus.textContent = "Saving…";
    try {
      const result = await fetchJson("/api/prospects/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (result.result.outcome === "duplicate") {
        elements.prospectAddStatus.textContent =
          `${result.result.company} is already on that list.`;
        return;
      }
      elements.prospectAddDialog.close();
      bdReload();
    } catch (error) {
      elements.prospectAddStatus.textContent =
        error.message ?? "That prospect could not be saved.";
    }
  }

  function renderBdOutreachTab(body) {
    body.append(dashLabel("Outreach"));
    const card = dashCard();
    card.append(
      dashEmpty(
        "Outreach drafting is not built yet (phases 3–5: Mailchimp campaign, tracking, follow-up).",
      ),
      dashNote(
        "The opener asset is live: every agency is featured on the experiential-agencies guide page with UTM-tagged links.",
      ),
    );
    body.append(card);
  }

  function renderBdListsTab(body) {
    body.append(dashLabel("Lists"));
    const card = dashCard();
    card.append(dashEmpty("Loading lists…"));
    body.append(card);
    void fetchJson(`/api/prospects?brand=${encodeURIComponent(activeBrand()?.id ?? "oddtoe")}`)
      .then((payload) => {
        card.replaceChildren();
        const lists = payload.summary?.listNames ?? [];
        if (lists.length === 0) {
          card.append(dashEmpty("No lists imported yet."));
          return;
        }
        for (const listName of lists) {
          const row = document.createElement("p");
          row.style.margin = "0.3rem 0";
          row.textContent = listName;
          card.append(row);
        }
      })
      .catch(() => {
        card.replaceChildren(dashEmpty("The prospect store is not reachable."));
      });
  }

  function pipelineItemsFor(payload, key) {
    const items = payload?.[key];
    return Array.isArray(items) ? items : [];
  }

  function itemMatchesBrand(item, brand) {
    return !brand || item.brand === "general" || item.brand === brand.id;
  }

  // Compact display title for an icon card: cut at the first heavy
  // delimiter so backlog prose reads as a card label, not a paragraph.
  function shortTitle(title) {
    let cut = title;
    for (const delimiter of [" — ", " (", ". ", "; ", ": "]) {
      const index = cut.indexOf(delimiter);
      if (index > 8) {
        cut = cut.slice(0, index);
      }
    }
    return cut.length > 72 ? `${cut.slice(0, 72)}…` : cut;
  }

  function makeIconCard(item, icon, { dimmed = false } = {}) {
    const card = document.createElement("button");
    card.className = "icon-card";
    card.type = "button";
    if (dimmed) {
      card.classList.add("icon-card--dimmed");
    }
    card.setAttribute("aria-expanded", "false");

    const head = document.createElement("span");
    head.className = "icon-card__head";
    const tile = document.createElement("span");
    tile.className = "icon-card__icon";
    tile.setAttribute("aria-hidden", "true");
    tile.textContent = icon;
    const title = document.createElement("span");
    title.className = "icon-card__title";
    const dot = document.createElement("span");
    dot.className = `kanban-card__brand kanban-card__brand--${item.brand}`;
    dot.title = item.brand;
    title.append(dot, document.createTextNode(shortTitle(item.title)));
    head.append(tile, title);
    card.append(head);

    const detail = document.createElement("span");
    detail.className = "icon-card__detail";
    detail.textContent = item.title;
    if (item.url) {
      const link = document.createElement("a");
      link.href = item.url;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = "Open ↗";
      link.addEventListener("click", (event) => event.stopPropagation());
      detail.append(document.createTextNode(" "), link);
    }
    card.append(detail);

    card.addEventListener("click", () => {
      const open = card.classList.toggle("icon-card--open");
      card.setAttribute("aria-expanded", String(open));
    });
    return card;
  }

  function renderMarketingOverviewTab(body) {
    const brand = activeBrand();
    body.append(
      dashLabel(
        brand ? `Content pipeline — ${brand.label}` : "Content pipeline",
      ),
    );
    const holder = dashCard();
    holder.append(dashEmpty("Loading the content pipeline…"));
    body.append(holder);
    void fetchJson("/api/pipeline")
      .then((payload) => {
        holder.replaceChildren();
        const forBrand = (key) =>
          pipelineItemsFor(payload, key).filter((item) =>
            itemMatchesBrand(item, brand),
          );
        const stats = document.createElement("div");
        stats.className = "dash-stats";
        stats.append(
          statCard(forBrand("nextPages").length, "Next pages"),
          statCard(forBrand("awaitingReview").length, "Awaiting review"),
          statCard(forBrand("outreach").length, "Outreach to send"),
          statCard(forBrand("published").length, "Recently published"),
        );
        holder.append(stats);
        const review = forBrand("awaitingReview");
        holder.append(dashLabel("Awaiting your review"));
        if (review.length === 0) {
          holder.append(dashEmpty("Nothing waiting on you for this brand."));
        } else {
          const grid = document.createElement("div");
          grid.className = "icon-card-grid";
          for (const item of review) {
            grid.append(makeIconCard(item, "👀"));
          }
          holder.append(grid);
        }
        const upNext = forBrand("nextPages");
        holder.append(dashLabel("Up next"));
        if (upNext.length === 0) {
          holder.append(dashEmpty("Backlog is clear for this brand."));
        } else {
          const grid = document.createElement("div");
          grid.className = "icon-card-grid";
          for (const item of upNext) {
            grid.append(makeIconCard(item, "📝"));
          }
          holder.append(grid);
        }
        if (payload.sample === true) {
          holder.append(dashNote("Sample data — the backlog skill is not present."));
        }
        holder.append(
          dashNote(
            "Click a card for the full note. Both-brand board lives under Content Pipeline.",
          ),
        );
      })
      .catch(() => {
        holder.replaceChildren(dashEmpty("The pipeline is not reachable."));
      });
  }

  function renderComingSoonTab(body, label) {
    body.append(dashLabel(label));
    const card = dashCard();
    card.append(
      dashEmpty(`${label} view is not designed yet.`),
      dashNote("Tell the agent what you want here and we will build it."),
    );
    body.append(card);
  }

  function renderAgentOverviewTab(body) {
    const agent = activeAgent();
    body.append(dashLabel("About this agent"));
    const about = dashCard();
    const description = document.createElement("p");
    description.style.margin = "0";
    description.textContent = agent?.description ?? "";
    about.append(description);
    body.append(about);

    const prompts = brandExamplePromptsFor(activeAgentId) ??
      agent?.examplePrompts ?? [];
    if (prompts.length > 0) {
      body.append(dashLabel("Start something"));
      const card = dashCard();
      for (const prompt of prompts.slice(0, 4)) {
        const button = document.createElement("button");
        button.className = "quick-action";
        button.type = "button";
        button.style.display = "block";
        button.style.width = "100%";
        button.style.textAlign = "left";
        button.style.marginBottom = "0.5rem";
        button.textContent = prompt;
        button.addEventListener("click", () => {
          openChatWithPrompt(prompt);
        });
        card.append(button);
      }
      body.append(card);
    }
    body.append(
      dashNote(
        "This section's dashboard is not designed yet — the chat drawer is the full agent.",
      ),
    );
  }

  function kanbanColumn(title, icon, items, brand) {
    const column = document.createElement("div");
    column.className = "kanban-col";
    const heading = document.createElement("p");
    heading.className = "kanban-col__title";
    const text = document.createElement("span");
    text.textContent = `${icon} ${title}`;
    const count = document.createElement("span");
    count.className = "kanban-col__count";
    count.textContent = String(items.length);
    heading.append(text, count);
    column.append(heading);
    if (items.length === 0) {
      column.append(dashEmpty("Empty."));
      return column;
    }
    for (const item of items) {
      column.append(
        makeIconCard(item, icon, {
          dimmed: !itemMatchesBrand(item, brand),
        }),
      );
    }
    return column;
  }

  function renderPipelineBoard(body) {
    const brand = activeBrand();
    body.append(
      dashLabel(
        brand
          ? `Content pipeline — both brands, ${brand.label} highlighted`
          : "Content pipeline — both brands",
      ),
    );
    const board = document.createElement("div");
    board.className = "kanban";
    body.append(board);
    board.append(dashEmpty("Loading the board…"));
    void fetchJson("/api/pipeline")
      .then((payload) => {
        board.replaceChildren(
          kanbanColumn(
            "Backlog",
            "📝",
            pipelineItemsFor(payload, "nextPages"),
            brand,
          ),
          kanbanColumn(
            "Awaiting review",
            "👀",
            pipelineItemsFor(payload, "awaitingReview"),
            brand,
          ),
          kanbanColumn(
            "Outreach to send",
            "📣",
            pipelineItemsFor(payload, "outreach"),
            brand,
          ),
          kanbanColumn(
            "Published",
            "✅",
            pipelineItemsFor(payload, "published"),
            brand,
          ),
        );
        if (payload.sample === true) {
          body.append(
            dashNote("Sample data — the backlog skill is not present."),
          );
        }
        body.append(
          dashNote("Click a card for the full note; dimmed cards belong to the other brand."),
        );
      })
      .catch(() => {
        board.replaceChildren(dashEmpty("The pipeline is not reachable."));
      });
  }

  function renderStage() {
    if (!elements.stageBody) {
      return;
    }
    renderStageTabs();
    elements.pipelineNavButton.setAttribute(
      "aria-pressed",
      String(activeView === "pipeline"),
    );
    const brand = activeBrand();
    elements.stageBrandLabel.textContent = brand ? brand.label : "Workspace";
    const body = document.createElement("div");
    if (activeView === "pipeline") {
      elements.stageTitle.textContent = "Content Pipeline";
      renderPipelineBoard(body);
    } else {
      elements.stageTitle.textContent = displayAgentName();
      if (activeTabId === "bd-pipeline") {
        renderBdPipelineTab(body);
      } else if (activeTabId === "bd-outreach") {
        renderBdOutreachTab(body);
      } else if (activeTabId === "bd-lists") {
        renderBdListsTab(body);
      } else if (activeTabId === "mk-overview") {
        renderMarketingOverviewTab(body);
      } else if (activeTabId === "mk-campaigns") {
        renderComingSoonTab(body, "Campaigns");
      } else if (activeTabId === "mk-content") {
        renderComingSoonTab(body, "Content");
      } else {
        renderAgentOverviewTab(body);
      }
    }
    elements.stageBody.replaceChildren(...body.children);
  }

  function brandExamplePromptsFor(agentId) {
    const brand = activeBrand();
    if (!brand) {
      return null;
    }
    const byBrand = config.brandExamplePrompts[agentId];
    const prompts =
      byBrand && typeof byBrand === "object" ? byBrand[brand.id] : null;
    if (!Array.isArray(prompts)) {
      return null;
    }
    const cleaned = prompts
      .filter((prompt) => typeof prompt === "string" && prompt.trim())
      .map((prompt) => prompt.trim().slice(0, 180));
    return cleaned.length > 0 ? cleaned : null;
  }

  function renderSuggestions() {
    elements.suggestionList.replaceChildren();
    const selectedPrompts =
      brandExamplePromptsFor(activeAgentId) ??
      (activeAgent()?.examplePrompts?.length > 0
        ? activeAgent().examplePrompts
        : config.examplePrompts);
    for (const prompt of selectedPrompts.slice(0, 6)) {
      const button = document.createElement("button");
      button.className = "suggestion-button";
      button.type = "button";
      button.textContent = prompt;
      button.addEventListener("click", () => {
        void sendMessage(prompt, true);
      });
      elements.suggestionList.append(button);
    }
  }

  function renderDocuments() {
    elements.documentList.replaceChildren();
    for (const documentItem of uploadedDocuments) {
      const chip = document.createElement("div");
      chip.className = "document-chip";

      const name = document.createElement("span");
      name.className = "document-chip__name";
      name.textContent = documentItem.name;
      name.title = documentItem.name;

      const metadata = document.createElement("span");
      metadata.className = "document-chip__meta";
      metadata.textContent = documentMetadata(documentItem);

      const remove = document.createElement("button");
      remove.className = "document-chip__remove";
      remove.type = "button";
      remove.textContent = "×";
      remove.setAttribute("aria-label", `Remove ${documentItem.name}`);
      remove.disabled = requestInProgress || documentRequestInProgress;
      remove.addEventListener("click", () => {
        void removeDocument(documentItem.id);
      });

      chip.append(name, metadata, remove);
      elements.documentList.append(chip);
    }
  }

  function renderNewConversation() {
    elements.conversation.replaceChildren();
    addMessage("agent", welcomeMessageFor(activeAgentId));
    elements.suggestions.hidden = false;
    elements.input.value = "";
    updateCharacterCount();
    resizeInput();
  }

  function setBusy(isBusy) {
    requestInProgress = isBusy;
    const controlsBusy = isBusy || documentRequestInProgress;
    if (controlsBusy) {
      setAttachmentMenuOpen(false);
    }
    elements.conversation.setAttribute("aria-busy", String(isBusy));
    elements.input.disabled = controlsBusy;
    elements.sendButton.disabled = controlsBusy;
    elements.resetButton.disabled = controlsBusy;
    elements.historyNew.disabled = controlsBusy;
    elements.historyMore.disabled = controlsBusy;
    elements.historySearchInput.disabled = controlsBusy;
    elements.attachmentMenuButton.disabled = controlsBusy;
    elements.uploadButton.disabled = controlsBusy;
    elements.pasteButton.disabled = controlsBusy;
    for (const suggestion of elements.suggestionList.querySelectorAll("button")) {
      suggestion.disabled = controlsBusy;
    }
    for (const historyControl of elements.historyList.querySelectorAll("button")) {
      historyControl.disabled = controlsBusy;
    }
    elements.sendButtonLabel.textContent = isBusy ? "Working" : "Send";
    elements.requestStatus.textContent = isBusy
      ? `${displayAgentName()} is working on your request…`
      : "Press Enter to send · Shift + Enter for a new line";
    renderAgentList();
    renderDocuments();
  }

  function setDocumentBusy(isBusy, message = "") {
    documentRequestInProgress = isBusy;
    elements.documentStatus.textContent = message;
    setBusy(requestInProgress);
  }

  function setAttachmentMenuOpen(isOpen) {
    elements.attachmentMenu.hidden = !isOpen;
    elements.attachmentMenuButton.setAttribute(
      "aria-expanded",
      String(isOpen),
    );
    if (isOpen) {
      elements.uploadButton.focus();
    }
  }

  async function uploadFile(file) {
    if (uploadedDocuments.length >= MAX_DOCUMENTS) {
      addError(`Add no more than ${MAX_DOCUMENTS} documents to one message.`);
      return;
    }

    setDocumentBusy(true, `Reading ${file.name}…`);
    try {
      const formData = new FormData();
      formData.append("sessionId", sessionId);
      formData.append("file", file);
      const response = await fetch("/api/documents", {
        method: "POST",
        body: formData,
      });
      const body = await parseResponse(
        response,
        "The document could not be read.",
      );
      if (!body?.document?.id) {
        throw new Error("The document reader returned an unexpected result.");
      }
      uploadedDocuments.push(body.document);
      sessionDocuments.push(body.document);
      renderDocuments();
      elements.documentStatus.textContent =
        body.document.warnings?.length > 0
          ? body.document.warnings[0]
          : "";
    } catch (error) {
      elements.documentStatus.textContent = "";
      addError(
        error instanceof Error
          ? error.message
          : "The document could not be read.",
      );
    } finally {
      documentRequestInProgress = false;
      setBusy(requestInProgress);
      elements.fileInput.value = "";
    }
  }

  async function uploadPastedText(name, text) {
    if (uploadedDocuments.length >= MAX_DOCUMENTS) {
      addError(`Add no more than ${MAX_DOCUMENTS} documents to one message.`);
      return false;
    }

    setDocumentBusy(true, "Preparing pasted text…");
    try {
      const response = await fetch("/api/documents/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sessionId, name, text }),
      });
      const body = await parseResponse(
        response,
        "The pasted text could not be prepared.",
      );
      if (!body?.document?.id) {
        throw new Error("The document reader returned an unexpected result.");
      }
      uploadedDocuments.push(body.document);
      sessionDocuments.push(body.document);
      renderDocuments();
      elements.documentStatus.textContent = "";
      return true;
    } catch (error) {
      elements.documentStatus.textContent = "";
      addError(
        error instanceof Error
          ? error.message
          : "The pasted text could not be prepared.",
      );
      return false;
    } finally {
      documentRequestInProgress = false;
      setBusy(requestInProgress);
    }
  }

  async function removeDocument(id) {
    const documentItem = uploadedDocuments.find((item) => item.id === id);
    if (!documentItem) {
      return;
    }

    setDocumentBusy(true, `Removing ${documentItem.name}…`);
    try {
      const response = await fetch(
        `/api/documents/${encodeURIComponent(id)}?sessionId=${encodeURIComponent(sessionId)}`,
        { method: "DELETE" },
      );
      if (!response.ok && response.status !== 404) {
        const body = await response.json().catch(() => null);
        throw new Error(
          friendlyError(body, "The document could not be removed."),
        );
      }
      uploadedDocuments = uploadedDocuments.filter((item) => item.id !== id);
      sessionDocuments = sessionDocuments.filter((item) => item.id !== id);
      elements.documentStatus.textContent = "";
    } catch (error) {
      addError(
        error instanceof Error
          ? error.message
          : "The document could not be removed.",
      );
    } finally {
      documentRequestInProgress = false;
      setBusy(requestInProgress);
    }
  }

  async function sendMessage(
    rawMessage,
    showUserMessage,
    retryDocuments,
  ) {
    if (requestInProgress || documentRequestInProgress) {
      return;
    }

    const message = rawMessage.trim();
    if (!message) {
      elements.input.focus();
      return;
    }

    const requestDocuments = Array.isArray(retryDocuments)
      ? retryDocuments
      : [...uploadedDocuments];

    if (showUserMessage) {
      addMessage("user", message, requestDocuments);
      uploadedDocuments = [];
      elements.fileInput.value = "";
      elements.pastedName.value = "";
      elements.pastedText.value = "";
      elements.documentStatus.textContent = "";
      renderDocuments();
    }
    elements.suggestions.hidden = true;
    elements.input.value = "";
    updateCharacterCount();
    resizeInput();
    setBusy(true);
    loadingMessage = addLoadingMessage();
    const requestId = createSessionId();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          requestId,
          sessionId,
          agentId: activeAgentId,
          message,
          documentIds: requestDocuments.map((item) => item.id),
        }),
      });

      const responseBody = await parseResponse(
        response,
        "The local agent could not reply. Check that n8n is running, then try again.",
      );
      if (
        typeof responseBody !== "object" ||
        responseBody === null ||
        responseBody.sessionId !== sessionId ||
        typeof responseBody.reply !== "string" ||
        !responseBody.reply.trim()
      ) {
        throw new Error(
          "The agent returned an unexpected response. Check the workflow and try again.",
        );
      }

      loadingMessage.remove();
      loadingMessage = null;
      addMessage("agent", responseBody.reply.trim());
      await loadConversationList();
      await loadConversation(sessionId, undefined, true);
    } catch (error) {
      loadingMessage?.remove();
      loadingMessage = null;
      try {
        await loadConversationList();
        await loadConversation(sessionId, undefined, true);
      } catch {
        // Keep the visible optimistic message when history refresh also fails.
      }
      addError(
        error instanceof Error
          ? error.message
          : "The local agent could not reply. Check n8n and try again.",
        { message, documents: requestDocuments },
      );
    } finally {
      setBusy(false);
      elements.input.focus();
    }
  }

  function updateCharacterCount() {
    const length = elements.input.value.length;
    elements.characterCount.textContent = `${length} / 8000`;
    elements.characterCount.classList.toggle(
      "character-count--near-limit",
      length >= 7_200,
    );
  }

  function resizeInput() {
    elements.input.style.height = "auto";
    elements.input.style.height = `${Math.min(elements.input.scrollHeight, 160)}px`;
  }

  function startNewConversation() {
    elements.fileInput.value = "";
    elements.pastedName.value = "";
    elements.pastedText.value = "";
    elements.documentStatus.textContent = "";
    setAttachmentMenuOpen(false);
    void createConversation(activeAgentId).catch((error) => {
      addError(
        error instanceof Error
          ? error.message
          : "A new conversation could not be created.",
      );
    });
  }

  elements.form.addEventListener("submit", (event) => {
    event.preventDefault();
    void sendMessage(elements.input.value, true);
  });

  elements.input.addEventListener("input", () => {
    updateCharacterCount();
    resizeInput();
  });

  elements.input.addEventListener("paste", (event) => {
    const pastedText = event.clipboardData?.getData("text") ?? "";
    if (
      pastedText.length > LARGE_PASTE_THRESHOLD ||
      elements.input.value.length + pastedText.length > 8_000
    ) {
      event.preventDefault();
      void uploadPastedText("Pasted transcript", pastedText).then((added) => {
        if (added) {
          elements.documentStatus.textContent =
            "Large pasted text was added as document context. Add an instruction below.";
        }
      });
    }
  });

  elements.input.addEventListener("keydown", (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.isComposing
    ) {
      event.preventDefault();
      elements.form.requestSubmit();
    }
  });

  elements.attachmentMenuButton.addEventListener("click", () => {
    setAttachmentMenuOpen(elements.attachmentMenu.hidden);
  });

  elements.uploadButton.addEventListener("click", () => {
    setAttachmentMenuOpen(false);
    elements.fileInput.click();
  });

  elements.fileInput.addEventListener("change", () => {
    const file = elements.fileInput.files?.[0];
    if (file) {
      void uploadFile(file);
    }
  });

  elements.pasteButton.addEventListener("click", () => {
    setAttachmentMenuOpen(false);
    elements.pastedName.value = "Pasted transcript";
    elements.pastedText.value = "";
    elements.pasteDialog.showModal();
    elements.pastedText.focus();
  });

  elements.prospectDialogClose?.addEventListener("click", () => {
    elements.prospectDialog.close();
  });
  elements.prospectAddCancel?.addEventListener("click", () => {
    elements.prospectAddDialog.close();
  });
  elements.prospectAddForm?.addEventListener("submit", (event) => {
    void submitAddProspect(event);
  });
  elements.pasteCancel.addEventListener("click", () => {
    elements.pasteDialog.close();
  });

  const MAX_AVATAR_CHARACTERS = 256 * 1024;

  async function loadProfile() {
    try {
      const response = await fetch("/api/profile", {
        headers: { Accept: "application/json" },
      });
      const body = await parseResponse(
        response,
        "Saved agent details could not be loaded.",
      );
      profile = body.profile ?? null;
    } catch {
      // A missing profile must never stop the chat from loading.
      profile = null;
    }
    applySavedAvatar();
  }

  function setAvatarPreview(dataUrl) {
    if (dataUrl.length > 0) {
      elements.profileAvatarButton.style.backgroundImage = `url("${dataUrl}")`;
      elements.profileAvatarInitials.textContent = "";
    } else {
      elements.profileAvatarButton.style.removeProperty("background-image");
      elements.profileAvatarInitials.textContent = getInitials(
        elements.profileAgentName.value || displayAgentName(),
      );
    }
  }

  async function openProfileDialog() {
    if (profile === null) {
      await loadProfile();
    }
    const saved = profile ?? {};
    elements.profileAgentName.value = saved.agentName ?? "";
    elements.profileBusinessName.value = saved.businessName ?? "";
    elements.profileWho.value = saved.whoYouServe ?? "";
    elements.profileOffer.value = saved.offer ?? saved.sells ?? "";
    elements.profilePrice.value = saved.price ?? "";
    elements.profileBoundaries.value = saved.boundaries ?? "";
    elements.profileVoice.value = saved.voice ?? saved.tone ?? "";
    const samples = Array.isArray(saved.voiceSamples) ? saved.voiceSamples : [];
    elements.profileSample1.value = samples[0] ?? "";
    elements.profileSample2.value = samples[1] ?? "";
    pendingAvatarDataUrl = saved.avatarDataUrl ?? "";
    setAvatarPreview(pendingAvatarDataUrl);
    elements.profileAvatar.value = "";
    elements.profileStatus.textContent = "";
    elements.profileDialog.showModal();
    elements.profileAgentName.focus();
  }

  elements.profileAgentName.addEventListener("input", () => {
    if (pendingAvatarDataUrl.length === 0) {
      setAvatarPreview("");
    }
  });

  elements.profileAvatar.addEventListener("change", () => {
    const file = elements.profileAvatar.files?.[0];
    if (!file) {
      return;
    }
    const reader = new FileReader();
    reader.addEventListener("load", () => {
      const result = typeof reader.result === "string" ? reader.result : "";
      if (result.length > MAX_AVATAR_CHARACTERS) {
        elements.profileStatus.textContent =
          "That picture is too large. Choose one under 180 KB.";
        elements.profileAvatar.value = "";
        return;
      }
      pendingAvatarDataUrl = result;
      setAvatarPreview(result);
      elements.profileStatus.textContent = "";
    });
    reader.addEventListener("error", () => {
      elements.profileStatus.textContent = "That picture could not be read.";
    });
    reader.readAsDataURL(file);
  });

  elements.profileAvatarButton.addEventListener("click", () => {
    elements.profileAvatar.click();
  });

  elements.profileCancel.addEventListener("click", () => {
    elements.profileDialog.close();
  });

  // A <dialog> backdrop is painted by the dialog itself, so a click on it
  // reports the dialog as the target. Anything inside the card reports that
  // card instead, which is what separates "outside" from "inside".
  for (const dialog of [elements.profileDialog, elements.pasteDialog]) {
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) {
        dialog.close();
      }
    });
  }

  elements.profileForm.addEventListener("submit", (event) => {
    event.preventDefault();
    void (async () => {
      elements.profileSave.disabled = true;
      elements.profileStatus.textContent = "Saving...";
      try {
        const response = await fetch("/api/profile", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            profile: {
              agentName: elements.profileAgentName.value,
              avatarDataUrl: pendingAvatarDataUrl,
              businessName: elements.profileBusinessName.value,
              whoYouServe: elements.profileWho.value,
              offer: elements.profileOffer.value,
              price: elements.profilePrice.value,
              boundaries: elements.profileBoundaries.value,
              voice: elements.profileVoice.value,
              voiceSamples: [
                elements.profileSample1.value,
                elements.profileSample2.value,
              ],
            },
          }),
        });
        const body = await parseResponse(
          response,
          "Your agent details could not be saved.",
        );
        profile = body.profile ?? null;
        applySavedAvatar();
        const articlePanel = elements.conversation.querySelector(".article-panel");
        if (articlePanel?.dataset.briefId) {
          const updateResponse = await fetch("/api/seo-article/briefs", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              sessionId,
              briefId: articlePanel.dataset.briefId,
            }),
          });
          await parseResponse(updateResponse, "The article choices could not be refreshed.");
          await refreshArticlePanel();
          elements.profileStatus.textContent =
            "Saved. This article now uses your updated details.";
        } else {
          elements.profileStatus.textContent =
            "Saved. Run Sync Skills once before using these details in every chat.";
        }
      } catch (error) {
        elements.profileStatus.textContent =
          error?.message ?? "Your agent details could not be saved.";
      } finally {
        elements.profileSave.disabled = false;
      }
    })();
  });

  document.addEventListener("click", (event) => {
    if (
      !elements.attachmentMenu.hidden &&
      !elements.attachmentMenu.contains(event.target) &&
      !elements.attachmentMenuButton.contains(event.target)
    ) {
      setAttachmentMenuOpen(false);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !elements.attachmentMenu.hidden) {
      event.preventDefault();
      setAttachmentMenuOpen(false);
      elements.attachmentMenuButton.focus();
    }
    if (
      event.key === "Escape" &&
      elements.agentPanel.classList.contains("agent-panel--open")
    ) {
      event.preventDefault();
      setHistoryOpen(false);
    }
  });

  elements.pasteForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const name = elements.pastedName.value;
    const text = elements.pastedText.value;
    void uploadPastedText(name, text).then((added) => {
      if (added) {
        elements.pasteDialog.close();
        elements.input.focus();
      }
    });
  });

  elements.resetButton.addEventListener("click", startNewConversation);
  elements.historyNew.addEventListener("click", startNewConversation);
  elements.historyButton.addEventListener("click", () => {
    setHistoryOpen(true);
  });
  elements.historyClose.addEventListener("click", () => {
    setHistoryOpen(false);
  });
  elements.historyMore.addEventListener("click", () => {
    void loadConversationList({ append: true }).catch((error) => {
      elements.historyStatus.textContent =
        error instanceof Error ? error.message : "More chats could not be loaded.";
    });
  });
  elements.historySearchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    void searchConversations(elements.historySearchInput.value).catch((error) => {
      elements.historyStatus.textContent =
        error instanceof Error ? error.message : "Saved chats could not be searched.";
    });
  });
  elements.historySearchInput.addEventListener("input", () => {
    if (!elements.historySearchInput.value.trim()) {
      renderHistoryList();
      elements.historyMore.hidden = !nextConversationCursor;
    }
  });
  narrowLayout.addEventListener("change", () => {
    if (!narrowLayout.matches) {
      elements.agentPanel.classList.remove("agent-panel--open");
      elements.historyButton.setAttribute("aria-expanded", "false");
    }
    syncHistoryPanelAccess();
  });

  function seedDemoConversation() {
    addMessage(
      "user",
      "Run an off-site consensus round for the workshop pricing page.",
    );
    addMessage(
      "agent",
      "Here's a LinkedIn post drafted from the new pricing page (Datalabs voice, playbook rules applied):\n\n\"How much does a corporate Power BI workshop actually cost in Australia? We just published our full pricing — day rates, half-day options, and what moves the number. No 'contact us for a quote' games. Link in comments. #PowerBI #DataStorytelling\"\n\nReview it, then copy and paste it into LinkedIn. Next up: one listicle pitch and one review request — say \"next\" when ready.",
    );
  }

  elements.chatToggle?.addEventListener("click", () => {
    setChatDrawerOpen(!chatDrawerOpen);
  });
  elements.drawerClose?.addEventListener("click", () => {
    setChatDrawerOpen(false);
  });
  elements.chatScrim?.addEventListener("click", () => {
    setChatDrawerOpen(false);
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && chatDrawerOpen) {
      setChatDrawerOpen(false);
    }
  });
  elements.pipelineNavButton?.addEventListener("click", () => {
    if (activeView === "pipeline") {
      return;
    }
    activeView = "pipeline";
    activeTabId = "";
    renderStage();
  });

  async function initialise() {
    syncHistoryPanelAccess();
    await loadAgents();
    await loadProfile();
    applyAgentIdentity();
    renderAgentList();
    renderSuggestions();
    renderDocuments();
    renderBrandBar();
    renderQuickActions();
    renderStage();
    void loadPipeline();
    if (new URLSearchParams(window.location.search).get("demo") === "1") {
      window.setTimeout(seedDemoConversation, 400);
    }
    try {
      await loadConversationList();
      try {
        await loadConversation(sessionId);
        return;
      } catch {
        // The browser may hold a pre-persistence session UUID.
      }
      const mostRecent = conversations.find(
        (conversation) => conversation.agentId === activeAgentId,
      ) ?? conversations[0];
      if (mostRecent) {
        await loadConversation(mostRecent.id);
      } else {
        await createConversation(activeAgentId);
      }
    } catch (error) {
      renderNewConversation();
      addError(
        error instanceof Error
          ? error.message
          : "Saved chats could not be loaded. Restart the local app and try again.",
      );
    }
  }

  void initialise();
})();
