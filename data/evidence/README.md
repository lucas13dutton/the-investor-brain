# Evidence log

This implements `docs/methodology.md` section 8. **No number is published without an entry here.** If a claim doesn't have a row, it isn't cited as settled anywhere outward-facing, no matter how well the dossier itself sources it.

The log is `evidence.csv`, one row per claim.

---

## Columns

| Column | Content |
|---|---|
| `claim_id` | Unique reference, format `<ASSET>-<NNNN>` (zero-padded to 4 digits), e.g. `GOLD-0001`, `SP500-0001`. Numbers are assigned in the order claims are added, per asset, and are never reused — even if a claim is later withdrawn. |
| `row_type` | `claim` (default), `structural`, `sensitivity`, or `withdrawn` — see "Row types" below. Determines which sourcing rule the row is held to. |
| `claim_text` | The exact number or statement as it appears (or will appear) in published content. Plain English, one sentence. |
| `asset` | The asset the claim is about, lowercase, matching the dossier filename without `.md` (e.g. `gold`, `sp500`). |
| `window` | The time window the claim covers (e.g. `2015-01 to 2025-12`), or `n/a` if the claim isn't window-dependent — most cost-stack and tax figures aren't. |
| `cost_scenario` | `low`, `central`, `high`, or `n/a` if the claim isn't a cost figure (methodology section 2.3). |
| `tax_scenario` | `taxable`, `sheltered`, or `n/a` if the claim doesn't depend on tax treatment (methodology section 2.2). |
| `value` | The bare number, with no unit or symbol attached (e.g. `0.06`, `3000`, `18`). Leave blank only for a qualitative claim with no single number (rare — most rows should have one). |
| `unit` | The unit for `value` (e.g. `%`, `% p.a.`, `£`, `days`, `bps`). |
| `source_1_name` | The first source: publisher and page/document name. |
| `source_1_tier` | `A`, `B` or `C`, per methodology section 7.1. |
| `source_1_quote` | The exact sentence or clause relied on, verbatim from the page — per methodology section 7.3, a source that names only a page with no quoted line does not belong here. On a `claim` row, `validate.py` rejects a quote that just describes why no quote was found (see "Quote integrity" below) — find the real quote, or change `row_type` instead. |
| `source_1_url` | The page's URL — but **only if you actually fetched it or it appeared verbatim in a source you read.** Never construct or guess one, including a publisher's homepage standing in for a specific page you never pinned down — that's still a fabrication even though it resolves. On a `claim` row this must start with `http`, or be the literal flag `NEEDS RE-VERIFICATION` if no real URL was ever obtained (see "Row types" and `docs/open-research-queue.md`). |
| `source_1_accessed` | The date the source was accessed, `YYYY-MM-DD`. |
| `source_2_name` … `source_2_accessed` | An optional second source, same five fields, for a claim that needs two sources (e.g. to clear the Tier C sole-support rule, or to show two sources disagree). Leave every `source_2_*` field blank if there's only one source — don't pad it out. |
| `calculation_ref` | Link or path to the code/notebook that produced the figure, if one exists. Write `n/a — directly sourced from <dossier> section <n>` for a figure taken straight from a cited source rather than calculated — true of almost every row until this company starts computing NRR figures. |
| `checked_by` | Which agent checked the claim, and a reference to its review, e.g. `skeptic agent, reviews/gold-review-2026-09-18-v2.md`. |
| `approved_by` | Who signed off on publishing this claim, e.g. `Lucas, 2026-09-20`. Blank until that sign-off actually happens. |
| `status` | `draft`, `live`, `corrected`, or `withdrawn` (methodology section 8). A claim is `draft` until it is actually published; `live` and `corrected` require `approved_by` to be filled in. |
| `created` | The date this row was first added, `YYYY-MM-DD`. |
| `last_verified` | The date this claim's sources were last checked and confirmed to still say what this row claims, `YYYY-MM-DD`. Update this whenever a claim is re-checked, even if nothing changed — a stale `last_verified` date is a signal the claim needs a fresh look before it's relied on again. |

---

## Row types

Every row has a `row_type`. Only `claim` rows are held to the full sourcing rule (a real, quoted, dated, `http` source, and no Tier C source alone without an approved exception). The other three each get a narrower rule of their own, enforced by `validate.py`:

- **`claim`** (default) — an ordinary sourced fact. Needs `source_1_*` (or `source_2_*`) fully filled in with a real quote and an `http` URL, and can't rest on Tier C alone without an `EXCEPTION APPROVED` marker (see below).
- **`structural`** — a fact with no source because none is needed, e.g. "home storage costs nothing" or a coin's minted specification. No sourcing rule applies at all; leave `source_1_*` blank or use it for background context, whichever reads better.
- **`sensitivity`** — a cost published as a labelled range or bound under methodology section 3's unsourced-cost sensitivity rule, because a genuine attempt found no real source. `value` and `unit` must state the bound, and **every `source_1_*`/`source_2_*` field must be blank** — a sensitivity row is an assumption, not an evidenced fact, and giving it a fake source manufactures a paper trail for something that isn't actually sourced.
- **`withdrawn`** — a figure known to be wrong or superseded. If a replacement claim exists, name it in `calculation_ref` or `claim_text` as "replaced by `<CLAIM-ID>`" — `validate.py` checks that ID is real. Naming a replacement is optional; not every withdrawn figure has one yet.

If a row genuinely can't be sourced and doesn't fit `structural` or `sensitivity` either, use `withdrawn` rather than forcing it to pass as a `claim`.

---

## Adding an entry

1. Pick the next unused `claim_id` for the asset (check the highest existing `<ASSET>-NNNN` in the file).
2. Decide the `row_type` (see "Row types" above) before filling in anything else — it determines which of the remaining steps actually apply.
3. Copy the claim's exact wording from the dossier into `claim_text`, and pull `value`/`unit` out of it as separate fields.
4. Fill in `window`, `cost_scenario` and `tax_scenario`, using `n/a` where they don't apply.
5. For a `claim` row: copy the citation from the dossier into `source_1_name`/`source_1_tier`/`source_1_quote`/`source_1_url`/`source_1_accessed`, with a real quote and an `http` URL. If the dossier gives a second, corroborating or contradicting source, use the `source_2_*` fields for it — otherwise leave them blank. For `structural`, `sensitivity` or `withdrawn`, follow that type's own rule instead.
6. Set `calculation_ref` and `checked_by` as they stand today. Leave `approved_by` blank until Lucas actually signs off.
7. Set `status` to `draft`, and `created`/`last_verified` to today's date.
8. When a claim is corrected or withdrawn after publication, don't edit its row's history silently — update `status` (and `row_type` to `withdrawn` if the figure itself is retired), and add a new row if a replacement claim is needed, per the corrections process in `docs/methodology.md` section 8.

---

## The no-entry-no-publication rule

Per `docs/methodology.md` section 8: **every published number has an entry here, or it isn't published.** In practice that means:

- A dossier can be well-sourced and skeptic-reviewed and still not be ready to publish from, if its numbers haven't been logged here yet.
- A row with `status: draft` is not cleared for publication — only a `live` row, which requires `approved_by` to be filled in (enforced by `validate.py`), represents something Lucas has actually signed off to publish. A `corrected` row should also carry `approved_by` as a matter of practice, even though the validator doesn't currently enforce that for `corrected` specifically.
- If you're checking whether a specific published figure is backed by evidence, look it up by `claim_id` here first. If it isn't in this file, treat it as unpublishable regardless of how it reads elsewhere.

---

## Running the validator and its tests

```
python3 data/evidence/validate.py
python3 data/evidence/test_validate.py
```

`validate.py` exits non-zero and prints every failing `claim_id` with the reason if any row breaks its type's rule (see the script's docstring for the exact list). Every row, regardless of type: no duplicate `claim_id`; no `live` row missing `approved_by`; no `last_verified` date more than 12 months old (or missing). A `claim` row additionally needs: at least one complete source (tier, quote, accessed date); no Tier-C-only sourcing without an `EXCEPTION APPROVED` marker; a real quote, not a description of why one couldn't be found; and a source URL starting with `http`, or the literal flag `NEEDS RE-VERIFICATION` if no real URL was ever obtained. `structural`, `sensitivity` and `withdrawn` rows each follow their own narrower rule instead — see "Row types" above.

**`NEEDS RE-VERIFICATION` flag**: write this exact phrase in `source_1_url` (or `source_2_url`) instead of a URL when you did real research on a page but never captured its exact address, or couldn't find/fetch it at all. It's the only honest alternative to a real `http` URL — never substitute a guessed or constructed one instead, even a plausible-looking homepage. Every row carrying this flag is tracked in `docs/open-research-queue.md`, which `report_stale.py` keeps current on every run.

**`EXCEPTION APPROVED` marker**, for a `claim` row that's genuinely Tier-C-only with Lucas's sign-off (e.g. a seller/platform's own current, dated fee page with no Tier A/B alternative): write the phrase anywhere in `claim_text`, a source name, or `calculation_ref`. A genuinely unsourced cost should usually be `row_type: sensitivity` instead, not a `claim` with this marker.

`test_validate.py` is a self-contained unit test suite with deliberately broken rows proving each rule actually fires (and control cases proving valid rows pass, including one per row type). Run it after any change to `validate.py`.
