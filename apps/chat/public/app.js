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
    if (activeAgentId === "business-development" && bdModesAvailable()) {
      if (bdMode === "festivals") {
        return [{ id: "bd-deadlines", label: "Deadlines" }];
      }
      if (bdMode === "press") {
        return [{ id: "bd-press", label: "Contacts" }];
      }
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
  // Set from the Lists tab so "Show on board" opens the board scoped to one
  // list. Empty means every list.
  let bdListFilter = "";
  // When set, the stage shows the compose screen instead of a tab body.
  // { listName } scopes which prospects are offered.
  let bdDraftContext = null;
  // Non-null puts the stage into a workflow screen: "import", "settings" or
  // "enrich".
  let bdScreen = null;
  // Three modes, because the three audiences are structurally different:
  // agencies are a commercial pipeline, festivals are deadlines, press is a
  // relationship. Oddtoe only for now — Datalabs has no festival or press
  // motion, so it stays on agencies.
  let bdMode = "agencies";
  let bdStreamFilter = "all";
  let bdImportList = "";

  const BD_MODES = [
    { id: "agencies", label: "Agencies" },
    { id: "festivals", label: "Festivals" },
    { id: "press", label: "Press" },
  ];

  function bdModesAvailable() {
    return (activeBrand()?.id ?? "oddtoe") === "oddtoe";
  }
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

  function bdStamp(value) {
    if (typeof value !== "string" || value === "") {
      return "";
    }
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return value;
    }
    return date.toLocaleString(undefined, {
      day: "numeric", month: "short", year: "numeric",
      hour: "2-digit", minute: "2-digit",
    });
  }

  // Where a list's rows actually came from. `source` is free text on the
  // prospect, so report what is there rather than mapping it to a guess.
  const BD_SOURCE_LABELS = {
    "synthetic-prototype": "Synthetic test data",
    manual: "Added by hand",
    "": "Imported",
  };

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
      bdScreen = "import";
      renderStage();
    });
    const findButton = document.createElement("button");
    findButton.className = "secondary-button";
    findButton.type = "button";
    findButton.textContent = "Find prospects";
    findButton.addEventListener("click", () => {
      bdScreen = "sourcing";
      renderStage();
    });
    actions.append(addButton, importButton, findButton);
    body.append(actions);

    if (bdListFilter !== "") {
      const filter = document.createElement("div");
      filter.className = "bd-filter";
      const label = document.createElement("span");
      label.textContent = `Showing ${bdListFilter}`;
      const clear = document.createElement("button");
      clear.type = "button";
      clear.className = "bd-filter__clear";
      clear.textContent = "Show all lists";
      clear.addEventListener("click", () => {
        bdListFilter = "";
        renderStage();
      });
      filter.append(label, clear);
      body.append(filter);
    }

    const status = document.createElement("p");
    status.className = "bd-board__status";
    status.setAttribute("role", "status");
    body.append(status);

    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading the prospect store…"));
    body.append(holder);

    const load = () => {
      const brand = activeBrand()?.id ?? "oddtoe";
      const listQuery = bdListFilter === ""
        ? ""
        : `&list=${encodeURIComponent(bdListFilter)}`;
      void fetchJson(
        `/api/prospects?brand=${encodeURIComponent(brand)}&limit=500${listQuery}`,
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

  function openAddProspectDialog(listName) {
    const dialog = elements.prospectAddDialog;
    if (!dialog) {
      return;
    }
    elements.prospectAddForm.reset();
    elements.prospectAddList.value = listName ?? "Manual additions";
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
      // Re-render the active tab rather than only the board: this dialog is
      // now reachable from Lists too.
      renderStage();
    } catch (error) {
      elements.prospectAddStatus.textContent =
        error.message ?? "That prospect could not be saved.";
    }
  }

  // ---- Outreach ---------------------------------------------------------
  // The sending operation: how much capacity is left today, whether the
  // guardrails that gate everything are actually configured, what is in
  // flight, who must never be contacted, and what has been happening.

  const BD_EVENT_TONE = {
    imported: "muted", enriched: "good", flagged: "warn", emailed: "good",
    opened: "good", clicked: "good", followed_up: "good", replied: "good",
    status_change: "muted",
  };

  function bdSection(title) {
    const wrap = document.createElement("section");
    wrap.className = "bd-section";
    const heading = document.createElement("h3");
    heading.className = "bd-section__title";
    heading.textContent = title;
    wrap.append(heading);
    return wrap;
  }

  function bdKeyValue(label, value, tone) {
    const row = document.createElement("div");
    row.className = "bd-kv";
    const name = document.createElement("dt");
    name.textContent = label;
    const detail = document.createElement("dd");
    detail.textContent = value === "" ? "—" : value;
    if (tone) {
      detail.classList.add(`bd-kv--${tone}`);
    }
    row.append(name, detail);
    return row;
  }

  function renderBdOutreachTab(body) {
    body.append(dashLabel("Outreach"));
    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading outreach…"));
    body.append(holder);

    const brand = activeBrand()?.id ?? "oddtoe";
    const q = encodeURIComponent(brand);
    void Promise.all([
      fetchJson(`/api/outreach/settings?brand=${q}`),
      fetchJson(`/api/prospects?brand=${q}&limit=500`),
      fetchJson(`/api/suppressions?brand=${q}`).catch(() => ({ suppressions: [] })),
      fetchJson(`/api/outreach/activity?brand=${q}&limit=15`).catch(() => ({ events: [] })),
    ])
      .then(([settingsPayload, boardPayload, suppressionPayload, activityPayload]) => {
        holder.replaceChildren();
        const configured = settingsPayload.configured === true;
        const settings = settingsPayload.settings;
        const prospects = boardPayload.prospects ?? [];
        const suppressions = suppressionPayload.suppressions ?? [];
        const suppressedKeys = new Set(suppressions.map((s) => s.emailKey));
        const events = activityPayload.events ?? [];

        // --- Not configured: nothing else on this screen matters ---------
        if (!configured) {
          const blocked = dashCard();
          blocked.append(
            dashEmpty(
              `No outreach settings for ${brand}. Nothing can be drafted until this brand has a sender name, a way to contact the sender, and an unsubscribe line — the store refuses to hand out a single prospect without them.`,
            ),
          );
          const setUp = document.createElement("button");
          setUp.type = "button";
          setUp.className = "secondary-button";
          setUp.textContent = "Set this up in chat";
          setUp.addEventListener("click", () => {
            bdScreen = "settings";
            renderStage();
          });
          blocked.append(setUp);
          holder.append(blocked);
          return;
        }

        // --- Today's capacity --------------------------------------------
        const today = new Date().toISOString().slice(0, 10);
        const draftedToday = prospects.filter(
          (p) => (p.draftedAt ?? "").slice(0, 10) === today,
        ).length;
        const remaining = Math.max(0, settings.dailyCap - draftedToday);
        const ready = prospects.filter(
          (p) =>
            BD_WORKABLE.includes(p.status) &&
            p.draftId === "" &&
            p.contactEmail !== "" &&
            !suppressedKeys.has(p.contactEmail.trim().toLowerCase()),
        );

        const capacity = bdSection("Today");
        const stats = document.createElement("div");
        stats.className = "dash-stats";
        stats.append(
          statCard(ready.length, "ready to draft"),
          statCard(draftedToday, "drafted today"),
          statCard(remaining, `left of ${settings.dailyCap}`),
        );
        capacity.append(stats);

        const meter = document.createElement("div");
        meter.className = "bd-meter";
        const fill = document.createElement("span");
        fill.className = "bd-meter__fill";
        fill.style.width = `${Math.min(100, (draftedToday / settings.dailyCap) * 100)}%`;
        meter.append(fill);
        capacity.append(meter);

        const capacityNote = document.createElement("p");
        capacityNote.className = "bd-listcard__note";
        capacityNote.textContent = remaining === 0
          ? `Today's cap of ${settings.dailyCap} is used up. Nothing further will be drafted until tomorrow.`
          : ready.length === 0
            ? "Nobody is ready to draft. Prospects need a contact email and must not be on the do-not-contact list."
            : `${Math.min(ready.length, remaining)} would be drafted in a run right now — ${ready.length} ready, capped at ${remaining} left today.`;
        capacity.append(capacityNote);

        if (ready.length > 0 && remaining > 0) {
          const draft = document.createElement("button");
          draft.type = "button";
          draft.className = "secondary-button";
          draft.textContent = `Draft ${Math.min(ready.length, remaining)} emails`;
          draft.addEventListener("click", () => {
            bdDraftContext = { listName: "" };
            renderStage();
          });
          capacity.append(draft);
        }
        holder.append(capacity);

        // --- The guardrails that gate everything -------------------------
        const setup = bdSection("Sending setup");
        const list = document.createElement("dl");
        list.className = "bd-kvlist";
        list.append(
          bdKeyValue("Sender", settings.senderName),
          bdKeyValue("Reply to", settings.senderContact),
          bdKeyValue("Opt-out line", settings.unsubscribeLine),
          bdKeyValue("Daily cap", `${settings.dailyCap} drafts`),
          bdKeyValue("Follow-up", `once, after ${settings.followUpDays} days`),
          bdKeyValue(
            "Guide page",
            settings.guidePageUrl === ""
              ? "not set — click tracking will stay empty for this brand"
              : settings.guidePageUrl,
            settings.guidePageUrl === "" ? "warn" : undefined,
          ),
          bdKeyValue("Last changed", bdStamp(settings.updatedAt)),
        );
        setup.append(list);
        const change = document.createElement("button");
        change.type = "button";
        change.className = "secondary-button";
        change.textContent = "Change these";
        change.addEventListener("click", () => {
          bdScreen = "settings";
          renderStage();
        });
        setup.append(change);
        holder.append(setup);

        // --- In flight ----------------------------------------------------
        const drafted = prospects.filter((p) => p.draftId !== "" && p.sentDate === "");
        const sent = prospects.filter((p) => p.sentDate !== "" && p.status !== "replied" && p.status !== "closed");
        const dueFollowUp = prospects.filter(
          (p) => p.followUpDue !== "" && p.followUpDue <= today && p.status !== "replied" && p.status !== "closed",
        );
        const replied = prospects.filter((p) => p.status === "replied");

        const flight = bdSection("In flight");
        const groups = [
          ["Waiting in Gmail, not sent", drafted, "Drafts you have not sent yet."],
          ["Sent, no reply yet", sent, "Out of your hands; waiting on them."],
          ["Follow-up due", dueFollowUp, "Past the follow-up date with no reply."],
          ["Replied — hand to Sales", replied, "BD is finished with these."],
        ];
        let anyFlight = false;
        for (const [title, rows, blurb] of groups) {
          if (rows.length === 0) {
            continue;
          }
          anyFlight = true;
          const group = document.createElement("div");
          group.className = "bd-flightgroup";
          const heading = document.createElement("p");
          heading.className = "bd-flightgroup__title";
          heading.textContent = `${title} (${rows.length})`;
          const note = document.createElement("p");
          note.className = "bd-flightgroup__note";
          note.textContent = blurb;
          group.append(heading, note);
          const names = document.createElement("div");
          names.className = "bd-flightgroup__names";
          for (const row of rows.slice(0, 12)) {
            const chip = document.createElement("button");
            chip.type = "button";
            chip.className = "bd-namechip";
            chip.textContent = row.company;
            chip.addEventListener("click", () => openProspectDialog(row.prospectId));
            names.append(chip);
          }
          if (rows.length > 12) {
            const more = document.createElement("span");
            more.className = "bd-flightgroup__more";
            more.textContent = `+${rows.length - 12} more`;
            names.append(more);
          }
          group.append(names);
          flight.append(group);
        }
        if (!anyFlight) {
          flight.append(
            dashEmpty("Nothing in flight. No drafts waiting, nothing sent, no follow-ups due."),
          );
        }
        holder.append(flight);

        // --- Do-not-contact -----------------------------------------------
        const dnc = bdSection(`Do-not-contact (${suppressions.length})`);
        const dncNote = document.createElement("p");
        dncNote.className = "bd-listcard__note";
        dncNote.textContent =
          "Checked before every draft and again before anything reaches Gmail. This is what makes the opt-out line real rather than decorative.";
        dnc.append(dncNote);

        if (suppressions.length > 0) {
          const table = document.createElement("div");
          table.className = "bd-dnclist";
          for (const entry of suppressions) {
            const row = document.createElement("div");
            row.className = "bd-dncrow";
            const email = document.createElement("span");
            email.className = "bd-dncrow__email";
            email.textContent = entry.emailKey;
            const reason = document.createElement("span");
            reason.className = "stage-chip stage-chip--closed";
            reason.textContent = entry.reason;
            const when = document.createElement("span");
            when.className = "bd-dncrow__when";
            when.textContent = bdStamp(entry.createdAt);
            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "bd-listcard__edit";
            remove.textContent = "Remove";
            remove.addEventListener("click", () => {
              remove.disabled = true;
              void fetchJson(
                `/api/suppressions?brand=${q}&email=${encodeURIComponent(entry.emailKey)}`,
                { method: "DELETE" },
              )
                .then(() => renderStage())
                .catch(() => {
                  remove.disabled = false;
                  remove.textContent = "Could not remove";
                });
            });
            row.append(email, reason, when, remove);
            table.append(row);
          }
          dnc.append(table);
        }

        const addForm = document.createElement("form");
        addForm.className = "bd-dncform";
        const emailField = document.createElement("input");
        emailField.type = "email";
        emailField.required = true;
        emailField.maxLength = 254;
        emailField.placeholder = "someone@example.com";
        emailField.setAttribute("aria-label", "Email to never contact");
        const reasonField = document.createElement("select");
        reasonField.setAttribute("aria-label", "Reason");
        for (const [value, label] of [
          ["unsubscribed", "Unsubscribed"], ["asked", "Asked to stop"],
          ["bounced", "Bounced"], ["manual", "Manual"],
        ]) {
          const option = document.createElement("option");
          option.value = value;
          option.textContent = label;
          reasonField.append(option);
        }
        const addButton = document.createElement("button");
        addButton.type = "submit";
        addButton.className = "secondary-button";
        addButton.textContent = "Never contact";
        const addStatus = document.createElement("p");
        addStatus.className = "prospect-add__status";
        addStatus.setAttribute("role", "status");
        addForm.addEventListener("submit", (event) => {
          event.preventDefault();
          addStatus.textContent = "Saving…";
          void fetchJson("/api/suppressions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              brand, email: emailField.value, reason: reasonField.value,
              detail: "Added from the Outreach screen",
            }),
          })
            .then(() => renderStage())
            .catch((error) => {
              addStatus.textContent = error.message ?? "Could not save that.";
            });
        });
        addForm.append(emailField, reasonField, addButton);
        dnc.append(addForm, addStatus);
        holder.append(dnc);

        // --- Recent activity ----------------------------------------------
        const activity = bdSection("Recent activity");
        if (events.length === 0) {
          activity.append(dashEmpty("Nothing recorded yet."));
        } else {
          const feed = document.createElement("ul");
          feed.className = "bd-feed";
          for (const event of events) {
            const item = document.createElement("li");
            const when = document.createElement("span");
            when.className = "bd-feed__when";
            when.textContent = bdStamp(event.occurredAt);
            const kind = document.createElement("span");
            kind.className = `bd-feed__kind bd-liststat--${BD_EVENT_TONE[event.eventType] ?? "muted"}`;
            kind.textContent = BD_EVENT_LABELS[event.eventType] ?? event.eventType;
            const what = document.createElement("span");
            what.className = "bd-feed__what";
            what.textContent = `${event.company} — ${event.detail}`;
            item.append(when, kind, what);
            feed.append(item);
          }
          activity.append(feed);
        }
        holder.append(activity);
      })
      .catch(() => {
        holder.replaceChildren(
          dashEmpty("The prospect store is not reachable. Restart the local app and reload."),
        );
      });
  }

  // ---- Draft & review ---------------------------------------------------
  // The act of BD. A template composes a first pass for everyone eligible;
  // every draft is then editable on its own, because a template that nobody
  // edits is what makes cold email read like cold email. Validation runs
  // server-side before anything is marked ready, so a draft the store would
  // refuse can never be approved here.

  const BD_DEFAULT_TEMPLATE = [
    "Hi {{first_name}},",
    "",
    "I put together a guide to the biggest experiential agencies and {{company}} is in it — here's the entry: {{link}}",
    "",
    "We make generative animation and projection content for agencies that would rather not build it in-house. If a brief ever calls for it, I'm easy to reach.",
    "",
    "{{unsubscribe}}",
    "",
    "{{sender}}",
    "{{sender_contact}}",
  ].join("\n");

  const BD_DEFAULT_SUBJECT = "{{company}} is on our agencies guide";

  let bdTemplate = null;
  let bdSubjectTemplate = null;

  function bdFillTemplate(text, prospect, outreachUrl, settings) {
    const first = (prospect.contactName || "").trim().split(" ")[0] || "there";
    return text
      .replaceAll("{{first_name}}", first)
      .replaceAll("{{contact_name}}", prospect.contactName || "there")
      .replaceAll("{{company}}", prospect.company)
      .replaceAll("{{link}}", outreachUrl)
      .replaceAll("{{unsubscribe}}", settings.unsubscribeLine)
      .replaceAll("{{sender}}", settings.senderName)
      .replaceAll("{{sender_contact}}", settings.senderContact);
  }

  function bdExitDraft() {
    bdDraftContext = null;
    bdTemplate = null;
    bdSubjectTemplate = null;
    renderStage();
  }

  function renderBdDraftScreen(body) {
    const brand = activeBrand()?.id ?? "oddtoe";
    const q = encodeURIComponent(brand);
    const scope = bdDraftContext.listName ?? "";

    const back = document.createElement("button");
    back.type = "button";
    back.className = "bd-back";
    back.textContent = "← Back to Business Development";
    back.addEventListener("click", bdExitDraft);
    body.append(back);

    body.append(dashLabel(scope === "" ? "Draft outreach" : `Draft outreach · ${scope}`));

    const holder = document.createElement("div");
    holder.append(dashEmpty("Working out who is eligible…"));
    body.append(holder);

    const listQuery = scope === "" ? "" : `&list=${encodeURIComponent(scope)}`;
    void Promise.all([
      fetchJson(`/api/prospects/draftable?brand=${q}${listQuery}`),
      fetchJson(`/api/outreach/prepared?brand=${q}`).catch(() => ({ drafts: [] })),
    ])
      .then(([draftable, prepared]) => {
        holder.replaceChildren();
        const settings = draftable.settings;
        const eligible = draftable.eligible ?? [];
        const saved = new Map(
          (prepared.drafts ?? []).map((d) => [d.prospectId, d]),
        );

        if (bdTemplate === null) {
          bdTemplate = BD_DEFAULT_TEMPLATE;
          bdSubjectTemplate = BD_DEFAULT_SUBJECT;
        }

        // --- Header: what this run would do ---------------------------
        const summary = document.createElement("p");
        summary.className = "bd-listcard__note";
        summary.textContent = eligible.length === 0
          ? `Nobody is eligible right now. ${draftable.skipped.length} prospects were excluded — every one with a reason.`
          : `${eligible.length} eligible · ${draftable.remainingToday} left of today's cap of ${draftable.dailyCap} · ${draftable.skipped.length} excluded.`;
        holder.append(summary);

        if (eligible.length === 0) {
          const why = dashCard();
          const reasons = new Map();
          for (const s of draftable.skipped) {
            reasons.set(s.reason, (reasons.get(s.reason) ?? 0) + 1);
          }
          for (const [reason, count] of [...reasons.entries()].sort((a, b) => b[1] - a[1])) {
            const row = document.createElement("p");
            row.className = "bd-listcard__note";
            row.textContent = `${count} — ${reason}`;
            why.append(row);
          }
          holder.append(why);
          return;
        }

        // --- Template -------------------------------------------------
        const tpl = bdSection("Template");
        const tplNote = document.createElement("p");
        tplNote.className = "bd-flightgroup__note";
        tplNote.textContent =
          "Generates a first pass for everyone below. Tokens: {{first_name}} {{company}} {{link}} {{unsubscribe}} {{sender}} {{sender_contact}}. The opt-out line, sender name and each prospect's own link are required — a draft without them is refused.";
        tpl.append(tplNote);

        const subjectField = document.createElement("input");
        subjectField.className = "bd-tplfield";
        subjectField.value = bdSubjectTemplate;
        subjectField.setAttribute("aria-label", "Subject template");
        const bodyField = document.createElement("textarea");
        bodyField.className = "bd-tplfield bd-tplfield--body";
        bodyField.rows = 10;
        bodyField.value = bdTemplate;
        bodyField.setAttribute("aria-label", "Body template");
        tpl.append(subjectField, bodyField);

        const apply = document.createElement("button");
        apply.type = "button";
        apply.className = "secondary-button";
        apply.textContent = "Apply to all drafts";
        apply.addEventListener("click", () => {
          bdTemplate = bodyField.value;
          bdSubjectTemplate = subjectField.value;
          const rows = eligible.map((e) => ({
            prospectId: e.prospect.prospectId,
            subject: bdFillTemplate(subjectField.value, e.prospect, e.outreachUrl, settings),
            body: bdFillTemplate(bodyField.value, e.prospect, e.outreachUrl, settings),
            hook: "featured on the agencies guide",
            hookEvidence: "listed on the experiential-agencies guide page",
            state: "composing",
          }));
          apply.disabled = true;
          apply.textContent = "Applying…";
          void fetchJson("/api/outreach/prepared", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ brand, drafts: rows }),
          })
            .then(() => renderStage())
            .catch(() => {
              apply.disabled = false;
              apply.textContent = "Could not apply";
            });
        });
        tpl.append(apply);
        holder.append(tpl);

        // --- One card per eligible prospect ---------------------------
        const drafts = bdSection(`Drafts (${eligible.length})`);
        const state = new Map();

        for (const entry of eligible) {
          const prospect = entry.prospect;
          const existing = saved.get(prospect.prospectId);
          const card = dashCard();
          card.className = "dash-card bd-draftcard";

          const head = document.createElement("div");
          head.className = "bd-listcard__head";
          const who = document.createElement("h3");
          who.className = "bd-listcard__title";
          who.textContent = prospect.company;
          head.append(who);
          head.append(stageChip(prospect.status));
          const to = document.createElement("span");
          to.className = "bd-listcard__count";
          to.textContent = `${prospect.contactName || "—"} · ${prospect.contactEmail}`;
          head.append(to);
          card.append(head);

          if (entry.warning !== "") {
            const warn = document.createElement("p");
            warn.className = "prospect-detail__warning";
            warn.textContent = entry.warning;
            card.append(warn);
          }

          const subject = document.createElement("input");
          subject.className = "bd-draftfield";
          subject.setAttribute("aria-label", `Subject for ${prospect.company}`);
          subject.value = existing?.subject
            ?? bdFillTemplate(bdSubjectTemplate, prospect, entry.outreachUrl, settings);
          const bodyBox = document.createElement("textarea");
          bodyBox.className = "bd-draftfield bd-draftfield--body";
          bodyBox.rows = 9;
          bodyBox.setAttribute("aria-label", `Body for ${prospect.company}`);
          bodyBox.value = existing?.body
            ?? bdFillTemplate(bdTemplate, prospect, entry.outreachUrl, settings);
          card.append(subject, bodyBox);

          const verdict = document.createElement("p");
          verdict.className = "bd-draftverdict";
          if (existing?.state === "approved") {
            verdict.textContent = "Ready to create in Gmail.";
            verdict.classList.add("bd-liststat--good");
          }
          card.append(verdict);

          const row = document.createElement("div");
          row.className = "bd-listcard__actions";
          const include = document.createElement("label");
          include.className = "bd-include";
          const box = document.createElement("input");
          box.type = "checkbox";
          box.checked = existing?.state !== "discarded";
          include.append(box, document.createTextNode(" Include in this run"));
          row.append(include);

          const discard = document.createElement("button");
          discard.type = "button";
          discard.className = "bd-listcard__edit";
          discard.textContent = "Discard draft";
          discard.addEventListener("click", () => {
            void fetchJson(
              `/api/outreach/prepared?brand=${q}&prospectId=${encodeURIComponent(prospect.prospectId)}`,
              { method: "DELETE" },
            ).then(() => renderStage());
          });
          row.append(discard);
          card.append(row);

          state.set(prospect.prospectId, { subject, bodyBox, box, verdict, prospect });
          drafts.append(card);
        }
        holder.append(drafts);

        // --- Save / check / hand off -----------------------------------
        const bar = document.createElement("div");
        bar.className = "bd-draftbar";
        const barStatus = document.createElement("p");
        barStatus.className = "bd-draftbar__status";
        barStatus.setAttribute("role", "status");

        const collect = () =>
          [...state.entries()]
            .filter(([, ui]) => ui.box.checked)
            .map(([prospectId, ui]) => ({
              prospectId,
              subject: ui.subject.value,
              body: ui.bodyBox.value,
              hook: "featured on the agencies guide",
              hookEvidence: "listed on the experiential-agencies guide page",
            }));

        const save = document.createElement("button");
        save.type = "button";
        save.className = "secondary-button";
        save.textContent = "Save drafts";
        save.addEventListener("click", () => {
          const rows = collect().map((d) => ({ ...d, state: "composing" }));
          barStatus.textContent = "Saving…";
          void fetchJson("/api/outreach/prepared", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ brand, drafts: rows }),
          })
            .then(() => { barStatus.textContent = `Saved ${rows.length}.`; })
            .catch((e) => { barStatus.textContent = e.message ?? "Could not save."; });
        });

        const check = document.createElement("button");
        check.type = "button";
        check.className = "secondary-button";
        check.textContent = "Check against the rules";
        check.addEventListener("click", () => {
          const rows = collect();
          if (rows.length === 0) {
            barStatus.textContent = "Nothing selected.";
            return;
          }
          barStatus.textContent = "Checking…";
          void fetchJson("/api/outreach/validate-drafts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ brand, drafts: rows }),
          })
            .then((result) => {
              let approved = 0;
              for (const r of result.results) {
                const ui = state.get(r.prospectId);
                if (!ui) { continue; }
                ui.verdict.classList.remove("bd-liststat--good", "bd-liststat--warn");
                if (r.approved) {
                  approved += 1;
                  ui.verdict.textContent = r.warnings.length > 0
                    ? `Passes — but ${r.warnings.join("; ")}`
                    : "Passes every check.";
                  ui.verdict.classList.add(r.warnings.length > 0 ? "bd-liststat--warn" : "bd-liststat--good");
                } else {
                  ui.verdict.textContent = `Refused: ${r.reasons.join("; ")}`;
                  ui.verdict.classList.add("bd-liststat--warn");
                }
              }
              barStatus.textContent = `${approved} of ${rows.length} pass. Refused drafts cannot be created.`;
              // Persist the verdict as state so a reload remembers it.
              void fetchJson("/api/outreach/prepared", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  brand,
                  drafts: result.results.filter((r) => r.approved).map((r) => {
                    const ui = state.get(r.prospectId);
                    return {
                      prospectId: r.prospectId,
                      subject: ui.subject.value,
                      body: ui.bodyBox.value,
                      state: "approved",
                    };
                  }),
                }),
              });
            })
            .catch((e) => { barStatus.textContent = e.message ?? "Could not check."; });
        });

        const hand = document.createElement("button");
        hand.type = "button";
        hand.className = "send-button";
        hand.textContent = "Create in Gmail";
        hand.addEventListener("click", () => {
          openChatWithPrompt(
            `Create the approved outreach drafts for ${brand} in Gmail. They are saved in the store — read them from /api/outreach/prepared?brand=${brand}&state=approved, create each one, then record the Gmail ids.`,
          );
        });

        bar.append(save, check, hand);
        holder.append(bar, barStatus);

        const gmailNote = document.createElement("p");
        gmailNote.className = "bd-flightgroup__note";
        gmailNote.textContent =
          "Nothing is sent from this screen. Creating in Gmail happens through the agent, which has the mailbox connection; you review each draft in Gmail and send it yourself.";
        holder.append(gmailNote);
      })
      .catch((error) => {
        holder.replaceChildren(
          dashEmpty(error.message ?? "The prospect store is not reachable."),
        );
      });
  }

  // ---- Import, Settings, Enrichment -------------------------------------

  function bdBackLink(body, label = "← Back to Business Development") {
    const back = document.createElement("button");
    back.type = "button";
    back.className = "bd-back";
    back.textContent = label;
    back.addEventListener("click", () => {
      bdScreen = null;
      bdImportList = "";
      renderStage();
    });
    body.append(back);
  }

  // Each mode imports a different shape, so the header map and the required
  // column differ. Anything unmapped is reported rather than dropped.
  const BD_IMPORT_SHAPES = {
    agencies: {
      title: "Import companies",
      required: "company",
      endpoint: "/api/prospects",
      needsList: true,
      map: {
        company: "company", companyname: "company", agency: "company", organisation: "company",
        region: "region", location: "region", city: "region",
        tier: "tier", source: "source",
        website: "website", site: "website", url: "website",
        linkedincompanyurl: "linkedinCompanyUrl", companylinkedin: "linkedinCompanyUrl",
        contactname: "contactName", contact: "contactName", name: "contactName",
        contactemail: "contactEmail", email: "contactEmail",
        linkedinurl: "linkedinUrl", linkedin: "linkedinUrl",
        status: "status", notes: "notes", note: "notes", comments: "notes",
      },
    },
    festivals: {
      title: "Import opportunities",
      required: "name",
      endpoint: "/api/opportunities/import",
      needsList: false,
      map: {
        name: "name", festival: "name", event: "name", opportunity: "name",
        organiser: "organiser", organizer: "organiser", host: "organiser",
        kind: "kind", type: "kind", stream: "kind",
        city: "city", country: "country",
        url: "url", website: "url", link: "url",
        start: "eventStart", eventstart: "eventStart", startdate: "eventStart",
        end: "eventEnd", eventend: "eventEnd", enddate: "eventEnd",
        pressdeadline: "pressDeadline", submissiondeadline: "submissionDeadline",
        deadline: "submissionDeadline",
        contact: "contact", presscontact: "contact",
        relevance: "relevance", focus: "relevance", blurb: "relevance",
        nextaction: "nextAction", notes: "notes", note: "notes",
      },
    },
    press: {
      title: "Import press contacts",
      required: "outlet",
      endpoint: "/api/media-contacts/import",
      needsList: false,
      map: {
        outlet: "outlet", publication: "outlet", masthead: "outlet", show: "outlet",
        segment: "segment", kind: "segment", type: "segment",
        person: "person", name: "person", contact: "person", journalist: "person",
        role: "role", title: "role",
        url: "url", website: "url", link: "url",
        email: "email", contactpage: "contactPage",
        linkedin: "linkedin", hook: "hook", angle: "hook",
        whyfit: "whyFit", why: "whyFit", relevance: "whyFit",
        notes: "notes", note: "notes",
      },
    },
  };

  function bdParseDelimited(text) {
    const firstLine = text.split("\n", 1)[0] ?? "";
    const tabs = (firstLine.match(/\t/g) ?? []).length;
    const commas = (firstLine.match(/,/g) ?? []).length;
    const delimiter = tabs > 0 && tabs >= commas ? "\t" : ",";
    const rows = [];
    let row = [];
    let field = "";
    let quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (quoted) {
        if (ch === '"') {
          if (text[i + 1] === '"') { field += '"'; i += 1; } else { quoted = false; }
        } else { field += ch; }
      } else if (ch === '"') { quoted = true; }
      else if (ch === delimiter) { row.push(field); field = ""; }
      else if (ch === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
      else if (ch !== "\r") { field += ch; }
    }
    if (field !== "" || row.length > 0) { row.push(field); rows.push(row); }
    return rows.filter((line) => line.some((cell) => cell.trim() !== ""));
  }

  function renderBdImportScreen(body) {
    const brand = activeBrand()?.id ?? "oddtoe";
    const shape = BD_IMPORT_SHAPES[bdMode] ?? BD_IMPORT_SHAPES.agencies;
    bdBackLink(body);
    body.append(dashLabel(shape.title));

    const intro = document.createElement("p");
    intro.className = "bd-listcard__note";
    intro.textContent = `Paste rows or choose a file. The first row must be a header. A ${shape.required} column is required; everything else is optional and anything unrecognised is reported rather than silently dropped.`;
    body.append(intro);

    const card = dashCard();

    let listField = null;
    if (shape.needsList) {
      const label = document.createElement("label");
      label.className = "bd-importlabel";
      label.textContent = "List name";
      listField = document.createElement("input");
      listField.className = "bd-tplfield";
      listField.maxLength = 120;
      listField.value = bdImportList || `Imported ${new Date().toISOString().slice(0, 10)}`;
      card.append(label, listField);
    }

    const fileLabel = document.createElement("label");
    fileLabel.className = "bd-importlabel";
    fileLabel.textContent = "Choose a CSV or TSV file";
    const file = document.createElement("input");
    file.type = "file";
    file.accept = ".csv,.tsv,.txt,text/csv,text/plain";
    file.className = "bd-importfile";

    const pasteLabel = document.createElement("label");
    pasteLabel.className = "bd-importlabel";
    pasteLabel.textContent = "…or paste the rows";
    const paste = document.createElement("textarea");
    paste.className = "bd-tplfield bd-tplfield--body";
    paste.rows = 8;
    paste.placeholder = `${shape.required},…\n`;

    card.append(fileLabel, file, pasteLabel, paste);

    const preview = document.createElement("div");
    preview.className = "bd-importpreview";
    const status = document.createElement("p");
    status.className = "bd-draftbar__status";
    status.setAttribute("role", "status");

    const actions = document.createElement("div");
    actions.className = "bd-listcard__actions";
    const check = document.createElement("button");
    check.type = "button";
    check.className = "secondary-button";
    check.textContent = "Preview";
    const commit = document.createElement("button");
    commit.type = "button";
    commit.className = "send-button";
    commit.textContent = "Import";
    commit.disabled = true;
    actions.append(check, commit);
    card.append(actions, status, preview);
    body.append(card);

    let parsed = null;

    file.addEventListener("change", () => {
      const chosen = file.files?.[0];
      if (!chosen) { return; }
      const reader = new FileReader();
      reader.onload = () => {
        paste.value = String(reader.result ?? "");
        status.textContent = `Loaded ${chosen.name}.`;
      };
      reader.readAsText(chosen);
    });

    check.addEventListener("click", () => {
      preview.replaceChildren();
      commit.disabled = true;
      const table = bdParseDelimited(paste.value);
      if (table.length < 2) {
        status.textContent = "Needs a header row and at least one row of data.";
        return;
      }
      const header = table[0].map((cell) =>
        shape.map[cell.trim().toLowerCase().replace(/[^a-z0-9]/g, "")] ?? null,
      );
      const unknown = table[0].filter((cell, i) => header[i] === null && cell.trim() !== "");
      if (!header.includes(shape.required)) {
        status.textContent = `No ${shape.required} column found. Rename a column to "${shape.required}" and preview again.`;
        return;
      }
      const rows = [];
      let skipped = 0;
      for (const cells of table.slice(1)) {
        const record = {};
        header.forEach((field, i) => {
          const value = (cells[i] ?? "").trim();
          if (field && value !== "") { record[field] = value; }
        });
        if (!record[shape.required]) { skipped += 1; continue; }
        rows.push(record);
      }
      parsed = rows;

      const mapped = document.createElement("p");
      mapped.className = "bd-listcard__note";
      mapped.textContent = `${rows.length} rows ready${skipped > 0 ? `, ${skipped} skipped for having no ${shape.required}` : ""}. Columns matched: ${[...new Set(header.filter(Boolean))].join(", ")}.`;
      preview.append(mapped);
      if (unknown.length > 0) {
        const ignored = document.createElement("p");
        ignored.className = "bd-oppcard__next";
        ignored.textContent = `Ignored ${unknown.length} unrecognised column(s): ${unknown.join(", ")}.`;
        preview.append(ignored);
      }

      const wrap = document.createElement("div");
      wrap.className = "dash-table-wrap";
      const grid = document.createElement("table");
      grid.className = "dash-table";
      const head = document.createElement("thead");
      const headRow = document.createElement("tr");
      const columns = [...new Set(header.filter(Boolean))].slice(0, 6);
      for (const column of columns) {
        const th = document.createElement("th");
        th.textContent = column;
        headRow.append(th);
      }
      head.append(headRow);
      const tbody = document.createElement("tbody");
      for (const record of rows.slice(0, 8)) {
        const tr = document.createElement("tr");
        for (const column of columns) {
          const td = document.createElement("td");
          const value = record[column] ?? "";
          td.textContent = value.length > 60 ? `${value.slice(0, 60)}…` : value;
          tr.append(td);
        }
        tbody.append(tr);
      }
      grid.append(head, tbody);
      wrap.append(grid);
      preview.append(wrap);
      if (rows.length > 8) {
        const more = document.createElement("p");
        more.className = "bd-oppcard__note";
        more.textContent = `Showing the first 8 of ${rows.length}.`;
        preview.append(more);
      }
      status.textContent = "Looks readable. Import when you're happy.";
      commit.disabled = rows.length === 0;
    });

    commit.addEventListener("click", () => {
      if (!parsed || parsed.length === 0) { return; }
      commit.disabled = true;
      status.textContent = "Importing…";
      const payload = shape.needsList
        ? { brand, listName: listField.value.trim(), rows: parsed }
        : { brand, rows: parsed };
      void fetchJson(shape.endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
        .then((result) => {
          const inserted = result.result?.inserted ?? result.written ?? parsed.length;
          const duplicates = result.result?.duplicates ?? 0;
          status.textContent = `Imported ${inserted}${duplicates > 0 ? `, ${duplicates} already there and left alone` : ""}.`;
          const done = document.createElement("button");
          done.type = "button";
          done.className = "secondary-button";
          done.textContent = "Back to the board";
          done.addEventListener("click", () => {
            bdScreen = null;
            bdImportList = "";
            activeTabId = "";
            renderStage();
          });
          preview.replaceChildren(done);
          if (duplicates > 0 && result.result?.duplicateCompanies?.length) {
            const names = document.createElement("p");
            names.className = "bd-oppcard__next";
            names.textContent = `Already present: ${result.result.duplicateCompanies.slice(0, 10).join(", ")}`;
            preview.append(names);
          }
        })
        .catch((error) => {
          commit.disabled = false;
          status.textContent = error.message ?? "That import could not be saved.";
        });
    });
  }

  function bdField(parent, label, value, { hint, kind = "input", maxLength = 300 } = {}) {
    const wrap = document.createElement("div");
    wrap.className = "bd-formrow";
    const name = document.createElement("label");
    name.className = "bd-importlabel";
    name.textContent = label;
    const field = document.createElement(kind === "area" ? "textarea" : "input");
    field.className = "bd-tplfield";
    field.maxLength = maxLength;
    field.value = value ?? "";
    if (kind === "area") { field.rows = 2; }
    if (kind === "number") { field.type = "number"; field.min = "1"; }
    name.setAttribute("for", "");
    wrap.append(name, field);
    if (hint) {
      const note = document.createElement("p");
      note.className = "bd-oppcard__next";
      note.textContent = hint;
      wrap.append(note);
    }
    parent.append(wrap);
    return field;
  }

  function renderBdSettingsScreen(body) {
    const brand = activeBrand()?.id ?? "oddtoe";
    const q = encodeURIComponent(brand);
    bdBackLink(body);
    body.append(dashLabel(`Outreach settings · ${activeBrand()?.label ?? brand}`));

    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading settings…"));
    body.append(holder);

    void Promise.all([
      fetchJson(`/api/outreach/settings?brand=${q}`),
      fetchJson(`/api/outreach/campaign-list?brand=${q}`).catch(() => ({ campaigns: [] })),
    ]).then(([settingsPayload, campaignPayload]) => {
      holder.replaceChildren();
      const s = settingsPayload.settings ?? {
        senderName: "", senderContact: "", unsubscribeLine: "",
        dailyCap: 10, followUpDays: 7, guidePageUrl: "",
      };

      const gate = document.createElement("p");
      gate.className = "bd-listcard__note";
      gate.textContent =
        "Nothing can be drafted for this brand until the sender name, reply address and opt-out line are all set. The store refuses to hand out a single prospect without them, and refuses any draft body that leaves the opt-out line or sender name out.";
      holder.append(gate);

      const form = dashCard();
      const senderName = bdField(form, "Sender name", s.senderName, { maxLength: 120, hint: "Appears in the sign-off and must appear verbatim in every draft." });
      const senderContact = bdField(form, "Reply address", s.senderContact, { maxLength: 200, hint: "Where replies go, and how the recipient can reach a human." });
      const unsubscribe = bdField(form, "Opt-out line", s.unsubscribeLine, { kind: "area", maxLength: 400, hint: "Must be a real opt-out: anyone who uses it goes on the do-not-contact list and can never be drafted to again." });
      const cap = bdField(form, "Daily cap", String(s.dailyCap), { kind: "number", hint: "Most drafts prepared in one day. Protects your domain reputation from a volume spike." });
      const followUp = bdField(form, "Follow-up interval (days)", String(s.followUpDays), { kind: "number", hint: "One follow-up only, this many days after sending." });
      const guide = bdField(form, "Guide page URL", s.guidePageUrl, { maxLength: 500, hint: "Each draft links here with the prospect's own utm_content. Leave blank and click tracking stays empty for this brand." });

      const preview = document.createElement("pre");
      preview.className = "bd-footerpreview";
      const paint = () => {
        preview.textContent = [
          "…",
          "",
          unsubscribe.value || "[no opt-out line — drafting is blocked]",
          "",
          senderName.value || "[no sender name — drafting is blocked]",
          senderContact.value,
        ].join("\n");
      };
      paint();
      for (const field of [senderName, senderContact, unsubscribe]) {
        field.addEventListener("input", paint);
      }
      const previewLabel = document.createElement("p");
      previewLabel.className = "bd-importlabel";
      previewLabel.textContent = "How every draft will end";
      form.append(previewLabel, preview);

      const status = document.createElement("p");
      status.className = "bd-draftbar__status";
      status.setAttribute("role", "status");
      const save = document.createElement("button");
      save.type = "button";
      save.className = "send-button";
      save.textContent = "Save settings";
      save.addEventListener("click", () => {
        status.textContent = "Saving…";
        void fetchJson("/api/outreach/settings", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            brand,
            senderName: senderName.value,
            senderContact: senderContact.value,
            unsubscribeLine: unsubscribe.value,
            dailyCap: Number(cap.value) || undefined,
            followUpDays: Number(followUp.value) || undefined,
            guidePageUrl: guide.value,
          }),
        })
          .then(() => { status.textContent = "Saved."; })
          .catch((error) => { status.textContent = error.message ?? "Could not save."; });
      });
      form.append(save, status);
      holder.append(form);

      // --- Campaigns ---------------------------------------------------
      const campaigns = campaignPayload.campaigns ?? [];
      const section = bdSection(`Campaigns (${campaigns.length})`);
      const why = document.createElement("p");
      why.className = "bd-listcard__note";
      why.textContent =
        "A campaign sets the offer and the utm_campaign tag on every link in a drafting run. Without one, links fall back to a generic tag and clicks cannot be attributed to a particular push.";
      section.append(why);

      for (const campaign of campaigns) {
        const row = document.createElement("div");
        row.className = "bd-dncrow";
        const name = document.createElement("span");
        name.className = "bd-dncrow__email";
        name.textContent = campaign.name;
        const tag = document.createElement("span");
        tag.className = "stage-chip stage-chip--tier";
        tag.textContent = campaign.brief.utmCampaign || "outreach";
        const when = document.createElement("span");
        when.className = "bd-dncrow__when";
        when.textContent = bdStamp(campaign.createdAt);
        row.append(name, tag, when);
        section.append(row);
      }

      const newCampaign = dashCard();
      const cName = bdField(newCampaign, "New campaign name", "", { maxLength: 120 });
      const cOffer = bdField(newCampaign, "Offer", "", { kind: "area", maxLength: 1000, hint: "What this push is actually offering. Reaches the drafting screen as context." });
      const cUtm = bdField(newCampaign, "UTM campaign tag", "", { maxLength: 120, hint: "Lowercase, hyphenated. Appears in every link so GA4 can attribute the clicks." });
      const cStatus = document.createElement("p");
      cStatus.className = "bd-draftbar__status";
      const create = document.createElement("button");
      create.type = "button";
      create.className = "secondary-button";
      create.textContent = "Create campaign";
      create.addEventListener("click", () => {
        if (cName.value.trim() === "") {
          cStatus.textContent = "A campaign needs a name.";
          return;
        }
        cStatus.textContent = "Creating…";
        void fetchJson("/api/outreach/campaigns", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            brand, name: cName.value, offer: cOffer.value,
            utmCampaign: cUtm.value, guidePageUrl: guide.value,
          }),
        })
          .then(() => renderStage())
          .catch((error) => { cStatus.textContent = error.message ?? "Could not create."; });
      });
      newCampaign.append(create, cStatus);
      section.append(newCampaign);
      holder.append(section);
    }).catch(() => {
      holder.replaceChildren(dashEmpty("The store is not reachable."));
    });
  }

  function renderBdEnrichScreen(body) {
    const brand = activeBrand()?.id ?? "oddtoe";
    const q = encodeURIComponent(brand);
    bdBackLink(body);
    body.append(dashLabel("Find contacts"));

    const holder = document.createElement("div");
    holder.append(dashEmpty("Working out who can be enriched…"));
    body.append(holder);

    const listQuery = bdImportList === "" ? "" : `&list=${encodeURIComponent(bdImportList)}`;
    void fetchJson(`/api/enrichment/quote?brand=${q}${listQuery}`)
      .then((quote) => {
        holder.replaceChildren();
        const eligible = quote.eligible ?? [];
        const missing = quote.missingUrl ?? [];

        const intro = document.createElement("p");
        intro.className = "bd-listcard__note";
        intro.textContent = `Enrichment searches LinkedIn for a named contact and an address at each company. It needs a LinkedIn company URL and an empty contact email. About $${quote.costPerCompanyUsd.toFixed(2)} per company, charged to your Apify credit.`;
        holder.append(intro);

        if (!quote.configured) {
          const blocked = dashCard();
          blocked.append(
            dashEmpty(
              "This screen cannot run enrichment yet: the app has no APIFY_TOKEN. Add APIFY_TOKEN=… to the project's .env and restart, and the run button here starts working. Until then you can still see who is eligible and what it would cost.",
            ),
          );
          holder.append(blocked);
        }

        if (eligible.length === 0) {
          holder.append(
            dashEmpty(
              missing.length > 0
                ? `Nobody is enrichable. ${missing.length} companies have no LinkedIn company URL, which enrichment needs first.`
                : "Nobody is enrichable — everyone already has a contact email.",
            ),
          );
        } else {
          const card = dashCard();
          const chosen = new Set(eligible.map((row) => row.prospectId));
          const cost = document.createElement("p");
          cost.className = "bd-listcard__note";
          const paintCost = () => {
            cost.textContent = `${chosen.size} selected · about $${(chosen.size * quote.costPerCompanyUsd).toFixed(2)}`;
          };
          for (const row of eligible) {
            const line = document.createElement("label");
            line.className = "bd-enrichrow";
            const box = document.createElement("input");
            box.type = "checkbox";
            box.checked = true;
            box.addEventListener("change", () => {
              if (box.checked) { chosen.add(row.prospectId); } else { chosen.delete(row.prospectId); }
              paintCost();
            });
            const name = document.createElement("span");
            name.className = "bd-enrichrow__name";
            name.textContent = row.company;
            const url = document.createElement("span");
            url.className = "bd-enrichrow__url";
            url.textContent = row.linkedinCompanyUrl;
            line.append(box, name, url);
            card.append(line);
          }
          paintCost();
          card.append(cost);

          const status = document.createElement("p");
          status.className = "bd-draftbar__status";
          status.setAttribute("role", "status");
          const run = document.createElement("button");
          run.type = "button";
          run.className = "send-button";
          run.textContent = "Run enrichment";
          run.disabled = !quote.configured;
          run.addEventListener("click", () => {
            run.disabled = true;
            status.textContent = "Running — this takes up to a minute per batch…";
            void fetchJson("/api/enrichment/run", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ brand, prospects: [...chosen] }),
            })
              .then((result) => {
                status.textContent = `Done. ${result.written} of ${result.findings.length} got a contact. Cost about $${result.costUsd.toFixed(2)}.`;
                const results = document.createElement("div");
                for (const finding of result.findings) {
                  const line = document.createElement("p");
                  line.className = finding.contactEmail === ""
                    ? "bd-oppcard__next"
                    : "bd-listcard__note";
                  line.textContent = finding.contactEmail === ""
                    ? `${finding.company}: nothing found — ${finding.flagReason}`
                    : `${finding.company}: ${finding.contactName || "(no name)"} ${finding.contactEmail} [${finding.confidence}]${finding.flagReason ? ` — ${finding.flagReason}` : ""}`;
                  results.append(line);
                }
                card.replaceChildren(results, status);
              })
              .catch((error) => {
                run.disabled = false;
                status.textContent = error.message ?? "The run failed.";
              });
          });
          card.append(run, status);
          holder.append(card);
        }

        if (missing.length > 0) {
          const gap = bdSection(`No LinkedIn company URL (${missing.length})`);
          const note = document.createElement("p");
          note.className = "bd-listcard__note";
          note.textContent = `Enrichment cannot look these up until each has a company page URL: ${missing.slice(0, 20).join(", ")}${missing.length > 20 ? "…" : ""}`;
          gap.append(note);
          holder.append(gap);
        }
      })
      .catch(() => {
        holder.replaceChildren(dashEmpty("The store is not reachable."));
      });
  }

  // ---- Find prospects ---------------------------------------------------
  // Sourcing is a judgement, not a scrape — deciding whether a company is a
  // fit is the whole job. So this screen is the brief plus a review queue:
  // the research is handed to the agent, and what comes back is accepted or
  // rejected here rather than landing straight in the pipeline.

  function renderBdSourcingScreen(body) {
    const brand = activeBrand()?.id ?? "oddtoe";
    const q = encodeURIComponent(brand);
    bdBackLink(body);
    body.append(dashLabel("Find prospects"));

    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading briefs…"));
    body.append(holder);

    void fetchJson(`/api/sourcing/briefs?brand=${q}`)
      .then((payload) => {
        holder.replaceChildren();
        const briefs = payload.briefs ?? [];
        const candidates = payload.candidates ?? [];

        const intro = document.createElement("p");
        intro.className = "bd-listcard__note";
        intro.textContent =
          "Write a brief describing who you want, hand it to the agent to research, then accept or reject what it proposes. Nothing reaches the pipeline until you say so — an unreviewed list of companies is worse than no list.";
        holder.append(intro);

        // --- Review queue first: it is the thing waiting on you ----------
        const proposed = candidates.filter((c) => c.state === "proposed");
        if (proposed.length > 0) {
          const byBrief = new Map();
          for (const c of proposed) {
            if (!byBrief.has(c.briefId)) { byBrief.set(c.briefId, []); }
            byBrief.get(c.briefId).push(c);
          }
          const queue = bdSection(`Waiting for your call (${proposed.length})`);
          for (const [briefId, rows] of byBrief.entries()) {
            const brief = briefs.find((b) => b.briefId === briefId);
            const listName = brief?.listName || "Sourced";
            const heading = document.createElement("p");
            heading.className = "bd-flightgroup__title";
            heading.textContent = `${brief?.name ?? "Unknown brief"} → ${listName}`;
            queue.append(heading);
            for (const candidate of rows) {
              queue.append(bdCandidateCard(candidate, brand, listName));
            }
          }
          holder.append(queue);
        }

        // --- Existing briefs ---------------------------------------------
        if (briefs.length > 0) {
          const section = bdSection(`Briefs (${briefs.length})`);
          for (const brief of briefs) {
            const mine = candidates.filter((c) => c.briefId === brief.briefId);
            const card = dashCard();
            card.className = "dash-card bd-listcard";
            const head = document.createElement("div");
            head.className = "bd-listcard__head";
            const title = document.createElement("h3");
            title.className = "bd-listcard__title";
            title.textContent = brief.name;
            head.append(title);
            const count = document.createElement("span");
            count.className = "bd-listcard__count";
            const accepted = mine.filter((c) => c.state === "accepted").length;
            const rejected = mine.filter((c) => c.state === "rejected").length;
            const waiting = mine.filter((c) => c.state === "proposed").length;
            count.textContent = `${waiting} waiting · ${accepted} accepted · ${rejected} rejected · target ${brief.targetCount}`;
            head.append(count);
            card.append(head);

            const detail = document.createElement("p");
            detail.className = "bd-listcard__note";
            detail.textContent = brief.lookingFor || "No description written.";
            card.append(detail);

            const meta = document.createElement("dl");
            meta.className = "bd-listmeta";
            const metaRow = (label, value) => {
              if (!value) { return; }
              const dt = document.createElement("dt");
              dt.textContent = label;
              const dd = document.createElement("dd");
              dd.textContent = value;
              meta.append(dt, dd);
            };
            metaRow("Where", brief.geography);
            metaRow("Signals", brief.signals);
            metaRow("Exclude", brief.exclude);
            metaRow("Lands in", brief.listName || "Sourced");
            metaRow("Updated", bdStamp(brief.updatedAt));
            card.append(meta);

            const actions = document.createElement("div");
            actions.className = "bd-listcard__actions";
            const research = document.createElement("button");
            research.type = "button";
            research.className = "secondary-button";
            research.textContent = `Research ${brief.targetCount} candidates`;
            research.addEventListener("click", () => {
              openChatWithPrompt(
                [
                  `Research candidates for the sourcing brief "${brief.name}" (${brand}).`,
                  ``,
                  `Looking for: ${brief.lookingFor}`,
                  brief.geography ? `Where: ${brief.geography}` : "",
                  brief.signals ? `Signals that mark a good fit: ${brief.signals}` : "",
                  brief.exclude ? `Exclude: ${brief.exclude}` : "",
                  `Target: ${brief.targetCount} companies.`,
                  ``,
                  `For each one give the company name, website, LinkedIn company URL, region, one sentence on why it fits, and the URL you verified it from. Do not invent companies or URLs — anything you cannot verify, leave blank and say so.`,
                  `Then POST them to http://127.0.0.1:3000/api/sourcing/candidates with {"brand":"${brand}","briefId":"${brief.briefId}","candidates":[…]} so they land in the review queue. Do not import them as prospects; I review them myself.`,
                ].filter(Boolean).join("\n"),
              );
            });
            actions.append(research);
            card.append(actions);
            section.append(card);
          }
          holder.append(section);
        }

        // --- New brief ----------------------------------------------------
        const form = bdSection(briefs.length > 0 ? "New brief" : "Write your first brief");
        const card = dashCard();
        const name = bdField(card, "Brief name", "", { maxLength: 120, hint: "Something you'll recognise later, like \"Sydney experiential agencies\"." });
        const lookingFor = bdField(card, "Who you're looking for", "", { kind: "area", maxLength: 2000, hint: "The kind of company, what they do, roughly what size." });
        const geography = bdField(card, "Where", "", { maxLength: 300, hint: "Cities, countries, or a region. Leave blank for anywhere." });
        const signals = bdField(card, "Signals of a good fit", "", { kind: "area", maxLength: 1000, hint: "What tells you one is worth approaching — the work they show, the clients they name, an office near you." });
        const exclude = bdField(card, "Exclude", "", { kind: "area", maxLength: 1000, hint: "Anything to keep out: competitors, companies too small to commission, anyone already on the board." });
        const targetCount = bdField(card, "How many", "10", { kind: "number" });
        const listName = bdField(card, "Accepted ones land in this list", "Sourced", { maxLength: 120 });

        const status = document.createElement("p");
        status.className = "bd-draftbar__status";
        status.setAttribute("role", "status");
        const save = document.createElement("button");
        save.type = "button";
        save.className = "send-button";
        save.textContent = "Save brief";
        save.addEventListener("click", () => {
          if (name.value.trim() === "") {
            status.textContent = "Give the brief a name.";
            return;
          }
          status.textContent = "Saving…";
          void fetchJson("/api/sourcing/briefs", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              brand, name: name.value, lookingFor: lookingFor.value,
              geography: geography.value, signals: signals.value,
              exclude: exclude.value, targetCount: Number(targetCount.value) || 10,
              listName: listName.value,
            }),
          })
            .then(() => renderStage())
            .catch((error) => { status.textContent = error.message ?? "Could not save."; });
        });
        card.append(save, status);
        form.append(card);
        holder.append(form);
      })
      .catch(() => {
        holder.replaceChildren(dashEmpty("The store is not reachable."));
      });
  }

  function bdCandidateCard(candidate, brand, listName) {
    const card = dashCard();
    card.className = "dash-card bd-oppcard";
    const head = document.createElement("div");
    head.className = "bd-listcard__head";
    const title = document.createElement("h3");
    title.className = "bd-listcard__title";
    title.textContent = candidate.company;
    head.append(title);
    if (candidate.region !== "") {
      const region = document.createElement("span");
      region.className = "bd-listcard__count";
      region.textContent = candidate.region;
      head.append(region);
    }
    card.append(head);

    if (candidate.whyFit !== "") {
      const why = document.createElement("p");
      why.className = "bd-listcard__note";
      why.textContent = bdPlainText(candidate.whyFit);
      card.append(why);
    }

    // No verified source is a reason to look harder, not a reason to hide it.
    const provenance = document.createElement("p");
    provenance.className = "bd-oppcard__next";
    provenance.textContent = candidate.evidenceUrl === ""
      ? `Found by ${candidate.foundBy} · no source URL given — check before accepting`
      : `Found by ${candidate.foundBy} · verified from ${candidate.evidenceUrl}`;
    card.append(provenance);

    const actions = document.createElement("div");
    actions.className = "bd-listcard__actions";
    const status = document.createElement("span");
    status.className = "bd-draftbar__status";

    const decide = (decision) => {
      status.textContent = decision === "accepted" ? "Adding…" : "Rejecting…";
      void fetchJson("/api/sourcing/candidates", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ brand, candidateId: candidate.candidateId, decision, listName }),
      })
        .then((result) => {
          if (result.outcome === "duplicate") {
            status.textContent = `${result.company} was already on that list.`;
            return;
          }
          renderStage();
        })
        .catch((error) => { status.textContent = error.message ?? "Could not save that."; });
    };

    const accept = document.createElement("button");
    accept.type = "button";
    accept.className = "secondary-button";
    accept.textContent = `Add to ${listName}`;
    accept.addEventListener("click", () => decide("accepted"));
    const reject = document.createElement("button");
    reject.type = "button";
    reject.className = "bd-listcard__edit";
    reject.textContent = "Not a fit";
    reject.addEventListener("click", () => decide("rejected"));
    actions.append(accept, reject);
    for (const [label, href] of [["Website", candidate.website], ["LinkedIn", candidate.linkedinCompanyUrl], ["Source", candidate.evidenceUrl]]) {
      if (!href) { continue; }
      const link = document.createElement("a");
      link.href = href;
      link.target = "_blank";
      link.rel = "noreferrer noopener";
      link.className = "bd-listcard__edit";
      link.textContent = label;
      actions.append(link);
    }
    card.append(actions, status);
    return card;
  }

  // ---- Mode toggle, Festivals and Press ---------------------------------

  function renderBdModeToggle() {
    const wrap = document.createElement("div");
    wrap.className = "bd-modes";
    wrap.setAttribute("role", "tablist");
    wrap.setAttribute("aria-label", "Business development audience");
    for (const mode of BD_MODES) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "bd-mode";
      button.setAttribute("role", "tab");
      button.setAttribute("aria-selected", String(mode.id === bdMode));
      if (mode.id === bdMode) {
        button.classList.add("bd-mode--on");
      }
      button.textContent = mode.label;
      button.addEventListener("click", () => {
        if (mode.id === bdMode) {
          return;
        }
        bdMode = mode.id;
        bdDraftContext = null;
        bdScreen = null;
        bdStreamFilter = "all";
        activeTabId = "";
        renderStage();
      });
      wrap.append(button);
    }
    return wrap;
  }

  // The research blurbs were written for a web page and carry markup and
  // HTML entities. Rendered with textContent they show as literal tags, so
  // strip them rather than trusting the source to be plain text.
  function bdPlainText(value) {
    return (value ?? "")
      .replace(/<[^>]*>/g, "")
      .replaceAll("&mdash;", "—")
      .replaceAll("&ndash;", "–")
      .replaceAll("&amp;", "&")
      .replaceAll("&nbsp;", " ")
      .replaceAll("&quot;", '"')
      .replaceAll("&#39;", "'")
      .replace(/\s+/g, " ")
      .trim();
  }

  const BD_KIND_LABELS = {
    press: "Press accreditation", market: "Market pitch", prize: "Prize",
    opencall: "Open call", register: "Register / EOI", scouting: "Scouting",
  };

  const BD_OPP_STATUSES = [
    "researching", "shortlisted", "preparing", "submitted",
    "accepted", "declined", "passed", "missed",
  ];

  const BD_MEDIA_STATUSES = ["sourced", "qualified", "drafted", "sent", "outcome"];

  // A deadline is only a date if someone read it on the organiser's page.
  // "TO VERIFY" is a real and common value in the source data and must not
  // be rendered as though it were a confirmed date.
  function bdDeadline(value) {
    const raw = (value ?? "").trim();
    if (raw === "") {
      return { kind: "none", text: "—", days: null };
    }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(raw)) {
      return { kind: "unverified", text: raw, days: null };
    }
    const days = Math.round(
      (new Date(`${raw}T00:00:00Z`).getTime() - Date.now()) / 86_400_000,
    );
    return { kind: days < 0 ? "past" : "date", text: raw, days };
  }

  // Order by the soonest date we actually have. A confirmed deadline wins;
  // failing that the event date, because press deadlines typically close two
  // to three months before an event, so the event date is a usable proxy for
  // urgency. The card still says which of the two it is — an inferred
  // urgency must never read as a confirmed deadline.
  function bdSoonest(opportunity) {
    const deadlines = [
      bdDeadline(opportunity.pressDeadline),
      bdDeadline(opportunity.submissionDeadline),
    ].filter((d) => d.days !== null);
    if (deadlines.length > 0) {
      return { days: Math.min(...deadlines.map((d) => d.days)), basis: "deadline" };
    }
    const event = bdDeadline(opportunity.eventStart);
    if (event.days !== null) {
      return { days: event.days, basis: "event" };
    }
    return null;
  }

  function bdSoonestDays(opportunity) {
    return bdSoonest(opportunity)?.days ?? null;
  }

  function bdFilterChips(counts, active, onPick) {
    const row = document.createElement("div");
    row.className = "bd-chips";
    const total = [...counts.values()].reduce((a, b) => a + b, 0);
    const make = (id, label, count) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "bd-chip";
      if (id === active) {
        chip.classList.add("bd-chip--on");
      }
      chip.textContent = `${label} ${count}`;
      chip.addEventListener("click", () => onPick(id));
      row.append(chip);
    };
    make("all", "All", total);
    for (const [key, count] of [...counts.entries()].sort((a, b) => b[1] - a[1])) {
      make(key, BD_KIND_LABELS[key] ?? key.replaceAll("_", " "), count);
    }
    return row;
  }

  function bdImportBar(body, label) {
    const actions = document.createElement("div");
    actions.className = "bd-actions";
    const importButton = document.createElement("button");
    importButton.type = "button";
    importButton.className = "secondary-button";
    importButton.textContent = label;
    importButton.addEventListener("click", () => {
      bdScreen = "import";
      renderStage();
    });
    actions.append(importButton);
    body.append(actions);
  }

  function renderBdFestivalsTab(body) {
    body.append(dashLabel("Deadlines"));
    bdImportBar(body, "Import opportunities");
    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading opportunities…"));
    body.append(holder);

    const brand = activeBrand()?.id ?? "oddtoe";
    void fetchJson(`/api/opportunities?brand=${encodeURIComponent(brand)}`)
      .then((payload) => {
        holder.replaceChildren();
        const all = payload.opportunities ?? [];
        if (all.length === 0) {
          holder.append(
            dashEmpty("No opportunities yet. Seed them with scripts/bd-seed-streams.mjs, or add one through chat."),
          );
          return;
        }

        const counts = new Map();
        for (const o of all) {
          counts.set(o.kind, (counts.get(o.kind) ?? 0) + 1);
        }
        holder.append(
          bdFilterChips(counts, bdStreamFilter, (id) => {
            bdStreamFilter = id;
            renderStage();
          }),
        );

        const rows = bdStreamFilter === "all"
          ? all
          : all.filter((o) => o.kind === bdStreamFilter);

        // The honest headline: most deadlines in the source data are not yet
        // confirmed, and that is the actual next job.
        const unverified = rows.filter(
          (o) =>
            bdDeadline(o.pressDeadline).kind === "unverified" ||
            bdDeadline(o.submissionDeadline).kind === "unverified",
        ).length;
        const summary = document.createElement("p");
        summary.className = "bd-listcard__note";
        const byEvent = rows.filter((o) => bdSoonest(o)?.basis === "event").length;
        summary.textContent = [
          `${rows.length} shown.`,
          unverified > 0
            ? `${unverified} have a deadline that still says "TO VERIFY" — read it on the organiser's page before trusting it.`
            : "",
          byEvent > 0
            ? `${byEvent} are ordered by event date because no deadline is confirmed; press deadlines usually close two to three months earlier, so treat those as sooner than they look.`
            : "",
        ].filter(Boolean).join(" ");
        holder.append(summary);

        const buckets = [
          ["Closing within 30 days", (d) => d !== null && d >= 0 && d <= 30],
          ["Within 90 days", (d) => d !== null && d > 30 && d <= 90],
          ["Later", (d) => d !== null && d > 90],
          ["Already passed", (d) => d !== null && d < 0],
          ["No date at all", (d) => d === null],
        ];

        for (const [title, test] of buckets) {
          const inBucket = rows.filter((o) => test(bdSoonestDays(o)));
          if (inBucket.length === 0) {
            continue;
          }
          const section = bdSection(`${title} (${inBucket.length})`);
          inBucket.sort((a, b) => {
            const da = bdSoonestDays(a);
            const db = bdSoonestDays(b);
            if (da === null && db === null) {
              return a.name.localeCompare(b.name);
            }
            if (da === null) { return 1; }
            if (db === null) { return -1; }
            return da - db;
          });
          for (const o of inBucket) {
            section.append(bdOpportunityCard(o, brand));
          }
          holder.append(section);
        }
      })
      .catch(() => {
        holder.replaceChildren(dashEmpty("The store is not reachable."));
      });
  }

  // Invented rows carry a demo- source id. They must be obvious: your real
  // festival research is verified against organiser pages, and a made-up
  // entry that looked real could send you chasing something that does not
  // exist.
  function bdDemoBadge(sourceId) {
    if (!(sourceId ?? "").startsWith("demo-")) {
      return null;
    }
    const chip = document.createElement("span");
    chip.className = "stage-chip stage-chip--flag";
    chip.textContent = "Demo";
    chip.title = "Invented row, added to fill out the interface. Not a real organisation.";
    return chip;
  }

  function bdOpportunityCard(opportunity, brand) {
    const card = dashCard();
    card.className = "dash-card bd-oppcard";

    const head = document.createElement("div");
    head.className = "bd-listcard__head";
    const title = document.createElement("h3");
    title.className = "bd-listcard__title";
    title.textContent = opportunity.name;
    head.append(title);
    const kind = document.createElement("span");
    kind.className = "stage-chip stage-chip--tier";
    kind.textContent = BD_KIND_LABELS[opportunity.kind] ?? opportunity.kind;
    head.append(kind);
    const demo = bdDemoBadge(opportunity.sourceId);
    if (demo) {
      head.append(demo);
    }
    const where = document.createElement("span");
    where.className = "bd-listcard__count";
    where.textContent = [opportunity.city, opportunity.country]
      .filter(Boolean).join(", ");
    head.append(where);
    card.append(head);

    const deadlines = document.createElement("div");
    deadlines.className = "bd-deadlines";
    const addDeadline = (label, value) => {
      const d = bdDeadline(value);
      if (d.kind === "none") {
        return;
      }
      const item = document.createElement("span");
      item.className = `bd-deadline bd-deadline--${d.kind}`;
      const suffix = d.days === null
        ? ""
        : d.days < 0
          ? ` · ${Math.abs(d.days)} days ago`
          : ` · in ${d.days} days`;
      item.textContent = `${label}: ${d.text}${suffix}`;
      deadlines.append(item);
    };
    addDeadline("Press", opportunity.pressDeadline);
    addDeadline("Submission", opportunity.submissionDeadline);
    if (opportunity.eventStart !== "") {
      const dates = document.createElement("span");
      const soonest = bdSoonest(opportunity);
      const inferred = soonest?.basis === "event";
      dates.className = `bd-deadline bd-deadline--${inferred ? "inferred" : "event"}`;
      const days = inferred && soonest.days >= 0 ? ` · in ${soonest.days} days` : "";
      dates.textContent = `Event: ${opportunity.eventStart}${opportunity.eventEnd ? ` → ${opportunity.eventEnd}` : ""}${days}`;
      dates.title = inferred
        ? "Sorted on this date because no deadline is confirmed. The real deadline is almost certainly earlier."
        : "";
      deadlines.append(dates);
    }
    if (deadlines.childElementCount > 0) {
      card.append(deadlines);
    }

    const relevance = bdPlainText(opportunity.relevance);
    if (relevance !== "") {
      const why = document.createElement("p");
      why.className = "bd-listcard__note";
      why.textContent = relevance.length > 240
        ? `${relevance.slice(0, 240)}…`
        : relevance;
      why.title = relevance;
      card.append(why);
    }
    if (opportunity.nextAction !== "") {
      const next = document.createElement("p");
      next.className = "bd-oppcard__next";
      next.textContent = `Next: ${opportunity.nextAction}`;
      card.append(next);
    }

    const actions = document.createElement("div");
    actions.className = "bd-listcard__actions";
    const select = document.createElement("select");
    select.className = "prospect-move__select";
    select.setAttribute("aria-label", `Status for ${opportunity.name}`);
    for (const status of BD_OPP_STATUSES) {
      const option = document.createElement("option");
      option.value = status;
      option.textContent = status;
      option.selected = status === opportunity.status;
      select.append(option);
    }
    select.addEventListener("change", () => {
      void fetchJson("/api/opportunities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          opportunityId: opportunity.opportunityId, status: select.value,
        }),
      }).then(() => renderStage());
    });
    actions.append(select);

    if (opportunity.url !== "") {
      const link = document.createElement("a");
      link.href = opportunity.url;
      link.target = "_blank";
      link.rel = "noreferrer noopener";
      link.className = "bd-listcard__edit";
      link.textContent = "Organiser page";
      actions.append(link);
    }
    const ask = document.createElement("button");
    ask.type = "button";
    ask.className = "bd-listcard__edit";
    ask.textContent = "Work on this in chat";
    ask.addEventListener("click", () => {
      openChatWithPrompt(
        `Verify the deadline for ${opportunity.name} on the organiser's own page, then tell me what applying involves.`,
      );
    });
    actions.append(ask);
    card.append(actions);
    return card;
  }

  function renderBdPressTab(body) {
    body.append(dashLabel("Press contacts"));
    bdImportBar(body, "Import press contacts");
    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading contacts…"));
    body.append(holder);

    const brand = activeBrand()?.id ?? "oddtoe";
    void fetchJson(`/api/media-contacts?brand=${encodeURIComponent(brand)}`)
      .then((payload) => {
        holder.replaceChildren();
        const all = payload.contacts ?? [];
        if (all.length === 0) {
          holder.append(dashEmpty("No press contacts yet."));
          return;
        }
        const counts = new Map();
        for (const c of all) {
          counts.set(c.segment, (counts.get(c.segment) ?? 0) + 1);
        }
        holder.append(
          bdFilterChips(counts, bdStreamFilter, (id) => {
            bdStreamFilter = id;
            renderStage();
          }),
        );
        const rows = bdStreamFilter === "all"
          ? all
          : all.filter((c) => c.segment === bdStreamFilter);

        for (const status of BD_MEDIA_STATUSES) {
          const inStatus = rows.filter((c) => c.status === status);
          if (inStatus.length === 0) {
            continue;
          }
          const section = bdSection(`${status} (${inStatus.length})`);
          for (const contact of inStatus) {
            section.append(bdMediaCard(contact));
          }
          holder.append(section);
        }
      })
      .catch(() => {
        holder.replaceChildren(dashEmpty("The store is not reachable."));
      });
  }

  function bdMediaCard(contact) {
    const card = dashCard();
    card.className = "dash-card bd-oppcard";
    const head = document.createElement("div");
    head.className = "bd-listcard__head";
    const title = document.createElement("h3");
    title.className = "bd-listcard__title";
    title.textContent = contact.outlet;
    head.append(title);
    const seg = document.createElement("span");
    seg.className = "stage-chip stage-chip--tier";
    seg.textContent = contact.segment.replaceAll("_", " ");
    head.append(seg);
    const demoChip = bdDemoBadge(contact.sourceId);
    if (demoChip) {
      head.append(demoChip);
    }
    const who = document.createElement("span");
    who.className = "bd-listcard__count";
    who.textContent = [contact.person, contact.role].filter(Boolean).join(" · ") || "no named contact yet";
    head.append(who);
    card.append(head);

    if (contact.hook !== "") {
      const hook = document.createElement("p");
      hook.className = "bd-listcard__note";
      hook.textContent = `Hook: ${bdPlainText(contact.hook)}`;
      card.append(hook);
    }
    const whyFit = bdPlainText(contact.whyFit);
    if (whyFit !== "") {
      const fit = document.createElement("p");
      fit.className = "bd-oppcard__next";
      fit.textContent = whyFit.length > 220 ? `${whyFit.slice(0, 220)}…` : whyFit;
      fit.title = whyFit;
      card.append(fit);
    }

    if (contact.outcome !== "") {
      const outcome = document.createElement("p");
      outcome.className = "bd-listcard__note";
      outcome.textContent = `Outcome: ${bdPlainText(contact.outcome)}`;
      card.append(outcome);
    }

    const reach = document.createElement("p");
    reach.className = "bd-oppcard__next";
    reach.textContent = contact.email !== ""
      ? `Email: ${contact.email}`
      : contact.contactPage !== ""
        ? "No direct email — via the outlet's contact page"
        : "No route to them recorded yet";
    card.append(reach);

    const actions = document.createElement("div");
    actions.className = "bd-listcard__actions";
    const select = document.createElement("select");
    select.className = "prospect-move__select";
    select.setAttribute("aria-label", `Status for ${contact.outlet}`);
    for (const status of BD_MEDIA_STATUSES) {
      const option = document.createElement("option");
      option.value = status;
      option.textContent = status;
      option.selected = status === contact.status;
      select.append(option);
    }
    select.addEventListener("change", () => {
      void fetchJson("/api/media-contacts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mediaId: contact.mediaId, status: select.value }),
      }).then(() => renderStage());
    });
    actions.append(select);
    for (const [label, href] of [
      ["Outlet", contact.url], ["Contact page", contact.contactPage],
      ["Evidence", contact.evidenceUrl],
    ]) {
      if (href === "") { continue; }
      const link = document.createElement("a");
      link.href = href;
      link.target = "_blank";
      link.rel = "noreferrer noopener";
      link.className = "bd-listcard__edit";
      link.textContent = label;
      actions.append(link);
    }
    card.append(actions);
    return card;
  }

  // ---- Lists ------------------------------------------------------------
  // A list is a cohort you work as a batch, so the question this screen has
  // to answer is "which one is worth my time, and what is stopping the rest".
  // Names alone cannot answer that; counts and the blocking reason can.

  const BD_WORKABLE = ["imported", "needs_review", "enriched"];

  function bdListStats(prospects, suppressed) {
    const byStatus = {};
    let ready = 0;
    let noEmail = 0;
    let flagged = 0;
    let noLinkedIn = 0;
    let suppressedCount = 0;
    let inFlight = 0;
    let lastTouched = "";
    let firstAdded = "";
    const sources = new Map();

    for (const p of prospects) {
      byStatus[p.status] = (byStatus[p.status] ?? 0) + 1;
      if (p.updatedAt > lastTouched) {
        lastTouched = p.updatedAt;
      }
      if (firstAdded === "" || p.createdAt < firstAdded) {
        firstAdded = p.createdAt;
      }
      const sourceKey = p.source ?? "";
      sources.set(sourceKey, (sources.get(sourceKey) ?? 0) + 1);
      if (p.status === "needs_review") {
        flagged += 1;
      }
      if (["emailed", "opened", "followed_up"].includes(p.status)) {
        inFlight += 1;
      }
      if (!BD_WORKABLE.includes(p.status) || p.draftId !== "") {
        continue;
      }
      if (p.contactEmail === "") {
        noEmail += 1;
        if (p.linkedinCompanyUrl === "") {
          noLinkedIn += 1;
        }
      } else if (suppressed.has(p.contactEmail.trim().toLowerCase())) {
        suppressedCount += 1;
      } else {
        ready += 1;
      }
    }
    return {
      total: prospects.length, byStatus, ready, noEmail, flagged,
      noLinkedIn, suppressed: suppressedCount, inFlight, lastTouched,
      firstAdded, sources,
    };
  }

  // A proportional bar beats eight numbers for "how far through is this".
  function bdStageBar(byStatus, total) {
    const bar = document.createElement("div");
    bar.className = "bd-listbar";
    for (const column of BD_COLUMNS) {
      const count = byStatus[column.status] ?? 0;
      if (count === 0) {
        continue;
      }
      const segment = document.createElement("span");
      segment.className = `bd-listbar__seg bd-listbar__seg--${column.status}`;
      segment.style.flexGrow = String(count);
      segment.title = `${count} ${column.label.toLowerCase()}`;
      bar.append(segment);
    }
    if (total === 0) {
      bar.classList.add("bd-listbar--empty");
    }
    return bar;
  }

  function bdStatLine(stats) {
    const line = document.createElement("div");
    line.className = "bd-liststats";
    const add = (value, label, tone) => {
      const item = document.createElement("span");
      item.className = `bd-liststat bd-liststat--${tone}`;
      const number = document.createElement("strong");
      number.textContent = String(value);
      item.append(number, document.createTextNode(` ${label}`));
      line.append(item);
    };
    add(stats.ready, "ready to draft", stats.ready > 0 ? "good" : "muted");
    add(stats.noEmail, "need a contact", stats.noEmail > 0 ? "warn" : "muted");
    add(stats.flagged, "flagged", stats.flagged > 0 ? "warn" : "muted");
    if (stats.inFlight > 0) {
      add(stats.inFlight, "in flight", "good");
    }
    if (stats.suppressed > 0) {
      add(stats.suppressed, "on do-not-contact", "muted");
    }
    return line;
  }

  function bdBlockerNote(stats) {
    if (stats.total === 0) {
      return "This list is empty.";
    }
    if (stats.ready === 0 && stats.noEmail > 0) {
      return stats.noLinkedIn > 0
        ? `Nothing can be drafted yet. ${stats.noEmail} need a contact, and ${stats.noLinkedIn} of those have no LinkedIn company URL, which enrichment needs first.`
        : `Nothing can be drafted yet. ${stats.noEmail} need a contact — enrichment can look for them.`;
    }
    if (stats.ready === 0) {
      return "Nothing left to draft in this list.";
    }
    if (stats.noEmail > 0) {
      return `${stats.ready} ready now; ${stats.noEmail} still need a contact before they can be drafted.`;
    }
    return `All ${stats.ready} workable prospects have a contact.`;
  }

  function renderBdListsTab(body) {
    body.append(dashLabel("Lists"));
    const holder = document.createElement("div");
    holder.append(dashEmpty("Loading lists…"));
    body.append(holder);

    const brand = activeBrand()?.id ?? "oddtoe";
    void Promise.all([
      fetchJson(`/api/prospects?brand=${encodeURIComponent(brand)}&limit=500`),
      fetchJson(`/api/suppressions?brand=${encodeURIComponent(brand)}`)
        .catch(() => ({ suppressions: [] })),
      fetchJson(`/api/prospects/lists?brand=${encodeURIComponent(brand)}`)
        .catch(() => ({ lists: [] })),
    ])
      .then(([payload, suppressionPayload, listPayload]) => {
        const meta = new Map(
          (listPayload.lists ?? []).map((l) => [l.listName, l]),
        );
        holder.replaceChildren();
        const prospects = Array.isArray(payload.prospects)
          ? payload.prospects
          : [];
        const suppressed = new Set(
          (suppressionPayload.suppressions ?? []).map((s) => s.emailKey),
        );
        if (prospects.length === 0) {
          holder.append(
            dashEmpty(
              "No lists yet. Import one through chat, or add a prospect on the board.",
            ),
          );
          return;
        }

        const byList = new Map();
        for (const prospect of prospects) {
          if (!byList.has(prospect.listName)) {
            byList.set(prospect.listName, []);
          }
          byList.get(prospect.listName).push(prospect);
        }

        const names = [...byList.keys()].sort();
        for (const listName of names) {
          const rows = byList.get(listName);
          const stats = bdListStats(rows, suppressed);
          const card = dashCard();
          card.className = "dash-card bd-listcard";

          const head = document.createElement("div");
          head.className = "bd-listcard__head";
          const title = document.createElement("h3");
          title.className = "bd-listcard__title";
          title.textContent = listName;
          head.append(title);
          // Synthetic rows must be obvious; a test list read as real would be
          // a genuinely bad mistake.
          if (rows.every((r) => r.source === "synthetic-prototype")) {
            const badge = document.createElement("span");
            badge.className = "stage-chip stage-chip--flag";
            badge.textContent = "Synthetic — test data";
            head.append(badge);
          }
          const count = document.createElement("span");
          count.className = "bd-listcard__count";
          count.textContent = `${stats.total} ${stats.total === 1 ? "prospect" : "prospects"}`;
          head.append(count);
          card.append(head);

          // Description: stored per list, editable in place. Nothing else
          // records what a list is for or why it exists.
          const description = document.createElement("p");
          description.className = "bd-listcard__desc";
          const savedDescription = meta.get(listName)?.description ?? "";
          description.textContent = savedDescription === ""
            ? "No description yet."
            : savedDescription;
          if (savedDescription === "") {
            description.classList.add("bd-listcard__desc--empty");
          }
          const editDescription = document.createElement("button");
          editDescription.type = "button";
          editDescription.className = "bd-listcard__edit";
          editDescription.textContent = savedDescription === "" ? "Add" : "Edit";
          editDescription.addEventListener("click", () => {
            const field = document.createElement("textarea");
            field.className = "bd-listcard__descedit";
            field.maxLength = 600;
            field.rows = 2;
            field.value = savedDescription;
            const save = document.createElement("button");
            save.type = "button";
            save.className = "secondary-button";
            save.textContent = "Save";
            save.addEventListener("click", () => {
              save.disabled = true;
              void fetchJson("/api/prospects/lists", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  brand, listName, description: field.value,
                }),
              })
                .then(() => renderStage())
                .catch(() => {
                  save.disabled = false;
                  save.textContent = "Could not save";
                });
            });
            const wrap = document.createElement("div");
            wrap.className = "bd-listcard__descwrap";
            wrap.append(field, save);
            descriptionRow.replaceWith(wrap);
            field.focus();
          });
          const descriptionRow = document.createElement("div");
          descriptionRow.className = "bd-listcard__descrow";
          descriptionRow.append(description, editDescription);
          card.append(descriptionRow);

          card.append(bdStageBar(stats.byStatus, stats.total));
          card.append(bdStatLine(stats));

          const note = document.createElement("p");
          note.className = "bd-listcard__note";
          note.textContent = bdBlockerNote(stats);
          card.append(note);

          const provenance = document.createElement("dl");
          provenance.className = "bd-listmeta";
          const metaRow = (label, value) => {
            if (value === "") {
              return;
            }
            const name = document.createElement("dt");
            name.textContent = label;
            const detail = document.createElement("dd");
            detail.textContent = value;
            provenance.append(name, detail);
          };
          const sourceText = [...stats.sources.entries()]
            .sort((a, b) => b[1] - a[1])
            .map(([key, n]) => `${BD_SOURCE_LABELS[key] ?? key} (${n})`)
            .join(" · ");
          metaRow("Source", sourceText);
          metaRow("First added", bdStamp(stats.firstAdded));
          metaRow("Last changed", bdStamp(stats.lastTouched));
          const listMeta = meta.get(listName);
          if (listMeta) {
            metaRow("Description saved", bdStamp(listMeta.updatedAt));
          }
          card.append(provenance);

          const actions = document.createElement("div");
          actions.className = "bd-listcard__actions";

          const show = document.createElement("button");
          show.type = "button";
          show.className = "secondary-button";
          show.textContent = "Show on board";
          show.addEventListener("click", () => {
            bdListFilter = listName;
            activeTabId = "bd-pipeline";
            renderStage();
          });
          actions.append(show);

          const addTo = document.createElement("button");
          addTo.type = "button";
          addTo.className = "secondary-button";
          addTo.textContent = "Add a prospect";
          addTo.addEventListener("click", () => {
            openAddProspectDialog(listName);
          });
          actions.append(addTo);

          const importMore = document.createElement("button");
          importMore.type = "button";
          importMore.className = "secondary-button";
          importMore.textContent = "Import more";
          importMore.addEventListener("click", () => {
            bdScreen = "import";
            bdImportList = listName;
            renderStage();
          });
          actions.append(importMore);

          if (stats.noEmail > 0) {
            const find = document.createElement("button");
            find.type = "button";
            find.className = "secondary-button";
            find.textContent = `Find ${stats.noEmail} contact${stats.noEmail === 1 ? "" : "s"}`;
            find.addEventListener("click", () => {
              bdScreen = "enrich";
              bdImportList = listName;
              renderStage();
            });
            actions.append(find);
          }

          if (stats.ready > 0) {
            const draft = document.createElement("button");
            draft.type = "button";
            draft.className = "secondary-button";
            draft.textContent = `Draft ${stats.ready} email${stats.ready === 1 ? "" : "s"}`;
            draft.addEventListener("click", () => {
              bdDraftContext = { listName };
              renderStage();
            });
            actions.append(draft);
          }

          card.append(actions);
          holder.append(card);
        }

        holder.append(
          dashNote(
            "Ready-to-draft counts the whole list; a drafting run is still capped at the daily send limit.",
          ),
        );
      })
      .catch(() => {
        holder.replaceChildren(
          dashEmpty("The prospect store is not reachable."),
        );
      });
  }

  let draggedPipelineItem = null;

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

  function makeIconCard(item, icon, { dimmed = false, draggable = false } = {}) {
    const card = document.createElement("button");
    card.className = "icon-card";
    card.type = "button";
    if (dimmed) {
      card.classList.add("icon-card--dimmed");
    }
    card.setAttribute("aria-expanded", "false");
    // A card can only be dragged when it maps back to a real line in a real
    // file; sample cards and anything the server marked unwritable stay put.
    if (draggable && item.source && Number.isInteger(item.line) && item.line >= 0) {
      card.draggable = true;
      card.classList.add("icon-card--draggable");
      card.addEventListener("dragstart", (event) => {
        draggedPipelineItem = item;
        card.classList.add("icon-card--dragging");
        event.dataTransfer.effectAllowed = "move";
        // Some browsers refuse to start a drag with an empty payload.
        event.dataTransfer.setData("text/plain", item.title);
      });
      card.addEventListener("dragend", () => {
        draggedPipelineItem = null;
        card.classList.remove("icon-card--dragging");
        for (const column of document.querySelectorAll(".kanban-col--drop")) {
          column.classList.remove("kanban-col--drop");
        }
      });
    }

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
    detail.textContent = item.note ?? item.title;
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

  // ---- Content Pipeline board ----
  // Every column is one marker in one of two markdown files, so a drag is a
  // one-character edit to a known line. Backlog, Awaiting review and Published
  // are the same file and move between each other freely; Outreach is a
  // different file and only ever leaves the board by being marked sent.
  const PIPELINE_COLUMNS = [
    {
      key: "nextPages",
      title: "Backlog",
      icon: "📝",
      source: "backlog",
      status: "queued",
      canAdd: true,
    },
    {
      key: "awaitingReview",
      title: "Awaiting review",
      icon: "👀",
      source: "backlog",
      status: "review",
    },
    {
      key: "outreach",
      title: "Outreach to send",
      icon: "📣",
      source: "outreach",
      status: "queued",
      canAdd: true,
      sendable: true,
    },
    {
      key: "published",
      title: "Published",
      icon: "✅",
      source: "backlog",
      status: "published",
    },
  ];

  function pipelinePost(payload) {
    return fetchJson("/api/pipeline", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload),
    });
  }

  function acceptsPipelineDrop(target, item) {
    return (
      Boolean(item) &&
      item.source === target.source &&
      item.status !== target.status
    );
  }

  // Wires one element as a drop target for a { source, status } pair.
  function pipelineDropTarget(element, target, commit) {
    element.addEventListener("dragover", (event) => {
      if (!acceptsPipelineDrop(target, draggedPipelineItem)) {
        return;
      }
      event.preventDefault();
      event.dataTransfer.dropEffect = "move";
      element.classList.add("kanban-col--drop");
    });
    element.addEventListener("dragleave", (event) => {
      if (!element.contains(event.relatedTarget)) {
        element.classList.remove("kanban-col--drop");
      }
    });
    element.addEventListener("drop", (event) => {
      const item = draggedPipelineItem;
      if (!acceptsPipelineDrop(target, item)) {
        return;
      }
      event.preventDefault();
      element.classList.remove("kanban-col--drop");
      commit(() =>
        pipelinePost({
          action: "move",
          source: item.source,
          line: item.line,
          fingerprint: item.fingerprint,
          status: target.status,
        }),
      );
    });
  }

  function pipelineAddForm(column, brand, commit) {
    const form = document.createElement("form");
    form.className = "kanban-add";
    const input = document.createElement("input");
    input.type = "text";
    input.className = "kanban-add__input";
    input.maxLength = 200;
    input.placeholder =
      column.source === "outreach" ? "Add an artifact…" : "Add a page…";
    input.setAttribute("aria-label", `Add a card to ${column.title}`);
    const select = document.createElement("select");
    select.className = "kanban-add__brand";
    select.setAttribute("aria-label", "Brand");
    for (const option of [
      { value: "datalabs", label: "Datalabs" },
      { value: "oddtoe", label: "Oddtoe" },
      { value: "general", label: "Both" },
    ]) {
      const element = document.createElement("option");
      element.value = option.value;
      element.textContent = option.label;
      select.append(element);
    }
    select.value = brand?.id ?? "general";
    const submit = document.createElement("button");
    submit.type = "submit";
    submit.className = "kanban-add__submit";
    submit.textContent = "Add";
    form.append(input, select, submit);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const title = input.value.trim();
      if (title === "") {
        input.focus();
        return;
      }
      commit(() =>
        pipelinePost({
          action: "add",
          source: column.source,
          brand: select.value,
          title,
        }),
      );
    });
    return form;
  }

  function pipelineColumn(column, payload, brand, commit) {
    const items = pipelineItemsFor(payload, column.key);
    const writable = payload.writable === true;
    const element = document.createElement("div");
    element.className = "kanban-col";

    const heading = document.createElement("p");
    heading.className = "kanban-col__title";
    const text = document.createElement("span");
    text.textContent = `${column.icon} ${column.title}`;
    const count = document.createElement("span");
    count.className = "kanban-col__count";
    count.textContent = String(items.length);
    heading.append(text, count);
    element.append(heading);

    // The list scrolls rather than truncating: the count in the heading is the
    // real number of items in the file, and all of them are reachable.
    const list = document.createElement("div");
    list.className = "kanban-col__list";
    if (items.length === 0) {
      list.append(dashEmpty("Empty."));
    }
    for (const item of items) {
      list.append(
        makeIconCard(item, column.icon, {
          dimmed: !itemMatchesBrand(item, brand),
          draggable: writable,
        }),
      );
    }
    element.append(list);

    if (writable) {
      pipelineDropTarget(element, column, commit);
      if (column.sendable) {
        // Sent outreach leaves the board, so it needs a target of its own.
        const sent = document.createElement("div");
        sent.className = "kanban-col__sent";
        sent.textContent = "✓ Drop here when sent";
        pipelineDropTarget(
          sent,
          { source: column.source, status: "published" },
          commit,
        );
        element.append(sent);
      }
      if (column.canAdd) {
        element.append(pipelineAddForm(column, brand, commit));
      }
    }
    return element;
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
    const status = document.createElement("p");
    status.className = "kanban-status";
    status.hidden = true;
    status.setAttribute("role", "status");
    body.append(status);
    const board = document.createElement("div");
    board.className = "kanban";
    body.append(board);
    const footer = document.createElement("div");
    body.append(footer);
    board.append(dashEmpty("Loading the board…"));

    let busy = false;
    function draw(payload) {
      board.replaceChildren(
        ...PIPELINE_COLUMNS.map((column) =>
          pipelineColumn(column, payload, brand, commit),
        ),
      );
      footer.replaceChildren();
      if (payload.sample === true) {
        footer.append(dashNote("Sample data — the backlog skill is not present."));
      }
      footer.append(
        dashNote(
          payload.writable === true
            ? "Click a card for its full note; dimmed cards belong to the other brand. Drag a card to a new column to change its marker in the backlog file."
            : "Click a card for its full note; dimmed cards belong to the other brand.",
        ),
      );
    }
    function commit(run) {
      if (busy) {
        return;
      }
      busy = true;
      status.hidden = false;
      status.className = "kanban-status";
      status.textContent = "Saving…";
      void run()
        .then((payload) => {
          status.hidden = true;
          draw(payload);
        })
        .catch((error) => {
          status.className = "kanban-status kanban-status--error";
          status.textContent =
            error?.message ?? "That change could not be saved.";
          // The file moved under us, so redraw from what is actually on disk.
          void fetchJson("/api/pipeline")
            .then(draw)
            .catch(() => {});
        })
        .finally(() => {
          busy = false;
        });
    }

    void fetchJson("/api/pipeline")
      .then(draw)
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
      if (activeAgentId === "business-development" && bdModesAvailable()) {
        body.append(renderBdModeToggle());
      }
      if (activeAgentId === "business-development" && bdScreen === "import") {
        renderBdImportScreen(body);
      } else if (activeAgentId === "business-development" && bdScreen === "settings") {
        renderBdSettingsScreen(body);
      } else if (activeAgentId === "business-development" && bdScreen === "enrich") {
        renderBdEnrichScreen(body);
      } else if (activeAgentId === "business-development" && bdScreen === "sourcing") {
        renderBdSourcingScreen(body);
      } else if (activeAgentId === "business-development" && bdDraftContext !== null) {
        renderBdDraftScreen(body);
      } else if (activeTabId === "bd-deadlines") {
        renderBdFestivalsTab(body);
      } else if (activeTabId === "bd-press") {
        renderBdPressTab(body);
      } else if (activeTabId === "bd-pipeline") {
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
