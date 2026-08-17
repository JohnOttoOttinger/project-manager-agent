/*
 * START HERE: make this agent feel like your own.
 *
 * Change only the words and colour between the quotes below, save the file,
 * then refresh http://localhost:3000 in your browser.
 *
 * Keep each example prompt on its own line and leave the commas in place.
 */
window.AGENT_CONFIG = Object.freeze({
  name: "Project Manager",
  subtitle: "Turn meetings, documents, and project ideas into clear next actions.",
  welcomeMessage:
    "Hello! I’m your Project Manager. Add a meeting transcript or tell me what you’re working on, and I’ll help turn it into decisions, plans, and safe next actions.",
  primaryColour: "#6D4AFF",
  /*
   * Per-agent welcome messages. Any agent without an entry here falls back
   * to the main welcomeMessage above.
   */
  welcomeMessages: {
    "business-development":
      "Hello! I’m your Business Development agent. Tell me about a job you won or lost and I’ll log it, draft a feedback ask for you to send, and surface the patterns once there are enough of them to see.",
    analytics:
      "Hello! I’m your Analytics agent. Ask me what actually moved — rankings, clicks, enquiries, campaign results — and I’ll answer from the numbers rather than from opinion.",
    sales:
      "Hello! I’m your Sales agent. Bring me an enquiry, a quote that went quiet, or a call to prepare for, and I’ll help you move it toward a yes.",
    marketing:
      "Hello! I’m your Marketing agent. I draft the posts, pitches, and pages that get Datalabs and Oddtoe seen — you review everything and hit send yourself.",
    investment:
      "Hello! I’m your Investment agent. I prepare budgets and weigh spending decisions for both businesses — I organise the numbers, you make the calls.",
    bookkeeping:
      "Hello! I’m your Bookkeeping agent. Invoices, expense categorisation, and BAS-time prep — bring me exports and I’ll get them organised.",
  },
  examplePrompts: [
    "Turn these meeting notes into decisions and action items",
    "Build a practical project plan from this document",
    "Show me the highest-priority work in my local project",
  ],
  /*
   * Brands the content skills can act for. The toggle above the message box
   * switches between them; the active brand is named in quick-action prompts
   * and decides which website drafts are pushed to.
   */
  brands: [
    { id: "datalabs", label: "Datalabs", colour: "#c39f76" },
    { id: "oddtoe", label: "Oddtoe", colour: "#8a8f6a" },
  ],
  /*
   * One-click starters for the GEO content skills. {brand} is replaced with
   * the active brand's name. Chips prefill the message box; you still press
   * Send yourself.
   */
  /*
   * "Try an example" prompts per agent per brand. When an agent and a brand
   * are both selected, the matching list below replaces that agent's generic
   * examples. Keys: agent id, then brand id. Up to 6 prompts show.
   */
  brandExamplePrompts: {
    "project-manager": {
      datalabs: [
        "Interview me about a recent client project and turn it into a case study with a named stat",
        "Draft the outline for a new Power BI training workshop topic",
        "Write the next money page in the backlog — interview me for real prices first",
        "Turn these meeting notes into decisions and action items",
        "Plan next week's content: one page, two LinkedIn posts, one pitch",
        "Show me the highest-priority work in my local project",
      ],
      oddtoe: [
        "Interview me about my last installation and turn it into a case study",
        "Turn this project list into the Oddtoe credits page",
        "Draft a proposal for a projection installation enquiry — interview me about the venue and budget",
        "Help me answer 'what does projection mapping cost?' for a prospect",
        "Find Melbourne festivals and venues that commission installations, and draft a pitch to one",
        "Turn my latest project into a LinkedIn post in Oddtoe's voice — playful, not corporate",
      ],
    },
    "business-development": {
      datalabs: [
        "We lost a workshop to a cheaper quote — log it and draft a feedback ask",
        "Show me my lost leads and any patterns in why we lose",
        "A lost lead replied with feedback — record what they said",
        "Which objection comes up most often in the leads I've lost?",
        "We won a job we expected to lose — log why, so I can repeat it",
      ],
      oddtoe: [
        "An event organiser went with another studio — log the lost lead and draft a feedback ask",
        "Show me my lost leads and any patterns in why we lose",
        "A lost lead replied with feedback — record what they said",
        "Are we losing on price, timeline, or scope? Show me the split",
        "We won a commission — log what made the difference",
      ],
    },
    sales: {
      datalabs: [
        "Import this prospect list — I've attached the CSV",
        "Show me the sales pipeline",
        "Draft a follow-up to a workshop enquiry that went quiet",
        "Prepare me for a discovery call with a corporate training buyer",
        "Write a proposal outline for a dashboard design project",
      ],
      oddtoe: [
        "Import my agency list — I've attached the CSV",
        "Show me the sales pipeline",
        "Enrich 3 prospects as a test",
        "Which prospects are flagged for review?",
        "Fill in the LinkedIn company URLs — I'll paste them",
        "Write a follow-up to an event organiser who went quiet after a quote",
      ],
    },
    marketing: {
      datalabs: [
        "Turn our latest page into two LinkedIn posts",
        "Draft a pitch to a 'best data visualization agencies' listicle",
        "Write a review request email to a past workshop client",
      ],
      oddtoe: [
        "Write a YouTube description for my newest animation so AI assistants can find it",
        "Turn my latest installation into a LinkedIn post",
        "Explain 'generative AI animation' in one Oddtoe-voiced paragraph I can reuse everywhere",
      ],
    },
    investment: {
      datalabs: [
        "Build a simple budget for next quarter's marketing spend",
        "Summarise this quarter's revenue by product line from this export",
        "Compare what the template shop earns vs what workshops earn",
      ],
      oddtoe: [
        "Estimate costs for a new installation build from this equipment list",
        "Compare festival application fees against likely commission value",
        "Rough out a budget for taking an installation to a Berlin venue",
      ],
    },
    bookkeeping: {
      datalabs: [
        "Draft invoice line items for a 2-day workshop engagement",
        "Categorise these expenses from this CSV export",
        "Prepare a BAS-time checklist of documents I need",
      ],
      oddtoe: [
        "Draft an invoice for an installation with staged payments",
        "Categorise these project expenses as materials vs labour",
        "List likely deductible gear purchases from this statement",
      ],
    },
  },
  quickActions: [
    {
      icon: "📄",
      label: "Next money page",
      prompt:
        "For {brand}: write the next money page in the backlog. Interview me for any real facts you need before drafting.",
    },
    {
      icon: "📣",
      label: "Get us mentioned",
      prompt:
        "For {brand}: draft the promotion batch for the most recently published page — LinkedIn posts, one listicle pitch, one review request. Drafts only; I'll send them myself.",
    },
    {
      icon: "📇",
      label: "Brand fact sheet",
      prompt:
        "Show me the {brand} brand fact sheet — canonical sentence, clients, services, prices — so I can review or update it.",
    },
  ],
});
