# Big Four quantitative research package

Research cutoff: **2026-07-18**  
Initial collection tranche: **global network core series**  
Front-end changes: **none**

This directory is the machine-readable evidence layer for the Big Four dashboard. The first tranche follows the ordering in `references/big_four_quantitative_data_extraction_prompt.md`: establish reporting entities and periods, inventory official sources, then extract global revenue, global workforce, service-line revenue, and regional revenue before expanding to national accounts, offices, audit clients, regulatory events, and other modules.

## Rules used in this tranche

- One observation, one entity, one period/as-of date, and one source per row.
- Source values are retained before normalization.
- Global networks and member firms are not mixed.
- Missing values are never represented by zero.
- `reported`, `calculated`, `proxy`, and restated values remain distinguishable.
- Historical values are not silently overwritten. Later restatements receive their own observation rows and point to the superseded row where identifiable.
- Grade B official network publications are the primary source class in this global-core tranche. Grade A filings and regulator records become more prominent in the national-firm, audit-client, and inspection tranches.

## Current files

- `01_entity_master.csv`: recurring reporting and legal entities.
- `02_metric_dictionary.csv`: definitions for every metric used so far.
- `03_source_ledger.csv`: document-level provenance and source grades.
- `04_observations_long.csv`: canonical long-form observations.
- `05_coverage_matrix.csv`: explicit coverage by firm, metric, and fiscal year.
- `06_service_line_crosswalk.csv`: source labels mapped to the canonical service-line taxonomy.
- `06_geography_crosswalk.csv`: source regions retained alongside canonical regions.
- `06_workforce_crosswalk.csv`: source workforce terms mapped to canonical categories.
- `07_global_financials.csv`: convenience view of total global revenue and growth.
- `08_service_line_data.csv`: convenience view of service-line revenue.
- `09_geographic_data.csv`: convenience view of regional revenue.
- `11_workforce_data.csv`: convenience view of global workforce observations.
- `27_quality_checks.csv`: structural and reconciliation checks.
- `27_source_url_checks.csv`: live primary-link and archive-fallback checks.
- `28_search_log.csv`: documented unresolved searches.
- `29_research_summary.md`: generated collection and coverage summary.
- `inbox/`: independently researched firm-level fragments retained for auditability.

The remaining numbered domain files from the commission are intentionally deferred rather than populated with empty or invented observations. They will be added as those research modules begin.

## Rebuild and validation

Run:

```sh
python3 scripts/build_research_package.py
```

The build fails on duplicate IDs, unknown source/entity/metric references, malformed dates, nonnumeric numeric fields, and invalid enumerations. It also produces reconciliation checks for service-line and regional totals.

## Known first-tranche comparability limits

- Reported revenue terminology differs by network (for example, aggregate, combined, or globally aggregated member-firm revenue).
- KPMG reports gross revenue including client-reimbursable expenses in recent releases; definitions for other firms and older periods require source-level review.
- Workforce measures can be average FTE, period-end headcount, or broadly described “people”; these remain separate through the source definition and notes.
- Fiscal year ends differ across the networks. Rankings should use an explicitly selected common cutoff, not merely matching fiscal-year labels.
- FY2025 is the latest public global year for all four networks as of the research cutoff, but it does not represent identical calendar periods.
