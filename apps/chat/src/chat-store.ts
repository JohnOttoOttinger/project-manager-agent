import { randomBytes, randomUUID } from "node:crypto";
import { chmodSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { DatabaseSync } from "node:sqlite";
import type {
  ArticleBriefData,
  ArticleBriefRecord,
  ArticleBriefStatus,
  ArticleBusinessContext,
  ArticleOpportunity,
} from "./article-brief.js";

const SCHEMA_VERSION = 11;
const DEFAULT_TITLE = "New conversation";
const MAX_TITLE_LENGTH = 80;
const MAX_SEARCH_LENGTH = 200;

export type MessageRole = "user" | "assistant";
export type MessageStatus =
  | "pending"
  | "complete"
  | "failed"
  | "interrupted";

export interface ConversationSummary {
  id: string;
  agentId: string;
  title: string;
  createdAt: string;
  updatedAt: string;
  messageCount: number;
}

export interface StoredAttachment {
  documentId: string;
  name: string;
  type: string;
  mimeType: string;
  wordCount: number;
  characterCount: number;
  pageCount?: number;
  expiresAt: string;
}

export interface StoredMessage {
  id: string;
  conversationId: string;
  requestId: string;
  role: MessageRole;
  content: string;
  status: MessageStatus;
  errorCode?: string;
  runId?: string;
  createdAt: string;
  sequence: number;
  attachments: StoredAttachment[];
}

export interface ConversationPage {
  conversation: ConversationSummary;
  messages: StoredMessage[];
  nextBefore?: number;
}

export interface ConversationListPage {
  conversations: ConversationSummary[];
  nextCursor?: string;
}

export interface ConversationSearchResult {
  conversationId: string;
  conversationTitle: string;
  messageId: string;
  role: MessageRole;
  snippet: string;
  createdAt: string;
}

export interface HistoryMessage {
  role: MessageRole;
  content: string;
}

export interface BusinessMemoryCompetitors {
  direct: Array<Record<string, unknown>>;
  seo: Array<Record<string, unknown>>;
  adjacent: Array<Record<string, unknown>>;
}

export interface BusinessMemoryInput {
  schemaVersion: 1;
  jobId: string;
  status: "completed" | "partial";
  domain: string;
  companyOverview: string;
  profile: Record<string, unknown>;
  competitors: BusinessMemoryCompetitors;
  seedKeywords: string[];
  keywordCandidates: Array<Record<string, unknown>>;
  keywordGroups: Array<Record<string, unknown>>;
  sources: Array<Record<string, unknown>>;
  warnings: string[];
  researchSummary: string;
  evidenceQuality: Record<string, unknown>;
  researchedAt?: string;
}

export interface BusinessMemoryRecord extends BusinessMemoryInput {
  researchedAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface DomainResearchJobRecord {
  jobId: string;
  sessionId: string;
  domain: string;
  status: "queued" | "completed" | "partial" | "failed";
  createdAt: string;
  updatedAt: string;
}

export type PaidResearchStatus = "completed" | "partial" | "failed";
export type PaidResearchDepth = "refresh" | "standard" | "deep";
export type PaidComponentStatus =
  | "success"
  | "no_results"
  | "failed"
  | "unavailable"
  | "skipped";

export interface SeoSnapshotInput {
  schemaVersion: 1;
  jobId: string;
  status: PaidResearchStatus;
  researchDepth: PaidResearchDepth;
  domain: string;
  locationCode: number;
  languageCode: string;
  device: "desktop" | "mobile";
  costLimitUsd: number;
  actualCostUsd: number;
  componentStatus: Record<string, PaidComponentStatus>;
  offeringProfile: Record<string, unknown>;
  rankedKeywords: Array<Record<string, unknown>>;
  keywordCandidates: Array<Record<string, unknown>>;
  selectedKeywords: Array<Record<string, unknown>>;
  seoCompetitors: Array<Record<string, unknown>>;
  serpEvidence: Array<Record<string, unknown>>;
  sources: Array<Record<string, unknown>>;
  warnings: string[];
  evidenceSummary: Record<string, unknown>;
  capturedAt?: string;
  expiresAt?: string;
}

export interface SeoSnapshotRecord extends SeoSnapshotInput {
  snapshotId: string;
  sessionId: string;
  capturedAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface SeoSnapshotSummary {
  snapshotId: string;
  jobId: string;
  status: PaidResearchStatus;
  researchDepth: PaidResearchDepth;
  domain: string;
  locationCode: number;
  languageCode: string;
  actualCostUsd: number;
  capturedAt: string;
  updatedAt: string;
  warningCount: number;
}

export type SeoArticleJobStatus =
  | "queued"
  | "running"
  | "completed"
  | "partial"
  | "failed"
  | "interrupted";

export interface SeoArticleJobInput {
  sessionId: string;
  requestId: string;
  domain: string;
  briefId: string;
  primaryKeyword: string;
  supportingKeywords: string[];
  input: Record<string, unknown>;
}

export interface SeoArticleJobRecord extends SeoArticleJobInput {
  jobId: string;
  status: SeoArticleJobStatus;
  stage: string;
  errorCode?: string;
  errorMessage?: string;
  latestVersionId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SeoArticleVersionInput {
  status: "completed" | "partial";
  domain: string;
  primaryKeyword: string;
  supportingKeywords: string[];
  context: Record<string, unknown>;
  plan: Record<string, unknown>;
  markdown: string;
  structuredData: Record<string, unknown>;
  metadata: Record<string, unknown>;
  answerBlocks: Array<Record<string, unknown>>;
  faq: unknown[];
  sources: unknown[];
  claimLedger: unknown[];
  qualityReport: Record<string, unknown>;
  warnings: string[];
  reviewStatus: "ready_for_review";
  model: string;
}

export interface SeoArticleVersionRecord extends SeoArticleVersionInput {
  versionId: string;
  jobId: string;
  versionNumber: number;
  parentVersionId?: string;
  downloadToken: string;
  createdAt: string;
}

export interface BusinessMemorySummary {
  jobId: string;
  status: "completed" | "partial";
  domain: string;
  brandName: string;
  warningCount: number;
  researchedAt: string;
  updatedAt: string;
}

export const PROSPECT_STATUSES = [
  "imported",
  "needs_review",
  "enriched",
  "emailed",
  "opened",
  "followed_up",
  "replied",
  "closed",
] as const;

export type ProspectStatus = (typeof PROSPECT_STATUSES)[number];

export const SUPPRESSION_REASONS = [
  "unsubscribed",
  "bounced",
  "asked",
  "manual",
] as const;

export type SuppressionReason = (typeof SUPPRESSION_REASONS)[number];

export interface SuppressionRecord {
  suppressionId: string;
  brand: string;
  emailKey: string;
  companyKey: string;
  reason: SuppressionReason;
  detail: string;
  createdAt: string;
}

/** Lowercase and trim an address so suppression matching is case-insensitive. */
export function suppressionKey(email: string): string {
  return email.trim().toLowerCase();
}

export interface OutreachSettingsInput {
  senderName: string;
  senderContact: string;
  unsubscribeLine: string;
  dailyCap?: number | undefined;
  followUpDays?: number | undefined;
  guidePageUrl?: string | undefined;
}

export interface OutreachSettingsRecord {
  brand: string;
  senderName: string;
  senderContact: string;
  unsubscribeLine: string;
  dailyCap: number;
  followUpDays: number;
  guidePageUrl: string;
  updatedAt: string;
}

export interface CampaignBrief {
  offer: string;
  guidePageUrl: string;
  utmCampaign: string;
  dailyCap?: number | undefined;
  followUpDays?: number | undefined;
}

export interface CampaignRecord {
  campaignId: string;
  brand: string;
  name: string;
  status: "draft" | "active" | "completed";
  brief: CampaignBrief;
  createdAt: string;
  updatedAt: string;
}

/** Why one prospect was left out of a drafting run. Reported, never silent. */
export interface DraftSkip {
  prospectId: string;
  company: string;
  reason: string;
}

export interface DraftCandidate {
  prospect: ProspectRecord;
  /** The guide-page link carrying this prospect's own utm_content. */
  outreachUrl: string;
  /** Set when the prospect is draftable but the user must look first. */
  warning: string;
}

export interface DraftableResult {
  brand: string;
  settings: OutreachSettingsRecord;
  campaign: CampaignRecord | undefined;
  eligible: DraftCandidate[];
  skipped: DraftSkip[];
  dailyCap: number;
  draftedToday: number;
  remainingToday: number;
}

export interface RecordedDraftInput {
  prospectId: string;
  draftId: string;
  hook?: string | undefined;
  hookEvidence?: string | undefined;
}

export interface RecordedDraftResult {
  prospectId: string;
  company: string;
  outcome: "recorded" | "not_found" | "suppressed";
  followUpDue: string;
}

export interface DraftToValidate {
  prospectId: string;
  subject: string;
  body: string;
}

export interface DraftValidation {
  prospectId: string;
  company: string;
  approved: boolean;
  reasons: string[];
  warnings: string[];
}

export interface ProspectListRecord {
  brand: string;
  listName: string;
  description: string;
  createdAt: string;
  updatedAt: string;
}

export const DRAFT_STATES = [
  "composing",
  "approved",
  "created",
  "discarded",
] as const;

export type DraftState = (typeof DRAFT_STATES)[number];

export interface PreparedDraftRecord {
  draftRowId: string;
  brand: string;
  prospectId: string;
  campaignId: string | undefined;
  subject: string;
  body: string;
  hook: string;
  hookEvidence: string;
  state: DraftState;
  createdAt: string;
  updatedAt: string;
}

export class OutreachNotConfiguredError extends Error {}

export const OUTREACH_EVENT_TYPES = [
  "imported",
  "enriched",
  "flagged",
  "emailed",
  "opened",
  "clicked",
  "followed_up",
  "replied",
  "status_change",
] as const;

export type OutreachEventType = (typeof OUTREACH_EVENT_TYPES)[number];

export interface OutreachEventRecord {
  eventId: string;
  prospectId: string;
  campaignId: string | undefined;
  eventType: OutreachEventType;
  detail: string;
  occurredAt: string;
}

export interface ProspectAddResult {
  outcome: "added" | "duplicate";
  company: string;
  prospect: ProspectRecord | undefined;
}

export interface ProspectRowInput {
  rowNumber?: number | undefined;
  company: string;
  region?: string | undefined;
  tier?: string | undefined;
  source?: string | undefined;
  website?: string | undefined;
  linkedinCompanyUrl?: string | undefined;
  contactName?: string | undefined;
  contactEmail?: string | undefined;
  linkedinUrl?: string | undefined;
  pdfSent?: string | undefined;
  sentDate?: string | undefined;
  opened?: string | undefined;
  followUpSent?: string | undefined;
  status?: ProspectStatus | undefined;
  notes?: string | undefined;
}

export interface ProspectRecord {
  prospectId: string;
  brand: string;
  listName: string;
  rowNumber: number | undefined;
  company: string;
  region: string;
  tier: string;
  source: string;
  website: string;
  linkedinCompanyUrl: string;
  contactName: string;
  contactEmail: string;
  linkedinUrl: string;
  confidence: string;
  flagReason: string;
  pdfSent: string;
  sentDate: string;
  opened: string;
  followUpSent: string;
  status: ProspectStatus;
  notes: string;
  hook: string;
  hookEvidence: string;
  draftId: string;
  draftedAt: string;
  clickedAt: string;
  followUpDue: string;
  closeReason: string;
  campaignId: string | undefined;
  createdAt: string;
  updatedAt: string;
}

export interface ProspectImportResult {
  brand: string;
  listName: string;
  inserted: number;
  duplicates: number;
  duplicateCompanies: string[];
  total: number;
}

export interface ProspectPipelineSummary {
  brand: string | undefined;
  total: number;
  byStatus: Partial<Record<ProspectStatus, number>>;
  listNames: string[];
  lastUpdatedAt: string | undefined;
}

export type EnrichmentJobStatus =
  | "queued"
  | "running"
  | "completed"
  | "partial"
  | "failed";

export interface EnrichmentJobRecord {
  jobId: string;
  sessionId: string;
  requestId: string;
  brand: string;
  listName: string;
  status: EnrichmentJobStatus;
  stage: string;
  targetCount: number;
  enrichedCount: number;
  flaggedCount: number;
  skipped: string[];
  providerCostUsd: number | undefined;
  errorCode: string | undefined;
  errorMessage: string | undefined;
  createdAt: string;
  updatedAt: string;
}

export const PROSPECT_CONFIDENCES = ["high", "medium", "low", "none"] as const;

export type ProspectConfidence = (typeof PROSPECT_CONFIDENCES)[number];

export interface EnrichmentResultInput {
  prospectId: string;
  contactName?: string | undefined;
  contactEmail?: string | undefined;
  linkedinUrl?: string | undefined;
  jobTitle?: string | undefined;
  confidence: ProspectConfidence;
  flagReason?: string | undefined;
}

export interface ProspectUpdateInput {
  company: string;
  listName?: string | undefined;
  fields: {
    linkedinCompanyUrl?: string | undefined;
    contactName?: string | undefined;
    contactEmail?: string | undefined;
    linkedinUrl?: string | undefined;
    website?: string | undefined;
    region?: string | undefined;
    tier?: string | undefined;
    status?: ProspectStatus | undefined;
    notes?: string | undefined;
    flagReason?: string | undefined;
    hook?: string | undefined;
    hookEvidence?: string | undefined;
    followUpDue?: string | undefined;
    closeReason?: string | undefined;
  };
}

export interface ProspectUpdateResult {
  company: string;
  outcome: "updated" | "not_found" | "ambiguous";
  changedFields: string[];
}

interface ProspectRow {
  prospect_id: string;
  brand: string;
  list_name: string;
  company_key: string;
  row_number: number | null;
  company: string;
  region: string;
  tier: string;
  source: string;
  website: string;
  linkedin_company_url: string;
  contact_name: string;
  contact_email: string;
  linkedin_url: string;
  confidence: string;
  flag_reason: string;
  pdf_sent: string;
  sent_date: string;
  opened: string;
  follow_up_sent: string;
  status: ProspectStatus;
  notes: string;
  hook: string;
  hook_evidence: string;
  draft_id: string;
  drafted_at: string;
  clicked_at: string;
  follow_up_due: string;
  close_reason: string;
  campaign_id: string | null;
  created_at: string;
  updated_at: string;
}

interface SuppressionRow {
  suppression_id: string;
  brand: string;
  email_key: string;
  company_key: string;
  reason: SuppressionReason;
  detail: string;
  created_at: string;
}

interface EnrichmentJobRow {
  job_id: string;
  session_id: string;
  request_id: string;
  brand: string;
  list_name: string;
  status: EnrichmentJobStatus;
  stage: string;
  target_count: number;
  enriched_count: number;
  flagged_count: number;
  skipped_json: string;
  provider_cost_usd: number | null;
  error_code: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

function enrichmentJobFromRow(row: EnrichmentJobRow): EnrichmentJobRecord {
  let skipped: string[] = [];
  try {
    const parsed = JSON.parse(row.skipped_json) as unknown;
    if (Array.isArray(parsed)) {
      skipped = parsed.filter((item): item is string => typeof item === "string");
    }
  } catch {
    skipped = [];
  }
  return {
    jobId: row.job_id,
    sessionId: row.session_id,
    requestId: row.request_id,
    brand: row.brand,
    listName: row.list_name,
    status: row.status,
    stage: row.stage,
    targetCount: row.target_count,
    enrichedCount: row.enriched_count,
    flaggedCount: row.flagged_count,
    skipped,
    providerCostUsd: row.provider_cost_usd ?? undefined,
    errorCode: row.error_code ?? undefined,
    errorMessage: row.error_message ?? undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

/**
 * Whitespace- and quote-insensitive containment. A composed email may wrap
 * the unsubscribe line differently or use typographic quotes; that should
 * not read as the line being absent.
 */
function containsNormalised(haystack: string, needle: string): boolean {
  const normalise = (value: string) =>
    value
      .replace(/[\u2018\u2019\u201a\u201b]/g, "'")
      .replace(/[\u201c\u201d\u201e\u201f]/g, '"')
      .replace(/[\u2010-\u2015]/g, "-")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();
  const trimmed = normalise(needle);
  return trimmed === "" ? true : normalise(haystack).includes(trimmed);
}

function clampWholeNumber(
  value: number | undefined,
  fallback: number,
  minimum: number,
  maximum: number,
): number {
  if (!Number.isFinite(value) || !Number.isInteger(value)) {
    return fallback;
  }
  return Math.max(minimum, Math.min(Number(value), maximum));
}

function addDaysIso(from: string, days: number): string {
  const date = new Date(from);
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().slice(0, 10);
}

/**
 * The guide-page link for one prospect. utm_content carries the prospect id
 * so a GA4 read can tell which single prospect clicked — distinct from the
 * guide's own outbound links, which measure traffic in the other direction.
 */
function buildOutreachUrl(
  guidePageUrl: string,
  utmCampaign: string,
  prospectId: string,
): string {
  if (guidePageUrl === "") {
    return "";
  }
  try {
    const url = new URL(guidePageUrl);
    url.searchParams.set("utm_source", "outreach");
    url.searchParams.set("utm_medium", "email");
    url.searchParams.set("utm_campaign", utmCampaign);
    url.searchParams.set("utm_content", prospectId);
    return url.toString();
  } catch {
    return "";
  }
}

function prospectFromRow(row: ProspectRow): ProspectRecord {
  return {
    prospectId: row.prospect_id,
    brand: row.brand,
    listName: row.list_name,
    rowNumber: row.row_number ?? undefined,
    company: row.company,
    region: row.region,
    tier: row.tier,
    source: row.source,
    website: row.website,
    linkedinCompanyUrl: row.linkedin_company_url,
    contactName: row.contact_name,
    contactEmail: row.contact_email,
    linkedinUrl: row.linkedin_url,
    confidence: row.confidence,
    flagReason: row.flag_reason,
    pdfSent: row.pdf_sent,
    sentDate: row.sent_date,
    opened: row.opened,
    followUpSent: row.follow_up_sent,
    status: row.status,
    notes: row.notes,
    hook: row.hook,
    hookEvidence: row.hook_evidence,
    draftId: row.draft_id,
    draftedAt: row.drafted_at,
    clickedAt: row.clicked_at,
    followUpDue: row.follow_up_due,
    closeReason: row.close_reason,
    campaignId: row.campaign_id ?? undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

export interface BeginTurnInput {
  conversationId: string;
  agentId: string;
  requestId: string;
  content: string;
  attachments?: readonly StoredAttachment[];
  createdAt?: string;
}

export interface CompleteTurnInput {
  conversationId: string;
  requestId: string;
  content: string;
  runId?: string;
  createdAt?: string;
}

export interface StoredTurn {
  user?: StoredMessage;
  assistant?: StoredMessage;
}

interface ConversationRow {
  id: string;
  agent_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

interface MessageRow {
  id: string;
  conversation_id: string;
  request_id: string;
  role: MessageRole;
  content: string;
  status: MessageStatus;
  error_code: string | null;
  run_id: string | null;
  created_at: string;
  sequence: number;
}

interface AttachmentRow {
  message_id: string;
  document_id: string;
  name: string;
  type: string;
  mime_type: string;
  word_count: number;
  character_count: number;
  page_count: number | null;
  expires_at: string;
}

interface SearchRow {
  conversation_id: string;
  conversation_title: string;
  message_id: string;
  role: MessageRole;
  snippet: string;
  created_at: string;
}

interface BusinessMemoryRow {
  schema_version: number;
  job_id: string;
  status: "completed" | "partial";
  domain: string;
  company_overview: string;
  profile_json: string;
  competitors_json: string;
  seed_keywords_json: string;
  keyword_candidates_json: string;
  keyword_groups_json: string;
  sources_json: string;
  warnings_json: string;
  research_summary: string;
  evidence_quality_json: string;
  researched_at: string;
  created_at: string;
  updated_at: string;
}

interface SeoSnapshotRow {
  snapshot_id: string;
  job_id: string;
  session_id: string;
  schema_version: number;
  status: PaidResearchStatus;
  research_depth: PaidResearchDepth;
  domain: string;
  location_code: number;
  language_code: string;
  device: "desktop" | "mobile";
  cost_limit_usd: number;
  actual_cost_usd: number;
  component_status_json: string;
  offering_profile_json: string;
  ranked_keywords_json: string;
  keyword_candidates_json: string;
  selected_keywords_json: string;
  seo_competitors_json: string;
  serp_evidence_json: string;
  sources_json: string;
  warnings_json: string;
  evidence_summary_json: string;
  captured_at: string;
  expires_at: string | null;
  created_at: string;
  updated_at: string;
}

interface SeoArticleJobRow {
  job_id: string;
  session_id: string;
  request_id: string;
  domain: string;
  brief_id: string | null;
  primary_keyword: string;
  supporting_keywords_json: string;
  input_json: string;
  status: SeoArticleJobStatus;
  stage: string;
  error_code: string | null;
  error_message: string | null;
  latest_version_id: string | null;
  created_at: string;
  updated_at: string;
}

interface ArticleBriefRow {
  brief_id: string;
  session_id: string;
  domain: string;
  research_key: string;
  status: ArticleBriefStatus;
  brief_json: string;
  created_at: string;
  updated_at: string;
}

interface SeoArticleVersionRow {
  version_id: string;
  job_id: string;
  version_number: number;
  parent_version_id: string | null;
  status: "completed" | "partial";
  domain: string;
  primary_keyword: string;
  supporting_keywords_json: string;
  context_json: string;
  plan_json: string;
  markdown: string;
  structured_data_json: string;
  metadata_json: string;
  answer_blocks_json: string;
  faq_json: string;
  sources_json: string;
  claim_ledger_json: string;
  quality_report_json: string;
  warnings_json: string;
  review_status: "ready_for_review";
  model: string;
  download_token: string;
  created_at: string;
}

function nowIso(): string {
  return new Date().toISOString();
}

function titleFromMessage(value: string): string {
  const normalised = value.replace(/\s+/g, " ").trim();
  if (normalised.length <= MAX_TITLE_LENGTH) {
    return normalised || DEFAULT_TITLE;
  }
  return `${normalised.slice(0, MAX_TITLE_LENGTH - 1).trimEnd()}…`;
}

function conversationFromRow(row: ConversationRow): ConversationSummary {
  return {
    id: row.id,
    agentId: row.agent_id,
    title: row.title,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    messageCount: Number(row.message_count),
  };
}

function searchExpression(value: string): string {
  return value
    .normalize("NFC")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map((term) => `"${term.replaceAll('"', '""')}"*`)
    .join(" AND ");
}

function businessMemoryFromRow(row: BusinessMemoryRow): BusinessMemoryRecord {
  return {
    schemaVersion: 1,
    jobId: row.job_id,
    status: row.status,
    domain: row.domain,
    companyOverview: row.company_overview,
    profile: JSON.parse(row.profile_json) as Record<string, unknown>,
    competitors: JSON.parse(row.competitors_json) as BusinessMemoryCompetitors,
    seedKeywords: JSON.parse(row.seed_keywords_json) as string[],
    keywordCandidates: JSON.parse(row.keyword_candidates_json) as Array<Record<string, unknown>>,
    keywordGroups: JSON.parse(row.keyword_groups_json) as Array<Record<string, unknown>>,
    sources: JSON.parse(row.sources_json) as Array<Record<string, unknown>>,
    warnings: JSON.parse(row.warnings_json) as string[],
    researchSummary: row.research_summary,
    evidenceQuality: JSON.parse(row.evidence_quality_json) as Record<string, unknown>,
    researchedAt: row.researched_at,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function seoSnapshotFromRow(row: SeoSnapshotRow): SeoSnapshotRecord {
  const result: SeoSnapshotRecord = {
    schemaVersion: 1,
    snapshotId: row.snapshot_id,
    jobId: row.job_id,
    sessionId: row.session_id,
    status: row.status,
    researchDepth: row.research_depth,
    domain: row.domain,
    locationCode: Number(row.location_code),
    languageCode: row.language_code,
    device: row.device,
    costLimitUsd: Number(row.cost_limit_usd),
    actualCostUsd: Number(row.actual_cost_usd),
    componentStatus: JSON.parse(row.component_status_json) as Record<string, PaidComponentStatus>,
    offeringProfile: JSON.parse(row.offering_profile_json) as Record<string, unknown>,
    rankedKeywords: JSON.parse(row.ranked_keywords_json) as Array<Record<string, unknown>>,
    keywordCandidates: JSON.parse(row.keyword_candidates_json) as Array<Record<string, unknown>>,
    selectedKeywords: JSON.parse(row.selected_keywords_json) as Array<Record<string, unknown>>,
    seoCompetitors: JSON.parse(row.seo_competitors_json) as Array<Record<string, unknown>>,
    serpEvidence: JSON.parse(row.serp_evidence_json) as Array<Record<string, unknown>>,
    sources: JSON.parse(row.sources_json) as Array<Record<string, unknown>>,
    warnings: JSON.parse(row.warnings_json) as string[],
    evidenceSummary: JSON.parse(row.evidence_summary_json) as Record<string, unknown>,
    capturedAt: row.captured_at,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
  if (row.expires_at !== null) {
    result.expiresAt = row.expires_at;
  }
  return result;
}

function seoArticleJobFromRow(row: SeoArticleJobRow): SeoArticleJobRecord {
  return {
    jobId: row.job_id,
    sessionId: row.session_id,
    requestId: row.request_id,
    domain: row.domain,
    briefId: row.brief_id ?? "",
    primaryKeyword: row.primary_keyword,
    supportingKeywords: JSON.parse(row.supporting_keywords_json) as string[],
    input: JSON.parse(row.input_json) as Record<string, unknown>,
    status: row.status,
    stage: row.stage,
    ...(row.error_code === null ? {} : { errorCode: row.error_code }),
    ...(row.error_message === null ? {} : { errorMessage: row.error_message }),
    ...(row.latest_version_id === null ? {} : { latestVersionId: row.latest_version_id }),
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function articleBriefFromRow(row: ArticleBriefRow): ArticleBriefRecord {
  const data = JSON.parse(row.brief_json) as ArticleBriefData;
  return {
    ...data,
    briefId: row.brief_id,
    sessionId: row.session_id,
    domain: row.domain,
    researchKey: row.research_key,
    status: row.status,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function seoArticleVersionFromRow(row: SeoArticleVersionRow): SeoArticleVersionRecord {
  return {
    versionId: row.version_id,
    jobId: row.job_id,
    versionNumber: Number(row.version_number),
    ...(row.parent_version_id === null ? {} : { parentVersionId: row.parent_version_id }),
    status: row.status,
    domain: row.domain,
    primaryKeyword: row.primary_keyword,
    supportingKeywords: JSON.parse(row.supporting_keywords_json) as string[],
    context: JSON.parse(row.context_json) as Record<string, unknown>,
    plan: JSON.parse(row.plan_json) as Record<string, unknown>,
    markdown: row.markdown,
    structuredData: JSON.parse(row.structured_data_json) as Record<string, unknown>,
    metadata: JSON.parse(row.metadata_json) as Record<string, unknown>,
    answerBlocks: JSON.parse(row.answer_blocks_json) as Array<Record<string, unknown>>,
    faq: JSON.parse(row.faq_json) as unknown[],
    sources: JSON.parse(row.sources_json) as unknown[],
    claimLedger: JSON.parse(row.claim_ledger_json) as unknown[],
    qualityReport: JSON.parse(row.quality_report_json) as Record<string, unknown>,
    warnings: JSON.parse(row.warnings_json) as string[],
    reviewStatus: row.review_status,
    model: row.model,
    downloadToken: row.download_token,
    createdAt: row.created_at,
  };
}

function encodeCursor(updatedAt: string, id: string): string {
  return Buffer.from(JSON.stringify({ updatedAt, id }), "utf8").toString(
    "base64url",
  );
}

function decodeCursor(value: string): { updatedAt: string; id: string } {
  try {
    const parsed = JSON.parse(
      Buffer.from(value, "base64url").toString("utf8"),
    ) as unknown;
    if (
      typeof parsed === "object" &&
      parsed !== null &&
      !Array.isArray(parsed) &&
      typeof (parsed as Record<string, unknown>).updatedAt === "string" &&
      typeof (parsed as Record<string, unknown>).id === "string"
    ) {
      return parsed as { updatedAt: string; id: string };
    }
  } catch {
    // Use the stable error below.
  }
  throw new Error("Invalid conversation cursor");
}

export class ChatStore {
  private readonly database: DatabaseSync;
  private closed = false;

  constructor(readonly databasePath: string) {
    const inMemory = databasePath === ":memory:";
    if (!inMemory) {
      mkdirSync(dirname(databasePath), { recursive: true, mode: 0o700 });
      if (process.platform !== "win32") {
        chmodSync(dirname(databasePath), 0o700);
      }
    }
    this.database = new DatabaseSync(databasePath);
    if (!inMemory && process.platform !== "win32") {
      chmodSync(databasePath, 0o600);
    }
    this.database.exec("PRAGMA foreign_keys = ON");
    this.database.exec("PRAGMA journal_mode = WAL");
    this.database.exec("PRAGMA synchronous = NORMAL");
    this.database.exec("PRAGMA busy_timeout = 5000");
    this.migrate();
    this.markPendingInterrupted();
  }

  private migrate(): void {
    const versionRow = this.database.prepare("PRAGMA user_version").get() as
      | { user_version: number }
      | undefined;
    const version = Number(versionRow?.user_version ?? 0);
    if (version > SCHEMA_VERSION) {
      throw new Error(
        `Chat database schema ${version} is newer than supported schema ${SCHEMA_VERSION}.`,
      );
    }
    if (version === 0) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE conversations (
            id TEXT PRIMARY KEY,
            agent_id TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          ) STRICT;

          CREATE TABLE messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            request_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('pending', 'complete', 'failed', 'interrupted')),
            error_code TEXT,
            run_id TEXT,
            created_at TEXT NOT NULL,
            sequence INTEGER NOT NULL,
            UNIQUE (conversation_id, request_id, role),
            UNIQUE (conversation_id, sequence)
          ) STRICT;

          CREATE INDEX messages_conversation_sequence
          ON messages(conversation_id, sequence);

          CREATE TABLE message_attachments (
            message_id TEXT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
            document_id TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            mime_type TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            character_count INTEGER NOT NULL,
            page_count INTEGER,
            expires_at TEXT NOT NULL,
            PRIMARY KEY (message_id, document_id)
          ) STRICT;

          CREATE VIRTUAL TABLE message_search USING fts5(
            content,
            content='messages',
            content_rowid='rowid',
            tokenize='unicode61'
          );

          CREATE TRIGGER messages_search_insert AFTER INSERT ON messages BEGIN
            INSERT INTO message_search(rowid, content) VALUES (new.rowid, new.content);
          END;

          CREATE TRIGGER messages_search_delete AFTER DELETE ON messages BEGIN
            INSERT INTO message_search(message_search, rowid, content)
            VALUES ('delete', old.rowid, old.content);
          END;

          CREATE TRIGGER messages_search_update AFTER UPDATE OF content ON messages BEGIN
            INSERT INTO message_search(message_search, rowid, content)
            VALUES ('delete', old.rowid, old.content);
            INSERT INTO message_search(rowid, content) VALUES (new.rowid, new.content);
          END;

          PRAGMA user_version = 1;
        `);
      });
    }
    if (version < 2) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE business_memory (
            domain TEXT PRIMARY KEY,
            schema_version INTEGER NOT NULL CHECK (schema_version = 1),
            job_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('completed', 'partial')),
            company_overview TEXT NOT NULL,
            profile_json TEXT NOT NULL,
            competitors_json TEXT NOT NULL,
            seed_keywords_json TEXT NOT NULL,
            keyword_candidates_json TEXT NOT NULL,
            keyword_groups_json TEXT NOT NULL,
            sources_json TEXT NOT NULL,
            warnings_json TEXT NOT NULL,
            research_summary TEXT NOT NULL,
            evidence_quality_json TEXT NOT NULL,
            researched_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          ) STRICT;

          CREATE INDEX business_memory_updated_at
          ON business_memory(updated_at DESC);

          CREATE TABLE domain_research_jobs (
            job_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            domain TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('queued', 'completed', 'partial')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          ) STRICT;

          CREATE INDEX domain_research_jobs_session
          ON domain_research_jobs(session_id, updated_at DESC);

          PRAGMA user_version = 2;
        `);
      });
    }
    if (version < 3) {
      this.transaction(() => {
        this.database.exec(`
          DROP INDEX domain_research_jobs_session;
          ALTER TABLE domain_research_jobs RENAME TO domain_research_jobs_v2;

          CREATE TABLE domain_research_jobs (
            job_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            domain TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('queued', 'completed', 'partial', 'failed')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          ) STRICT;

          INSERT INTO domain_research_jobs(
            job_id, session_id, domain, status, created_at, updated_at
          )
          SELECT job_id, session_id, domain, status, created_at, updated_at
          FROM domain_research_jobs_v2;

          DROP TABLE domain_research_jobs_v2;

          CREATE INDEX domain_research_jobs_session
          ON domain_research_jobs(session_id, updated_at DESC);

          CREATE TABLE seo_snapshots (
            snapshot_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL UNIQUE,
            session_id TEXT NOT NULL,
            schema_version INTEGER NOT NULL CHECK (schema_version = 1),
            status TEXT NOT NULL CHECK (status IN ('completed', 'partial', 'failed')),
            research_depth TEXT NOT NULL CHECK (research_depth IN ('refresh', 'standard', 'deep')),
            domain TEXT NOT NULL,
            location_code INTEGER NOT NULL,
            language_code TEXT NOT NULL,
            device TEXT NOT NULL CHECK (device IN ('desktop', 'mobile')),
            cost_limit_usd REAL NOT NULL CHECK (cost_limit_usd >= 0),
            actual_cost_usd REAL NOT NULL CHECK (actual_cost_usd >= 0),
            component_status_json TEXT NOT NULL,
            offering_profile_json TEXT NOT NULL,
            ranked_keywords_json TEXT NOT NULL,
            keyword_candidates_json TEXT NOT NULL,
            selected_keywords_json TEXT NOT NULL,
            seo_competitors_json TEXT NOT NULL,
            serp_evidence_json TEXT NOT NULL,
            sources_json TEXT NOT NULL,
            warnings_json TEXT NOT NULL,
            evidence_summary_json TEXT NOT NULL,
            captured_at TEXT NOT NULL,
            expires_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          ) STRICT;

          CREATE INDEX seo_snapshots_domain_captured
          ON seo_snapshots(domain, captured_at DESC);

          CREATE INDEX seo_snapshots_session_updated
          ON seo_snapshots(session_id, updated_at DESC);

          PRAGMA user_version = 3;
        `);
      });
    }
    if (version < 4) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE seo_article_jobs (
            job_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            domain TEXT NOT NULL,
            primary_keyword TEXT NOT NULL,
            supporting_keywords_json TEXT NOT NULL,
            input_json TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('queued', 'running', 'completed', 'partial', 'failed', 'interrupted')),
            stage TEXT NOT NULL,
            error_code TEXT,
            error_message TEXT,
            latest_version_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(session_id, request_id)
          ) STRICT;

          CREATE INDEX seo_article_jobs_session_updated
          ON seo_article_jobs(session_id, updated_at DESC);

          CREATE INDEX seo_article_jobs_domain_updated
          ON seo_article_jobs(session_id, domain, updated_at DESC);

          CREATE TABLE seo_article_versions (
            version_id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL REFERENCES seo_article_jobs(job_id) ON DELETE CASCADE,
            version_number INTEGER NOT NULL CHECK (version_number > 0),
            parent_version_id TEXT,
            status TEXT NOT NULL CHECK (status IN ('completed', 'partial')),
            domain TEXT NOT NULL,
            primary_keyword TEXT NOT NULL,
            supporting_keywords_json TEXT NOT NULL,
            context_json TEXT NOT NULL,
            plan_json TEXT NOT NULL,
            markdown TEXT NOT NULL,
            structured_data_json TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            answer_blocks_json TEXT NOT NULL,
            faq_json TEXT NOT NULL,
            sources_json TEXT NOT NULL,
            claim_ledger_json TEXT NOT NULL,
            quality_report_json TEXT NOT NULL,
            warnings_json TEXT NOT NULL,
            review_status TEXT NOT NULL CHECK (review_status = 'ready_for_review'),
            model TEXT NOT NULL,
            download_token TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            UNIQUE(job_id, version_number)
          ) STRICT;

          CREATE INDEX seo_article_versions_job_created
          ON seo_article_versions(job_id, created_at DESC);

          PRAGMA user_version = 4;
        `);
      });
    }
    if (version < 5) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE seo_article_briefs (
            brief_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            domain TEXT NOT NULL,
            research_key TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('choosing', 'needs_details', 'writing', 'complete', 'failed')),
            brief_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(session_id, domain, research_key)
          ) STRICT;

          CREATE INDEX seo_article_briefs_session_updated
          ON seo_article_briefs(session_id, updated_at DESC);

          ALTER TABLE seo_article_jobs ADD COLUMN brief_id TEXT;

          CREATE INDEX seo_article_jobs_brief
          ON seo_article_jobs(brief_id, updated_at DESC);

          PRAGMA user_version = 5;
        `);
      });
    }
    if (version < 6) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE prospects (
            prospect_id TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            list_name TEXT NOT NULL,
            company_key TEXT NOT NULL,
            row_number INTEGER,
            company TEXT NOT NULL,
            region TEXT NOT NULL DEFAULT '',
            tier TEXT NOT NULL DEFAULT '',
            source TEXT NOT NULL DEFAULT '',
            website TEXT NOT NULL DEFAULT '',
            linkedin_company_url TEXT NOT NULL DEFAULT '',
            contact_name TEXT NOT NULL DEFAULT '',
            contact_email TEXT NOT NULL DEFAULT '',
            linkedin_url TEXT NOT NULL DEFAULT '',
            confidence TEXT NOT NULL DEFAULT ''
              CHECK (confidence IN ('', 'high', 'medium', 'low', 'none')),
            flag_reason TEXT NOT NULL DEFAULT '',
            pdf_sent TEXT NOT NULL DEFAULT '',
            sent_date TEXT NOT NULL DEFAULT '',
            opened TEXT NOT NULL DEFAULT '',
            follow_up_sent TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'imported'
              CHECK (status IN ('imported', 'needs_review', 'enriched', 'emailed', 'opened', 'followed_up', 'replied', 'closed')),
            notes TEXT NOT NULL DEFAULT '',
            campaign_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(brand, list_name, company_key)
          ) STRICT;

          CREATE INDEX prospects_brand_status
          ON prospects(brand, status, updated_at DESC);

          CREATE INDEX prospects_brand_list
          ON prospects(brand, list_name, row_number ASC);

          CREATE TABLE campaigns (
            campaign_id TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            name TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'draft'
              CHECK (status IN ('draft', 'active', 'completed')),
            brief_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          ) STRICT;

          CREATE INDEX campaigns_brand_updated
          ON campaigns(brand, updated_at DESC);

          CREATE TABLE outreach_events (
            event_id TEXT PRIMARY KEY,
            prospect_id TEXT NOT NULL REFERENCES prospects(prospect_id) ON DELETE CASCADE,
            campaign_id TEXT,
            event_type TEXT NOT NULL
              CHECK (event_type IN ('imported', 'enriched', 'flagged', 'emailed', 'opened', 'clicked', 'followed_up', 'replied', 'status_change')),
            detail TEXT NOT NULL DEFAULT '',
            occurred_at TEXT NOT NULL,
            created_at TEXT NOT NULL
          ) STRICT;

          CREATE INDEX outreach_events_prospect
          ON outreach_events(prospect_id, occurred_at DESC);

          PRAGMA user_version = 6;
        `);
      });
    }
    if (version < 7) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE enrichment_jobs (
            job_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            request_id TEXT NOT NULL,
            brand TEXT NOT NULL,
            list_name TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL CHECK (status IN ('queued', 'running', 'completed', 'partial', 'failed')),
            stage TEXT NOT NULL,
            target_count INTEGER NOT NULL DEFAULT 0,
            enriched_count INTEGER NOT NULL DEFAULT 0,
            flagged_count INTEGER NOT NULL DEFAULT 0,
            skipped_json TEXT NOT NULL DEFAULT '[]',
            provider_cost_usd REAL,
            error_code TEXT,
            error_message TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(session_id, request_id)
          ) STRICT;

          CREATE INDEX enrichment_jobs_session_updated
          ON enrichment_jobs(session_id, updated_at DESC);

          PRAGMA user_version = 7;
        `);
      });
    }
    if (version < 8) {
      this.transaction(() => {
        this.database.exec(`
          ALTER TABLE prospects ADD COLUMN hook TEXT NOT NULL DEFAULT '';
          ALTER TABLE prospects ADD COLUMN hook_evidence TEXT NOT NULL DEFAULT '';
          ALTER TABLE prospects ADD COLUMN draft_id TEXT NOT NULL DEFAULT '';
          ALTER TABLE prospects ADD COLUMN drafted_at TEXT NOT NULL DEFAULT '';
          ALTER TABLE prospects ADD COLUMN clicked_at TEXT NOT NULL DEFAULT '';
          ALTER TABLE prospects ADD COLUMN follow_up_due TEXT NOT NULL DEFAULT '';
          ALTER TABLE prospects ADD COLUMN close_reason TEXT NOT NULL DEFAULT '';

          CREATE INDEX prospects_follow_up_due
          ON prospects(brand, follow_up_due)
          WHERE follow_up_due <> '';

          CREATE TABLE suppressions (
            suppression_id TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            email_key TEXT NOT NULL,
            company_key TEXT NOT NULL DEFAULT '',
            reason TEXT NOT NULL
              CHECK (reason IN ('unsubscribed', 'bounced', 'asked', 'manual')),
            detail TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            UNIQUE(brand, email_key)
          ) STRICT;

          CREATE INDEX suppressions_brand_created
          ON suppressions(brand, created_at DESC);

          PRAGMA user_version = 8;
        `);
      });
    }
    if (version < 9) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE outreach_settings (
            brand TEXT PRIMARY KEY,
            sender_name TEXT NOT NULL,
            sender_contact TEXT NOT NULL,
            unsubscribe_line TEXT NOT NULL,
            daily_cap INTEGER NOT NULL DEFAULT 20,
            follow_up_days INTEGER NOT NULL DEFAULT 7,
            guide_page_url TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL
          ) STRICT;

          PRAGMA user_version = 9;
        `);
      });
    }
    if (version < 10) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE prospect_lists (
            brand TEXT NOT NULL,
            list_name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (brand, list_name)
          ) STRICT;

          PRAGMA user_version = 10;
        `);
      });
    }
    if (version < 11) {
      this.transaction(() => {
        this.database.exec(`
          CREATE TABLE outreach_drafts (
            draft_row_id TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            prospect_id TEXT NOT NULL
              REFERENCES prospects(prospect_id) ON DELETE CASCADE,
            campaign_id TEXT,
            subject TEXT NOT NULL DEFAULT '',
            body TEXT NOT NULL DEFAULT '',
            hook TEXT NOT NULL DEFAULT '',
            hook_evidence TEXT NOT NULL DEFAULT '',
            state TEXT NOT NULL DEFAULT 'composing'
              CHECK (state IN ('composing', 'approved', 'created', 'discarded')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(prospect_id)
          ) STRICT;

          CREATE INDEX outreach_drafts_brand_state
          ON outreach_drafts(brand, state, updated_at DESC);

          PRAGMA user_version = 11;
        `);
      });
    }
    this.database.prepare("SELECT rowid FROM message_search LIMIT 1").all();
    this.database.prepare("SELECT domain FROM business_memory LIMIT 1").all();
    this.database.prepare("SELECT job_id FROM domain_research_jobs LIMIT 1").all();
    this.database.prepare("SELECT snapshot_id FROM seo_snapshots LIMIT 1").all();
    this.database.prepare("SELECT job_id FROM seo_article_jobs LIMIT 1").all();
    this.database.prepare("SELECT version_id FROM seo_article_versions LIMIT 1").all();
    this.database.prepare("SELECT brief_id FROM seo_article_briefs LIMIT 1").all();
    this.database.prepare("SELECT prospect_id FROM prospects LIMIT 1").all();
    this.database.prepare("SELECT campaign_id FROM campaigns LIMIT 1").all();
    this.database.prepare("SELECT event_id FROM outreach_events LIMIT 1").all();
    this.database.prepare("SELECT job_id FROM enrichment_jobs LIMIT 1").all();
    this.database.prepare("SELECT suppression_id FROM suppressions LIMIT 1").all();
    this.database.prepare("SELECT brand FROM outreach_settings LIMIT 1").all();
    this.database.prepare("SELECT list_name FROM prospect_lists LIMIT 1").all();
    this.database.prepare("SELECT draft_row_id FROM outreach_drafts LIMIT 1").all();
  }

  private transaction<T>(operation: () => T): T {
    this.database.exec("BEGIN IMMEDIATE");
    try {
      const result = operation();
      this.database.exec("COMMIT");
      return result;
    } catch (error) {
      this.database.exec("ROLLBACK");
      throw error;
    }
  }

  private nextSequence(conversationId: string): number {
    const row = this.database
      .prepare(
        "SELECT COALESCE(MAX(sequence), 0) + 1 AS sequence FROM messages WHERE conversation_id = ?",
      )
      .get(conversationId) as { sequence: number };
    return Number(row.sequence);
  }

  private attachmentsFor(messageIds: readonly string[]): Map<string, StoredAttachment[]> {
    const result = new Map<string, StoredAttachment[]>();
    if (messageIds.length === 0) {
      return result;
    }
    const placeholders = messageIds.map(() => "?").join(", ");
    const rows = this.database
      .prepare(
        `SELECT message_id, document_id, name, type, mime_type, word_count,
                character_count, page_count, expires_at
         FROM message_attachments
         WHERE message_id IN (${placeholders})
         ORDER BY rowid`,
      )
      .all(...messageIds) as unknown as AttachmentRow[];
    for (const row of rows) {
      const attachment: StoredAttachment = {
        documentId: row.document_id,
        name: row.name,
        type: row.type,
        mimeType: row.mime_type,
        wordCount: Number(row.word_count),
        characterCount: Number(row.character_count),
        expiresAt: row.expires_at,
      };
      if (row.page_count !== null) {
        attachment.pageCount = Number(row.page_count);
      }
      const entries = result.get(row.message_id) ?? [];
      entries.push(attachment);
      result.set(row.message_id, entries);
    }
    return result;
  }

  private messagesFromRows(rows: readonly MessageRow[]): StoredMessage[] {
    const attachments = this.attachmentsFor(rows.map((row) => row.id));
    return rows.map((row) => {
      const message: StoredMessage = {
        id: row.id,
        conversationId: row.conversation_id,
        requestId: row.request_id,
        role: row.role,
        content: row.content,
        status: row.status,
        createdAt: row.created_at,
        sequence: Number(row.sequence),
        attachments: attachments.get(row.id) ?? [],
      };
      if (row.error_code !== null) {
        message.errorCode = row.error_code;
      }
      if (row.run_id !== null) {
        message.runId = row.run_id;
      }
      return message;
    });
  }

  private messageById(id: string): StoredMessage | undefined {
    const row = this.database
      .prepare("SELECT * FROM messages WHERE id = ?")
      .get(id) as MessageRow | undefined;
    return row === undefined ? undefined : this.messagesFromRows([row])[0];
  }

  createConversation(
    id: string,
    agentId: string,
    createdAt = nowIso(),
  ): ConversationSummary {
    this.database
      .prepare(
        `INSERT INTO conversations(id, agent_id, title, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?)
         ON CONFLICT(id) DO NOTHING`,
      )
      .run(id, agentId, DEFAULT_TITLE, createdAt, createdAt);
    const conversation = this.getConversation(id);
    if (!conversation || conversation.agentId !== agentId) {
      throw new Error("Conversation belongs to a different agent");
    }
    return conversation;
  }

  getConversation(id: string): ConversationSummary | undefined {
    const row = this.database
      .prepare(
        `SELECT c.*, COUNT(m.id) AS message_count
         FROM conversations c
         LEFT JOIN messages m ON m.conversation_id = c.id
         WHERE c.id = ?
         GROUP BY c.id`,
      )
      .get(id) as ConversationRow | undefined;
    return row === undefined ? undefined : conversationFromRow(row);
  }

  listConversations(limit: number, cursor?: string): ConversationListPage {
    const boundedLimit = Math.max(1, Math.min(limit, 100));
    const cursorValue = cursor === undefined ? undefined : decodeCursor(cursor);
    const rows = (cursorValue === undefined
      ? this.database
          .prepare(
            `SELECT c.*, COUNT(m.id) AS message_count
             FROM conversations c
             LEFT JOIN messages m ON m.conversation_id = c.id
             GROUP BY c.id
             ORDER BY c.updated_at DESC, c.id DESC
             LIMIT ?`,
          )
          .all(boundedLimit + 1)
      : this.database
          .prepare(
            `SELECT c.*, COUNT(m.id) AS message_count
             FROM conversations c
             LEFT JOIN messages m ON m.conversation_id = c.id
             WHERE c.updated_at < ? OR (c.updated_at = ? AND c.id < ?)
             GROUP BY c.id
             ORDER BY c.updated_at DESC, c.id DESC
             LIMIT ?`,
          )
          .all(
            cursorValue.updatedAt,
            cursorValue.updatedAt,
            cursorValue.id,
            boundedLimit + 1,
          )) as unknown as ConversationRow[];
    const hasMore = rows.length > boundedLimit;
    const selected = rows.slice(0, boundedLimit);
    const page: ConversationListPage = {
      conversations: selected.map(conversationFromRow),
    };
    const last = selected.at(-1);
    if (hasMore && last) {
      page.nextCursor = encodeCursor(last.updated_at, last.id);
    }
    return page;
  }

  getConversationPage(
    id: string,
    limit: number,
    before?: number,
  ): ConversationPage | undefined {
    const conversation = this.getConversation(id);
    if (!conversation) {
      return undefined;
    }
    const boundedLimit = Math.max(1, Math.min(limit, 200));
    const rows = (before === undefined
      ? this.database
          .prepare(
            `SELECT * FROM messages
             WHERE conversation_id = ?
             ORDER BY sequence DESC
             LIMIT ?`,
          )
          .all(id, boundedLimit + 1)
      : this.database
          .prepare(
            `SELECT * FROM messages
             WHERE conversation_id = ? AND sequence < ?
             ORDER BY sequence DESC
             LIMIT ?`,
          )
          .all(id, before, boundedLimit + 1)) as unknown as MessageRow[];
    const hasMore = rows.length > boundedLimit;
    const selected = rows.slice(0, boundedLimit).reverse();
    const page: ConversationPage = {
      conversation,
      messages: this.messagesFromRows(selected),
    };
    if (hasMore && selected[0]) {
      page.nextBefore = Number(selected[0].sequence);
    }
    return page;
  }

  renameConversation(id: string, title: string): ConversationSummary | undefined {
    const cleaned = title.replace(/\s+/g, " ").trim();
    if (cleaned.length === 0 || cleaned.length > MAX_TITLE_LENGTH) {
      throw new Error("Invalid conversation title");
    }
    const result = this.database
      .prepare("UPDATE conversations SET title = ? WHERE id = ?")
      .run(cleaned, id);
    return Number(result.changes) === 0 ? undefined : this.getConversation(id);
  }

  deleteConversation(id: string): boolean {
    const result = this.database
      .prepare("DELETE FROM conversations WHERE id = ?")
      .run(id);
    return Number(result.changes) > 0;
  }

  beginTurn(input: BeginTurnInput): StoredTurn {
    return this.transaction(() => {
      const existing = this.getTurn(input.conversationId, input.requestId);
      if (existing.user) {
        return existing;
      }
      const createdAt = input.createdAt ?? nowIso();
      const conversation = this.createConversation(
        input.conversationId,
        input.agentId,
        createdAt,
      );
      const id = randomUUID();
      const sequence = this.nextSequence(input.conversationId);
      this.database
        .prepare(
          `INSERT INTO messages(
             id, conversation_id, request_id, role, content, status,
             error_code, run_id, created_at, sequence
           ) VALUES (?, ?, ?, 'user', ?, 'pending', NULL, NULL, ?, ?)`,
        )
        .run(
          id,
          input.conversationId,
          input.requestId,
          input.content,
          createdAt,
          sequence,
        );
      const insertAttachment = this.database.prepare(
        `INSERT INTO message_attachments(
           message_id, document_id, name, type, mime_type, word_count,
           character_count, page_count, expires_at
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      );
      for (const attachment of input.attachments ?? []) {
        insertAttachment.run(
          id,
          attachment.documentId,
          attachment.name,
          attachment.type,
          attachment.mimeType,
          attachment.wordCount,
          attachment.characterCount,
          attachment.pageCount ?? null,
          attachment.expiresAt,
        );
      }
      const title =
        conversation.messageCount === 0 && conversation.title === DEFAULT_TITLE
          ? titleFromMessage(input.content)
          : conversation.title;
      this.database
        .prepare(
          "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
        )
        .run(title, createdAt, input.conversationId);
      const user = this.messageById(id);
      if (!user) {
        throw new Error("Stored user message could not be read");
      }
      return { user };
    });
  }

  completeTurn(input: CompleteTurnInput): StoredTurn {
    return this.transaction(() => {
      const existing = this.getTurn(input.conversationId, input.requestId);
      if (!existing.user) {
        throw new Error("User message does not exist");
      }
      if (existing.assistant) {
        return existing;
      }
      const createdAt = input.createdAt ?? nowIso();
      this.database
        .prepare(
          `UPDATE messages
           SET status = 'complete', error_code = NULL
           WHERE conversation_id = ? AND request_id = ? AND role = 'user'`,
        )
        .run(input.conversationId, input.requestId);
      const assistantId = randomUUID();
      this.database
        .prepare(
          `INSERT INTO messages(
             id, conversation_id, request_id, role, content, status,
             error_code, run_id, created_at, sequence
           ) VALUES (?, ?, ?, 'assistant', ?, 'complete', NULL, ?, ?, ?)`,
        )
        .run(
          assistantId,
          input.conversationId,
          input.requestId,
          input.content,
          input.runId ?? null,
          createdAt,
          this.nextSequence(input.conversationId),
        );
      this.database
        .prepare("UPDATE conversations SET updated_at = ? WHERE id = ?")
        .run(createdAt, input.conversationId);
      return this.getTurn(input.conversationId, input.requestId);
    });
  }

  failTurn(conversationId: string, requestId: string, errorCode: string): void {
    this.database
      .prepare(
        `UPDATE messages
         SET status = 'failed', error_code = ?
         WHERE conversation_id = ? AND request_id = ? AND role = 'user'
           AND status = 'pending'`,
      )
      .run(errorCode, conversationId, requestId);
  }

  getTurn(conversationId: string, requestId: string): StoredTurn {
    const rows = this.database
      .prepare(
        `SELECT * FROM messages
         WHERE conversation_id = ? AND request_id = ?
         ORDER BY sequence`,
      )
      .all(conversationId, requestId) as unknown as MessageRow[];
    const messages = this.messagesFromRows(rows);
    const user = messages.find((message) => message.role === "user");
    const assistant = messages.find((message) => message.role === "assistant");
    return {
      ...(user === undefined ? {} : { user }),
      ...(assistant === undefined ? {} : { assistant }),
    };
  }

  getHistory(
    conversationId: string,
    maximumTurns = 6,
    maximumCharacters = 24_000,
  ): HistoryMessage[] {
    const rows = this.database
      .prepare(
        `SELECT u.content AS user_content, a.content AS assistant_content
         FROM messages u
         JOIN messages a
           ON a.conversation_id = u.conversation_id
          AND a.request_id = u.request_id
          AND a.role = 'assistant'
          AND a.status = 'complete'
         WHERE u.conversation_id = ?
           AND u.role = 'user'
           AND u.status = 'complete'
         ORDER BY a.sequence DESC`,
      )
      .all(conversationId) as unknown as Array<{
      user_content: string;
      assistant_content: string;
    }>;
    const selected: Array<[HistoryMessage, HistoryMessage]> = [];
    let characters = 0;
    for (const row of rows) {
      if (selected.length >= maximumTurns) {
        break;
      }
      const pairCharacters =
        row.user_content.length + row.assistant_content.length;
      if (characters + pairCharacters > maximumCharacters) {
        break;
      }
      selected.push([
        { role: "user", content: row.user_content },
        { role: "assistant", content: row.assistant_content },
      ]);
      characters += pairCharacters;
    }
    return selected.reverse().flat();
  }

  search(query: string, limit: number): ConversationSearchResult[] {
    const cleaned = query.normalize("NFC").trim();
    if (cleaned.length === 0 || cleaned.length > MAX_SEARCH_LENGTH) {
      throw new Error("Invalid search query");
    }
    const expression = searchExpression(cleaned);
    if (expression.length === 0) {
      return [];
    }
    const boundedLimit = Math.max(1, Math.min(limit, 100));
    const rows = this.database
      .prepare(
        `SELECT m.conversation_id, c.title AS conversation_title,
                m.id AS message_id, m.role,
                snippet(message_search, 0, '', '', ' … ', 18) AS snippet,
                m.created_at
         FROM message_search
         JOIN messages m ON m.rowid = message_search.rowid
         JOIN conversations c ON c.id = m.conversation_id
         WHERE message_search MATCH ?
         ORDER BY rank, m.created_at DESC
         LIMIT ?`,
      )
      .all(expression, boundedLimit) as unknown as SearchRow[];
    return rows.map((row) => ({
      conversationId: row.conversation_id,
      conversationTitle: row.conversation_title,
      messageId: row.message_id,
      role: row.role,
      snippet: row.snippet,
      createdAt: row.created_at,
    }));
  }

  saveBusinessMemory(input: BusinessMemoryInput): BusinessMemoryRecord {
    const timestamp = nowIso();
    const researchedAt = input.researchedAt ?? timestamp;
    this.database
      .prepare(
        `INSERT INTO business_memory(
           domain, schema_version, job_id, status, company_overview,
           profile_json, competitors_json, seed_keywords_json,
           keyword_candidates_json, keyword_groups_json, sources_json,
           warnings_json, research_summary, evidence_quality_json,
           researched_at, created_at, updated_at
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(domain) DO UPDATE SET
           schema_version = excluded.schema_version,
           job_id = excluded.job_id,
           status = excluded.status,
           company_overview = excluded.company_overview,
           profile_json = excluded.profile_json,
           competitors_json = excluded.competitors_json,
           seed_keywords_json = excluded.seed_keywords_json,
           keyword_candidates_json = excluded.keyword_candidates_json,
           keyword_groups_json = excluded.keyword_groups_json,
           sources_json = excluded.sources_json,
           warnings_json = excluded.warnings_json,
           research_summary = excluded.research_summary,
           evidence_quality_json = excluded.evidence_quality_json,
           researched_at = excluded.researched_at,
           updated_at = excluded.updated_at`,
      )
      .run(
        input.domain,
        input.schemaVersion,
        input.jobId,
        input.status,
        input.companyOverview,
        JSON.stringify(input.profile),
        JSON.stringify(input.competitors),
        JSON.stringify(input.seedKeywords),
        JSON.stringify(input.keywordCandidates),
        JSON.stringify(input.keywordGroups),
        JSON.stringify(input.sources),
        JSON.stringify(input.warnings),
        input.researchSummary,
        JSON.stringify(input.evidenceQuality),
        researchedAt,
        timestamp,
        timestamp,
      );
    const stored = this.getBusinessMemory(input.domain);
    if (!stored) {
      throw new Error("Stored business memory could not be read");
    }
    return stored;
  }

  registerDomainResearchJob(
    sessionId: string,
    jobId: string,
    domain: string,
  ): void {
    this.transaction(() => {
      const existing = this.database
        .prepare("SELECT session_id, domain FROM domain_research_jobs WHERE job_id = ?")
        .get(jobId) as { session_id: string; domain: string } | undefined;
      if (
        existing &&
        (existing.session_id !== sessionId || existing.domain !== domain)
      ) {
        throw new Error("Domain research job belongs to a different conversation");
      }
      const timestamp = nowIso();
      this.database
        .prepare(
          `INSERT INTO domain_research_jobs(
             job_id, session_id, domain, status, created_at, updated_at
           ) VALUES (?, ?, ?, 'queued', ?, ?)
           ON CONFLICT(job_id) DO UPDATE SET updated_at = excluded.updated_at`,
        )
        .run(jobId, sessionId, domain, timestamp, timestamp);
    });
  }

  getDomainResearchJob(
    sessionId: string,
    jobId: string,
  ): DomainResearchJobRecord | undefined {
    const row = this.database
      .prepare(
        `SELECT job_id, session_id, domain, status, created_at, updated_at
         FROM domain_research_jobs
         WHERE job_id = ?`,
      )
      .get(jobId) as
      | {
          job_id: string;
          session_id: string;
          domain: string;
          status: DomainResearchJobRecord["status"];
          created_at: string;
          updated_at: string;
        }
      | undefined;
    // A job is only visible to the conversation that registered it.
    if (!row || row.session_id !== sessionId) {
      return undefined;
    }
    return {
      jobId: row.job_id,
      sessionId: row.session_id,
      domain: row.domain,
      status: row.status,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    };
  }

  saveBusinessMemoryForJob(
    sessionId: string,
    input: BusinessMemoryInput,
  ): BusinessMemoryRecord {
    return this.transaction(() => {
      const job = this.database
        .prepare(
          "SELECT session_id, domain FROM domain_research_jobs WHERE job_id = ?",
        )
        .get(input.jobId) as { session_id: string; domain: string } | undefined;
      if (!job || job.session_id !== sessionId || job.domain !== input.domain) {
        throw new Error("Domain research job is not registered to this conversation");
      }
      const stored = this.saveBusinessMemory(input);
      this.database
        .prepare(
          `UPDATE domain_research_jobs
           SET status = ?, updated_at = ?
           WHERE job_id = ? AND session_id = ?`,
        )
        .run(input.status, nowIso(), input.jobId, sessionId);
      return stored;
    });
  }

  savePaidDomainResearchForJob(
    sessionId: string,
    snapshot: SeoSnapshotInput,
    memory?: BusinessMemoryInput,
  ): { snapshot: SeoSnapshotRecord; memory?: BusinessMemoryRecord } {
    return this.transaction(() => {
      const job = this.database
        .prepare(
          "SELECT session_id, domain FROM domain_research_jobs WHERE job_id = ?",
        )
        .get(snapshot.jobId) as { session_id: string; domain: string } | undefined;
      if (!job || job.session_id !== sessionId || job.domain !== snapshot.domain) {
        throw new Error("Paid domain research job is not registered to this conversation");
      }
      if (snapshot.status !== "failed") {
        if (
          memory === undefined ||
          memory.jobId !== snapshot.jobId ||
          memory.domain !== snapshot.domain ||
          memory.status !== snapshot.status
        ) {
          throw new Error("Successful paid research requires matching business memory");
        }
      } else if (memory !== undefined) {
        throw new Error("Failed paid research cannot replace business memory");
      }

      const existing = this.database
        .prepare("SELECT snapshot_id, created_at FROM seo_snapshots WHERE job_id = ?")
        .get(snapshot.jobId) as { snapshot_id: string; created_at: string } | undefined;
      const timestamp = nowIso();
      const capturedAt = snapshot.capturedAt ?? timestamp;
      const snapshotId = existing?.snapshot_id ?? randomUUID();
      const createdAt = existing?.created_at ?? timestamp;
      this.database
        .prepare(
          `INSERT INTO seo_snapshots(
             snapshot_id, job_id, session_id, schema_version, status,
             research_depth, domain, location_code, language_code, device,
             cost_limit_usd, actual_cost_usd, component_status_json,
             offering_profile_json, ranked_keywords_json,
             keyword_candidates_json, selected_keywords_json,
             seo_competitors_json, serp_evidence_json, sources_json,
             warnings_json, evidence_summary_json, captured_at, expires_at,
             created_at, updated_at
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(job_id) DO UPDATE SET
             status = excluded.status,
             research_depth = excluded.research_depth,
             location_code = excluded.location_code,
             language_code = excluded.language_code,
             device = excluded.device,
             cost_limit_usd = excluded.cost_limit_usd,
             actual_cost_usd = excluded.actual_cost_usd,
             component_status_json = excluded.component_status_json,
             offering_profile_json = excluded.offering_profile_json,
             ranked_keywords_json = excluded.ranked_keywords_json,
             keyword_candidates_json = excluded.keyword_candidates_json,
             selected_keywords_json = excluded.selected_keywords_json,
             seo_competitors_json = excluded.seo_competitors_json,
             serp_evidence_json = excluded.serp_evidence_json,
             sources_json = excluded.sources_json,
             warnings_json = excluded.warnings_json,
             evidence_summary_json = excluded.evidence_summary_json,
             captured_at = excluded.captured_at,
             expires_at = excluded.expires_at,
             updated_at = excluded.updated_at`,
        )
        .run(
          snapshotId,
          snapshot.jobId,
          sessionId,
          snapshot.schemaVersion,
          snapshot.status,
          snapshot.researchDepth,
          snapshot.domain,
          snapshot.locationCode,
          snapshot.languageCode,
          snapshot.device,
          snapshot.costLimitUsd,
          snapshot.actualCostUsd,
          JSON.stringify(snapshot.componentStatus),
          JSON.stringify(snapshot.offeringProfile),
          JSON.stringify(snapshot.rankedKeywords),
          JSON.stringify(snapshot.keywordCandidates),
          JSON.stringify(snapshot.selectedKeywords),
          JSON.stringify(snapshot.seoCompetitors),
          JSON.stringify(snapshot.serpEvidence),
          JSON.stringify(snapshot.sources),
          JSON.stringify(snapshot.warnings),
          JSON.stringify(snapshot.evidenceSummary),
          capturedAt,
          snapshot.expiresAt ?? null,
          createdAt,
          timestamp,
        );

      const savedMemory = memory === undefined ? undefined : this.saveBusinessMemory(memory);
      this.database
        .prepare(
          `UPDATE domain_research_jobs
           SET status = ?, updated_at = ?
           WHERE job_id = ? AND session_id = ?`,
        )
        .run(snapshot.status, timestamp, snapshot.jobId, sessionId);
      const savedSnapshot = this.getSeoSnapshotForJob(sessionId, snapshot.jobId);
      if (savedSnapshot === undefined) {
        throw new Error("Stored paid domain research snapshot could not be read");
      }
      return {
        snapshot: savedSnapshot,
        ...(savedMemory === undefined ? {} : { memory: savedMemory }),
      };
    });
  }

  getSeoSnapshotForJob(
    sessionId: string,
    jobId: string,
  ): SeoSnapshotRecord | undefined {
    const row = this.database
      .prepare("SELECT * FROM seo_snapshots WHERE job_id = ? AND session_id = ?")
      .get(jobId, sessionId) as SeoSnapshotRow | undefined;
    return row === undefined ? undefined : seoSnapshotFromRow(row);
  }

  getLatestSeoSnapshot(domain: string): SeoSnapshotRecord | undefined {
    const row = this.database
      .prepare(
        `SELECT * FROM seo_snapshots
         WHERE domain = ? AND status IN ('completed', 'partial')
         ORDER BY captured_at DESC, updated_at DESC
         LIMIT 1`,
      )
      .get(domain) as SeoSnapshotRow | undefined;
    return row === undefined ? undefined : seoSnapshotFromRow(row);
  }

  listSeoSnapshotSummaries(domain?: string, limit = 20): SeoSnapshotSummary[] {
    const boundedLimit = Math.max(1, Math.min(limit, 100));
    const rows = (domain === undefined
      ? this.database
          .prepare("SELECT * FROM seo_snapshots ORDER BY captured_at DESC LIMIT ?")
          .all(boundedLimit)
      : this.database
          .prepare(
            "SELECT * FROM seo_snapshots WHERE domain = ? ORDER BY captured_at DESC LIMIT ?",
          )
          .all(domain, boundedLimit)) as unknown as SeoSnapshotRow[];
    return rows.map((row) => ({
      snapshotId: row.snapshot_id,
      jobId: row.job_id,
      status: row.status,
      researchDepth: row.research_depth,
      domain: row.domain,
      locationCode: Number(row.location_code),
      languageCode: row.language_code,
      actualCostUsd: Number(row.actual_cost_usd),
      capturedAt: row.captured_at,
      updatedAt: row.updated_at,
      warningCount: (JSON.parse(row.warnings_json) as unknown[]).length,
    }));
  }

  getBusinessMemory(domain: string): BusinessMemoryRecord | undefined {
    const row = this.database
      .prepare("SELECT * FROM business_memory WHERE domain = ?")
      .get(domain) as BusinessMemoryRow | undefined;
    return row === undefined ? undefined : businessMemoryFromRow(row);
  }

  listBusinessMemory(limit = 50): BusinessMemoryRecord[] {
    const boundedLimit = Math.max(1, Math.min(limit, 100));
    const rows = this.database
      .prepare(
        `SELECT * FROM business_memory
         ORDER BY updated_at DESC, domain ASC
         LIMIT ?`,
      )
      .all(boundedLimit) as unknown as BusinessMemoryRow[];
    return rows.map(businessMemoryFromRow);
  }

  listBusinessMemorySummaries(limit = 50): BusinessMemorySummary[] {
    const boundedLimit = Math.max(1, Math.min(limit, 100));
    const rows = this.database
      .prepare(
        `SELECT job_id, status, domain, profile_json, warnings_json,
                researched_at, updated_at
         FROM business_memory
         ORDER BY updated_at DESC, domain ASC
         LIMIT ?`,
      )
      .all(boundedLimit) as unknown as Array<
      Pick<
        BusinessMemoryRow,
        | "job_id"
        | "status"
        | "domain"
        | "profile_json"
        | "warnings_json"
        | "researched_at"
        | "updated_at"
      >
    >;
    return rows.map((row) => {
      const profile = JSON.parse(row.profile_json) as Record<string, unknown>;
      const warnings = JSON.parse(row.warnings_json) as unknown[];
      return {
        jobId: row.job_id,
        status: row.status,
        domain: row.domain,
        brandName: typeof profile.brandName === "string" ? profile.brandName : "",
        warningCount: Array.isArray(warnings) ? warnings.length : 0,
        researchedAt: row.researched_at,
        updatedAt: row.updated_at,
      };
    });
  }

  importProspects(
    brand: string,
    listName: string,
    rows: readonly ProspectRowInput[],
  ): ProspectImportResult {
    const now = nowIso();
    let inserted = 0;
    const duplicateCompanies: string[] = [];
    this.transaction(() => {
      const existing = this.database.prepare(
        `SELECT prospect_id FROM prospects
         WHERE brand = ? AND list_name = ? AND company_key = ?`,
      );
      const insert = this.database.prepare(
        `INSERT INTO prospects (
           prospect_id, brand, list_name, company_key, row_number, company,
           region, tier, source, website, linkedin_company_url,
           contact_name, contact_email, linkedin_url,
           pdf_sent, sent_date, opened, follow_up_sent,
           status, notes, created_at, updated_at
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      );
      const insertEvent = this.database.prepare(
        `INSERT INTO outreach_events (
           event_id, prospect_id, event_type, detail, occurred_at, created_at
         ) VALUES (?, ?, 'imported', ?, ?, ?)`,
      );
      for (const row of rows) {
        const company = row.company.trim();
        const companyKey = company.toLowerCase();
        if (existing.get(brand, listName, companyKey) !== undefined) {
          duplicateCompanies.push(company);
          continue;
        }
        const prospectId = randomUUID();
        insert.run(
          prospectId,
          brand,
          listName,
          companyKey,
          Number.isInteger(row.rowNumber) ? Number(row.rowNumber) : null,
          company,
          row.region?.trim() ?? "",
          row.tier?.trim() ?? "",
          row.source?.trim() ?? "",
          row.website?.trim() ?? "",
          row.linkedinCompanyUrl?.trim() ?? "",
          row.contactName?.trim() ?? "",
          row.contactEmail?.trim() ?? "",
          row.linkedinUrl?.trim() ?? "",
          row.pdfSent?.trim() ?? "",
          row.sentDate?.trim() ?? "",
          row.opened?.trim() ?? "",
          row.followUpSent?.trim() ?? "",
          row.status ?? "imported",
          row.notes?.trim() ?? "",
          now,
          now,
        );
        insertEvent.run(randomUUID(), prospectId, `Imported into ${listName}`, now, now);
        inserted += 1;
      }
    });
    return {
      brand,
      listName,
      inserted,
      duplicates: duplicateCompanies.length,
      duplicateCompanies,
      total: rows.length,
    };
  }

  listProspects(filters: {
    brand?: string | undefined;
    status?: ProspectStatus | undefined;
    listName?: string | undefined;
    limit?: number | undefined;
  }): ProspectRecord[] {
    const boundedLimit = Math.max(1, Math.min(filters.limit ?? 100, 500));
    const conditions: string[] = [];
    const parameters: string[] = [];
    if (filters.brand !== undefined) {
      conditions.push("brand = ?");
      parameters.push(filters.brand);
    }
    if (filters.status !== undefined) {
      conditions.push("status = ?");
      parameters.push(filters.status);
    }
    if (filters.listName !== undefined) {
      conditions.push("list_name = ?");
      parameters.push(filters.listName);
    }
    const where = conditions.length > 0 ? `WHERE ${conditions.join(" AND ")}` : "";
    const rows = this.database
      .prepare(
        `SELECT * FROM prospects ${where}
         ORDER BY list_name ASC, row_number ASC, company ASC
         LIMIT ?`,
      )
      .all(...parameters, boundedLimit) as unknown as ProspectRow[];
    return rows.map(prospectFromRow);
  }

  prospectPipelineSummary(brand?: string): ProspectPipelineSummary {
    const where = brand === undefined ? "" : "WHERE brand = ?";
    const parameters = brand === undefined ? [] : [brand];
    const statusRows = this.database
      .prepare(
        `SELECT status, COUNT(*) AS status_count FROM prospects ${where}
         GROUP BY status`,
      )
      .all(...parameters) as unknown as Array<{
      status: ProspectStatus;
      status_count: number;
    }>;
    const listRows = this.database
      .prepare(
        `SELECT DISTINCT list_name FROM prospects ${where} ORDER BY list_name ASC`,
      )
      .all(...parameters) as unknown as Array<{ list_name: string }>;
    const updatedRow = this.database
      .prepare(`SELECT MAX(updated_at) AS last_updated FROM prospects ${where}`)
      .get(...parameters) as { last_updated: string | null } | undefined;
    const byStatus: Partial<Record<ProspectStatus, number>> = {};
    let total = 0;
    for (const row of statusRows) {
      byStatus[row.status] = row.status_count;
      total += row.status_count;
    }
    return {
      brand,
      total,
      byStatus,
      listNames: listRows.map((row) => row.list_name),
      lastUpdatedAt: updatedRow?.last_updated ?? undefined,
    };
  }

  listCampaigns(brand?: string): Array<{
    campaignId: string;
    brand: string;
    name: string;
    status: string;
    createdAt: string;
    updatedAt: string;
  }> {
    const where = brand === undefined ? "" : "WHERE brand = ?";
    const parameters = brand === undefined ? [] : [brand];
    const rows = this.database
      .prepare(
        `SELECT campaign_id, brand, name, status, created_at, updated_at
         FROM campaigns ${where}
         ORDER BY updated_at DESC`,
      )
      .all(...parameters) as unknown as Array<{
      campaign_id: string;
      brand: string;
      name: string;
      status: string;
      created_at: string;
      updated_at: string;
    }>;
    return rows.map((row) => ({
      campaignId: row.campaign_id,
      brand: row.brand,
      name: row.name,
      status: row.status,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    }));
  }

  listEnrichableProspects(
    brand: string,
    listName: string | undefined,
    limit: number,
  ): { eligible: ProspectRecord[]; missingUrl: string[] } {
    const boundedLimit = Math.max(1, Math.min(limit, 200));
    const listCondition = listName === undefined ? "" : "AND list_name = ?";
    const parameters = listName === undefined ? [brand] : [brand, listName];
    const rows = this.database
      .prepare(
        `SELECT * FROM prospects
         WHERE brand = ? ${listCondition}
           AND status IN ('imported', 'needs_review')
           AND contact_email = ''
         ORDER BY list_name ASC, row_number ASC, company ASC`,
      )
      .all(...parameters) as unknown as ProspectRow[];
    const records = rows.map(prospectFromRow);
    const eligible = records
      .filter((record) => record.linkedinCompanyUrl !== "")
      .slice(0, boundedLimit);
    const missingUrl = records
      .filter((record) => record.linkedinCompanyUrl === "")
      .map((record) => record.company);
    return { eligible, missingUrl };
  }

  registerEnrichmentJob(input: {
    sessionId: string;
    requestId: string;
    brand: string;
    listName: string;
    targetCount: number;
  }): { job: EnrichmentJobRecord; created: boolean } {
    const existing = this.database
      .prepare(
        `SELECT * FROM enrichment_jobs WHERE session_id = ? AND request_id = ?`,
      )
      .get(input.sessionId, input.requestId) as EnrichmentJobRow | undefined;
    if (existing !== undefined) {
      return { job: enrichmentJobFromRow(existing), created: false };
    }
    const now = nowIso();
    const jobId = randomUUID();
    this.database
      .prepare(
        `INSERT INTO enrichment_jobs (
           job_id, session_id, request_id, brand, list_name,
           status, stage, target_count, created_at, updated_at
         ) VALUES (?, ?, ?, ?, ?, 'queued', 'queued', ?, ?, ?)`,
      )
      .run(
        jobId,
        input.sessionId,
        input.requestId,
        input.brand,
        input.listName,
        input.targetCount,
        now,
        now,
      );
    const row = this.database
      .prepare(`SELECT * FROM enrichment_jobs WHERE job_id = ?`)
      .get(jobId) as unknown as EnrichmentJobRow;
    return { job: enrichmentJobFromRow(row), created: true };
  }

  updateEnrichmentJob(
    jobId: string,
    changes: {
      status?: EnrichmentJobStatus | undefined;
      stage?: string | undefined;
      enrichedCount?: number | undefined;
      flaggedCount?: number | undefined;
      skipped?: string[] | undefined;
      providerCostUsd?: number | undefined;
      errorCode?: string | undefined;
      errorMessage?: string | undefined;
    },
  ): EnrichmentJobRecord | undefined {
    const row = this.database
      .prepare(`SELECT * FROM enrichment_jobs WHERE job_id = ?`)
      .get(jobId) as EnrichmentJobRow | undefined;
    if (row === undefined) {
      return undefined;
    }
    this.database
      .prepare(
        `UPDATE enrichment_jobs SET
           status = ?, stage = ?, enriched_count = ?, flagged_count = ?,
           skipped_json = ?, provider_cost_usd = ?, error_code = ?,
           error_message = ?, updated_at = ?
         WHERE job_id = ?`,
      )
      .run(
        changes.status ?? row.status,
        changes.stage ?? row.stage,
        changes.enrichedCount ?? row.enriched_count,
        changes.flaggedCount ?? row.flagged_count,
        changes.skipped === undefined
          ? row.skipped_json
          : JSON.stringify(changes.skipped.slice(0, 200)),
        changes.providerCostUsd ?? row.provider_cost_usd,
        changes.errorCode ?? row.error_code,
        changes.errorMessage ?? row.error_message,
        nowIso(),
        jobId,
      );
    const updated = this.database
      .prepare(`SELECT * FROM enrichment_jobs WHERE job_id = ?`)
      .get(jobId) as unknown as EnrichmentJobRow;
    return enrichmentJobFromRow(updated);
  }

  getEnrichmentJob(
    sessionId: string,
    jobId: string,
  ): EnrichmentJobRecord | undefined {
    const row = this.database
      .prepare(
        `SELECT * FROM enrichment_jobs WHERE job_id = ? AND session_id = ?`,
      )
      .get(jobId, sessionId) as EnrichmentJobRow | undefined;
    return row === undefined ? undefined : enrichmentJobFromRow(row);
  }

  applyEnrichmentResults(
    jobId: string,
    results: readonly EnrichmentResultInput[],
  ): { enriched: number; flagged: number; missing: number } {
    const now = nowIso();
    let enriched = 0;
    let flagged = 0;
    let missing = 0;
    this.transaction(() => {
      const read = this.database.prepare(
        `SELECT * FROM prospects WHERE prospect_id = ?`,
      );
      const write = this.database.prepare(
        `UPDATE prospects SET
           contact_name = ?, contact_email = ?, linkedin_url = ?,
           confidence = ?, flag_reason = ?, status = ?, notes = ?, updated_at = ?
         WHERE prospect_id = ?`,
      );
      const insertEvent = this.database.prepare(
        `INSERT INTO outreach_events (
           event_id, prospect_id, event_type, detail, occurred_at, created_at
         ) VALUES (?, ?, ?, ?, ?, ?)`,
      );
      for (const result of results) {
        const row = read.get(result.prospectId) as ProspectRow | undefined;
        if (row === undefined) {
          missing += 1;
          continue;
        }
        const isHigh = result.confidence === "high";
        const status: ProspectStatus = isHigh ? "enriched" : "needs_review";
        const roleNote = result.jobTitle
          ? `Role: ${result.jobTitle}`
          : "";
        const notes = roleNote === ""
          ? row.notes
          : row.notes === ""
            ? roleNote
            : `${row.notes} | ${roleNote}`;
        write.run(
          result.contactName ?? "",
          result.contactEmail ?? "",
          result.linkedinUrl ?? "",
          result.confidence,
          result.flagReason ?? "",
          status,
          notes.slice(0, 1000),
          now,
          result.prospectId,
        );
        insertEvent.run(
          randomUUID(),
          result.prospectId,
          isHigh ? "enriched" : "flagged",
          isHigh
            ? `Enriched: ${result.contactName ?? ""} <${result.contactEmail ?? ""}>`
            : `Flagged (${result.confidence}): ${result.flagReason ?? "needs review"}`,
          now,
          now,
        );
        if (isHigh) {
          enriched += 1;
        } else {
          flagged += 1;
        }
      }
    });
    return { enriched, flagged, missing };
  }

  updateProspectFields(
    brand: string,
    updates: readonly ProspectUpdateInput[],
  ): ProspectUpdateResult[] {
    const now = nowIso();
    const outcomes: ProspectUpdateResult[] = [];
    this.transaction(() => {
      const insertEvent = this.database.prepare(
        `INSERT INTO outreach_events (
           event_id, prospect_id, event_type, detail, occurred_at, created_at
         ) VALUES (?, ?, 'status_change', ?, ?, ?)`,
      );
      for (const update of updates) {
        const companyKey = update.company.trim().toLowerCase();
        const listCondition = update.listName === undefined ? "" : "AND list_name = ?";
        const parameters = update.listName === undefined
          ? [brand, companyKey]
          : [brand, companyKey, update.listName];
        const rows = this.database
          .prepare(
            `SELECT * FROM prospects
             WHERE brand = ? AND company_key = ? ${listCondition}`,
          )
          .all(...parameters) as unknown as ProspectRow[];
        if (rows.length === 0) {
          outcomes.push({ company: update.company, outcome: "not_found", changedFields: [] });
          continue;
        }
        if (rows.length > 1) {
          outcomes.push({ company: update.company, outcome: "ambiguous", changedFields: [] });
          continue;
        }
        const row = rows[0]!;
        const columnByField: Record<string, string> = {
          linkedinCompanyUrl: "linkedin_company_url",
          contactName: "contact_name",
          contactEmail: "contact_email",
          linkedinUrl: "linkedin_url",
          website: "website",
          region: "region",
          tier: "tier",
          status: "status",
          notes: "notes",
          flagReason: "flag_reason",
          hook: "hook",
          hookEvidence: "hook_evidence",
          followUpDue: "follow_up_due",
          closeReason: "close_reason",
        };
        const assignments: string[] = [];
        const values: Array<string | number> = [];
        const changedFields: string[] = [];
        for (const [field, column] of Object.entries(columnByField)) {
          const value = (update.fields as Record<string, unknown>)[field];
          if (typeof value === "string") {
            assignments.push(`${column} = ?`);
            values.push(value);
            changedFields.push(field);
          }
        }
        if (assignments.length === 0) {
          outcomes.push({ company: update.company, outcome: "updated", changedFields: [] });
          continue;
        }
        this.database
          .prepare(
            `UPDATE prospects SET ${assignments.join(", ")}, updated_at = ?
             WHERE prospect_id = ?`,
          )
          .run(...values, now, row.prospect_id);
        if (typeof update.fields.status === "string" && update.fields.status !== row.status) {
          insertEvent.run(
            randomUUID(),
            row.prospect_id,
            `Status ${row.status} -> ${update.fields.status} (manual update)`,
            now,
            now,
          );
        }
        outcomes.push({ company: update.company, outcome: "updated", changedFields });
      }
    });
    return outcomes;
  }

  getProspect(prospectId: string): ProspectRecord | undefined {
    const row = this.database
      .prepare(`SELECT * FROM prospects WHERE prospect_id = ?`)
      .get(prospectId) as unknown as ProspectRow | undefined;
    return row === undefined ? undefined : prospectFromRow(row);
  }

  /**
   * Add one prospect by hand from the board. Same duplicate rule as an
   * import — a company already on that brand's list is reported back, never
   * silently merged.
   */
  addProspect(
    brand: string,
    listName: string,
    input: ProspectRowInput,
  ): ProspectAddResult {
    const company = input.company.trim();
    const companyKey = company.toLowerCase();
    return this.transaction(() => {
      const existing = this.database
        .prepare(
          `SELECT prospect_id FROM prospects
           WHERE brand = ? AND list_name = ? AND company_key = ?`,
        )
        .get(brand, listName, companyKey);
      if (existing !== undefined) {
        return { outcome: "duplicate" as const, company, prospect: undefined };
      }
      const now = nowIso();
      const prospectId = randomUUID();
      this.database
        .prepare(
          `INSERT INTO prospects (
             prospect_id, brand, list_name, company_key, row_number, company,
             region, tier, source, website, linkedin_company_url,
             contact_name, contact_email, linkedin_url,
             pdf_sent, sent_date, opened, follow_up_sent,
             status, notes, created_at, updated_at
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        )
        .run(
          prospectId,
          brand,
          listName,
          companyKey,
          null,
          company,
          input.region?.trim() ?? "",
          input.tier?.trim() ?? "",
          input.source?.trim() ?? "manual",
          input.website?.trim() ?? "",
          input.linkedinCompanyUrl?.trim() ?? "",
          input.contactName?.trim() ?? "",
          input.contactEmail?.trim() ?? "",
          input.linkedinUrl?.trim() ?? "",
          "",
          "",
          "",
          "",
          input.status ?? "imported",
          input.notes?.trim() ?? "",
          now,
          now,
        );
      this.database
        .prepare(
          `INSERT INTO outreach_events (
             event_id, prospect_id, event_type, detail, occurred_at, created_at
           ) VALUES (?, ?, 'imported', ?, ?, ?)`,
        )
        .run(randomUUID(), prospectId, `Added by hand to ${listName}`, now, now);
      return {
        outcome: "added" as const,
        company,
        prospect: this.getProspect(prospectId),
      };
    });
  }

  /**
   * Move one card to a new column. A deliberate exception to the app's
   * proposal-and-confirmation rule: a status change is local, low-consequence
   * and reversible by dragging back. Every other prospect write keeps the
   * confirmation phrase.
   */
  setProspectStatus(
    prospectId: string,
    status: ProspectStatus,
    options: { closeReason?: string | undefined; detail?: string | undefined } = {},
  ): ProspectRecord | undefined {
    return this.transaction(() => {
      const row = this.database
        .prepare(`SELECT * FROM prospects WHERE prospect_id = ?`)
        .get(prospectId) as unknown as ProspectRow | undefined;
      if (row === undefined) {
        return undefined;
      }
      const now = nowIso();
      const closeReason = status === "closed"
        ? (options.closeReason ?? row.close_reason)
        : "";
      this.database
        .prepare(
          `UPDATE prospects SET status = ?, close_reason = ?, updated_at = ?
           WHERE prospect_id = ?`,
        )
        .run(status, closeReason, now, prospectId);
      if (status !== row.status) {
        const detail = options.detail
          ?? `Status ${row.status} -> ${status} (moved on the board)`;
        this.database
          .prepare(
            `INSERT INTO outreach_events (
               event_id, prospect_id, campaign_id, event_type, detail,
               occurred_at, created_at
             ) VALUES (?, ?, ?, 'status_change', ?, ?, ?)`,
          )
          .run(randomUUID(), prospectId, row.campaign_id, detail, now, now);
      }
      return this.getProspect(prospectId);
    });
  }

  listOutreachEvents(prospectId: string, limit = 50): OutreachEventRecord[] {
    const boundedLimit = Math.max(1, Math.min(limit, 200));
    const rows = this.database
      .prepare(
        `SELECT event_id, prospect_id, campaign_id, event_type, detail, occurred_at
         FROM outreach_events
         WHERE prospect_id = ?
         ORDER BY occurred_at DESC
         LIMIT ?`,
      )
      .all(prospectId, boundedLimit) as unknown as Array<{
      event_id: string;
      prospect_id: string;
      campaign_id: string | null;
      event_type: OutreachEventType;
      detail: string;
      occurred_at: string;
    }>;
    return rows.map((row) => ({
      eventId: row.event_id,
      prospectId: row.prospect_id,
      campaignId: row.campaign_id ?? undefined,
      eventType: row.event_type,
      detail: row.detail,
      occurredAt: row.occurred_at,
    }));
  }

  /**
   * Recent outreach activity across one brand. The per-prospect timeline
   * answers "what happened to this company"; this answers "what has been
   * happening at all", which is what the Outreach screen needs.
   */
  listRecentOutreachEvents(
    brand: string,
    limit = 25,
  ): Array<OutreachEventRecord & { company: string; listName: string }> {
    const boundedLimit = Math.max(1, Math.min(limit, 200));
    const rows = this.database
      .prepare(
        `SELECT e.event_id, e.prospect_id, e.campaign_id, e.event_type,
                e.detail, e.occurred_at, p.company, p.list_name
         FROM outreach_events e
         JOIN prospects p ON p.prospect_id = e.prospect_id
         WHERE p.brand = ?
         ORDER BY e.occurred_at DESC
         LIMIT ?`,
      )
      .all(brand, boundedLimit) as unknown as Array<{
      event_id: string;
      prospect_id: string;
      campaign_id: string | null;
      event_type: OutreachEventType;
      detail: string;
      occurred_at: string;
      company: string;
      list_name: string;
    }>;
    return rows.map((row) => ({
      eventId: row.event_id,
      prospectId: row.prospect_id,
      campaignId: row.campaign_id ?? undefined,
      eventType: row.event_type,
      detail: row.detail,
      occurredAt: row.occurred_at,
      company: row.company,
      listName: row.list_name,
    }));
  }

  /**
   * The do-not-contact list. This is what makes the unsubscribe line in every
   * draft a real opt-out rather than decoration: nothing is drafted to an
   * address recorded here.
   */
  addSuppression(input: {
    brand: string;
    email: string;
    companyKey?: string | undefined;
    reason: SuppressionReason;
    detail?: string | undefined;
  }): SuppressionRecord {
    const emailKey = suppressionKey(input.email);
    const now = nowIso();
    return this.transaction(() => {
      this.database
        .prepare(
          `INSERT INTO suppressions (
             suppression_id, brand, email_key, company_key, reason, detail, created_at
           ) VALUES (?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(brand, email_key) DO UPDATE SET
             reason = excluded.reason,
             detail = excluded.detail`,
        )
        .run(
          randomUUID(),
          input.brand,
          emailKey,
          input.companyKey?.trim().toLowerCase() ?? "",
          input.reason,
          input.detail?.trim() ?? "",
          now,
        );
      const row = this.database
        .prepare(
          `SELECT * FROM suppressions WHERE brand = ? AND email_key = ?`,
        )
        .get(input.brand, emailKey) as unknown as SuppressionRow;
      return {
        suppressionId: row.suppression_id,
        brand: row.brand,
        emailKey: row.email_key,
        companyKey: row.company_key,
        reason: row.reason,
        detail: row.detail,
        createdAt: row.created_at,
      };
    });
  }

  removeSuppression(brand: string, email: string): boolean {
    const result = this.database
      .prepare(`DELETE FROM suppressions WHERE brand = ? AND email_key = ?`)
      .run(brand, suppressionKey(email));
    return result.changes > 0;
  }

  listSuppressions(brand?: string): SuppressionRecord[] {
    const where = brand === undefined ? "" : "WHERE brand = ?";
    const parameters = brand === undefined ? [] : [brand];
    const rows = this.database
      .prepare(
        `SELECT * FROM suppressions ${where} ORDER BY created_at DESC LIMIT 500`,
      )
      .all(...parameters) as unknown as SuppressionRow[];
    return rows.map((row) => ({
      suppressionId: row.suppression_id,
      brand: row.brand,
      emailKey: row.email_key,
      companyKey: row.company_key,
      reason: row.reason,
      detail: row.detail,
      createdAt: row.created_at,
    }));
  }

  /**
   * Which of these addresses must not be contacted. Returns the matching
   * keys so the caller can report every skipped prospect by name rather than
   * dropping them quietly.
   */
  suppressedEmails(brand: string, emails: readonly string[]): Set<string> {
    const keys = emails
      .map((email) => suppressionKey(email))
      .filter((key) => key.length > 0);
    if (keys.length === 0) {
      return new Set();
    }
    const placeholders = keys.map(() => "?").join(", ");
    const rows = this.database
      .prepare(
        `SELECT email_key FROM suppressions
         WHERE brand = ? AND email_key IN (${placeholders})`,
      )
      .all(brand, ...keys) as unknown as Array<{ email_key: string }>;
    return new Set(rows.map((row) => row.email_key));
  }

  // ---- Outreach settings, campaigns and drafting -------------------------

  saveOutreachSettings(
    brand: string,
    input: OutreachSettingsInput,
  ): OutreachSettingsRecord {
    const now = nowIso();
    const dailyCap = clampWholeNumber(input.dailyCap, 20, 1, 200);
    const followUpDays = clampWholeNumber(input.followUpDays, 7, 1, 90);
    this.database
      .prepare(
        `INSERT INTO outreach_settings (
           brand, sender_name, sender_contact, unsubscribe_line,
           daily_cap, follow_up_days, guide_page_url, updated_at
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(brand) DO UPDATE SET
           sender_name = excluded.sender_name,
           sender_contact = excluded.sender_contact,
           unsubscribe_line = excluded.unsubscribe_line,
           daily_cap = excluded.daily_cap,
           follow_up_days = excluded.follow_up_days,
           guide_page_url = excluded.guide_page_url,
           updated_at = excluded.updated_at`,
      )
      .run(
        brand,
        input.senderName.trim(),
        input.senderContact.trim(),
        input.unsubscribeLine.trim(),
        dailyCap,
        followUpDays,
        input.guidePageUrl?.trim() ?? "",
        now,
      );
    return this.getOutreachSettings(brand)!;
  }

  getOutreachSettings(brand: string): OutreachSettingsRecord | undefined {
    const row = this.database
      .prepare(`SELECT * FROM outreach_settings WHERE brand = ?`)
      .get(brand) as unknown as
      | {
          brand: string;
          sender_name: string;
          sender_contact: string;
          unsubscribe_line: string;
          daily_cap: number;
          follow_up_days: number;
          guide_page_url: string;
          updated_at: string;
        }
      | undefined;
    if (row === undefined) {
      return undefined;
    }
    return {
      brand: row.brand,
      senderName: row.sender_name,
      senderContact: row.sender_contact,
      unsubscribeLine: row.unsubscribe_line,
      dailyCap: row.daily_cap,
      followUpDays: row.follow_up_days,
      guidePageUrl: row.guide_page_url,
      updatedAt: row.updated_at,
    };
  }

  createCampaign(
    brand: string,
    name: string,
    brief: CampaignBrief,
  ): CampaignRecord {
    const now = nowIso();
    const campaignId = randomUUID();
    this.database
      .prepare(
        `INSERT INTO campaigns (
           campaign_id, brand, name, status, brief_json, created_at, updated_at
         ) VALUES (?, ?, ?, 'active', ?, ?, ?)`,
      )
      .run(campaignId, brand, name.trim(), JSON.stringify(brief), now, now);
    return this.getCampaign(campaignId)!;
  }

  getCampaign(campaignId: string): CampaignRecord | undefined {
    const row = this.database
      .prepare(`SELECT * FROM campaigns WHERE campaign_id = ?`)
      .get(campaignId) as unknown as
      | {
          campaign_id: string;
          brand: string;
          name: string;
          status: "draft" | "active" | "completed";
          brief_json: string;
          created_at: string;
          updated_at: string;
        }
      | undefined;
    if (row === undefined) {
      return undefined;
    }
    let brief: CampaignBrief = { offer: "", guidePageUrl: "", utmCampaign: "" };
    try {
      const parsed = JSON.parse(row.brief_json) as Partial<CampaignBrief>;
      brief = {
        offer: typeof parsed.offer === "string" ? parsed.offer : "",
        guidePageUrl:
          typeof parsed.guidePageUrl === "string" ? parsed.guidePageUrl : "",
        utmCampaign:
          typeof parsed.utmCampaign === "string" ? parsed.utmCampaign : "",
        dailyCap:
          typeof parsed.dailyCap === "number" ? parsed.dailyCap : undefined,
        followUpDays:
          typeof parsed.followUpDays === "number"
            ? parsed.followUpDays
            : undefined,
      };
    } catch {
      // A malformed brief falls back to the brand defaults rather than
      // taking the whole drafting run down.
    }
    return {
      campaignId: row.campaign_id,
      brand: row.brand,
      name: row.name,
      status: row.status,
      brief,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    };
  }

  /**
   * Who may be drafted to right now, and — just as important — who may not
   * and why. The guardrails live here rather than in the skill so that a
   * model cannot talk its way past a suppression, a missing address or the
   * daily cap.
   */
  draftableProspects(
    brand: string,
    options: {
      campaignId?: string | undefined;
      listName?: string | undefined;
      limit?: number | undefined;
    } = {},
  ): DraftableResult {
    const settings = this.getOutreachSettings(brand);
    if (settings === undefined) {
      throw new OutreachNotConfiguredError(
        `No outreach settings for ${brand}. Set the sender name, contact and unsubscribe line before drafting anything.`,
      );
    }
    const campaign = options.campaignId === undefined
      ? undefined
      : this.getCampaign(options.campaignId);
    if (options.campaignId !== undefined && campaign === undefined) {
      throw new OutreachNotConfiguredError("That campaign does not exist.");
    }
    if (campaign !== undefined && campaign.brand !== brand) {
      throw new OutreachNotConfiguredError(
        "That campaign belongs to the other brand.",
      );
    }

    const dailyCap = campaign?.brief.dailyCap ?? settings.dailyCap;
    const draftedToday = this.countDraftedToday(brand);
    const remainingToday = Math.max(0, dailyCap - draftedToday);

    const guidePageUrl =
      campaign?.brief.guidePageUrl || settings.guidePageUrl;
    const utmCampaign = campaign?.brief.utmCampaign || "outreach";

    const conditions = ["brand = ?"];
    const parameters: string[] = [brand];
    if (options.listName !== undefined) {
      conditions.push("list_name = ?");
      parameters.push(options.listName);
    }
    const rows = this.database
      .prepare(
        `SELECT * FROM prospects WHERE ${conditions.join(" AND ")}
         ORDER BY
           CASE WHEN tier = '' THEN 99 ELSE CAST(tier AS INTEGER) END ASC,
           company ASC`,
      )
      .all(...parameters) as unknown as ProspectRow[];
    const prospects = rows.map(prospectFromRow);

    const suppressed = this.suppressedEmails(
      brand,
      prospects.map((prospect) => prospect.contactEmail),
    );

    const eligible: DraftCandidate[] = [];
    const skipped: DraftSkip[] = [];
    const requestedLimit = clampWholeNumber(options.limit, remainingToday, 0, 500);
    const allowance = Math.min(remainingToday, requestedLimit);

    for (const prospect of prospects) {
      const skip = (reason: string) => {
        skipped.push({
          prospectId: prospect.prospectId,
          company: prospect.company,
          reason,
        });
      };
      if (!["imported", "needs_review", "enriched"].includes(prospect.status)) {
        skip(`already ${prospect.status.replaceAll("_", " ")}`);
        continue;
      }
      if (prospect.draftId !== "") {
        skip("a draft already exists for this prospect");
        continue;
      }
      if (prospect.contactEmail === "") {
        skip("no contact email — enrich or fill it first");
        continue;
      }
      if (suppressed.has(suppressionKey(prospect.contactEmail))) {
        skip("on the do-not-contact list");
        continue;
      }
      if (eligible.length >= allowance) {
        skip(
          remainingToday === 0
            ? `today's cap of ${dailyCap} is already used`
            : "over the number asked for in this run",
        );
        continue;
      }
      eligible.push({
        prospect,
        outreachUrl: buildOutreachUrl(
          guidePageUrl,
          utmCampaign,
          prospect.prospectId,
        ),
        warning:
          prospect.status === "needs_review"
            ? `Enrichment flagged this contact${prospect.flagReason ? `: ${prospect.flagReason}` : ""}. Check it before you send.`
            : "",
      });
    }

    return {
      brand,
      settings,
      campaign,
      eligible,
      skipped,
      dailyCap,
      draftedToday,
      remainingToday,
    };
  }

  /**
   * The last gate before a draft is created in Gmail. Deterministic and
   * server-side, so the unsubscribe line cannot go missing because a model
   * decided the email read better without it.
   */
  validateDrafts(
    brand: string,
    drafts: readonly DraftToValidate[],
  ): DraftValidation[] {
    const settings = this.getOutreachSettings(brand);
    if (settings === undefined) {
      throw new OutreachNotConfiguredError(
        `No outreach settings for ${brand}. Set the sender name, contact and unsubscribe line before drafting anything.`,
      );
    }
    const remaining = Math.max(
      0,
      settings.dailyCap - this.countDraftedToday(brand),
    );
    const results: DraftValidation[] = [];
    let approvedSoFar = 0;

    for (const draft of drafts) {
      const reasons: string[] = [];
      const warnings: string[] = [];
      const prospect = this.getProspect(draft.prospectId);

      if (prospect === undefined || prospect.brand !== brand) {
        results.push({
          prospectId: draft.prospectId,
          company: "",
          approved: false,
          reasons: ["that prospect is not on this brand's board"],
          warnings: [],
        });
        continue;
      }
      if (!["imported", "needs_review", "enriched"].includes(prospect.status)) {
        reasons.push(`already ${prospect.status.replaceAll("_", " ")}`);
      }
      if (prospect.draftId !== "") {
        reasons.push("a draft already exists for this prospect");
      }
      if (prospect.contactEmail === "") {
        reasons.push("no contact email");
      } else if (
        this.suppressedEmails(brand, [prospect.contactEmail]).size > 0
      ) {
        reasons.push("on the do-not-contact list");
      }
      if (draft.subject.trim() === "") {
        reasons.push("no subject line");
      }
      if (!containsNormalised(draft.body, settings.unsubscribeLine)) {
        reasons.push("the unsubscribe line is missing from the body");
      }
      if (!containsNormalised(draft.body, settings.senderName)) {
        reasons.push("the sender is not identified in the body");
      }
      if (
        settings.guidePageUrl !== "" &&
        !draft.body.includes(`utm_content=${prospect.prospectId}`)
      ) {
        warnings.push(
          "the body has no guide-page link tagged for this prospect, so a click will not be attributable",
        );
      }
      if (prospect.status === "needs_review") {
        warnings.push(
          `enrichment flagged this contact${prospect.flagReason ? `: ${prospect.flagReason}` : ""}`,
        );
      }
      if (reasons.length === 0 && approvedSoFar >= remaining) {
        reasons.push(
          `over today's cap of ${settings.dailyCap} (${remaining} left when this run started)`,
        );
      }
      const approved = reasons.length === 0;
      if (approved) {
        approvedSoFar += 1;
      }
      results.push({
        prospectId: draft.prospectId,
        company: prospect.company,
        approved,
        reasons,
        warnings,
      });
    }
    return results;
  }

  listProspectListMeta(brand: string): ProspectListRecord[] {
    const rows = this.database
      .prepare(
        `SELECT * FROM prospect_lists WHERE brand = ? ORDER BY list_name ASC`,
      )
      .all(brand) as unknown as Array<{
      brand: string;
      list_name: string;
      description: string;
      created_at: string;
      updated_at: string;
    }>;
    return rows.map((row) => ({
      brand: row.brand,
      listName: row.list_name,
      description: row.description,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    }));
  }

  saveProspectListMeta(
    brand: string,
    listName: string,
    description: string,
  ): ProspectListRecord {
    const now = nowIso();
    this.database
      .prepare(
        `INSERT INTO prospect_lists (brand, list_name, description, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?)
         ON CONFLICT(brand, list_name) DO UPDATE SET
           description = excluded.description,
           updated_at = excluded.updated_at`,
      )
      .run(brand, listName, description.trim(), now, now);
    return this.listProspectListMeta(brand).find(
      (record) => record.listName === listName,
    )!;
  }

  /**
   * Composed-but-not-yet-created drafts. Kept in the store rather than in
   * the page so a half-written batch survives a reload or a wander to
   * another screen — losing ten hand-edited emails would be the worst part
   * of this flow.
   */
  savePreparedDrafts(
    brand: string,
    drafts: ReadonlyArray<{
      prospectId: string;
      subject: string;
      body: string;
      hook?: string | undefined;
      hookEvidence?: string | undefined;
      state?: DraftState | undefined;
      campaignId?: string | undefined;
    }>,
  ): PreparedDraftRecord[] {
    const now = nowIso();
    this.transaction(() => {
      const upsert = this.database.prepare(
        `INSERT INTO outreach_drafts (
           draft_row_id, brand, prospect_id, campaign_id, subject, body,
           hook, hook_evidence, state, created_at, updated_at
         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(prospect_id) DO UPDATE SET
           subject = excluded.subject,
           body = excluded.body,
           hook = excluded.hook,
           hook_evidence = excluded.hook_evidence,
           state = excluded.state,
           campaign_id = excluded.campaign_id,
           updated_at = excluded.updated_at`,
      );
      for (const draft of drafts) {
        upsert.run(
          randomUUID(),
          brand,
          draft.prospectId,
          draft.campaignId ?? null,
          draft.subject,
          draft.body,
          draft.hook ?? "",
          draft.hookEvidence ?? "",
          draft.state ?? "composing",
          now,
          now,
        );
      }
    });
    return this.listPreparedDrafts(brand);
  }

  listPreparedDrafts(brand: string, state?: DraftState): PreparedDraftRecord[] {
    const where = state === undefined
      ? "WHERE brand = ? AND state <> 'discarded'"
      : "WHERE brand = ? AND state = ?";
    const parameters = state === undefined ? [brand] : [brand, state];
    const rows = this.database
      .prepare(`SELECT * FROM outreach_drafts ${where} ORDER BY updated_at DESC`)
      .all(...parameters) as unknown as Array<{
      draft_row_id: string; brand: string; prospect_id: string;
      campaign_id: string | null; subject: string; body: string;
      hook: string; hook_evidence: string; state: DraftState;
      created_at: string; updated_at: string;
    }>;
    return rows.map((row) => ({
      draftRowId: row.draft_row_id,
      brand: row.brand,
      prospectId: row.prospect_id,
      campaignId: row.campaign_id ?? undefined,
      subject: row.subject,
      body: row.body,
      hook: row.hook,
      hookEvidence: row.hook_evidence,
      state: row.state,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    }));
  }

  discardPreparedDraft(brand: string, prospectId: string): boolean {
    const result = this.database
      .prepare(
        `DELETE FROM outreach_drafts WHERE brand = ? AND prospect_id = ?`,
      )
      .run(brand, prospectId);
    return result.changes > 0;
  }

  countDraftedToday(brand: string): number {
    const today = nowIso().slice(0, 10);
    const row = this.database
      .prepare(
        `SELECT COUNT(*) AS drafted FROM prospects
         WHERE brand = ? AND substr(drafted_at, 1, 10) = ?`,
      )
      .get(brand, today) as { drafted: number } | undefined;
    return row?.drafted ?? 0;
  }

  /**
   * Record drafts the agent has created in Gmail. Suppression is re-checked
   * here as well as in draftableProspects — the list can change between
   * reading the candidates and writing the result.
   */
  recordProspectDrafts(
    brand: string,
    entries: readonly RecordedDraftInput[],
    campaignId?: string,
  ): RecordedDraftResult[] {
    const settings = this.getOutreachSettings(brand);
    if (settings === undefined) {
      throw new OutreachNotConfiguredError(
        `No outreach settings for ${brand}.`,
      );
    }
    const campaign = campaignId === undefined
      ? undefined
      : this.getCampaign(campaignId);
    const followUpDays = campaign?.brief.followUpDays ?? settings.followUpDays;
    const now = nowIso();
    const followUpDue = addDaysIso(now, followUpDays);
    const results: RecordedDraftResult[] = [];

    this.transaction(() => {
      for (const entry of entries) {
        const row = this.database
          .prepare(
            `SELECT * FROM prospects WHERE prospect_id = ? AND brand = ?`,
          )
          .get(entry.prospectId, brand) as unknown as ProspectRow | undefined;
        if (row === undefined) {
          results.push({
            prospectId: entry.prospectId,
            company: "",
            outcome: "not_found",
            followUpDue: "",
          });
          continue;
        }
        if (
          this.suppressedEmails(brand, [row.contact_email]).size > 0
        ) {
          results.push({
            prospectId: entry.prospectId,
            company: row.company,
            outcome: "suppressed",
            followUpDue: "",
          });
          continue;
        }
        this.database
          .prepare(
            `UPDATE prospects SET
               draft_id = ?, drafted_at = ?, hook = ?, hook_evidence = ?,
               follow_up_due = ?, status = 'emailed', campaign_id = ?,
               updated_at = ?
             WHERE prospect_id = ?`,
          )
          .run(
            entry.draftId.trim(),
            now,
            entry.hook?.trim() ?? "",
            entry.hookEvidence?.trim() ?? "",
            followUpDue,
            campaignId ?? row.campaign_id,
            now,
            entry.prospectId,
          );
        this.database
          .prepare(
            `INSERT INTO outreach_events (
               event_id, prospect_id, campaign_id, event_type, detail,
               occurred_at, created_at
             ) VALUES (?, ?, ?, 'emailed', ?, ?, ?)`,
          )
          .run(
            randomUUID(),
            entry.prospectId,
            campaignId ?? row.campaign_id,
            `Gmail draft prepared${entry.hook ? ` — hook: ${entry.hook}` : ""}`,
            now,
            now,
          );
        results.push({
          prospectId: entry.prospectId,
          company: row.company,
          outcome: "recorded",
          followUpDue,
        });
      }
    });
    return results;
  }

  prepareArticleBrief(
    sessionId: string,
    domain: string,
    researchKey: string,
    data: ArticleBriefData,
  ): ArticleBriefRecord {
    return this.transaction(() => {
      const existing = this.database
        .prepare(
          `SELECT * FROM seo_article_briefs
           WHERE session_id = ? AND domain = ? AND research_key = ?`,
        )
        .get(sessionId, domain, researchKey) as ArticleBriefRow | undefined;
      if (existing !== undefined && !["complete", "failed"].includes(existing.status)) {
        return articleBriefFromRow(existing);
      }
      const timestamp = nowIso();
      const briefId = existing?.brief_id ?? `brief-${randomUUID()}`;
      const createdAt = existing?.created_at ?? timestamp;
      this.database
        .prepare(
          `INSERT INTO seo_article_briefs(
             brief_id, session_id, domain, research_key, status,
             brief_json, created_at, updated_at
           ) VALUES (?, ?, ?, ?, 'choosing', ?, ?, ?)
           ON CONFLICT(session_id, domain, research_key) DO UPDATE SET
             status = 'choosing', brief_json = excluded.brief_json,
             updated_at = excluded.updated_at`,
        )
        .run(
          briefId,
          sessionId,
          domain,
          researchKey,
          JSON.stringify(data),
          createdAt,
          timestamp,
        );
      const stored = this.getArticleBrief(sessionId, briefId);
      if (stored === undefined) throw new Error("Stored article brief could not be read");
      return stored;
    });
  }

  getArticleBrief(sessionId: string, briefId: string): ArticleBriefRecord | undefined {
    const row = this.database
      .prepare("SELECT * FROM seo_article_briefs WHERE brief_id = ? AND session_id = ?")
      .get(briefId, sessionId) as ArticleBriefRow | undefined;
    return row === undefined ? undefined : articleBriefFromRow(row);
  }

  getLatestArticleBrief(
    sessionId: string,
    domain?: string,
  ): ArticleBriefRecord | undefined {
    const row = (domain === undefined
      ? this.database
          .prepare(
            `SELECT * FROM seo_article_briefs
             WHERE session_id = ? ORDER BY updated_at DESC LIMIT 1`,
          )
          .get(sessionId)
      : this.database
          .prepare(
            `SELECT * FROM seo_article_briefs
             WHERE session_id = ? AND domain = ? ORDER BY updated_at DESC LIMIT 1`,
          )
          .get(sessionId, domain)) as ArticleBriefRow | undefined;
    return row === undefined ? undefined : articleBriefFromRow(row);
  }

  updateArticleBrief(
    sessionId: string,
    briefId: string,
    update: {
      status: ArticleBriefStatus;
      selection?: ArticleOpportunity;
      context?: ArticleBusinessContext;
      missingFields?: string[];
      linkedJobId?: string;
    },
  ): ArticleBriefRecord {
    return this.transaction(() => {
      const current = this.getArticleBrief(sessionId, briefId);
      if (current === undefined) {
        throw new Error("Article brief is not registered to this conversation");
      }
      const selection = update.selection ?? current.selection;
      const linkedJobId = update.linkedJobId ?? current.linkedJobId;
      const data: ArticleBriefData = {
        schemaVersion: 1,
        research: current.research,
        opportunities: current.opportunities,
        context: update.context ?? current.context,
        missingFields: update.missingFields ?? current.missingFields,
        ...(selection === undefined ? {} : { selection }),
        ...(linkedJobId === undefined ? {} : { linkedJobId }),
      };
      this.database
        .prepare(
          `UPDATE seo_article_briefs
           SET status = ?, brief_json = ?, updated_at = ?
           WHERE brief_id = ? AND session_id = ?`,
        )
        .run(update.status, JSON.stringify(data), nowIso(), briefId, sessionId);
      const stored = this.getArticleBrief(sessionId, briefId);
      if (stored === undefined) throw new Error("Updated article brief could not be read");
      return stored;
    });
  }

  registerSeoArticleJob(input: SeoArticleJobInput): {
    job: SeoArticleJobRecord;
    created: boolean;
  } {
    return this.transaction(() => {
      const existing = this.database
        .prepare("SELECT * FROM seo_article_jobs WHERE session_id = ? AND request_id = ?")
        .get(input.sessionId, input.requestId) as SeoArticleJobRow | undefined;
      if (existing !== undefined) {
        if (
          existing.domain !== input.domain ||
          (existing.brief_id ?? "") !== input.briefId ||
          existing.primary_keyword !== input.primaryKeyword ||
          existing.supporting_keywords_json !== JSON.stringify(input.supportingKeywords)
        ) {
          throw new Error("The article request ID is already used for different inputs");
        }
        if (input.briefId) {
          const brief = this.getArticleBrief(input.sessionId, input.briefId);
          if (brief !== undefined) {
            const data: ArticleBriefData = {
              schemaVersion: 1,
              research: brief.research,
              opportunities: brief.opportunities,
              context: brief.context,
              missingFields: [],
              ...(brief.selection === undefined ? {} : { selection: brief.selection }),
              linkedJobId: existing.job_id,
            };
            this.database
              .prepare(
                `UPDATE seo_article_briefs
                 SET status = 'writing', brief_json = ?, updated_at = ?
                 WHERE brief_id = ? AND session_id = ?`,
              )
              .run(
                JSON.stringify(data),
                nowIso(),
                input.briefId,
                input.sessionId,
              );
          }
        }
        return { job: seoArticleJobFromRow(existing), created: false };
      }
      const timestamp = nowIso();
      const jobId = `article-${randomUUID()}`;
      this.database
        .prepare(
          `INSERT INTO seo_article_jobs(
             job_id, session_id, request_id, domain, brief_id, primary_keyword,
             supporting_keywords_json, input_json, status, stage,
             created_at, updated_at
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'queued', 'queued', ?, ?)`,
        )
        .run(
          jobId,
          input.sessionId,
          input.requestId,
          input.domain,
          input.briefId || null,
          input.primaryKeyword,
          JSON.stringify(input.supportingKeywords),
          JSON.stringify(input.input),
          timestamp,
          timestamp,
        );
      if (input.briefId) {
        const brief = this.getArticleBrief(input.sessionId, input.briefId);
        if (brief === undefined || brief.domain !== input.domain) {
          throw new Error("Article brief is not registered to this conversation");
        }
        const data: ArticleBriefData = {
          schemaVersion: 1,
          research: brief.research,
          opportunities: brief.opportunities,
          context: brief.context,
          missingFields: [],
          ...(brief.selection === undefined ? {} : { selection: brief.selection }),
          linkedJobId: jobId,
        };
        this.database
          .prepare(
            `UPDATE seo_article_briefs
             SET status = 'writing', brief_json = ?, updated_at = ?
             WHERE brief_id = ? AND session_id = ?`,
          )
          .run(JSON.stringify(data), timestamp, input.briefId, input.sessionId);
      }
      const stored = this.getSeoArticleJob(input.sessionId, jobId);
      if (stored === undefined) throw new Error("Stored article job could not be read");
      return { job: stored, created: true };
    });
  }

  updateSeoArticleJob(
    sessionId: string,
    jobId: string,
    update: {
      status: SeoArticleJobStatus;
      stage: string;
      errorCode?: string;
      errorMessage?: string;
    },
  ): SeoArticleJobRecord {
    const result = this.database
      .prepare(
        `UPDATE seo_article_jobs
         SET status = ?, stage = ?, error_code = ?, error_message = ?, updated_at = ?
         WHERE job_id = ? AND session_id = ?`,
      )
      .run(
        update.status,
        update.stage,
        update.errorCode ?? null,
        update.errorMessage ?? null,
        nowIso(),
        jobId,
        sessionId,
      );
    if (Number(result.changes) !== 1) throw new Error("Article job is not registered to this conversation");
    const stored = this.getSeoArticleJob(sessionId, jobId);
    if (stored === undefined) throw new Error("Updated article job could not be read");
    if (
      stored.briefId &&
      (update.status === "failed" || update.status === "interrupted")
    ) {
      this.updateArticleBrief(sessionId, stored.briefId, { status: "failed" });
    }
    return stored;
  }

  getSeoArticleJob(sessionId: string, jobId: string): SeoArticleJobRecord | undefined {
    const row = this.database
      .prepare("SELECT * FROM seo_article_jobs WHERE job_id = ? AND session_id = ?")
      .get(jobId, sessionId) as SeoArticleJobRow | undefined;
    return row === undefined ? undefined : seoArticleJobFromRow(row);
  }

  getLatestSeoArticleJob(sessionId: string, domain: string): SeoArticleJobRecord | undefined {
    const row = this.database
      .prepare(
        `SELECT * FROM seo_article_jobs
         WHERE session_id = ? AND domain = ?
         ORDER BY updated_at DESC LIMIT 1`,
      )
      .get(sessionId, domain) as SeoArticleJobRow | undefined;
    return row === undefined ? undefined : seoArticleJobFromRow(row);
  }

  saveSeoArticleVersion(
    sessionId: string,
    jobId: string,
    input: SeoArticleVersionInput,
  ): { job: SeoArticleJobRecord; version: SeoArticleVersionRecord } {
    return this.transaction(() => {
      const job = this.database
        .prepare("SELECT * FROM seo_article_jobs WHERE job_id = ? AND session_id = ?")
        .get(jobId, sessionId) as SeoArticleJobRow | undefined;
      if (job === undefined) throw new Error("Article job is not registered to this conversation");
      if (job.domain !== input.domain || job.primary_keyword !== input.primaryKeyword) {
        throw new Error("Article result does not match the registered request");
      }
      const numberRow = this.database
        .prepare("SELECT COALESCE(MAX(version_number), 0) + 1 AS next_number FROM seo_article_versions WHERE job_id = ?")
        .get(jobId) as { next_number: number };
      const versionId = randomUUID();
      const timestamp = nowIso();
      const downloadToken = randomBytes(32).toString("base64url");
      this.database
        .prepare(
          `INSERT INTO seo_article_versions(
             version_id, job_id, version_number, parent_version_id, status,
             domain, primary_keyword, supporting_keywords_json, context_json,
             plan_json, markdown, structured_data_json, metadata_json,
             answer_blocks_json, faq_json, sources_json, claim_ledger_json,
             quality_report_json, warnings_json, review_status, model,
             download_token, created_at
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        )
        .run(
          versionId,
          jobId,
          Number(numberRow.next_number),
          job.latest_version_id,
          input.status,
          input.domain,
          input.primaryKeyword,
          JSON.stringify(input.supportingKeywords),
          JSON.stringify(input.context),
          JSON.stringify(input.plan),
          input.markdown,
          JSON.stringify(input.structuredData),
          JSON.stringify(input.metadata),
          JSON.stringify(input.answerBlocks),
          JSON.stringify(input.faq),
          JSON.stringify(input.sources),
          JSON.stringify(input.claimLedger),
          JSON.stringify(input.qualityReport),
          JSON.stringify(input.warnings),
          input.reviewStatus,
          input.model,
          downloadToken,
          timestamp,
        );
      this.database
        .prepare(
          `UPDATE seo_article_jobs
           SET status = ?, stage = 'ready_for_review', error_code = NULL,
               error_message = NULL, latest_version_id = ?, updated_at = ?
           WHERE job_id = ? AND session_id = ?`,
        )
        .run(input.status, versionId, timestamp, jobId, sessionId);
      if (job.brief_id !== null) {
        this.database
          .prepare(
            `UPDATE seo_article_briefs
             SET status = 'complete', updated_at = ?
             WHERE brief_id = ? AND session_id = ?`,
          )
          .run(timestamp, job.brief_id, sessionId);
      }
      const storedJob = this.getSeoArticleJob(sessionId, jobId);
      const version = this.getSeoArticleVersionForJob(sessionId, jobId, versionId);
      if (storedJob === undefined || version === undefined) {
        throw new Error("Stored article version could not be read");
      }
      return { job: storedJob, version };
    });
  }

  getSeoArticleVersionForJob(
    sessionId: string,
    jobId: string,
    versionId?: string,
  ): SeoArticleVersionRecord | undefined {
    const row = this.database
      .prepare(
        `SELECT v.* FROM seo_article_versions v
         JOIN seo_article_jobs j ON j.job_id = v.job_id
         WHERE j.session_id = ? AND v.job_id = ?
           AND (? IS NULL OR v.version_id = ?)
         ORDER BY v.version_number DESC LIMIT 1`,
      )
      .get(sessionId, jobId, versionId ?? null, versionId ?? null) as SeoArticleVersionRow | undefined;
    return row === undefined ? undefined : seoArticleVersionFromRow(row);
  }

  getSeoArticleVersionByDownloadToken(token: string): SeoArticleVersionRecord | undefined {
    const row = this.database
      .prepare("SELECT * FROM seo_article_versions WHERE download_token = ?")
      .get(token) as SeoArticleVersionRow | undefined;
    return row === undefined ? undefined : seoArticleVersionFromRow(row);
  }

  getLatestSuccessfulSeoArticleVersion(
    sessionId: string,
    domain: string,
  ): SeoArticleVersionRecord | undefined {
    const row = this.database
      .prepare(
        `SELECT v.* FROM seo_article_versions v
         JOIN seo_article_jobs j ON j.job_id = v.job_id
         WHERE j.session_id = ? AND v.domain = ?
         ORDER BY v.created_at DESC LIMIT 1`,
      )
      .get(sessionId, domain) as SeoArticleVersionRow | undefined;
    return row === undefined ? undefined : seoArticleVersionFromRow(row);
  }

  markPendingInterrupted(): number {
    return this.transaction(() => {
      const messages = this.database
        .prepare(
          `UPDATE messages
           SET status = 'interrupted', error_code = 'REQUEST_INTERRUPTED'
           WHERE status = 'pending'`,
        )
        .run();
      this.database
        .prepare(
          `UPDATE seo_article_jobs
           SET status = 'interrupted', stage = 'interrupted',
               error_code = 'WORKER_INTERRUPTED',
               error_message = 'The article worker stopped before it finished.',
               updated_at = ?
           WHERE status IN ('queued', 'running')`,
        )
        .run(nowIso());
      this.database
        .prepare(
          `UPDATE seo_article_briefs
           SET status = 'failed', updated_at = ?
           WHERE status = 'writing'`,
        )
        .run(nowIso());
      return Number(messages.changes);
    });
  }

  health(): { schemaVersion: number; quickCheck: string } {
    const version = this.database.prepare("PRAGMA user_version").get() as {
      user_version: number;
    };
    const check = this.database.prepare("PRAGMA quick_check").get() as {
      quick_check: string;
    };
    return {
      schemaVersion: Number(version.user_version),
      quickCheck: String(check.quick_check),
    };
  }

  close(): void {
    if (this.closed) {
      return;
    }
    this.database.exec("PRAGMA wal_checkpoint(TRUNCATE)");
    this.database.close();
    this.closed = true;
  }
}
