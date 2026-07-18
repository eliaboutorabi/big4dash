# Deep-Research Commission: Big Four Quantitative Dashboard

## Role

Act as a senior research analyst, audit-market specialist, data engineer, geospatial researcher, and information designer. Produce a source-cited, dashboard-ready research package comparing the four global professional-services networks:

- Deloitte
- PwC
- EY
- KPMG

The final research must support an unusually engaging, rigorous, and visually rich dashboard for accountants, audit committee members, investors, finance professionals, current and prospective employees, clients, journalists, academics, regulators, and anyone interested in the firms.

Do not merely write a narrative report. Build a structured quantitative evidence base, a data dictionary, a source ledger, a comparability assessment, a geospatial office dataset, client-level audit datasets, and a visualization plan.

## Central objective

Answer, with transparent evidence:

1. Which network is largest, fastest-growing, most productive, most geographically diversified, and most resilient?
2. How does each network make money, and how has its service mix changed?
3. Where does each network operate, and how dense is its real office and delivery-center footprint?
4. Which public companies, sectors, indices, and major institutions does each firm audit or serve?
5. How do audit quality, independence, regulatory outcomes, client tenure, and audit fees compare?
6. How do their workforces, leverage models, compensation, training, diversity, retention, and career outcomes compare?
7. Which firms appear to be investing most heavily and effectively in AI, technology, alliances, managed services, cybersecurity, and sustainability?
8. How do legal, regulatory, reputational, operational, and concentration risks compare after normalizing for scale?
9. What is genuinely comparable, what is only a proxy, and what is not publicly disclosed?
10. What are the most surprising, useful, and defensible visual stories in the data?

## Non-negotiable research principles

1. **Distinguish the global network from national member firms and legal audit entities.** Never combine a global-network numerator with an unrelated member-firm denominator.
2. **Use the firms’ own terminology in the raw data.** Create separate canonical crosswalks for service lines, regions, people categories, partner categories, and reporting scopes.
3. **Label network revenue exactly as reported**—for example, aggregate, combined, or gross global revenue—rather than implying that the network is a single consolidated corporation.
4. **Do not treat “clients served” as “audit clients.”** Keep audit, tax, advisory, consulting, legal, managed-service, and unspecified client relationships separate.
5. **Preserve fiscal dates.** Record reporting-period start and end dates, not only labels such as FY2025.
6. **Never silently estimate missing data.** Mark each value as reported, derived, estimated, modeled, proxy, not disclosed, not applicable, or not comparable.
7. **Prefer average headcount for per-employee metrics.** When only period-end headcount is available, label the calculation as a proxy.
8. **Separate actual spending from announced, planned, or committed investment.** Apply the same rule to acquisitions, technology programs, hiring plans, emissions targets, and office openings.
9. **Show denominators and sample sizes.** This is mandatory for inspection rates, restatement rates, employee-review data, salary data, client-market shares, and all survey-based measures.
10. **Do not extrapolate risk-based regulatory inspection samples to an entire audit population without an explicit caveat.**
11. **Do not rank firms on a metric unless the definitions are sufficiently comparable.** When comparability is weak, show the values side by side with a warning instead of declaring a winner.
12. **Every published number must have a traceable citation** to the exact source, page or section, reporting period, scope, and extraction note.

## Execution date, time horizon, and comparison periods

At the beginning of the project:

1. State the execution date.
2. Identify the latest publicly released global fiscal-year result for each network.
3. Identify the latest common comparable cutoff year across all four networks.
4. Use the latest common year for primary rankings, while permitting a clearly labeled “latest available” view.
5. Collect at least ten fiscal years for global revenue and headcount where possible, at least five years for service-line and regional data, at least five regulatory inspection cycles, and at least three years of client-level audit-fee data.
6. For current office locations, leadership, alliances, open jobs, and active targets, use a clearly dated current snapshot.
7. Preserve both nominal values and inflation-adjusted trend values where a long time series is shown.

## Source hierarchy

Use sources in this order and record the source grade:

### Grade A — authoritative primary sources

- Statutory filings, audited member-firm accounts, official corporate registries, court records, procurement records, regulator decisions, regulator datasets, and public-company filings.
- Official audit inspection reports and downloadable inspection data.
- Official public-company annual reports, proxy statements, auditor reports, and stock-exchange filings.

### Grade B — official but generally unaudited network disclosures

- Global annual reviews, impact reports, value-realized reports, revenue announcements, transparency reports, sustainability reports, diversity reports, office directories, careers data, and official press releases.

### Grade C — direct counterparty or institutional sources

- Client announcements, alliance-partner announcements, university or professional-body data, official index constituent files, and government agency records.

### Grade D — reputable secondary sources

- High-quality financial press, professional publications, established market-research providers, recognized league tables, and credible academic studies.

### Grade E — commercial, modeled, or crowdsourced sources

- Employee-review sites, salary aggregators, social platforms, web-traffic estimates, proprietary databases, and media-sentiment tools.

Grade E data must never be blended into an official-data series without a prominent visual distinction.

## Required output data model

Create a normalized long-form master table with at least these fields:

- `metric_id`
- `metric_name`
- `metric_family`
- `firm_network`
- `member_firm_or_legal_entity`
- `reporting_scope`
- `geography_original`
- `geography_canonical`
- `service_line_original`
- `service_line_canonical`
- `industry_original`
- `industry_canonical`
- `period_start`
- `period_end`
- `fiscal_year_label`
- `value_reported`
- `unit_reported`
- `currency_reported`
- `value_usd_nominal`
- `value_usd_constant`
- `value_type` — reported, derived, estimated, modeled, proxy
- `formula_or_method`
- `denominator`
- `source_grade`
- `source_title`
- `source_publisher`
- `source_url`
- `publication_date`
- `page_or_section`
- `source_excerpt`
- `retrieval_date`
- `comparability_rating`
- `confidence_rating`
- `missingness_code`
- `notes`
- `revision_status`

Use explicit missingness codes:

- `ND` — not disclosed
- `NA` — not applicable
- `NC` — not comparable
- `NE` — not estimable responsibly
- `P` — proxy
- `E` — estimated or modeled
- `R` — directly reported

## Canonical taxonomy crosswalks

Create and publish separate crosswalk tables rather than overwriting the original labels.

### Service-line crosswalk

At minimum, map source labels into these broad analytical families when defensible:

1. Audit, assurance, and related attest
2. Tax and legal
3. Consulting, transformation, and implementation
4. Strategy, deals, transactions, valuation, and corporate finance
5. Risk, cyber, compliance, forensic, and resilience
6. Managed services and business-process services
7. Internal, enabling, shared, or other

A source category may map to more than one canonical family only when the source provides a usable sub-breakdown. Otherwise retain it as a combined category.

### Geographic crosswalk

Preserve each firm’s reported regions, then map countries into a common country-level taxonomy and, where possible, a common high-level view:

- Americas
- Europe
- Middle East and Africa
- Asia-Pacific

Do not force a regional mapping when the source combines regions differently and country-level data is unavailable. Explain treatment of India and any other territories whose classification differs by network.

### Workforce crosswalk

Distinguish:

- total people
- employees excluding partners
- all partners
- equity partners
- non-equity or salaried partners
- principals or directors
- client-service professionals
- support or internal-services staff
- contractors, interns, and temporary staff

## Complete research inventory

For every metric below, research all four networks, record availability, rate comparability, calculate derived metrics only when valid, and specify the best dashboard visualization.

# 1. Identity, reporting perimeter, structure, and history

Collect:

- Official network name and coordination entity
- Legal form and governance structure
- Global headquarters or principal coordinating location
- Fiscal year-end and reporting period
- Number of member firms or legal entities, if disclosed
- Countries, territories, cities, offices, and delivery centers
- Current global chair, CEO, and major regional leaders
- Founding dates, major mergers, brand changes, consulting divestitures, reorganizations, and material strategic restructurings
- Major current strategic programs and stated priorities
- Definitions used for revenue, people, partners, countries, offices, clients, and service lines

Derived measures:

- Network age
- Reporting lag in days
- Disclosure freshness
- Historical continuity of reported metrics
- Structural-event timeline

Recommended visuals:

- Global-network-to-member-firm architecture diagram
- Fiscal-year calendar comparing the four firms
- Interactive historical timeline
- “How to read the data” scope diagram

# 2. Financial scale, growth, and resilience

Collect:

- Global revenue for every available year
- Revenue growth in reported currency, U.S. dollars, local currency, and constant currency
- Revenue by region
- Revenue by service line
- Revenue by industry, when disclosed
- Material currency impact
- Organic versus acquisition-driven growth, when disclosed
- Selected national member-firm revenue for countries where statutory accounts are available
- Operating profit, distributable profit, operating costs, cash generation, and capital only where legally and definitionally comparable
- Any reported recurring or managed-services revenue

Derived measures:

- Year-over-year growth
- Three-, five-, and ten-year CAGR
- Inflation-adjusted real growth
- Growth volatility
- Revenue share by firm within the Big Four total
- Revenue per employee
- Revenue per client, when a compatible client count exists
- Revenue per partner
- Revenue per office and per city
- Revenue-growth-minus-headcount-growth productivity gap
- Growth relative to global GDP, relevant professional-services market growth, and wage inflation
- Downturn resilience and recovery speed

Recommended visuals:

- Ten-year revenue line chart with nominal/real toggle
- Latest-year ranked bars
- Five-year slopegraph
- Revenue-growth waterfall separating organic, acquired, and currency effects when disclosed
- Revenue versus headcount bubble chart
- Growth versus productivity quadrant
- Small-multiple sparklines

# 3. Service-line composition and strategic mix

Collect:

- Revenue, headcount, growth, and partner counts by reported service line
- Sub-practice data for audit, tax, legal, consulting, technology, cyber, risk, transactions, strategy, managed services, sustainability, and other material practices
- Audit/assurance versus non-audit revenue
- Consulting-to-audit ratio
- Tax-and-legal share
- Technology-enabled and managed-service share
- Service-line reorganizations and classification changes

Derived measures:

- Service-line share of revenue
- Service-line share of headcount
- Revenue per employee by service line
- Service-line contribution to total growth
- Service diversification using a Herfindahl-Hirschman Index
- Audit dependence
- Advisory dependence
- Change in service mix over time

Recommended visuals:

- One-hundred-percent stacked bars
- Service-mix streamgraph or ribbon chart over time
- Small-multiple service-line growth charts
- Sankey from firm to service line and then region only when a genuine cross-tab exists
- Service diversification matrix

# 4. Geographic footprint and office map

Build a current, geocoded office-level dataset with:

- Firm network
- Member firm or legal entity
- Office name
- Full street address
- City
- State, province, or administrative region
- Postal code
- Country and ISO country code
- Latitude and longitude
- Geocoding source
- Geocoding precision
- Headquarters, regional hub, delivery center, innovation center, or ordinary office flag
- Services offered, when stated
- Office phone and official office-page URL
- Current, announced, opened, relocated, merged, or closed status
- Source date and retrieval date
- Duplicate-location and co-location flags

Also collect:

- Revenue, headcount, and growth by region and country when available
- Office openings, closures, and relocations
- Global delivery centers and centers of excellence
- Countries in which a network claims presence but no public office can be located

Derived measures:

- Countries and territories served
- Cities served
- Physical office count
- Average people per office
- Offices per million employees or residents, where useful
- Largest-region revenue share
- Regional concentration HHI
- Revenue per employee by region
- Share of world GDP covered by countries with a presence
- Share of world population covered by countries with a presence
- Office density relative to national GDP or population
- Time-zone coverage
- New-market entry rate and office contraction rate

Map design requirements:

- Global choropleth for country presence
- Clustered point map for offices
- Proportional symbols for regional headcount or revenue
- Optional layers for delivery centers, innovation hubs, audit clients, acquisitions, and regulatory events
- Filters for firm, country, region, office type, service capability, and status
- Tooltips containing address, source, office type, and last verification date
- Do not imply revenue or headcount at an office unless directly disclosed

# 5. Market position and client penetration

Collect separately for audit, tax, consulting/advisory, deals, legal, and unspecified services:

- Total client count, when disclosed
- Public-company and private-company client counts
- Percentage and count of major-company universes served
- Public-company audit market share by jurisdiction and index
- Consulting, tax, transaction-advisory, and other market rankings from credible providers
- Major client wins and losses
- Average client tenure
- Client mix by sector, geography, size, and ownership type
- Public-sector clients and contract awards
- IPO, private-equity, banking, insurance, asset-management, technology, healthcare, energy, and sustainability-assurance exposure

For audit-market comparisons, calculate market share using multiple denominators:

- Number of audit clients
- Aggregate client revenue
- Aggregate client assets
- Aggregate client market capitalization
- Aggregate audit fees

At minimum, design the research to support selectable major-index universes in North America, the United Kingdom, continental Europe, Asia-Pacific, India, Japan, Hong Kong, Singapore, Australia, Canada, and South Africa. De-duplicate companies that appear in multiple indices and preserve the constituent snapshot date.

Derived measures:

- Market share by count, value, assets, revenue, and fees
- Sector-specific audit share
- Share of systemically important or very large institutions audited
- New-client win rate
- Client loss rate
- Net audit-client change
- Average and median client tenure
- Client portfolio concentration and HHI

Recommended visuals:

- Index-by-firm market-share matrix
- Sector treemap
- Client headquarters map
- Bubble chart sized by client market capitalization
- Wins-and-losses slopegraph
- Market-share small multiples

# 6. Client-level audit engagement and fee dataset

For every company in the selected audit universes, collect:

- Company legal name
- Ticker, exchange, CIK, LEI, or other stable identifier
- Headquarters country and coordinates
- Index membership and snapshot date
- Industry and sector
- Fiscal year-end
- Audit firm network
- Signing member firm or legal audit entity
- Engagement partner, when public
- Audit report date
- Auditor appointment date and tenure
- Audit fees
- Audit-related fees
- Tax fees
- All other fees
- Total fees
- Currency
- Audit committee pre-approval disclosure
- Critical Audit Matter or Key Audit Matter count and themes
- Going-concern language
- Internal-control material weakness
- Restatement occurrence and severity
- Late filing, when material
- Auditor resignation, dismissal, or switch
- Predecessor and successor auditor
- Client revenue, assets, employees, and market capitalization
- Relevant source filing and page or section

Derived measures:

- Non-audit-fee-to-audit-fee ratio
- Non-audit share of total fees
- Audit fee per billion dollars of client revenue
- Audit fee per billion dollars of client assets
- Audit fee relative to market capitalization
- Median and distribution of audit fees by firm, sector, and client size
- Fee growth
- Fee change following an auditor switch
- Client concentration by audit fees
- Auditor-tenure distribution
- Partner workload measured by public-company audits per named partner
- Critical or Key Audit Matter density

Recommended visuals:

- Searchable audit-client explorer
- Fee-distribution boxplots or beeswarms
- Auditor-tenure histogram
- Auditor-switch Sankey or chord diagram
- Fee-composition stacked bars
- Outlier table with source links
- Engagement-partner workload distribution

# 7. Audit quality and financial-reporting outcomes

Collect by firm, member firm, jurisdiction, and inspection cycle:

- Number of audits inspected
- Number and percentage with deficiencies
- Inspection grading categories
- Deficiency themes and severity
- Quality-control or system-of-quality-management findings
- Good-practice findings
- Internal inspection results, when disclosed
- Audit-quality indicators
- Audit partner workload
- Specialist participation
- Audit hours and offshore/shared-service participation, when disclosed
- Restatement rate among audit clients
- Internal-control material-weakness rate
- Going-concern-opinion rate
- Audit-report lag
- Enforcement actions related to audit quality
- Withdrawn or revised audit opinions
- Sustainability-assurance quality indicators, where available

Method rules:

- Keep each regulator and jurisdiction separate unless methodologies are demonstrably compatible.
- Always show inspected-audit count and risk-selection caveat.
- Preserve changes in inspection methodology over time.
- Do not label a firm “best quality” based on a tiny or non-comparable sample.

Derived measures:

- Inspection deficiency rate
- Positive quality-outcome rate
- Five-year quality trend
- Restatement rate per 100 audit clients
- Material-weakness rate per 100 audit clients
- Audit-report lag median
- Quality-adjusted trend score with transparent methodology

Recommended visuals:

- Firm-by-year quality heatmap
- Dot plots with sample-size labels
- Small-multiple inspection trends
- Deficiency-theme matrix
- Quality-versus-market-share quadrant

# 8. Auditor independence and conflicts

Collect:

- Audit, audit-related, tax, and other fees by client
- Pre-approval policies
- Auditor tenure and mandatory-rotation dates
- Independence-related inspection findings
- Regulatory actions involving prohibited services, financial relationships, employment relationships, or conflicts
- Client concentration in a member firm, when disclosed
- Partner rotation information, when public
- Joint-audit arrangements

Derived measures:

- Audit versus non-audit fee ratio
- Non-audit share of total client fees
- Long-tenure client share
- Independence-event count and value
- Concentration of fees among top audit clients

Recommended visuals:

- Fee-composition bars
- Independence-risk scatterplot
- Long-tenure client table
- Regulatory-event timeline

# 9. Workforce scale, leverage, talent flows, and diversity

Collect:

- Total global people by year
- Average and period-end headcount
- Headcount by region, country, service line, job family, and level
- Partner counts, distinguishing equity and non-equity when possible
- Principals, directors, managers, professionals, and support staff
- Graduate hires, experienced hires, interns, apprentices, and contractors
- Promotions by level
- New partner admissions and partner departures
- Voluntary and total attrition
- Average tenure
- Employee engagement and recommendation scores
- Women and underrepresented groups in total workforce, management, partnership, boards, and senior leadership
- Gender and ethnicity pay gaps
- Disability, nationality, veteran, LGBTQ+, and other inclusion data where lawfully and consistently disclosed
- Training hours and expenditure
- Professional certifications and exam pass rates
- International assignments and internal mobility
- Workforce reductions and announced hiring plans

Derived measures:

- Employees per partner
- Client-service staff per partner
- Headcount CAGR
- Revenue per employee and per partner
- Training hours and spend per employee
- Promotion rate
- Partner-admission rate
- Turnover rate
- Representation gap between workforce and leadership
- Workforce growth versus revenue growth
- Geographic and service-line talent concentration

Recommended visuals:

- Workforce pyramid
- Career-flow Sankey
- Headcount and partner trend lines
- Diversity representation slopegraphs
- Region-by-level heatmap
- Training-intensity bars

# 10. Employee experience and career outcomes

Collect by country, city, service line, role, and level where possible:

- Starting salary
- Median base pay
- Bonus
- Total compensation
- Compensation growth
- Busy-season and annual working hours
- Billable utilization
- Vacation entitlement and reported usage
- Promotion speed
- Time to manager and partner
- Internal mobility
- Remote or hybrid-work policy
- Employee-review ratings and themes
- Offer, acceptance, and retention rates when public
- Professional-exam sponsorship and pass rates
- Alumni destinations, leadership roles, entrepreneurship, and board appointments
- Active job postings by location, service line, seniority, and requested skill

Method rules:

- Keep official and crowdsourced data in separate layers.
- Record sample size, collection window, role mapping, and city-level cost of living.
- Adjust compensation for purchasing power only as an optional derived view.
- Do not compare job titles without a role-level crosswalk.

Derived measures:

- Compensation by level and location
- Cost-of-living-adjusted compensation
- Promotion velocity
- Busy-season premium
- Employee sentiment trend
- Hiring velocity
- Demand for AI, data, cyber, sustainability, tax, and audit skills

Recommended visuals:

- Salary beeswarm or boxplot
- Role-and-country explorer
- Promotion timeline
- Job-demand heatmap
- Employee sentiment small multiples

# 11. Productivity and operating efficiency

Collect when available:

- Revenue per professional
- Billable utilization
- Realization rate
- Average billing rate
- Engagement duration
- Project gross margin
- Support-cost ratio
- Technology spend per employee
- Shared-service or delivery-center usage
- Hours saved through automation
- Revenue growth relative to headcount growth
- Clients per partner
- Engagements per partner

Derived measures:

- Productivity gap: revenue growth minus headcount growth
- Revenue per employee growth
- Revenue per partner growth
- Office productivity proxy
- Technology intensity
- Operating leverage

Recommended visuals:

- Productivity-versus-growth quadrant
- Revenue/headcount indexed lines
- Efficiency scorecard with comparability warnings
- Firm-level slopegraphs

# 12. Profitability and partner economics

Research globally but publish comparisons only where scope and definitions align. Collect:

- Operating profit
- Operating margin
- Distributable profit
- Profit per equity partner
- Average partner compensation
- Partner compensation growth
- Capital contributed per partner
- Cash generation
- Debt and lease obligations
- Tax paid
- Profitability by service line or geography, where disclosed

Method rules:

- Label this primarily as a member-firm or country-market comparison.
- Do not infer global profit from national accounts.
- Separate equity partner profit share from salaried partner compensation.

Recommended visuals:

- Country-selector small multiples
- Margin and partner-pay trend lines
- Profit bridge or waterfall
- Revenue-versus-profitability scatterplot

# 13. Growth strategy, acquisitions, divestitures, and market entries

Build an event-level dataset containing:

- Announcement date
- Closing date
- Acquirer and target
- Geography
- Target capability and industry
- Deal value, if disclosed
- Revenue or headcount acquired
- Offices added
- Transaction status
- Integration or rebranding status
- Source and confidence

Also collect:

- Divestitures
- New member firms
- Departing member firms
- Office openings and closures
- Major practice launches
- Strategic reorganizations
- Announced investment programs

Derived measures:

- Acquisition count and disclosed value by year
- Acquired headcount
- Capability mix of acquisitions
- Geographic expansion intensity
- Organic-versus-acquired growth indicators

Recommended visuals:

- M&A timeline
- Acquisition world map
- Capability treemap
- Strategy milestone ribbon

# 14. Technology, AI, data, cyber, and innovation

Collect:

- Actual annual technology investment
- Planned or committed multiyear investment, separately labeled
- Technology investment as a share of revenue
- AI-related revenue and growth, when disclosed
- AI, cloud, data, cyber, engineering, and product headcount
- Technology certifications
- Patents and proprietary platforms
- Audit technology and analytics tools
- Percentage of engagements using AI, automation, or advanced analytics
- Hours saved or productivity gains from automation
- Digital and AI training hours
- Responsible-AI governance and certifications
- Cybersecurity and privacy certifications
- Innovation centers and labs
- Technology-related acquisitions

Derived measures:

- Technology investment intensity
- AI revenue growth
- Tech specialist share of workforce
- Digital-training intensity
- Platform and product-launch count
- Technology-related acquisition share

Recommended visuals:

- Tech-investment timeline
- Innovation-intensity scatterplot
- AI-adoption heatmap
- Platform launch timeline
- Specialist-workforce bars

# 15. Alliance and ecosystem network

Build a structured alliance dataset with:

- Alliance partner
- Alliance category: cloud, AI, ERP, CRM, data, cyber, workflow, industry platform, university, or other
- Announcement and renewal dates
- Geographic scope
- Joint solution or platform
- Joint investment
- Certifications or trained professionals
- Partner tier or award status
- Disclosed joint revenue or pipeline, if any
- Source and current status

Derived measures:

- Active alliance count
- Alliance diversity
- Certifications per employee
- Alliance launch rate
- Network centrality by technology category

Recommended visuals:

- Interactive alliance network graph
- Firm-by-platform heatmap
- Alliance timeline
- Certification leaderboard

# 16. Industry specialization and transaction credentials

Collect:

- Revenue and headcount by industry
- Client count by industry
- Audit market share by industry
- Named industry specialists
- Sector-specific acquisitions and alliances
- Critical or Key Audit Matter themes by industry
- M&A, IPO, restructuring, and transaction-advisory league-table positions by deal count and value
- Share of major banks, insurers, asset managers, energy companies, technology companies, healthcare companies, government entities, and private-equity-backed companies audited or advised
- Sustainability-assurance engagements by sector

Derived measures:

- Sector specialization index
- Sector client concentration
- Industry audit-fee premium or discount after controlling for client size where feasible
- Share of systemically important institutions audited
- Deal-advisory market share

Recommended visuals:

- Sector-strength heatmap
- Industry treemap
- Deal league tables
- Key Audit Matter topic map
- Sector concentration radar only as an optional, six-axis maximum small multiple

# 17. Environmental sustainability

Collect:

- Scope 1, Scope 2 market-based, Scope 2 location-based, and Scope 3 emissions
- Business-travel emissions
- Purchased goods and services emissions
- Energy consumption
- Renewable-energy share
- Water and waste
- Office-space or green-building measures
- Carbon offsets and removals
- Base year, target year, and target boundary
- Net-zero and interim targets
- External target validation
- Supplier-engagement targets
- Progress against targets
- Sustainability-assurance status of the reported data

Derived measures:

- Emissions per employee
- Emissions per million dollars of revenue
- Business-travel emissions per employee
- Renewable-energy progress
- Target trajectory gap
- Five-year emissions CAGR

Recommended visuals:

- Emissions trajectory lines
- Scope waterfall
- Intensity comparison bars
- Target-versus-actual bullet charts
- Travel-emissions map or regional view when available

# 18. Social impact, ethics, and governance

Collect:

- Community investment
- Charitable giving
- Pro bono hours
- Volunteer hours
- Beneficiaries
- Foundation grants
- Supplier diversity
- Local procurement
- Human-rights and modern-slavery measures
- Ethics training completion
- Whistleblowing reports and substantiation rates, if disclosed
- Board, executive, and governance-body diversity
- Independent public-interest members
- Governance meetings and attendance, where meaningful

Derived measures:

- Community investment per employee and per revenue
- Volunteer and pro bono hours per employee
- Supplier-diversity share
- Governance representation metrics
- Ethics-training completion rate

Recommended visuals:

- Impact KPI tiles
- Social-impact trend lines
- Governance composition diagram
- Representation bars

# 19. Legal, regulatory, cyber, and reputational risk

Build a case-level dataset with:

- Firm network and member firm
- Event date
- Jurisdiction
- Regulator, court, or claimant
- Case type
- Service line
- Client involved, when public
- Allegation, finding, settlement, or judgment status
- Fine, settlement, damages, or remediation amount
- Currency and conversion method
- Restrictions, bans, monitorships, or remedial requirements
- Appeal status
- Final resolution date
- Source grade

Include:

- Audit and accounting enforcement
- Independence violations
- Tax-related cases
- Consulting conflicts
- Data privacy and cybersecurity incidents
- Professional-indemnity cases
- Debarments and procurement restrictions
- Major client-collapse controversies
- Withdrawn audit opinions and major restatements linked to auditor issues

Method rules:

- Separate allegations from final findings.
- Avoid double counting the same case across regulator, court, and media reports.
- Record gross and net amounts where recoveries or insurance are disclosed.

Derived measures:

- Fines and settlements per billion dollars of revenue
- Events per 100,000 employees
- Rolling five-year regulatory cost
- Event severity index with published weights
- Case duration
- Risk concentration by jurisdiction and service line

Recommended visuals:

- Regulatory-event timeline
- World map of finalized actions
- Five-year normalized-risk bars
- Service-line risk heatmap
- Case-status funnel

# 20. Public-sector footprint and policy influence

Collect where legally available:

- Government contract count and value
- Contracting agency
- Service category
- Procurement method
- Geography
- Contract start, end, and status
- Public-sector framework membership
- Contract disputes, cancellations, and debarments
- Lobbying expenditure
- Political contributions
- Secondments and public appointments
- Comment letters and formal policy submissions
- Participation in standard-setting and professional bodies

Derived measures:

- Public-sector revenue proxy
- Contract concentration by agency
- Contract win rate where bid data exists
- Lobbying or policy activity intensity

Recommended visuals:

- Public-contract map
- Agency treemap
- Contract timeline
- Policy-activity trend

# 21. Brand reach, public interest, and thought leadership

Treat this as an optional, lower-confidence module. Collect:

- Brand-value rankings
- Employer rankings
- Social followers and engagement
- Search interest
- Website traffic estimates
- Media mention volume and sentiment
- Thought-leadership publication count
- Research citations
- Event, webinar, podcast, and conference volume
- Awards by service line and geography

Derived measures:

- Share of voice
- Search-interest trend
- Publication intensity per 1,000 employees
- Media sentiment with methodology and uncertainty

Recommended visuals:

- Share-of-voice trend
- Topic map
- Publication and event calendar
- Search-interest small multiples

# 22. Disclosure quality and data transparency

Create an objective disclosure score based on a published rubric. Score separately for:

- Financial history
- Service-line detail
- Geographic detail
- Workforce detail
- Partner detail
- Audit-quality detail
- Sustainability detail
- Methodological definitions
- Machine-readability
- Historical accessibility
- Timeliness
- Source permanence

Do not equate disclosure volume with business quality. This score measures research transparency only.

Recommended visuals:

- Firm-by-category completeness heatmap
- Source-grade distribution
- Data-confidence badge
- Missing-data matrix

# 23. Resilience, diversification, and scenario-based composite views

Create derived indicators for:

- Revenue growth and volatility
- Service diversification
- Geographic diversification
- Client concentration
- Audit quality
- Talent stability
- Productivity
- Regulatory burden
- Innovation intensity
- Carbon intensity
- Disclosure completeness

Do not publish a single universal “best Big Four” score as the default. Instead create transparent presets for different users:

1. Business scale and growth
2. Audit committee and investor
3. Prospective employee
4. Consulting or transformation client
5. Tax client
6. Sustainability-focused user
7. Risk and regulation analyst

Allow user-defined weights and show sensitivity to changes in weights.

Composite-score rules:

- Include only metrics with adequate comparability.
- Publish directionality, normalization, weights, winsorization, and missing-value treatment.
- Show raw values beside scores.
- Include confidence-adjusted and unadjusted versions.
- Prevent a missing metric from automatically becoming an average score without disclosure.

## Required formulas and derived measures

At minimum calculate, where valid:

- `YoY growth = current / prior - 1`
- `CAGR = (ending / beginning)^(1 / years) - 1`
- `Revenue per employee = revenue / average headcount`
- `Revenue per partner = revenue / compatible partner count`
- `Employees per partner = compatible employee count / compatible partner count`
- `Productivity gap = revenue growth - headcount growth`
- `Service or geographic HHI = sum of squared shares`
- `Largest-region concentration = largest regional revenue / total revenue`
- `Market share by count = firm clients / universe clients`
- `Market share by value = sum of selected client value for firm / total universe value`
- `Non-audit ratio = non-audit fees / audit fees`
- `Non-audit share = non-audit fees / total fees`
- `Inspection deficiency rate = deficient audits / inspected audits`
- `Restatement rate = restating audit clients / observed audit clients`
- `Audit fee intensity = audit fees / client revenue or assets`
- `Fines intensity = finalized fines and settlements / revenue`
- `Carbon intensity = emissions / revenue and emissions / employees`
- `Training intensity = training hours or spend / employees`
- `Technology intensity = actual technology investment / revenue`
- `Office density = offices / population or GDP`
- `Economic coverage = GDP of countries with verified presence / world GDP`
- `Population coverage = population of countries with verified presence / world population`
- `Client concentration HHI = sum of squared client fee shares`
- `Auditor win rate = wins / (wins + losses)`
- `Partner workload = public-company audit engagements / named engagement partners`

For each formula, state the denominator scope and whether it uses average or period-end values.

## Currency, inflation, and fiscal-period rules

- Preserve reported currency and reported U.S.-dollar values.
- For member-firm revenue and fees, convert flow measures using an annual average exchange rate unless a more appropriate source-specific method exists.
- Preserve the exchange-rate source and rate.
- Create constant-dollar series for long-term trends using a stated inflation index.
- Do not use inflation-adjusted values for official headline figures unless the view is explicitly labeled “real.”
- Never compare local-currency growth with U.S.-dollar growth without labeling the difference.
- Align ranking views to the latest common fiscal cutoff and show latest-available values separately.

## Comparability and confidence framework

Give every metric two separate scores:

### Comparability

- 5 — same definition, scope, period, and unit
- 4 — minor reconcilable differences
- 3 — usable with meaningful caveats
- 2 — directional only
- 1 — not suitable for ranking

### Confidence

- 5 — statutory, audited, or regulator-derived primary data
- 4 — official firm data with clear methodology
- 3 — credible primary or high-quality secondary data
- 2 — estimated, modeled, or incomplete
- 1 — crowdsourced, anecdotal, or weakly sourced

Do not combine these into one opaque score.

## Dashboard information architecture

Design the research outputs to support these pages or modes:

1. **Home / Big Four at a glance** — four firm cards, latest common-year headline metrics, trend sparklines, and defensible “largest,” “fastest-growing,” or similar badges.
2. **Scale and growth** — revenue, headcount, productivity, profitability where comparable, and resilience.
3. **What they sell** — service-line mix, growth, diversification, and strategic change.
4. **World footprint** — interactive country and office map.
5. **Audit market** — index and industry market share, client explorer, fees, tenure, switches, and partner workload.
6. **Audit quality and independence** — regulator results, financial-reporting outcomes, and fee mix.
7. **People and careers** — workforce, leverage, diversity, training, pay, reviews, and hiring demand.
8. **Technology and alliances** — investment, AI, platforms, acquisitions, and partner ecosystem.
9. **Sustainability and social impact** — emissions, targets, community impact, and governance.
10. **Risk and reputation** — finalized regulatory actions, litigation, cyber incidents, and normalized risk.
11. **Compare two firms** — synchronized side-by-side view with metric selector.
12. **Firm profile** — one deep page per network.
13. **Methodology and sources** — source ledger, definitions, crosswalks, missing-data matrix, and downloadable data.

## Visual and interaction specifications

Use a polished data-journalism aesthetic rather than a crowded corporate scorecard.

- Use a neutral base palette with each network’s verified brand color as an accent.
- Ensure color-blind accessibility; pair color with labels, shapes, or patterns.
- Use tabular numerals and strong hierarchy for financial data.
- Default to direct labels rather than legends where practical.
- Use subtle motion only for transitions, filtering, and change over time.
- Every tooltip must show value, unit, period, definition, source, comparability, and confidence.
- Provide an absolute/per-employee/per-partner/per-billion-revenue toggle where meaningful.
- Provide a nominal/real and reported/local-currency toggle where meaningful.
- Provide a year slider and a “latest common year / latest available” toggle.
- Provide a visible sample-size and caveat area for audit-quality and employee-review charts.
- Make the map cluster points at low zoom and expose exact locations only at appropriate zoom.
- Enable downloadable CSV and source citation for every chart.
- Include a “data confidence” filter.
- Include a guided story mode with the strongest evidence-backed insights.
- Include a metric explorer for expert users.
- Avoid 3D charts, decorative gauges, misleading area encodings, and unlabeled dual axes.
- Use pie or donut charts only for a very small number of categories.
- Use radar charts only as optional small multiples with no more than six normalized axes and with raw values available.

## Signature diagrams to prepare

Prepare data and specifications for these visually distinctive elements:

1. Network structure diagram: global coordination entity → member firms → offices
2. Ten-year revenue and headcount “race” with a time slider
3. Service-line river or ribbon chart
4. Global office and delivery-center map
5. Audit-client market-share mosaic by index and sector
6. Auditor-switch Sankey or chord diagram
7. Audit-quality heatmap with sample sizes
8. Public-audit engagement-partner workload distribution
9. Workforce leverage pyramid
10. Career-flow Sankey from entry level to partner or alumni outcomes
11. AI and technology alliance network graph
12. Acquisition and strategic-milestone timeline
13. Emissions pathway versus targets
14. Regulatory-event world map and normalized five-year timeline
15. Disclosure-completeness matrix
16. Optional six-axis “firm fingerprint” profile with user-selectable metrics

## Research workflow

### Phase 1 — source inventory and taxonomy

- Build a source map for every firm and jurisdiction.
- Identify latest reports and historical archives.
- Document reporting definitions and create taxonomy crosswalks.
- Propose the common comparison year and explain it.

### Phase 2 — core global data

- Revenue, growth, headcount, partners, countries, offices, service lines, regions, technology, sustainability, and official quality indicators.

### Phase 3 — geospatial and client-level audit data

- Geocode offices.
- Build index constituent universes.
- Extract auditor, engagement partner, fees, tenure, Critical or Key Audit Matters, restatements, internal-control outcomes, and switches.

### Phase 4 — extended and lower-confidence data

- Compensation, employee sentiment, job postings, media interest, web traffic, brand rankings, lobbying, and other proxy metrics.

### Phase 5 — QA and reconciliation

- Reconcile totals to reported headlines.
- Check service-line and regional sums.
- Detect duplicate offices, clients, cases, and events.
- Validate currency conversions.
- Check source dates and superseded reports.
- Review outliers manually.
- Produce a discrepancy log.

### Phase 6 — insight and visualization package

- Identify the 20 strongest quantitative insights.
- Identify 10 counterintuitive findings.
- Identify 10 important caveats.
- Recommend an MVP, Phase 2, and Phase 3 dashboard scope.
- Produce a chart specification for every recommended visual.

## Required deliverables

Deliver all of the following:

1. **Executive research summary** with the most defensible findings and major data gaps.
2. **Master metrics table** in CSV or spreadsheet form.
3. **Data dictionary** defining every field and formula.
4. **Taxonomy crosswalks** for service lines, regions, workforce levels, industries, and legal entities.
5. **Source ledger** with exact citations and source grades.
6. **Office geospatial table** with latitude, longitude, status, and geocoding confidence.
7. **Audit-client table** for the selected company universes.
8. **Audit-quality table** by regulator, jurisdiction, firm, year, and sample.
9. **Regulatory and litigation events table** with status and duplicate controls.
10. **Acquisition, alliance, and strategic-events table.**
11. **Sustainability and social-impact table.**
12. **Workforce and career table.**
13. **Missing-data and non-comparability matrix.**
14. **Derived-metric calculation file** with formulas visible.
15. **Dashboard storyboard and page-level wireframe.**
16. **Visualization catalog** containing chart type, fields, filters, encodings, tooltip content, caveats, and fallback chart.
17. **MVP / should-have / experimental prioritization.**
18. **Update schedule** stating which fields should refresh annually, quarterly, monthly, or on event.
19. **Twenty headline insights, ten surprises, and ten caveats.**
20. **A concise methodology suitable for publishing inside the dashboard.**

## Suggested file structure

- `firms.csv`
- `metrics_long.csv`
- `service_line_crosswalk.csv`
- `geography_crosswalk.csv`
- `workforce_crosswalk.csv`
- `offices.csv`
- `audit_clients.csv`
- `audit_fees.csv`
- `audit_quality.csv`
- `regulatory_events.csv`
- `acquisitions.csv`
- `alliances.csv`
- `sustainability.csv`
- `workforce.csv`
- `careers_and_compensation.csv`
- `public_sector_contracts.csv`
- `sources.csv`
- `data_gaps.csv`
- `derived_metrics.csv`
- `visual_catalog.csv`
- `dashboard_storyboard.md`
- `methodology.md`
- `insights.md`

## Completion criteria

The work is complete only when:

- Every core metric has been researched for all four firms, even when the result is “not disclosed.”
- Every displayed value has an exact source and period.
- Network-level and member-firm-level data are never silently mixed.
- At least ten years of revenue and headcount have been attempted.
- At least five years of service-line, regional, and audit-quality data have been attempted.
- The current office map is fully geocoded, deduplicated, and date-stamped.
- The audit-client universe has a fixed constituent snapshot date and stable company identifiers.
- All derived values can be reproduced from the raw data.
- All rankings pass the comparability threshold.
- Missing data and proxies are visible rather than hidden.
- The final package identifies what belongs in the launch dashboard, what belongs in later releases, and what should be omitted because it is misleading or too weakly sourced.

## Final response format

Return the work in this order:

1. Scope and execution date
2. Latest comparable fiscal periods
3. Executive findings
4. Data availability and comparability matrix
5. Core metric tables
6. Office-map dataset summary
7. Audit-market and client-level findings
8. Workforce and career findings
9. Technology, alliances, sustainability, and risk findings
10. Dashboard architecture and visual specifications
11. MVP / Phase 2 / experimental roadmap
12. Methodology, caveats, and source ledger
13. Links or attachments to all machine-readable files

Do not invent values. Do not conceal scope differences. Make the research package impressive enough that a separate visualization team can build the dashboard without returning for missing definitions, denominators, locations, or citations.
