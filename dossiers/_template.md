# <Asset name>

**Status:** draft · **Owner:** researcher agent · **Date checked:** <YYYY-MM-DD>
Built per `docs/methodology.md` and `docs/house-rules.md`. Where this template and those documents disagree, the documents win.

**Every numeric claim carries its evidence-log claim ID in brackets immediately after it**, e.g. "0.12% p.a. [GOLD-0015]", matching a real row in `data/evidence/evidence.csv`. No number is published without one — see `data/evidence/README.md`.

---

## 1. What it is

<Plain-English description of the asset. No jargon without a one-line explanation.>

## 2. How an ordinary UK retail investor buys it

<The real, ordinary retail channels a UK investor would use — retail platforms, dealers, marketplaces, auction houses. Not institutional or special access. If the asset has more than one distinct buying route (e.g. physical vs a fund wrapper), describe each route separately, since the rest of this dossier must cost and tax them separately too.>

## 3. The cost stack

Every stage from `docs/methodology.md` section 3 must have a row. If a cost does not apply, write "none" in that row and say why — a blank row blocks publication. Every value needs a source and a tier (A, B or C). No Tier C source may be the sole support for a value. Every value also needs its claim ID in brackets, e.g. "3-5% [GOLD-0002]".

### 3.1 Buying

| Cost | Low | Central | High | Source (tier) |
|---|---|---|---|---|
| Dealer premium / spread | | | | |
| Commission | | | | |
| Platform fees | | | | |
| Stamp duty or VAT | | | | |
| Buyer's premium | | | | |
| Delivery | | | | |
| Authentication or grading | | | | |

### 3.2 Holding

| Cost | Low | Central | High | Source (tier) |
|---|---|---|---|---|
| Storage | | | | |
| Insurance | | | | |
| Platform or account fees | | | | |
| Fund charges | | | | |
| Maintenance or servicing | | | | |
| Mortgage interest | | | | |
| Voids | | | | |
| Management fees | | | | |

### 3.3 Selling

| Cost | Low | Central | High | Source (tier) |
|---|---|---|---|---|
| Seller's fees | | | | |
| Marketplace and payment fees | | | | |
| Postage and packaging | | | | |
| Dealer buy-back spread | | | | |
| Agent or legal fees | | | | |

### 3.4 Currency

<Conversion cost when the asset is priced in another currency. If priced in GBP throughout, write "none" and say why.>

### 3.5 Time to sell

<Typical days to sell at a fair price, recorded separately from money per the methodology, with low/central/high and sources. Also record the typical sell spread — the gap between what dealers pay and what they charge.>

## 4. UK tax treatment

<Tax scenario as defined in `docs/methodology.md` section 2.2 — Taxable (default) and Sheltered (ISA/pension, where the asset is eligible there). State the date this was checked and cite HMRC guidance or an equivalent official source (Tier A). Cover Capital Gains Tax, Income Tax where relevant, VAT, and any asset-specific exemptions. Flag any HMRC guidance that is unclear or contested as an escalation to Lucas, rather than resolving it yourself.>

## 5. Price data sources

For every price series that exists for this asset:

| Source | Publisher | Tier | Licence terms | Coverage dates | Known gaps |
|---|---|---|---|---|---|
| | | | | | |

<Record whether each source can be used and republished within its licence terms. Never suggest scraping against a site's terms. Flag any source that requires payment or a licence agreement as an escalation to Lucas rather than assuming it can be used. Asking prices are never treated as sale prices — say clearly which sources are one or the other.>

## 6. Index or items, and survivorship bias

<State whether this asset is one price series (an index or fund) or many separate items (e.g. LEGO sets, cards, watches).
- If it is an index: say so and explain why the item-based rules in `docs/methodology.md` section 5 don't apply.
- If it is item-based: describe the selection rule for a fair sample (written down before analysis, never after seeing results), whether the source suffers survivorship bias (does it include items that fell in value or stopped trading?), and note that any published result must show the median item, the share of items that lost money, and the 10th and 90th percentiles.>

## 7. Risks and scams

<How people actually lose money in this asset — counterfeiting, fraud, custody or counterparty risk, price transparency issues, high-pressure sales tactics, unregulated sellers, and so on. Cite official sources (FCA, Action Fraud, Insolvency Service, court or regulator findings) where they exist. Use "alleged" for anything not yet a final finding, per `docs/house-rules.md`.>

## 8. Open questions

<What couldn't be established from available sources, and what would settle it. Anything that should go to Lucas — an unclear tax question, a source requiring payment, an asset with no honest cost model available — is listed here explicitly, not quietly assumed.>

## 9. Sources

<Full list of every source cited above, each with its tier (A, B or C) and the date it was accessed. When sources disagree, record both and say which is stronger and why.>

## Confidence

<High, medium or low, and what would raise it.>
