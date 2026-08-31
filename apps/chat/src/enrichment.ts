// Contact enrichment via the harvestapi LinkedIn actor on Apify.
//
// Two hard-won rules are encoded here:
//
// 1. `maxItems` is REQUIRED. Without it (or `takePages`) the actor logs a
//    warning, exits SUCCEEDED with zero items and a "no limits" status, and
//    charges almost nothing — a silent no-op that reads as "no profiles
//    returned" for every company. That failure ran unnoticed for weeks.
//
// 2. Contacts are picked deterministically, never by a model. Everything
//    written back must be present in the scraped payload, so an address
//    cannot be invented or pattern-guessed into the store.

const ACTOR = "harvestapi~linkedin-company-employees";
const API = "https://api.apify.com/v2";

export interface EnrichmentTarget {
  prospectId: string;
  company: string;
  linkedinCompanyUrl: string;
}

export interface EnrichmentFinding {
  prospectId: string;
  company: string;
  contactName: string;
  contactEmail: string;
  linkedinUrl: string;
  jobTitle: string;
  confidence: "high" | "medium" | "low" | "none";
  flagReason: string;
}

export class EnrichmentUnavailableError extends Error {}

const JOB_TITLES = [
  "Marketing", "Business Development", "Partnerships",
  "Creative Director", "Production",
];

/** Roles worth reaching first, best last so a higher index wins. */
const ROLE_PRIORITY = [
  "producer", "creative director", "marketing",
  "partnership", "business development",
];

function roleScore(title: string): number {
  const lower = title.toLowerCase();
  let score = 0;
  ROLE_PRIORITY.forEach((needle, index) => {
    if (lower.includes(needle)) {
      score = Math.max(score, index + 1);
    }
  });
  return score;
}

interface ScrapedEmail {
  email?: string;
  status?: string;
  deliverable?: boolean;
  catchAllDomain?: boolean;
  qualityScore?: number;
  foundInLinkedInProfile?: boolean;
}

interface ScrapedProfile {
  firstName?: string;
  lastName?: string;
  headline?: string;
  linkedinUrl?: string;
  emails?: ScrapedEmail[] | null;
  currentPosition?: Array<{
    position?: string;
    companyName?: string;
    companyLinkedinUrl?: string;
    companyUniversalName?: string;
  }>;
}

/**
 * Rate one scraped address. A catch-all domain accepts anything, so a hit
 * there is pattern-derived and unverifiable — it must never be reported as
 * a confirmed find.
 */
function rateEmail(entry: ScrapedEmail): {
  confidence: EnrichmentFinding["confidence"];
  flagReason: string;
} {
  if (typeof entry.email !== "string" || entry.email === "") {
    return { confidence: "none", flagReason: "No address found." };
  }
  if (entry.foundInLinkedInProfile === true) {
    return { confidence: "high", flagReason: "" };
  }
  if (entry.status === "valid" && entry.deliverable === true && entry.catchAllDomain !== true) {
    return { confidence: "high", flagReason: "" };
  }
  if (entry.catchAllDomain === true) {
    return {
      confidence: "low",
      flagReason: `Catch-all domain (status ${entry.status ?? "unknown"}, quality ${entry.qualityScore ?? "?"}) — the address is pattern-derived and cannot be verified.`,
    };
  }
  return {
    confidence: "medium",
    flagReason: `Address status ${entry.status ?? "unknown"}, quality ${entry.qualityScore ?? "?"} — check before sending.`,
  };
}

function matchesCompany(profile: ScrapedProfile, target: EnrichmentTarget): boolean {
  const slug = target.linkedinCompanyUrl
    .replace(/\/+$/, "")
    .split("/")
    .pop()!
    .toLowerCase();
  return (profile.currentPosition ?? []).some((position) => {
    const url = (position.companyLinkedinUrl ?? "").toLowerCase();
    const universal = (position.companyUniversalName ?? "").toLowerCase();
    return url.includes(slug) || universal === slug;
  });
}

async function apify(
  path: string,
  token: string,
  init?: { method?: string; body?: string },
): Promise<unknown> {
  const response = await fetch(`${API}${path}`, {
    method: init?.method ?? "GET",
    headers: {
      Authorization: `Bearer ${token}`,
      ...(init?.body ? { "Content-Type": "application/json" } : {}),
    },
    ...(init?.body ? { body: init.body } : {}),
  });
  if (!response.ok) {
    throw new EnrichmentUnavailableError(
      `Apify returned ${response.status}. Check the APIFY_TOKEN in the app's .env.`,
    );
  }
  return response.json();
}

export function enrichmentCostUsd(companyCount: number, perCompany = 3): number {
  // Actor start fee per company (one_by_one) plus full-profile-with-email.
  return Number((companyCount * (0.02 + perCompany * 0.012)).toFixed(2));
}

export async function runEnrichment(
  targets: readonly EnrichmentTarget[],
  options: {
    token: string | undefined;
    perCompany?: number;
    pollMs?: number;
    maxWaitMs?: number;
    now?: () => number;
  },
): Promise<{ findings: EnrichmentFinding[]; runId: string; costUsd: number }> {
  if (!options.token) {
    throw new EnrichmentUnavailableError(
      "No APIFY_TOKEN in the app's environment. Add it to .env and restart, and this will run from here.",
    );
  }
  if (targets.length === 0) {
    throw new EnrichmentUnavailableError("Nothing selected to enrich.");
  }
  const perCompany = options.perCompany ?? 3;
  const costCap = Math.max(0.5, enrichmentCostUsd(targets.length, perCompany) * 1.3);

  const started = (await apify(
    `/acts/${ACTOR}/runs?maxTotalChargeUsd=${costCap.toFixed(2)}`,
    options.token,
    {
      method: "POST",
      body: JSON.stringify({
        companies: targets.map((t) => t.linkedinCompanyUrl),
        jobTitles: JOB_TITLES,
        profileScraperMode: "Full + email search ($12 per 1k)",
        companyBatchMode: "one_by_one",
        maxItemsPerCompany: perCompany,
        // Required — see the note at the top of this file.
        maxItems: targets.length * perCompany,
      }),
    },
  )) as { data?: { id?: string; defaultDatasetId?: string } };

  const runId = started.data?.id;
  const datasetId = started.data?.defaultDatasetId;
  if (!runId || !datasetId) {
    throw new EnrichmentUnavailableError("The Apify run could not be started.");
  }

  const pollMs = options.pollMs ?? 5_000;
  const maxWaitMs = options.maxWaitMs ?? 300_000;
  const clock = options.now ?? Date.now;
  const deadline = clock() + maxWaitMs;
  let status = "RUNNING";
  while (clock() < deadline) {
    const run = (await apify(`/actor-runs/${runId}`, options.token)) as {
      data?: { status?: string };
    };
    status = run.data?.status ?? "RUNNING";
    if (["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"].includes(status)) {
      break;
    }
    await new Promise((resolve) => setTimeout(resolve, pollMs));
  }
  if (status !== "SUCCEEDED") {
    throw new EnrichmentUnavailableError(`The Apify run ended as ${status}.`);
  }

  const items = (await apify(
    `/datasets/${datasetId}/items?clean=true&format=json&limit=1000`,
    options.token,
  )) as ScrapedProfile[];

  const findings: EnrichmentFinding[] = [];
  for (const target of targets) {
    const candidates = items.filter((item) => matchesCompany(item, target));
    let best: { finding: EnrichmentFinding; score: number } | undefined;
    for (const profile of candidates) {
      const title = profile.currentPosition?.[0]?.position ?? profile.headline ?? "";
      for (const entry of profile.emails ?? []) {
        const rated = rateEmail(entry);
        if (rated.confidence === "none") {
          continue;
        }
        const weight =
          (rated.confidence === "high" ? 100 : rated.confidence === "medium" ? 50 : 20) +
          roleScore(title) * 5;
        if (best === undefined || weight > best.score) {
          best = {
            score: weight,
            finding: {
              prospectId: target.prospectId,
              company: target.company,
              contactName: [profile.firstName, profile.lastName].filter(Boolean).join(" "),
              contactEmail: entry.email!,
              linkedinUrl: profile.linkedinUrl ?? "",
              jobTitle: title,
              confidence: rated.confidence,
              flagReason: rated.flagReason,
            },
          };
        }
      }
    }
    findings.push(
      best?.finding ?? {
        prospectId: target.prospectId,
        company: target.company,
        contactName: "",
        contactEmail: "",
        linkedinUrl: "",
        jobTitle: "",
        confidence: "none",
        flagReason:
          candidates.length === 0
            ? "No profiles returned for this company URL. Check the URL, or the job-title filter may exclude everyone there."
            : "Profiles found, but none carried an address.",
      },
    );
  }

  return { findings, runId, costUsd: enrichmentCostUsd(targets.length, perCompany) };
}
