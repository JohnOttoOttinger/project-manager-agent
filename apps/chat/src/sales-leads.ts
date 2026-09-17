import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { dirname, join } from "node:path";

/**
 * The sales CRM board.
 *
 * Unlike the content pipeline — a view onto hand-kept markdown where a card is
 * "which file, which line" — a lead is a record with fields nobody wants to
 * hand-edit inside a bullet: contact, value, stage, note. So this store owns a
 * JSON file of its own and the board is the only thing that writes it.
 *
 * Every write re-reads the file, applies the change, and renames a temporary
 * file over the target, so a crash mid-write cannot leave a half-written board.
 * Writes are serialised because two drags landing together must not each read
 * the file, edit their own copy, and race to write it back.
 */

export const LEAD_STAGES = [
  "new",
  "contacted",
  "talking",
  "proposal",
  "won",
  "lost",
] as const;
export type LeadStage = (typeof LEAD_STAGES)[number];

export const LEAD_BRANDS = ["datalabs", "oddtoe", "general"] as const;
export type LeadBrand = (typeof LEAD_BRANDS)[number];

export interface Lead {
  id: string;
  company: string;
  contact: string;
  email: string;
  value: number | null;
  stage: LeadStage;
  brand: LeadBrand;
  source: string;
  note: string;
  createdAt: string;
  updatedAt: string;
}

export interface LeadsPayload {
  writable: boolean;
  leads: Lead[];
}

const FIELD_LIMITS = {
  company: 120,
  contact: 120,
  email: 160,
  source: 80,
  note: 2_000,
} as const;

const MAX_LEADS = 500;
const MAX_VALUE = 100_000_000;

export class LeadValidationError extends Error {}

function text(
  value: unknown,
  field: keyof typeof FIELD_LIMITS,
  { required = false } = {},
): string {
  if (value === undefined || value === null) {
    if (required) {
      throw new LeadValidationError(`Give the lead a ${field}.`);
    }
    return "";
  }
  if (typeof value !== "string") {
    throw new LeadValidationError(`The ${field} must be text.`);
  }
  const trimmed = value.trim();
  if (required && trimmed === "") {
    throw new LeadValidationError(`Give the lead a ${field}.`);
  }
  if (trimmed.length > FIELD_LIMITS[field]) {
    throw new LeadValidationError(
      `Keep the ${field} under ${FIELD_LIMITS[field]} characters.`,
    );
  }
  return trimmed;
}

export function validateStage(value: unknown): LeadStage {
  if (
    typeof value === "string" &&
    (LEAD_STAGES as readonly string[]).includes(value)
  ) {
    return value as LeadStage;
  }
  throw new LeadValidationError("That is not a column on this board.");
}

function validateBrand(value: unknown): LeadBrand {
  if (
    typeof value === "string" &&
    (LEAD_BRANDS as readonly string[]).includes(value)
  ) {
    return value as LeadBrand;
  }
  throw new LeadValidationError("Choose which brand this lead belongs to.");
}

// A deal value is optional: plenty of leads arrive before anyone has put a
// number on them, and a board that demands one invites made-up figures.
function validateValue(value: unknown): number | null {
  if (value === undefined || value === null || value === "") {
    return null;
  }
  const parsed = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(parsed) || parsed < 0 || parsed > MAX_VALUE) {
    throw new LeadValidationError(
      "Write the value as a plain number of dollars, or leave it blank.",
    );
  }
  return Math.round(parsed);
}

export function validateLeadId(value: unknown): string {
  if (typeof value !== "string" || value.trim() === "" || value.length > 80) {
    throw new LeadValidationError("That lead could not be identified.");
  }
  return value.trim();
}

function normaliseLead(raw: unknown): Lead | null {
  if (raw === null || typeof raw !== "object") {
    return null;
  }
  const record = raw as Record<string, unknown>;
  const company = typeof record.company === "string" ? record.company.trim() : "";
  if (company === "") {
    return null;
  }
  const now = new Date().toISOString();
  return {
    id:
      typeof record.id === "string" && record.id.trim() !== ""
        ? record.id.trim().slice(0, 80)
        : randomUUID(),
    company: company.slice(0, FIELD_LIMITS.company),
    contact:
      typeof record.contact === "string"
        ? record.contact.trim().slice(0, FIELD_LIMITS.contact)
        : "",
    email:
      typeof record.email === "string"
        ? record.email.trim().slice(0, FIELD_LIMITS.email)
        : "",
    value:
      typeof record.value === "number" && Number.isFinite(record.value)
        ? Math.round(record.value)
        : null,
    stage: (LEAD_STAGES as readonly string[]).includes(
      record.stage as string,
    )
      ? (record.stage as LeadStage)
      : "new",
    brand: (LEAD_BRANDS as readonly string[]).includes(record.brand as string)
      ? (record.brand as LeadBrand)
      : "general",
    source:
      typeof record.source === "string"
        ? record.source.trim().slice(0, FIELD_LIMITS.source)
        : "",
    note:
      typeof record.note === "string"
        ? record.note.trim().slice(0, FIELD_LIMITS.note)
        : "",
    createdAt: typeof record.createdAt === "string" ? record.createdAt : now,
    updatedAt: typeof record.updatedAt === "string" ? record.updatedAt : now,
  };
}

export class SalesLeadStore {
  readonly #file: string;
  #writeQueue: Promise<unknown> = Promise.resolve();

  constructor(directory: string) {
    this.#file = join(directory, "leads.json");
  }

  async #read(): Promise<Lead[]> {
    let text: string;
    try {
      text = await readFile(this.#file, "utf8");
    } catch {
      // No board yet — an empty one is the correct starting state, not an error.
      return [];
    }
    let parsed: unknown;
    try {
      parsed = JSON.parse(text);
    } catch {
      throw new LeadValidationError(
        "The saved lead board could not be read. Check data/sales/leads.json.",
      );
    }
    const rows = Array.isArray(parsed)
      ? parsed
      : Array.isArray((parsed as { leads?: unknown })?.leads)
        ? ((parsed as { leads: unknown[] }).leads)
        : [];
    return rows
      .map((row) => normaliseLead(row))
      .filter((lead): lead is Lead => lead !== null);
  }

  async #write(leads: Lead[]): Promise<void> {
    await mkdir(dirname(this.#file), { recursive: true });
    const body = `${JSON.stringify({ schemaVersion: 1, leads }, null, 2)}\n`;
    const temporary = `${this.#file}.${randomUUID()}.tmp`;
    await writeFile(temporary, body, "utf8");
    await rename(temporary, this.#file);
  }

  #locked<T>(task: () => Promise<T>): Promise<T> {
    const run = this.#writeQueue.then(task, task);
    this.#writeQueue = run.then(
      () => undefined,
      () => undefined,
    );
    return run;
  }

  async load(): Promise<LeadsPayload> {
    return { writable: true, leads: await this.#read() };
  }

  async add(input: unknown): Promise<LeadsPayload> {
    const body = (input ?? {}) as Record<string, unknown>;
    const now = new Date().toISOString();
    const lead: Lead = {
      id: randomUUID(),
      company: text(body.company, "company", { required: true }),
      contact: text(body.contact, "contact"),
      email: text(body.email, "email"),
      value: validateValue(body.value),
      stage: body.stage === undefined ? "new" : validateStage(body.stage),
      brand: validateBrand(body.brand ?? "general"),
      source: text(body.source, "source"),
      note: text(body.note, "note"),
      createdAt: now,
      updatedAt: now,
    };
    return this.#locked(async () => {
      const leads = await this.#read();
      if (leads.length >= MAX_LEADS) {
        throw new LeadValidationError(
          `The board holds ${MAX_LEADS} leads. Archive some won or lost cards first.`,
        );
      }
      leads.push(lead);
      await this.#write(leads);
      return { writable: true, leads };
    });
  }

  async move(id: string, stage: LeadStage): Promise<LeadsPayload> {
    return this.#locked(async () => {
      const leads = await this.#read();
      const lead = leads.find((candidate) => candidate.id === id);
      if (!lead) {
        throw new LeadValidationError(
          "That lead is no longer on the board — reload and try again.",
        );
      }
      lead.stage = stage;
      lead.updatedAt = new Date().toISOString();
      await this.#write(leads);
      return { writable: true, leads };
    });
  }

  async update(id: string, input: unknown): Promise<LeadsPayload> {
    const body = (input ?? {}) as Record<string, unknown>;
    return this.#locked(async () => {
      const leads = await this.#read();
      const lead = leads.find((candidate) => candidate.id === id);
      if (!lead) {
        throw new LeadValidationError(
          "That lead is no longer on the board — reload and try again.",
        );
      }
      if (body.company !== undefined) {
        lead.company = text(body.company, "company", { required: true });
      }
      if (body.contact !== undefined) {
        lead.contact = text(body.contact, "contact");
      }
      if (body.email !== undefined) {
        lead.email = text(body.email, "email");
      }
      if (body.value !== undefined) {
        lead.value = validateValue(body.value);
      }
      if (body.stage !== undefined) {
        lead.stage = validateStage(body.stage);
      }
      if (body.brand !== undefined) {
        lead.brand = validateBrand(body.brand);
      }
      if (body.source !== undefined) {
        lead.source = text(body.source, "source");
      }
      if (body.note !== undefined) {
        lead.note = text(body.note, "note");
      }
      lead.updatedAt = new Date().toISOString();
      await this.#write(leads);
      return { writable: true, leads };
    });
  }

  async remove(id: string): Promise<LeadsPayload> {
    return this.#locked(async () => {
      const leads = await this.#read();
      const remaining = leads.filter((lead) => lead.id !== id);
      if (remaining.length === leads.length) {
        throw new LeadValidationError(
          "That lead is no longer on the board — reload and try again.",
        );
      }
      await this.#write(remaining);
      return { writable: true, leads: remaining };
    });
  }
}
