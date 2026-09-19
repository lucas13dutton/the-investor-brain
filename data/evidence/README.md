# Evidence log

This implements `docs/methodology.md` section 8. **Every published number has an entry here. No entry, no publication.**

The log lives in `evidence.csv`. `validate.py` checks every row against the rules below and fails the build if any row breaks one.

---

## Columns

| Column | Content |
|---|---|
| `claim_id` | Unique reference, format `<ASSET>-<NNNN>` (zero-padded to 4 digits), e.g. `GOLD-0001`. Numbers are assigned in the order claims are added and are never reused, even if a claim is later withdrawn. |
| `claim` | The exact number or statement as it appears (or will appear) in published content. Plain English, one sentence. |
| `asset` | The asset the claim is about, e.g. `gold`. Matches the dossier filename without `.md`. |
| `window` | The time window the claim covers, e.g. `2015-01 to 2025-12`, or `n/a` for a claim that isn't window-dependent (most cost-stack figures aren't). |
| `cost_scenario` | `low`, `central`, `high`, or `n/a` if the claim isn't a cost figure (methodology section 2.3). |
| `tax_scenario` | `taxable`, `sheltered`, or `n/a` if the claim doesn't depend on tax treatment (methodology section 2.2). |
| `sources` | One or more sources supporting the claim. See format below. Required on every row. |
| `calculation_ref` | Link or path to the code/notebook that produced the figure, if any was computed. Write `n/a — directly sourced` for a figure taken straight from a cited source rather than calculated (most cost-stack and tax figures). |
| `checked_by` | Which agent checked the claim, and a reference to its review, e.g. `skeptic agent, reviews/gold-review-2026-09-18-v2.md`. |
| `approved_by` | Who signed off on publishing this claim, e.g. `Lucas, 2026-09-20`. Blank until that sign-off happens. |
| `published_in` | Where the claim has been published (video, newsletter, page, with dates), or blank if not yet published. |
| `status` | One of `draft`, `live`, `corrected`, `withdrawn` (methodology section 8). A claim is `draft` until it is actually published. |

---

## The `sources` format

Each source is written as:

```
<short description> (Tier <A|B|C>, accessed <YYYY-MM-DD>): "<exact quoted sentence or clause>"
```

Multiple sources for the same claim are separated by ` ; `.

Example, one source:

```
HMRC Capital Gains Manual CG78305 (Tier A, accessed 2026-09-18): "Sovereigns minted in 1837 and later years and Britannia gold coins are currency but, like all sterling currency, are exempt because of TCGA92/S21(1)(b)."
```

Example, two sources:

```
BullionVault tariff (Tier B, accessed 2026-09-18): "0.12% per year... minimum of $4" ; Royal Mint Storage Fees (Tier B, accessed 2026-09-18): "1% + VAT"
```

This mirrors `docs/methodology.md` section 7.3: a citation naming only a page or document, with no quoted line, is not acceptable here either. If the quoted line can't be found, the claim does not get a row yet — it stays in the dossier's Open Questions instead.

### Tier-C-only exception

Per methodology section 7.1, a Tier C source may never be the sole support for a published number — unless Lucas explicitly approves a labelled exception. If every source on a row is Tier C, one of them must carry an explicit exception flag, or `validate.py` fails the row:

```
Spink buyer's premium page (Tier C, accessed 2026-09-18, EXCEPTION APPROVED by Lucas 2026-09-18): "..."
```

The literal text `EXCEPTION APPROVED` (any case) must appear somewhere in the `sources` cell.

---

## Adding an entry

1. Pick the next unused `claim_id` for the asset (check the highest existing `<ASSET>-NNNN` in the file).
2. Copy the claim's exact wording from the dossier into `claim`.
3. Fill in `window`, `cost_scenario` and `tax_scenario`, using `n/a` where they don't apply.
4. Copy the claim's citation(s) from the dossier into `sources`, in the format above. Every source needs a tier and an access date; at least one non-Tier-C source unless an approved exception is flagged.
5. Set `calculation_ref`, `checked_by`, `published_in` and `status` as they stand today. Leave `approved_by` and `published_in` blank until they're true.
6. Run `python3 data/evidence/validate.py` and fix anything it flags before committing.
7. When a claim is corrected or withdrawn after publication, do not edit its row's history silently — update `status` and add a new row if a replacement claim is needed, per the corrections process in `docs/methodology.md` section 8.

---

## Running the validator

```
python3 data/evidence/validate.py
```

Exits non-zero and prints every failing `claim_id` with the reason if any row breaks a rule. See the script for the exact checks.
