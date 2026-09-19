# Evidence log

This implements `docs/methodology.md` section 8. **No number is published without an entry here.** If a claim doesn't have a row, it isn't cited as settled anywhere outward-facing, no matter how well the dossier itself sources it.

The log is `evidence.csv`, one row per claim.

---

## Columns

| Column | Content |
|---|---|
| `claim_id` | Unique reference, format `<ASSET>-<NNNN>` (zero-padded to 4 digits), e.g. `GOLD-0001`, `SP500-0001`. Numbers are assigned in the order claims are added, per asset, and are never reused — even if a claim is later withdrawn. |
| `claim_text` | The exact number or statement as it appears (or will appear) in published content. Plain English, one sentence. |
| `asset` | The asset the claim is about, lowercase, matching the dossier filename without `.md` (e.g. `gold`, `sp500`). |
| `window` | The time window the claim covers (e.g. `2015-01 to 2025-12`), or `n/a` if the claim isn't window-dependent — most cost-stack and tax figures aren't. |
| `cost_scenario` | `low`, `central`, `high`, or `n/a` if the claim isn't a cost figure (methodology section 2.3). |
| `tax_scenario` | `taxable`, `sheltered`, or `n/a` if the claim doesn't depend on tax treatment (methodology section 2.2). |
| `value` | The bare number, with no unit or symbol attached (e.g. `0.06`, `3000`, `18`). Leave blank only for a qualitative claim with no single number (rare — most rows should have one). |
| `unit` | The unit for `value` (e.g. `%`, `% p.a.`, `£`, `days`, `bps`). |
| `source_1_name` | The first source: publisher and page/document name. |
| `source_1_tier` | `A`, `B` or `C`, per methodology section 7.1. |
| `source_1_quote` | The exact sentence or clause relied on, verbatim from the page — per methodology section 7.3, a source that names only a page with no quoted line does not belong here. |
| `source_1_url` | The page's URL. If the dossier this row is drawn from didn't capture a full, precise URL (some don't), say so plainly in this field (e.g. `"gov.uk (full page path not captured in dossiers/x.md)"`) rather than inventing one — and fix it with the real URL as soon as it's found. |
| `source_1_accessed` | The date the source was accessed, `YYYY-MM-DD`. |
| `source_2_name` … `source_2_accessed` | An optional second source, same five fields, for a claim that needs two sources (e.g. to clear the Tier C sole-support rule, or to show two sources disagree). Leave every `source_2_*` field blank if there's only one source — don't pad it out. |
| `calculation_ref` | Link or path to the code/notebook that produced the figure, if one exists. Write `n/a — directly sourced from <dossier> section <n>` for a figure taken straight from a cited source rather than calculated — true of almost every row until this company starts computing NRR figures. |
| `checked_by` | Which agent checked the claim, and a reference to its review, e.g. `skeptic agent, reviews/gold-review-2026-09-18-v2.md`. |
| `approved_by` | Who signed off on publishing this claim, e.g. `Lucas, 2026-09-20`. Blank until that sign-off actually happens. |
| `status` | `draft`, `live`, `corrected`, or `withdrawn` (methodology section 8). A claim is `draft` until it is actually published; `live` and `corrected` require `approved_by` to be filled in. |
| `created` | The date this row was first added, `YYYY-MM-DD`. |
| `last_verified` | The date this claim's sources were last checked and confirmed to still say what this row claims, `YYYY-MM-DD`. Update this whenever a claim is re-checked, even if nothing changed — a stale `last_verified` date is a signal the claim needs a fresh look before it's relied on again. |

---

## Adding an entry

1. Pick the next unused `claim_id` for the asset (check the highest existing `<ASSET>-NNNN` in the file).
2. Copy the claim's exact wording from the dossier into `claim_text`, and pull `value`/`unit` out of it as separate fields.
3. Fill in `window`, `cost_scenario` and `tax_scenario`, using `n/a` where they don't apply.
4. Copy the claim's citation from the dossier into `source_1_name`/`source_1_tier`/`source_1_quote`/`source_1_url`/`source_1_accessed`. If the dossier gives a second, corroborating or contradicting source, use the `source_2_*` fields for it — otherwise leave them blank.
5. Set `calculation_ref` and `checked_by` as they stand today. Leave `approved_by` blank until Lucas actually signs off.
6. Set `status` to `draft`, and `created`/`last_verified` to today's date.
7. When a claim is corrected or withdrawn after publication, don't edit its row's history silently — update `status`, and add a new row if a replacement claim is needed, per the corrections process in `docs/methodology.md` section 8.

---

## The no-entry-no-publication rule

Per `docs/methodology.md` section 8: **every published number has an entry here, or it isn't published.** In practice that means:

- A dossier can be well-sourced and skeptic-reviewed and still not be ready to publish from, if its numbers haven't been logged here yet.
- A row with `status: draft` is not cleared for publication — only `live` or `corrected` rows, which require `approved_by` to be filled in, represent something Lucas has actually signed off to publish.
- If you're checking whether a specific published figure is backed by evidence, look it up by `claim_id` here first. If it isn't in this file, treat it as unpublishable regardless of how it reads elsewhere.
