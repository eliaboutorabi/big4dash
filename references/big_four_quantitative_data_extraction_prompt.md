# Deep Research Prompt: Build a Complete Quantitative Dataset on the Big Four

## Assignment

Act as a senior investigative researcher, financial-data analyst, audit-market specialist, and data engineer. Your task is to **research, extract, verify, normalize, and deliver the actual numerical data** needed to compare the four global professional-services networks:

- Deloitte
- PwC
- EY
- KPMG

This is **not** an assignment to suggest metrics, design a dashboard, write a high-level comparison, or describe where data might be found. You must go onto the Internet, find the relevant sources, extract the numbers, and return a structured, source-level dataset.

The objective is to create the most complete defensible public-data repository possible for the Big Four. Treat “complete” as:

1. Every relevant quantitative observation covered by the metric catalogue below.
2. Every year available within the requested time horizon.
3. All four firms, even when the result for a firm is “not disclosed” or “not comparable.”
4. Both global-network data and clearly separated national member-firm data where global figures do not exist.
5. Any additional quantitative metric discovered during research that is useful for comparing scale, economics, clients, people, audit quality, technology, geography, risk, or social impact.

Do not stop after finding the latest headline revenue and headcount. Do not return a narrative-only report. The principal deliverable is data.

---

## 1. Scope and entity rules

### 1.1 Global networks

Research the four global networks as distinct reporting organizations. Verify and record each network’s current official coordinating entity, reporting perimeter, fiscal year-end, reporting currency, and terminology.

Never assume that the global network is a single consolidated corporation. Preserve terms such as “aggregate,” “combined,” “global,” or “member-firm” revenue exactly as the source uses them.

### 1.2 National member firms and legal audit entities

Global-network figures and national member-firm figures must never be mixed without explicit labels. For every observation, identify whether it relates to:

- the global network;
- a regional organization;
- a national member firm;
- a specific legal audit firm;
- a consulting, tax, legal, or other subsidiary;
- an individual office or delivery center;
- an individual audit client; or
- another clearly described reporting entity.

Collect public national member-firm financial and workforce data whenever available. Give particular attention to large markets and jurisdictions with accessible statutory filings, transparency reports, or regulator data, including at least:

- United States
- United Kingdom
- Canada
- Australia
- Germany
- France
- Netherlands
- Switzerland
- Ireland
- Spain
- Italy
- Japan
- mainland China
- Hong Kong
- India
- Singapore
- South Africa
- Brazil
- Mexico
- Saudi Arabia
- United Arab Emirates
- New Zealand
- the Nordic countries where comparable data are available

This is a minimum priority list, not a limit. Add other countries whenever meaningful public data exist.

### 1.3 Time horizon

Use the following default time horizons:

- **Global revenue and global headcount:** every available year, with FY2010 through the latest available year as the target minimum.
- **Revenue by service line and region:** every available year, with FY2015 through the latest available year as the target minimum.
- **National member-firm accounts and partner economics:** every available year, with at least the latest five fiscal years where public filings permit.
- **Audit-client, audit-fee, auditor-tenure, and auditor-switch data:** latest five completed fiscal years, plus earlier years needed to establish tenure.
- **Regulatory inspections, enforcement, litigation, fines, and major controversies:** January 1, 2010 through the research cutoff date.
- **Acquisitions, divestitures, strategic investments, alliances, office openings/closures, and restructuring events:** January 1, 2010 through the research cutoff date.
- **Sustainability data:** every available reporting year and the original baseline year for every target.
- **Salary, job-posting, employee-review, and career data:** latest three calendar years, while retaining older series where consistently available.
- **Office locations:** a current snapshot as of the research date, plus known opening and closing dates where available.

State the exact research cutoff date. Preserve exact period-start, period-end, publication, filing, announcement, and event dates.

### 1.4 Current versus historical facts

For quantities that change continuously—headcount, office count, social-media followers, job openings, leadership, index constituents, market capitalization, and office locations—record an exact `as_of_date`. Never present a current snapshot as a fiscal-year value unless the source does so.

---

## 2. Non-negotiable output requirements

### 2.1 Deliver data files, not only prose

Return a downloadable research package containing, at minimum:

1. `00_README.md`
2. `01_entity_master.csv`
3. `02_metric_dictionary.csv`
4. `03_source_ledger.csv`
5. `04_observations_long.csv`
6. `05_coverage_matrix.csv`
7. `06_taxonomy_crosswalks.xlsx` or separate CSV crosswalks
8. `07_global_financials.csv`
9. `08_service_line_data.csv`
10. `09_geographic_data.csv`
11. `10_office_locations.csv`
12. `11_workforce_data.csv`
13. `12_member_firm_financials.csv`
14. `13_audit_clients.csv`
15. `14_audit_fees.csv`
16. `15_auditor_switches.csv`
17. `16_audit_quality_inspections.csv`
18. `17_regulatory_legal_events.csv`
19. `18_acquisitions_divestitures.csv`
20. `19_technology_ai_investments.csv`
21. `20_alliances.csv`
22. `21_sustainability.csv`
23. `22_social_diversity_training.csv`
24. `23_compensation_careers.csv`
25. `24_public_sector_contracts.csv`
26. `25_brand_digital_optional.csv`
27. `26_derived_metrics.csv`
28. `27_quality_checks.csv`
29. `28_search_log.csv`
30. `29_research_summary.md`

The domain-specific files may be omitted only when every relevant observation is already cleanly represented in `04_observations_long.csv`; however, the client, office, regulatory-event, acquisition, alliance, and contract files should remain separate because they are event- or entity-level datasets.

If the environment cannot create files, return each dataset as a separate CSV-formatted code block in logical batches. Do not substitute a narrative summary for the requested data.

### 2.2 One observation per row

The master observations file must contain one metric, one entity, one period or as-of date, one geography, and one source per row. Do not place several years in one cell. Do not use merged cells. Use UTF-8, snake_case field names, ISO 8601 dates, ISO country codes, and numeric fields that do not contain currency symbols or commas.

### 2.3 Preserve the source value before normalization

For every number, retain:

- the exact value as printed or rendered in the source;
- the parsed numeric value;
- original unit and scale;
- original currency;
- whether it is a count, amount, percentage, ratio, rate, range, target, estimate, or point-in-time balance;
- the source’s definition verbatim or faithfully paraphrased;
- the reporting scope;
- any denominator or sample size;
- and the normalized value, if normalization is appropriate.

Never overwrite the raw value with a converted or calculated value.

### 2.4 Every number needs provenance

Every row must link to a `source_id` in the source ledger and include an exact locator such as page number, table number, section heading, filing item, paragraph, database record, or query date. Include a short supporting excerpt or table label sufficient to verify the number.

A bare homepage link is not an adequate citation when a specific report, filing, PDF page, database result, or press release is available.

### 2.5 No silent gaps and no fabricated zeros

For every requested firm-metric-period combination, use one of these statuses:

- `reported` — directly stated by a source;
- `calculated` — computed only from cited raw inputs;
- `proxy` — a clearly identified substitute for an unavailable metric;
- `estimated_external` — a third party’s estimate, kept separate from official data;
- `target` — a future commitment or goal;
- `not_disclosed` — the firm or source does not disclose it;
- `not_found_after_search` — a documented search did not locate it;
- `not_comparable` — definitions or scopes conflict materially;
- `not_applicable` — the metric does not apply.

Never enter zero for a missing value. Never infer “not disclosed” merely because the first source does not contain the number.

### 2.6 Do not combine reported values with estimates

Official reported data, calculated values, proxies, third-party estimates, and crowdsourced observations must remain distinguishable at row level and in separate analytical layers. The primary dataset should default to reported and reproducibly calculated figures.

---

## 3. Required schemas

### 3.1 Entity master

Create one row for each network, member firm, subsidiary, legal audit entity, office, regulator, client company, alliance partner, acquisition target, or other recurring entity. Include:

- `entity_id`
- `entity_name_canonical`
- `entity_name_original`
- `entity_type`
- `parent_entity_id`
- `big_four_network`
- `member_firm_name`
- `legal_name`
- `former_names`
- `jurisdiction`
- `country_iso2`
- `country_iso3`
- `legal_form`
- `registration_number`
- `lei`
- `cik`
- `website`
- `active_from`
- `active_to`
- `status`
- `notes`
- `source_id`

### 3.2 Metric dictionary

For every metric used, define:

- `metric_id`
- `metric_name_canonical`
- `metric_family`
- `description`
- `raw_or_derived`
- `preferred_unit`
- `preferred_currency`
- `frequency`
- `stock_or_flow`
- `preferred_denominator`
- `calculation_formula`
- `inclusions`
- `exclusions`
- `known_definition_issues`
- `comparability_requirements`
- `priority_level`

### 3.3 Source ledger

Include:

- `source_id`
- `source_title`
- `publisher`
- `publisher_type`
- `document_type`
- `url`
- `archived_url`
- `publication_date`
- `filing_date`
- `reporting_period_start`
- `reporting_period_end`
- `access_date`
- `language`
- `official_source_flag`
- `audited_flag`
- `primary_or_secondary`
- `paywall_flag`
- `local_filename_if_saved`
- `notes`

### 3.4 Master observations table

Include at least:

- `observation_id`
- `metric_id`
- `firm_network`
- `entity_id`
- `entity_name`
- `entity_scope`
- `jurisdiction`
- `geography_original`
- `geography_canonical`
- `service_line_original`
- `service_line_canonical`
- `industry_original`
- `industry_canonical`
- `client_id`
- `period_start`
- `period_end`
- `fiscal_year_label`
- `calendar_year`
- `as_of_date`
- `value_original_text`
- `value_numeric`
- `value_low`
- `value_high`
- `unit_original`
- `unit_canonical`
- `scale_original`
- `currency_original`
- `value_in_original_currency`
- `value_usd_nominal`
- `value_usd_constant_price`
- `fx_rate_used`
- `fx_rate_type`
- `inflation_index_used`
- `observation_status`
- `reported_calculated_proxy_or_estimate`
- `definition_from_source`
- `formula_or_transformation`
- `numerator_observation_ids`
- `denominator_observation_ids`
- `sample_size`
- `population_size`
- `source_id`
- `source_locator`
- `source_excerpt`
- `extraction_method`
- `comparability_score`
- `confidence_score`
- `quality_flag`
- `revision_flag`
- `supersedes_observation_id`
- `researcher_notes`

### 3.5 Coverage matrix

For every metric family, firm, geography, and year, show whether data are:

- complete;
- partial;
- reported only for selected firms;
- available only through a proxy;
- not disclosed;
- not found;
- or not comparable.

The matrix must make missingness visible rather than hiding it.

### 3.6 Search log

For unresolved data points, record:

- `search_id`
- `metric_id`
- `firm_network`
- `entity_or_geography`
- `period`
- `search_date`
- `search_query`
- `domains_checked`
- `databases_checked`
- `reports_checked`
- `result`
- `reason_unresolved`

Do not mark a high-priority figure `not_found_after_search` without checking the official global site, relevant national site or registry, relevant regulator or public filing database, and at least one reputable secondary source.

---

## 4. Source hierarchy and research standards

Use the strongest source available and assign a source grade.

### Grade A: authoritative primary records

Examples:

- statutory accounts and corporate-registry filings;
- securities filings and public-company annual reports;
- proxy statements and audit committee disclosures;
- official regulator inspection reports and downloadable data;
- enforcement decisions, court judgments, and settlement documents;
- government procurement and contract-award databases;
- official emissions registries and target-validation records;
- official index constituent lists and exchange records;
- official professional-body examination statistics.

### Grade B: official firm publications

Examples:

- global and national annual reviews;
- revenue announcements;
- transparency reports;
- audit-quality reports;
- sustainability, impact, diversity, and workforce reports;
- official office directories;
- official press releases;
- official job postings;
- official acquisition and alliance announcements.

### Grade C: direct institutional counterparties

Examples:

- client announcements;
- technology-partner announcements;
- university, standards body, or professional-association records;
- public tender notices;
- official event and certification databases.

### Grade D: reputable secondary research

Examples:

- established financial press;
- respected accounting and legal publications;
- recognized market-research firms;
- academic papers;
- established league tables and compensation surveys.

### Grade E: modeled, crowdsourced, or digital-trace data

Examples:

- salary and employee-review sites;
- social-media counts;
- web-traffic estimates;
- search-interest indexes;
- media-sentiment databases;
- commercial estimates.

Keep Grade E data in separately labeled files or rows. Always record sample size, date, geography, method, and platform. Do not blend these values with official workforce or financial data.

### Research conduct

- Search official sources first, including local-language national websites.
- Search historical annual-report and transparency-report archives, not only current pages.
- Use Internet archives when official historical links are broken, while retaining the original publisher and archived URL.
- Inspect tables, footnotes, appendices, and definitions in PDFs; do not rely only on press-release summaries.
- Where a number is reproduced in multiple sources, identify the earliest authoritative source and preserve later revisions.
- For important headline values, reconcile the source number against at least one additional source or against component totals.
- Do not bypass paywalls or access restrictions. Record inaccessible sources and use lawful alternatives.
- Translate non-English source labels but preserve the original text.

---

## 5. Canonical taxonomies

Preserve original labels and also map them to canonical taxonomies. Never force a mapping that the source cannot support.

### 5.1 Service lines

Map, when defensible, into:

1. `audit_assurance_attest`
2. `tax_legal`
3. `consulting_transformation_implementation`
4. `strategy_deals_transactions_corporate_finance`
5. `risk_cyber_forensics_compliance_resilience`
6. `managed_services_business_process`
7. `internal_enabling_shared_other`
8. `combined_not_separable`

Record the original firm label in all cases. Do not split a combined category without a source-supported breakdown.

### 5.2 Geography

Use ISO countries and preserve firm-defined regions. Also map countries, where useful, to:

- Americas
- Europe
- Middle East and Africa
- Asia-Pacific

Do not force India, Central Asia, or other ambiguously grouped markets into a common region without recording the treatment.

### 5.3 Workforce

Distinguish:

- all people;
- employees excluding partners;
- all partners;
- equity partners;
- non-equity or salaried partners;
- principals;
- directors;
- managers;
- senior associates or seniors;
- associates or analysts;
- interns and apprentices;
- contractors and temporary workers;
- client-service professionals;
- internal or enabling staff.

### 5.4 Industries

Use the source’s industry labels and additionally map, when possible, to a standard such as GICS, NAICS, or NACE. At minimum support:

- financial services and insurance;
- technology, media, and telecommunications;
- consumer and retail;
- industrials and manufacturing;
- energy, utilities, and resources;
- healthcare and life sciences;
- government and public sector;
- real estate, construction, and hospitality;
- transportation and logistics;
- private equity and asset management;
- professional and business services;
- education and nonprofit.

### 5.5 Audit fee categories

Preserve the filing label and map to:

- audit fees;
- audit-related fees;
- tax fees;
- all other fees;
- total non-audit fees;
- total fees.

### 5.6 Regulatory event categories

Map events into:

- audit-quality failure;
- independence or conflict violation;
- tax conduct;
- consulting or advisory conduct;
- anti-money-laundering or financial-crime control;
- data protection or cybersecurity;
- misconduct or ethics;
- competition or procurement;
- employment;
- insolvency or client-failure litigation;
- other.

---

## 6. Complete quantitative research catalogue

For every metric below, seek the **actual values for all four firms**, all requested years, and all applicable entities. Add newly discovered metrics to the metric dictionary rather than omitting them.

### A. Organization, reporting perimeter, and physical scale

Collect:

- official global network name;
- coordinating entity and legal form;
- fiscal year start and end dates;
- reporting currency;
- founding year and major merger years;
- number of member firms;
- number of legal entities, when disclosed;
- countries served;
- territories served;
- cities served;
- physical offices;
- audit offices;
- consulting offices;
- delivery centers, acceleration centers, shared-service centers, technology centers, innovation labs, and centers of excellence;
- newly opened offices and centers;
- closed or consolidated offices;
- number of clients served, preserving the source definition;
- number of global strategic clients, when disclosed;
- number of major alliances or ecosystem partners;
- number of global leadership, board, council, and governance members;
- reporting publication lag in days.

Do not treat countries, territories, cities, and offices as interchangeable.

### B. Global financial performance

Collect by fiscal year:

- total global network revenue exactly as reported;
- reported year-over-year growth;
- growth in local currency;
- growth in constant currency;
- growth in U.S. dollars or other reporting currency;
- foreign-exchange effect in amount and percentage, when disclosed;
- organic growth;
- acquisition-driven growth;
- gross billings, net revenue, aggregate revenue, combined revenue, and other variants, preserving definitions;
- revenue by service line;
- revenue by sub-practice;
- revenue by region;
- revenue by country, when disclosed;
- revenue by industry, when disclosed;
- recurring revenue;
- managed-services revenue;
- technology-related revenue;
- sustainability-related revenue;
- public-sector revenue;
- audit and assurance revenue;
- tax and legal revenue;
- consulting and advisory revenue;
- deals, strategy, and transactions revenue;
- revenue from acquisitions or newly consolidated entities;
- member-firm contributions or network fees, where public.

For every revenue figure, record whether it includes subcontractors, reimbursable expenses, inter-firm billings, pass-through revenue, or taxes if the source explains this.

### C. National member-firm financial statements and partner economics

For each public national member-firm filing, collect:

- turnover or revenue;
- revenue by service line;
- revenue by geography or legal entity;
- audit fee income;
- non-audit fee income;
- cost of sales or direct costs;
- personnel expense;
- operating expenses;
- operating profit;
- operating margin if directly reported;
- profit before tax;
- tax expense;
- net profit;
- distributable profit;
- profit attributable to members or partners;
- average profit per equity partner;
- highest-paid partner amount, where legally disclosed;
- partner remuneration and pension expense;
- partner capital contributions;
- partner loans and current accounts;
- cash and cash equivalents;
- debt, borrowings, and credit facilities;
- trade receivables;
- work in progress or contract assets;
- total assets;
- total liabilities;
- net assets or equity;
- operating cash flow;
- capital expenditure;
- lease liabilities;
- provisions, including legal or insurance provisions;
- insurance or professional indemnity arrangements when quantified;
- dividends or partner distributions;
- number of equity partners and total partners used in profit calculations.

Do not compare national-firm profit metrics unless legal entity, accounting basis, and partner definitions are recorded.

### D. Service-line mix and practice development

For every source-defined service line and year, collect:

- revenue;
- reported growth rate;
- headcount;
- partner count;
- office count, where practice-specific;
- client count;
- engagement count;
- average engagement value;
- billable hours;
- utilization;
- realization;
- pricing or billing rates;
- recurring or managed-services share;
- acquisitions assigned to the practice;
- technology investment assigned to the practice;
- training and certification counts;
- service-line-specific attrition;
- service-line-specific audit or regulatory restrictions;
- service-line-specific market share from credible market research.

Cover, at minimum, audit and assurance, tax, legal, consulting, technology implementation, cyber, risk, forensic, deals, valuation, strategy, corporate finance, sustainability, cloud, data and AI, managed services, and internal enabling functions.

### E. Geographic revenue, workforce, and economic exposure

For each reported region and country, collect:

- revenue;
- revenue growth;
- headcount;
- partner count;
- number of offices;
- number of delivery centers;
- hiring;
- attrition;
- acquisitions;
- new market entries;
- office openings and closures;
- audit-client count;
- public-company audit fees;
- public-sector contract value;
- emissions and travel data where geographically reported;
- local statutory revenue and profit;
- local market share where credible.

Preserve the firm’s original regional boundaries. Provide a country-level bridge only when source data support it.

### F. Office and site location dataset

Build one row for every current physical site located. Include:

- `site_id`
- firm network;
- member firm or operating entity;
- site name;
- office type;
- street address;
- postal code;
- city;
- state, province, or region;
- country;
- latitude;
- longitude;
- coordinate source;
- coordinate precision;
- phone number;
- office webpage;
- services offered, if listed;
- employee count, if available;
- partner count, if available;
- opening date;
- closing date;
- active status;
- whether it is a client-service office, delivery center, shared-service center, innovation lab, training center, legal practice, or other facility;
- source and snapshot date.

Deduplicate alternate spellings and multiple webpages for the same physical address. Do not geocode a city center when a precise office address is available. Retain separate rows for multiple sites in the same city.

### G. Workforce scale and structure

Collect by year, geography, service line, and level whenever available:

- total people;
- employees excluding partners;
- total partners;
- equity partners;
- non-equity or salaried partners;
- principals and managing directors;
- directors;
- managers;
- seniors;
- associates and analysts;
- interns, apprentices, and trainees;
- contractors and temporary workers;
- client-service employees;
- internal and enabling employees;
- full-time and part-time employees;
- full-time equivalents;
- average headcount;
- period-end headcount;
- headcount added through acquisitions;
- headcount by region;
- headcount by country;
- headcount by service line;
- headcount by office or delivery center;
- remote or hybrid workforce counts;
- expatriates and international-assignment counts.

### H. Hiring, retention, promotion, and training

Collect:

- total hires;
- graduate hires;
- experienced hires;
- intern and apprentice intake;
- applications;
- offers;
- offer-acceptance rates;
- vacancies and open job postings at snapshot dates;
- departures;
- voluntary departures;
- involuntary departures;
- layoffs and announced job reductions;
- attrition and turnover rates;
- retention rates;
- average tenure;
- promotion counts;
- promotion rates;
- promotions to manager;
- promotions to director;
- partner admissions;
- partner departures and retirements;
- internal mobility;
- international transfers;
- succession rates;
- training hours;
- training expenditure;
- learning hours by subject;
- AI, data, cloud, cyber, audit, ethics, and sustainability training participation;
- professional certifications earned;
- professional-exam candidates and pass rates;
- tuition, exam, or certification support expenditure;
- employee engagement scores;
- survey response rates;
- absenteeism and leave metrics;
- vacation entitlement and usage where reported.

Always record whether a rate uses average or period-end headcount and whether partners are included.

### I. Diversity, equity, inclusion, and leadership representation

Collect counts and percentages by year and level for:

- gender;
- race and ethnicity, where legally reported;
- nationality;
- disability;
- veteran status;
- LGBTQ+ identity, where voluntarily reported;
- age bands;
- women among all employees;
- women among partners;
- women among equity partners;
- women among new partner admissions;
- women in boards, executive committees, and leadership;
- racial and ethnic representation by level;
- pay gaps by gender and ethnicity;
- promotion, hiring, and attrition rates by demographic group;
- parental leave usage and return-to-work rates;
- flexible-work participation;
- inclusion or belonging survey scores;
- diversity hiring targets and progress;
- supplier-diversity expenditure.

Preserve jurisdiction-specific demographic definitions and do not merge incompatible categories.

### J. Productivity and operating-efficiency inputs

Search for and collect all available raw inputs for:

- billable hours;
- available hours;
- utilization rate;
- realization rate;
- collection rate;
- average billing rate;
- standard billing rate;
- average engagement duration;
- average engagement size;
- projects or engagements per professional;
- clients per partner;
- audit clients per engagement partner;
- staff-to-partner ratio;
- manager-to-partner ratio;
- support-staff ratio;
- revenue per office;
- technology spend;
- occupancy and real-estate costs;
- travel expense;
- subcontractor expense;
- offshoring and delivery-center headcount;
- shared-service headcount;
- internal hours saved through automation;
- percentage of engagements using specified technology;
- audit hours by level;
- specialist hours;
- component-auditor hours;
- average report lag;
- work-in-progress days;
- receivable days;
- write-offs.

These figures are often unavailable globally. Collect member-firm, regulator, court, procurement, or engagement-level data where public and label the exact scope.

### K. Client counts, market share, and portfolio composition

Collect:

- total clients served, preserving the precise definition;
- audit-client counts;
- listed-company audit-client counts;
- private-company audit-client counts;
- public-interest-entity audit-client counts;
- large-private-company audit-client counts;
- tax clients;
- consulting clients;
- managed-services clients;
- government clients;
- clients by industry;
- clients by geography;
- client wins;
- client losses;
- audit tenders won and lost;
- client retention rates;
- average client tenure;
- top-client concentration, only when disclosed;
- top 10, top 20, top 50, or top 100 client revenue concentration, only when disclosed;
- cross-service penetration, only when directly reported;
- number of services per client, only when directly reported;
- market share by number of clients;
- market share weighted by client revenue;
- market share weighted by client assets;
- market share weighted by client market capitalization;
- market share weighted by audit fees;
- consulting, tax, deals, cyber, and other market-share estimates from credible sources.

Do not infer total firm revenue concentration from public-company audit fees. Such a calculation may be produced only as a clearly named audit-portfolio proxy.

### L. Public-company audit-client dataset

Build a client-year panel. At minimum, research the latest five fiscal years for constituents of major publicly available indices or comparable large-company universes, including where feasible:

- S&P 500 and a broader U.S. large-cap universe;
- FTSE 100 and FTSE 350;
- STOXX Europe 600 and/or major national European indices;
- S&P/TSX 60;
- ASX 200;
- Nikkei 225;
- Hang Seng Index;
- Straits Times Index;
- Nifty 50;
- FTSE/JSE Top 40;
- Ibovespa;
- other major markets where accessible constituent and filing data exist.

For every company-year, collect:

- company name;
- former name;
- ticker;
- exchange;
- CIK, LEI, ISIN, or local identifier;
- headquarters country;
- incorporation country;
- industry;
- index membership and index snapshot date;
- fiscal year-end;
- annual report or filing date;
- company revenue;
- total assets;
- market capitalization at a documented date;
- auditor global network;
- exact legal audit firm;
- engagement partner or signing partner, where disclosed;
- other participating audit firms or component auditors, where disclosed;
- auditor appointment date;
- auditor-since year;
- tenure in years;
- audit report date;
- audit opinion type;
- going-concern language;
- internal-control opinion;
- material weakness count;
- Critical Audit Matter or Key Audit Matter count;
- CAM/KAM titles and categories;
- audit fee;
- audit-related fee;
- tax fee;
- all other fee;
- total fee;
- non-audit fee;
- fee currency;
- prior-year fees;
- audit-fee approval policy;
- auditor change flag;
- outgoing auditor;
- incoming auditor;
- appointment, resignation, or dismissal date;
- stated reason for change;
- audit tender date;
- restatement flag;
- restatement announcement date;
- restated periods;
- late-filing flag;
- regulator enforcement flag;
- bankruptcy or major distress flag;
- source IDs for every field.

Do not rely on a single aggregate market-share article when client-level public filings can establish the underlying appointments.

### M. Audit fees and auditor independence

Collect and preserve the raw fee categories from public-company filings. Also collect:

- audit-fee growth;
- total non-audit fees;
- tax services provided by the auditor;
- audit-related services;
- other services;
- non-audit-fee approval thresholds;
- fee waivers or unusual one-time items;
- fee dependence on individual clients where disclosed;
- auditor tenure;
- partner rotation dates;
- independence violations;
- prohibited-service findings;
- financial-interest violations;
- business-relationship violations;
- employment-relationship violations;
- conflict checks and remediation counts, where reported;
- joint-audit arrangements;
- component-auditor usage;
- audit committee votes concerning ratification or reappointment.

### N. Audit quality and regulator inspection data

Collect engagement- and firm-level data from audit regulators in every jurisdiction where comparable public information exists. For each inspection cycle and legal audit firm, collect:

- regulator;
- jurisdiction;
- inspection year;
- report date;
- inspected population;
- sample-selection method;
- number of audits inspected;
- number of audits with findings;
- number of audits without findings;
- deficiency rate as reported;
- number and type of significant deficiencies;
- financial-statement audit deficiencies;
- internal-control audit deficiencies;
- independence deficiencies;
- quality-control findings;
- repeat findings;
- severity or rating categories;
- audit areas implicated;
- industries represented;
- issuer versus broker-dealer or other engagement type;
- remediation status;
- whether findings were later made public;
- enforcement referrals;
- fines or sanctions arising from the inspection;
- regulator caveats concerning extrapolation.

Also collect any published Audit Quality Indicators, including:

- partner and manager workload;
- average experience by level;
- staff turnover;
- hours by level;
- specialist hours;
- use of shared service centers;
- milestone completion;
- internal inspection pass rates;
- consultation counts;
- independence confirmations;
- training hours;
- employee survey results;
- audit-report lag;
- engagement quality-review statistics;
- root-cause themes;
- remediation completion.

Never rank firms by inspection percentage without displaying the regulator, inspected-audit count, population, sample method, year, and scope.

### O. Financial-reporting outcomes among audit clients

Using public filings and regulator records, collect by client and year:

- financial restatements;
- reissuance versus revision restatements;
- duration of restated periods;
- magnitude of reported adjustment, when available;
- material weaknesses;
- significant deficiencies, when public;
- late filings;
- auditor resignations;
- auditor dismissals;
- modified opinions;
- adverse internal-control opinions;
- going-concern opinions or material uncertainty language;
- regulator accounting or disclosure enforcement;
- fraud allegations and findings;
- bankruptcy or insolvency within a defined period after the audit;
- shareholder or creditor claims involving the auditor;
- audit report lag;
- subsequent auditor changes.

Do not claim causation between the audit firm and client outcomes. Treat these as portfolio outcome measures with documented limitations.

### P. Legal, regulatory, disciplinary, and reputational events

Build an event-level register from January 1, 2010 onward. Include:

- event ID;
- global network;
- member firm or legal entity;
- regulator, court, professional body, or claimant;
- jurisdiction;
- case or reference number;
- announcement date;
- conduct period;
- decision date;
- settlement date;
- appeal status;
- event category;
- service line;
- client involved;
- description of alleged or proven conduct;
- finding status: allegation, settlement without admission, final finding, appeal pending, overturned, or other;
- fine amount;
- settlement amount;
- damages amount;
- costs award;
- remediation cost;
- disgorgement;
- original currency;
- amount in USD at event-date exchange rate;
- non-monetary sanction;
- practice restriction;
- audit ban or suspension duration;
- license action;
- partner or employee sanctions;
- required remediation;
- affected client count;
- affected record or person count in privacy/cyber events;
- related insurance recovery, where disclosed;
- source IDs.

Separate allegations from final findings and separate civil settlements from regulator penalties. Do not add amounts from overlapping proceedings without identifying double counting.

### Q. Growth actions, acquisitions, divestitures, and restructuring

Build an event-level dataset containing:

- acquiring network and member firm;
- target name;
- target country;
- target service line;
- announcement date;
- completion date;
- acquisition, merger, team hire, asset purchase, alliance, joint venture, divestiture, or closure classification;
- purchase price;
- consideration type;
- target revenue;
- target profit;
- target employees;
- target partners;
- target offices;
- target clients;
- capabilities acquired;
- integration brand;
- geographic expansion;
- disclosed revenue contribution;
- goodwill or intangible assets when available from member-firm accounts;
- divestiture proceeds;
- jobs added or removed;
- restructuring charges;
- layoffs;
- office closures;
- business exits;
- strategic program investment and duration.

Keep announced transactions separate from completed transactions and do not invent transaction values when undisclosed.

### R. Technology, data, AI, cloud, and cybersecurity

Collect by firm, year, program, and geography:

- actual annual technology expenditure;
- announced investment commitment;
- commitment period;
- amount actually spent to date;
- capital expenditure and operating expenditure where disclosed;
- AI investment;
- generative-AI investment;
- cloud investment;
- cybersecurity investment;
- data and analytics investment;
- audit-technology investment;
- number of technology employees;
- number of AI specialists;
- number of data scientists;
- number of cloud professionals;
- number of cybersecurity professionals;
- number of technology partners;
- number of certifications by platform or provider;
- patents filed or granted;
- proprietary platforms and launch dates;
- internal platform users;
- client users;
- engagements using AI, analytics, automation, or specific platforms;
- percentage of audits using advanced analytics;
- percentage of employees trained in AI or digital skills;
- training hours;
- productivity or hours-saved claims;
- technology-enabled revenue;
- managed-services revenue;
- AI-related sales pipeline or bookings, when disclosed;
- innovation centers, labs, and staff;
- cyber incidents, affected users, and financial impact;
- technology acquisitions and acquired headcount.

Strictly distinguish actual expenditure from a multiyear commitment, a marketing announcement, a revenue target, and an external estimate.

### S. Alliances and ecosystem data

Create one row per alliance or major partnership. Include:

- Big Four network or member firm;
- partner organization;
- partner category;
- technology or capability area;
- start date;
- renewal date;
- end date;
- geographic scope;
- service-line scope;
- joint investment amount;
- joint fund amount;
- revenue target;
- bookings or pipeline, when disclosed;
- number of certified professionals;
- number of joint clients;
- number of solutions or accelerators;
- number of countries covered;
- joint centers or labs;
- staff dedicated to the alliance;
- awards or tier status with date;
- acquisition or exclusivity connection;
- source from both parties where possible.

Examples of alliance categories include cloud, enterprise software, AI, data, CRM, ERP, cybersecurity, workflow, financial technology, sustainability, universities, and industry platforms.

### T. Industry specialization and transaction credentials

For each major industry, collect:

- revenue;
- revenue growth;
- clients served;
- audit clients;
- public-company audit share;
- audit fees;
- client market capitalization;
- industry specialists;
- partners;
- offices or centers dedicated to the industry;
- acquisitions;
- published industry reports;
- relevant certifications;
- major announced client wins;
- IPO audit or advisory mandates;
- M&A transaction counts and value;
- restructuring engagements;
- valuation mandates;
- league-table position and methodology;
- industry-specific regulatory findings;
- industry-specific CAM/KAM counts and themes.

Use a consistent industry crosswalk and retain the source-defined sector.

### U. Environmental sustainability

Collect every reported year and baseline year for:

- Scope 1 emissions;
- Scope 2 location-based emissions;
- Scope 2 market-based emissions;
- Scope 3 emissions;
- each disclosed Scope 3 category;
- business-travel emissions;
- air-travel emissions;
- hotel emissions;
- employee-commuting emissions;
- purchased-goods-and-services emissions;
- capital-goods emissions;
- fuel and energy activities;
- waste emissions;
- total operational carbon footprint;
- carbon removals;
- offsets or credits purchased;
- renewable electricity purchased;
- renewable-energy percentage;
- electricity consumption;
- total energy consumption;
- natural gas and fuel use;
- office floor area;
- green-building certifications;
- water withdrawal and consumption;
- waste generated;
- waste recycled;
- paper use;
- emissions target base year;
- target year;
- target reduction percentage;
- net-zero year;
- science-based target validation status and date;
- progress against target;
- internal carbon price;
- sustainability-linked financing, when applicable;
- supplier target coverage;
- suppliers engaged;
- sustainability-training participation;
- sustainability-services revenue and headcount where disclosed.

Record reporting boundary, methodology, consolidation approach, emission factors, restatements, and assurance status.

### V. Social impact, ethics, and governance

Collect:

- community investment expenditure;
- charitable donations;
- pro bono hours;
- volunteer hours;
- participating employees;
- beneficiaries reached;
- education or skills-program participants;
- social-enterprise spending;
- supplier-diversity spending;
- ethics training completion;
- independence training completion;
- whistleblowing reports;
- substantiated cases;
- disciplinary actions;
- hotline response time;
- human-rights assessments;
- modern-slavery or supply-chain audits;
- board or governance-body size;
- independent governance members;
- public-interest body members;
- governance meeting counts;
- executive compensation metrics if disclosed;
- partner-voting participation;
- risk and quality committee counts and composition.

### W. Compensation, employee experience, and career outcomes

Collect by country, city, year, service line, role, and experience level:

- base salary;
- total cash compensation;
- bonus;
- signing bonus;
- overtime pay;
- pension or retirement contribution;
- healthcare and other quantified benefits;
- salary ranges in official job postings;
- starting graduate salary;
- intern pay;
- manager, director, and partner compensation;
- compensation growth;
- pay-gap data;
- average weekly hours;
- busy-season weekly hours;
- chargeable-hour target;
- vacation entitlement;
- employee-review overall score;
- compensation score;
- work-life-balance score;
- career-opportunity score;
- senior-leadership score;
- recommendation rate;
- CEO approval score;
- number of reviews;
- job-posting counts;
- application counts;
- time to promotion by level;
- time to partner;
- partner-admission rate;
- professional-exam pass rates;
- alumni destinations or exit-role distributions where credible;
- international-assignment counts;
- internal-transfer counts.

Official disclosures and job postings must be separated from surveys, self-reported salaries, and employee reviews. For crowdsourced data, preserve platform, sample size, collection date, location, role filters, and percentile or distribution statistics rather than only an average.

### X. Public-sector contracts and policy activity

Build a contract-level dataset from government procurement sources. Include:

- network and contracting legal entity;
- government or agency;
- country and subnational jurisdiction;
- contract identifier;
- procurement framework;
- award date;
- start and end dates;
- extension options;
- contract ceiling;
- awarded value;
- actual spend to date, when available;
- currency;
- service description;
- service line;
- lead contractor or subcontractor status;
- consortium partners;
- competitive versus sole-source method;
- number of bidders, when public;
- modifications and added value;
- termination or suspension;
- performance findings;
- conflict or independence concerns;
- source.

Also collect, where legally disclosed:

- lobbying expenditure;
- political contributions;
- trade-association payments;
- secondments to public bodies;
- participation counts in standards boards, regulator panels, and government advisory groups;
- public comments on accounting, audit, tax, and sustainability standards.

### Y. Brand, knowledge output, and digital reach — separate lower-confidence layer

Collect only with exact snapshot dates and clear methodology:

- brand valuation estimates;
- employer-ranking positions;
- reputation or trust survey scores;
- search-interest index;
- website visits and engagement estimates;
- LinkedIn followers;
- other social-media followers;
- posting frequency;
- social engagement;
- news-mention volume;
- positive, neutral, and negative sentiment counts;
- share of voice;
- official reports and articles published;
- academic citations;
- conference and webinar counts;
- event registrations or attendance;
- podcast or video views;
- newsletter subscribers;
- awards by category and year.

Do not treat marketing reach as a measure of revenue, quality, or client satisfaction.

### Z. Resilience, concentration, and operational risk inputs

Collect raw inputs for:

- revenue decline during downturns;
- headcount reductions;
- hiring freezes;
- restructuring charges;
- office closures;
- geographic revenue concentration;
- service-line revenue concentration;
- disclosed client concentration;
- dependence on public-interest-entity audit revenue;
- exposure to major failed or distressed clients;
- insurance coverage and claims;
- legal provisions;
- debt and liquidity facilities;
- partner capital;
- pension obligations;
- cybersecurity incidents;
- business-continuity events;
- sanctions-related exits;
- country exits or network-member expulsions;
- major quality-remediation programs;
- regulator-imposed growth restrictions;
- audit-client losses following mandatory rotation;
- acquisition dependence;
- foreign-exchange sensitivity.

---

## 7. Required derived metrics — calculate only after raw extraction

Create a separate `derived_metrics` file. Every calculated row must cite the exact input observation IDs and formula. Do not place a calculated value into the raw-value field.

Calculate when the underlying definitions are sufficiently comparable:

### Scale and growth

- year-over-year revenue growth;
- three-, five-, and ten-year revenue CAGR;
- real revenue growth after inflation;
- revenue share of the Big Four total;
- headcount growth;
- partner growth;
- revenue-growth-minus-headcount-growth;
- revenue per average employee;
- revenue per period-end employee, labeled as a proxy;
- revenue per partner;
- revenue per office;
- revenue per country;
- revenue per client only where client count and revenue scope match.

### Mix and concentration

- service-line share of total revenue;
- audit versus non-audit revenue share;
- consulting-to-audit revenue ratio;
- regional revenue share;
- largest-region share;
- service-line Herfindahl-Hirschman Index;
- geographic HHI;
- disclosed client concentration;
- audit-portfolio fee concentration.

### Workforce and careers

- employees per partner;
- employees per equity partner;
- managers per partner;
- partner admission rate;
- promotion rate;
- voluntary turnover rate;
- retention rate;
- training hours per employee;
- training expenditure per employee;
- women-partner share;
- leadership representation gap;
- compensation growth;
- estimated promotion duration only when supported by cohort data.

### Market position and clients

- audit market share by client count;
- audit market share by client revenue;
- audit market share by client assets;
- audit market share by market capitalization;
- audit market share by audit fees;
- client win/loss net change;
- median auditor tenure;
- average and median audit fee;
- audit fee as a percentage of client revenue or assets;
- audit-fee growth;
- client retention rate where a stable universe exists.

### Independence and audit quality

- non-audit fees as a percentage of audit fees;
- non-audit fees as a percentage of total fees;
- inspection deficiency rate;
- confidence intervals around inspection rates where statistically appropriate;
- restatement rate within the observed client portfolio;
- material-weakness rate;
- going-concern rate;
- late-filing rate;
- auditor-switch rate;
- median report lag;
- enforcement events per 100 audit clients;
- partner workload from public engagement-partner data.

### Risk and sustainability

- fines and settlements relative to revenue;
- event count by category and jurisdiction;
- five-year rolling penalties;
- emissions per employee;
- emissions per million dollars of revenue;
- travel emissions per employee;
- renewable electricity share;
- progress from baseline to target;
- community investment per employee;
- volunteer hours per employee.

Use formulas such as:

`yoy_growth = current_value / prior_value - 1`

`cagr = (ending_value / beginning_value)^(1 / number_of_years) - 1`

`revenue_per_employee = revenue / average_headcount`

`employees_per_partner = employees_excluding_partners / total_partners`

`audit_market_share_by_count = firm_audit_clients / total_companies_in_defined_universe`

`inspection_deficiency_rate = audits_with_deficiencies / audits_inspected`

`non_audit_fee_ratio = (audit_related_fees + tax_fees + other_fees) / audit_fees`

`carbon_intensity = total_emissions_tco2e / revenue_usd_millions`

Do not calculate a single overall “best firm” score unless separately requested. The purpose of this assignment is to acquire defensible data, not impose arbitrary weights.

---

## 8. Currency, inflation, and unit normalization

- Preserve every original-currency value.
- Convert financial flows using a documented annual-average exchange rate for the relevant reporting period unless a different rate is analytically required.
- Convert point-in-time balances using a period-end exchange rate.
- State the FX source, rate, date or averaging period, and direction.
- Use one consistent inflation series for constant-price comparisons and record the base year.
- Do not convert percentages, ratios, headcounts, or quantities unnecessarily.
- Preserve whether figures are stated in units, thousands, millions, or billions.
- Confirm metric prefixes and decimal separators in non-English sources.
- Keep metric tonnes of CO2e, energy units, hours, square meters, and other nonfinancial units explicit.

---

## 9. Validation and reconciliation checks

Run and report at least the following checks:

1. Service-line revenue versus total revenue.
2. Regional revenue versus total revenue.
3. Workforce subgroup totals versus reported total people.
4. Partner subtype totals versus total partners.
5. Recalculated revenue growth versus reported growth.
6. Audit-fee components versus total fees.
7. Inspection-deficiency numerator versus denominator and published percentage.
8. Scope 1 + Scope 2 + Scope 3 versus total emissions where the reporting boundary permits.
9. Current office duplicates and address conflicts.
10. Acquisition duplicate announcements versus completion events.
11. Regulatory penalties duplicated across regulator, court, and press sources.
12. Currency-unit and scale consistency.
13. Fiscal-year labels versus exact period dates.
14. Global network versus national member-firm scope conflicts.
15. “People,” “employees,” and “FTE” definition conflicts.
16. “Partner,” “equity partner,” “principal,” and “director” definition conflicts.
17. Index membership dates versus client fiscal years.
18. Restated or revised historical figures versus originally published values.
19. Broken source links and missing locators.
20. Calculated observations without complete input lineage.

For each check, output `pass`, `warning`, or `fail`, the affected observation IDs, and the resolution or caveat.

---

## 10. Comparability and confidence scoring

Assign each observation:

### Comparability score

- `5` — same metric definition, entity scope, period basis, and unit across firms;
- `4` — minor definitional differences that can be normalized;
- `3` — useful with visible caveats;
- `2` — proxy or materially different scope;
- `1` — not suitable for direct comparison.

### Confidence score

- `5` — audited filing, regulator data, or equivalent primary record;
- `4` — official firm report with clear definition;
- `3` — credible institutional or high-quality secondary source;
- `2` — modeled, survey, or crowdsourced data with adequate method;
- `1` — weak or poorly documented estimate.

Do not suppress low-scoring observations, but keep them visibly labeled and out of the primary comparable series.

---

## 11. Required research workflow

Follow this sequence:

### Step 1: Establish reporting entities and periods

For each firm, verify the global coordination entity, official fiscal period, reporting currency, and the meaning of revenue and people. Build the entity master before combining figures.

### Step 2: Build a source inventory by firm and year

Locate all global annual reviews, revenue releases, transparency reports, audit-quality reports, sustainability reports, diversity reports, national annual reports, statutory filings, and archived historical versions.

### Step 3: Extract global core series

Complete revenue, growth, headcount, partners, service lines, regions, countries, offices, and major sustainability figures before moving to lower-priority digital or crowdsourced metrics.

### Step 4: Extract national member-firm accounts

Capture profit, partner economics, balance-sheet, workforce, and audit-fee data from public filings and transparency reports.

### Step 5: Build the office dataset

Use official office directories and member-firm pages, then geocode and deduplicate every physical site.

### Step 6: Build audit-client and audit-fee panels

Use public-company filings, regulator databases, auditor-search tools, company annual reports, and index constituent lists. Preserve the legal audit firm and signing partner where available.

### Step 7: Build audit-quality and regulatory datasets

Extract inspection denominators, findings, enforcement actions, penalties, and remediation data directly from regulators and court records.

### Step 8: Extract people, technology, M&A, sustainability, and public-sector data

Use official reports first and record event-level details for acquisitions, alliances, contracts, and investments.

### Step 9: Run reconciliation and quality checks

Resolve discrepancies or preserve both values with a clear revision or scope note.

### Step 10: Calculate derived metrics

Compute only after the raw observations and taxonomies are complete.

### Step 11: Produce the coverage matrix and unresolved-search log

Show exactly what was and was not found. For each high-priority gap, state which sources and query paths were checked.

### Step 12: Write a concise research summary

Only after delivering the data, provide:

- key coverage statistics;
- highest-confidence datasets;
- material comparability limitations;
- unresolved gaps;
- source-quality distribution;
- data-currentness by module;
- and recommended refresh frequency.

Do not substitute “key findings” for the underlying data.

---

## 12. Minimum completion standard

The assignment is not complete unless:

- all four networks appear in every high-priority metric family;
- at least ten years of global revenue and headcount are attempted;
- all available service-line and regional revenue histories are extracted;
- global and member-firm entities are separated;
- every current office located has an address and source, and coordinates where reasonably obtainable;
- at least the defined major public-company audit universes are attempted;
- audit fees and auditor identity are collected at client-year level where filings permit;
- regulator inspection counts and denominators are preserved;
- legal and regulatory events are event-level, not only totals;
- investment commitments are separated from actual expenditure;
- original values and normalized values are both retained;
- every value has a source ID and exact locator;
- missing values carry explicit status codes;
- a coverage matrix and search log are included;
- all calculations cite their raw input observation IDs;
- and no unsupported estimate is presented as fact.

For metrics that prove unavailable, do not fill the gap with speculation. Document the search thoroughly and leave a transparent missing value.

---

## 13. Final response format

Return the work in this order:

1. Links to or attachments for the data files.
2. A data-package inventory with row counts and date coverage.
3. A coverage summary by firm and metric family.
4. A list of the most important unresolved gaps.
5. A list of material comparability warnings.
6. A concise methodology and source-quality summary.
7. A bibliography or source ledger preview.

Do not lead with a prose comparison of which firm is “best.” Do not provide visualization or dashboard recommendations unless asked in a later assignment. The output of this assignment is the raw, normalized, source-cited numerical evidence base.
