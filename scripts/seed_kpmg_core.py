#!/usr/bin/env python3
"""Write the reproducible KPMG global-core observation fragment."""

from __future__ import annotations

import csv
from pathlib import Path

from build_research_package import OBSERVATION_FIELDS, ROOT


OUTPUT = ROOT / "data" / "inbox" / "kpmg_observations.csv"
ENTITY_ID = "ent_kpmg_global"
ENTITY_NAME = "KPMG global organization"
rows: list[dict[str, str]] = []
counter = 0


def fiscal_dates(year: int) -> tuple[str, str]:
    return f"{year - 1}-10-01", f"{year}-09-30"


def add(
    metric_id: str,
    fiscal_year: int | None,
    value_numeric: str | float | int = "",
    *,
    source_id: str,
    source_locator: str,
    source_excerpt: str,
    value_original_text: str = "",
    unit_original: str = "",
    unit_canonical: str = "",
    scale_original: str = "",
    currency_original: str = "",
    value_in_original_currency: str | float | int = "",
    value_usd_nominal: str | float | int = "",
    value_low: str | float | int = "",
    value_high: str | float | int = "",
    as_of_date: str = "",
    geography_original: str = "",
    geography_canonical: str = "",
    service_line_original: str = "",
    service_line_canonical: str = "",
    status: str = "reported",
    observation_type: str = "reported",
    definition: str = "",
    extraction_method: str = "manual_web_text",
    comparability_score: str = "3",
    confidence_score: str = "4",
    quality_flag: str = "",
    revision_flag: str = "false",
    supersedes: str = "",
    notes: str = "",
) -> str:
    global counter
    counter += 1
    observation_id = f"obs_kpmg_{counter:04d}"
    period_start = period_end = fiscal_year_label = calendar_year = ""
    if fiscal_year is not None:
        period_start, period_end = fiscal_dates(fiscal_year)
        fiscal_year_label = f"FY{fiscal_year}"
        calendar_year = str(fiscal_year)
    row = {field: "" for field in OBSERVATION_FIELDS}
    row.update({
        "observation_id": observation_id,
        "metric_id": metric_id,
        "firm_network": "KPMG",
        "entity_id": ENTITY_ID,
        "entity_name": ENTITY_NAME,
        "entity_scope": "global_network",
        "jurisdiction": "Global",
        "geography_original": geography_original,
        "geography_canonical": geography_canonical,
        "service_line_original": service_line_original,
        "service_line_canonical": service_line_canonical,
        "period_start": period_start,
        "period_end": period_end,
        "fiscal_year_label": fiscal_year_label,
        "calendar_year": calendar_year,
        "as_of_date": as_of_date,
        "value_original_text": value_original_text,
        "value_numeric": str(value_numeric),
        "value_low": str(value_low),
        "value_high": str(value_high),
        "unit_original": unit_original,
        "unit_canonical": unit_canonical,
        "scale_original": scale_original,
        "currency_original": currency_original,
        "value_in_original_currency": str(value_in_original_currency),
        "value_usd_nominal": str(value_usd_nominal),
        "observation_status": status,
        "reported_calculated_proxy_or_estimate": observation_type,
        "definition_from_source": definition,
        "source_id": source_id,
        "source_locator": source_locator,
        "source_excerpt": source_excerpt,
        "extraction_method": extraction_method,
        "comparability_score": comparability_score,
        "confidence_score": confidence_score,
        "quality_flag": quality_flag,
        "revision_flag": revision_flag,
        "supersedes_observation_id": supersedes,
        "researcher_notes": notes,
    })
    rows.append(row)
    return observation_id


def add_revenue_total(year: int, billions: float, source: str, locator: str, excerpt: str, **kwargs: str) -> str:
    return add(
        "global_revenue_total", year, billions,
        source_id=source, source_locator=locator, source_excerpt=excerpt,
        value_original_text=f"US${billions:g} billion", unit_original="US$ billion",
        unit_canonical="USD_millions", scale_original="billion", currency_original="USD",
        value_in_original_currency=round(billions * 1000, 6), value_usd_nominal=round(billions * 1000, 6),
        definition="Combined or aggregated revenue of independent KPMG member firms; exact terminology and inclusions follow the cited source.",
        comparability_score="4", **kwargs,
    )


def add_money_component(
    metric_id: str, year: int, billions: float, source: str, locator: str, excerpt: str,
    *, geography: str = "", canonical_geography: str = "", service_line: str = "",
    canonical_service_line: str = "", **kwargs: str,
) -> str:
    return add(
        metric_id, year, billions,
        source_id=source, source_locator=locator, source_excerpt=excerpt,
        value_original_text=f"US${billions:g} billion", unit_original="US$ billion",
        unit_canonical="USD_millions", scale_original="billion", currency_original="USD",
        value_in_original_currency=round(billions * 1000, 6), value_usd_nominal=round(billions * 1000, 6),
        geography_original=geography, geography_canonical=canonical_geography,
        service_line_original=service_line, service_line_canonical=canonical_service_line,
        definition="Source-defined global member-firm revenue component.", comparability_score="3", **kwargs,
    )


def add_growth(metric_id: str, year: int, percent: float, source: str, locator: str, excerpt: str, definition: str, **kwargs: str) -> str:
    return add(
        metric_id, year, percent, source_id=source, source_locator=locator,
        source_excerpt=excerpt, value_original_text=f"{percent:g}%", unit_original="percent",
        unit_canonical="percent", definition=definition, comparability_score="3", **kwargs,
    )


def add_people(
    year: int, value: int | str, source: str, locator: str, excerpt: str, definition: str,
    *, original: str | None = None, as_of: str = "", low: int | str = "",
    comparability_score: str = "3", **kwargs: str,
) -> str:
    numeric = value if value != "" else ""
    return add(
        "global_people_total", year, numeric, source_id=source, source_locator=locator,
        source_excerpt=excerpt, value_original_text=original or str(value), value_low=low,
        unit_original="people", unit_canonical="people", as_of_date=as_of,
        definition=definition, comparability_score=comparability_score, **kwargs,
    )


# Global revenue totals, FY2010-FY2025.
add_revenue_total(2010, 20.63, "src_kpmg_ar2011", "PDF p.32, Total Revenues chart", "FY10 $20.63 billion")
add_revenue_total(2011, 22.71, "src_kpmg_ar2011", "PDF p.32, Global Total Revenues", "FY11 $22.71 billion")
add_revenue_total(2012, 23.03, "src_kpmg_ar2013", "PDF p.28, Global total revenues", "FY12 23.03")
add_revenue_total(2013, 23.42, "src_kpmg_ar2013", "PDF p.28, Global total revenues", "FY13 23.42")
add_revenue_total(2014, 24.82, "src_kpmg_ar2014", "PDF p.37, Global total revenues", "FY14 $24.82")
add_revenue_total(2015, 24.44, "src_kpmg_ar2015", "PDF p.37, Financials and organization", "FY15 $24.44")
add_revenue_total(2016, 25.42, "src_kpmg_ar2016", "PDF p.36, By function", "FY16 $25.42 billion")
add_revenue_total(2017, 26.40, "src_kpmg_ar2017", "PDF p.40, Financials", "FY17 $26.40 billion")
add_revenue_total(2018, 28.96, "src_kpmg_fy18", "PDF p.1 and p.4, highlights/table", "FY18 US$28.96 billion")
add_revenue_total(2019, 29.75, "src_kpmg_ar2019", "PDF p.49, FY19 global revenue table", "Combined global revenues $29.75 billion", extraction_method="official_search_index", quality_flag="verify_pdf_on_refresh")
add_revenue_total(2020, 29.22, "src_kpmg_fy20", "Highlights and opening paragraph", "FY20 global revenue US$29.22 billion")
add_revenue_total(2021, 32.13, "src_kpmg_fy21", "Opening paragraph and revenue table", "FY21 $32.13 billion")
add_revenue_total(2022, 34.64, "src_kpmg_fy22", "Notes to editors, FY22 revenue table", "FY22 total 34.64")
add_revenue_total(2023, 36.4, "src_kpmg_fy23", "Notes to editors, FY23 revenue table", "FY23 total 36.4")
fy24_total_original = add_revenue_total(2024, 38.4, "src_kpmg_fy24", "Notes to editors, FY24 revenue table", "FY24 total 38.4", quality_flag="exclude_from_primary", notes="Superseded for continuing-operations comparisons by the FY25 release's restated FY24 value.")
add_revenue_total(2024, 37.8, "src_kpmg_fy25", "Embedded Revenue Region/Function tables", "FY24 37.8", revision_flag="true", supersedes=fy24_total_original, extraction_method="embedded_infogram_json", notes="Restated on a continuing-operations basis after divestitures and exits; preferred for FY24-to-FY25 comparison.")
add_revenue_total(2025, 39.8, "src_kpmg_fy25", "Opening paragraph and embedded revenue tables", "FY25 39.8", extraction_method="embedded_infogram_json", notes="Continuing-operations headline basis.")
add_revenue_total(2025, 40.2, "src_kpmg_fy25", "Notes to editors", "FY25 full basis US$40.2 billion", quality_flag="exclude_from_primary", notes="Full-basis alternative; the continuing-operations headline is US$39.8 billion.")

# Source-reported growth rates. No calculated growth is placed in the raw layer.
add_growth("global_revenue_growth_usd", 2011, 10.1, "src_kpmg_ar2011", "PDF p.32, Global Total Revenues", "10.1 percent in U.S. dollars", "US-dollar growth based on reported member-firm revenue.")
add_growth("global_revenue_growth_local_currency", 2011, 6.2, "src_kpmg_ar2011", "PDF p.32, Global Total Revenues", "6.2 percent in local currency", "Local-currency growth.")
add_growth("global_revenue_growth_local_currency", 2015, 8.1, "src_kpmg_ar2015", "PDF p.37, Financials and organization", "Growth 8.1%", "Local-currency growth.", extraction_method="visual_pdf_table")
add_growth("global_revenue_growth_local_currency", 2016, 8.0, "src_kpmg_ar2016", "PDF p.36, Growth", "Growth 8.0%", "Local-currency growth.")
add_growth("global_revenue_growth_local_currency", 2017, 4.8, "src_kpmg_ar2017", "PDF p.40, FY17 global revenue growth", "Revenue growth 4.8%", "Local-currency growth.")
add_growth("global_revenue_growth_local_currency", 2018, 7.1, "src_kpmg_fy18", "PDF p.1 and p.4", "FY18 local growth 7.1%", "Local-currency growth.")
add_growth("global_revenue_growth_usd", 2018, 9.7, "src_kpmg_fy18", "PDF p.4, revenue table", "Total US$ Growth 9.7%", "US-dollar growth.")
add_growth("global_revenue_growth_local_currency", 2019, 6.2, "src_kpmg_ar2019", "PDF p.49, FY19 summary", "Revenue growth 6.2% in local currency", "Local-currency growth.", extraction_method="official_search_index", quality_flag="verify_pdf_on_refresh")
add_growth("global_revenue_growth_usd", 2021, 10.0, "src_kpmg_fy21", "Opening paragraph", "10% increase in US dollar revenues", "US-dollar growth.")
add_growth("global_revenue_growth_reported", 2022, 14.0, "src_kpmg_fy22", "Opening paragraph and footnote", "increase of 14%", "Headline continuing-operations growth; excludes businesses sold or exited.")
add_growth("global_revenue_growth_local_currency", 2022, 13.0, "src_kpmg_fy22", "Notes to editors, total row", "Total local growth 13%", "Unrestated local-currency growth; the continuing-operations headline is 14%.")
add_growth("global_revenue_growth_local_currency", 2023, 8.0, "src_kpmg_fy23", "Notes to editors, total row", "Total local growth 8%", "Local-currency growth at consistent exchange rates.")
add_growth("global_revenue_growth_usd", 2023, 5.0, "src_kpmg_fy23", "Notes to editors, total row", "Total US$ growth 5%", "US-dollar growth derived by the firm from unrounded values.")
add_growth("global_revenue_growth_local_currency", 2024, 5.1, "src_kpmg_fy24", "Notes to editors, total row", "Total local growth 5.1%", "Local-currency growth at consistent exchange rates.", quality_flag="exclude_from_primary", notes="Original FY24 publication; FY25 later restated the comparison perimeter.")
add_growth("global_revenue_growth_usd", 2024, 5.4, "src_kpmg_fy24", "Notes to editors, total row", "Total US$ growth 5.4%", "US-dollar growth derived by the firm from unrounded values.", quality_flag="exclude_from_primary", notes="Original FY24 publication; FY25 later restated the comparison perimeter.")
add_growth("global_revenue_growth_local_currency", 2025, 5.1, "src_kpmg_fy25", "Opening paragraph and embedded tables", "Local growth 5.1%", "Continuing-operations local-currency growth at consistent exchange rates.", extraction_method="embedded_infogram_json")
add_growth("global_revenue_growth_usd", 2025, 5.4, "src_kpmg_fy25", "Opening paragraph and embedded tables", "US$ growth 5.4%", "Continuing-operations US-dollar growth derived by the firm from unrounded values.", extraction_method="embedded_infogram_json")

# Workforce. Missing FY2010/FY2011 rows make attempted coverage explicit.
add_people(2010, "", "src_kpmg_ar2011", "Annual review searched", "No defensible FY2010 workforce total located.", "Missing after documented search; timing and population definition are unavailable.", original="not found after search", status="not_found_after_search", observation_type="", comparability_score="1", notes="See search_kpmg_0001.")
add_people(2011, "", "src_kpmg_ar2011", "Annual review and official 2012 publications searched", "No value with an explicit FY2011 timing basis located.", "Missing after documented search; timing and population definition are unavailable.", original="not found after search", status="not_found_after_search", observation_type="", comparability_score="1", notes="Official 2012 publications say 145000 people but do not establish the number as FY2011 average or period-end; see search_kpmg_0002.")
add_people(2012, 152390, "src_kpmg_ar2013", "PDF p.29, People table", "FY12 total 152390", "Source table total people; timing basis not explicit in the cited table.")
add_people(2013, 155180, "src_kpmg_ar2013", "PDF p.29, People table", "FY13 total 155180", "Source table total people; timing basis not explicit in the cited table.")
add_people(2014, 162031, "src_kpmg_ar2014", "PDF p.38, People table", "FY14 total 162031", "Average FTE during the fiscal year.")
add_people(2015, 173965, "src_kpmg_ar2015", "PDF p.37 and p.40, People", "FY15 total 173965", "Average FTE during the fiscal year.", extraction_method="visual_pdf_table")
add_people(2016, 188982, "src_kpmg_ar2016", "PDF p.39, People", "188982 people worldwide", "Average FTE during the fiscal year.")
add_people(2017, 197263, "src_kpmg_ar2017", "PDF p.40 and p.43, People", "197263 people", "Average FTE during the fiscal year.")
add_people(2018, 207000, "src_kpmg_fy18", "PDF p.1-p.2, workforce highlights", "record-high of 207000 people", "Average FTE during the fiscal year; value is rounded as published.", original="207,000")
add_people(2019, 219281, "src_kpmg_ar2019", "PDF p.49, FY19 summary", "People 219281", "Source-described global people count; report should be rechecked for average/period-end timing.", extraction_method="official_search_index", quality_flag="verify_pdf_on_refresh")
add_people(2020, 226882, "src_kpmg_fy21", "Notes to editors, comparative average FTE", "226882 reported in FY20", "Average FTE during FY2020.")
add_people(2021, 230477, "src_kpmg_fy21", "Notes to editors", "average FTE for FY21 was 230477", "Average FTE during FY2021.", quality_flag="average_fte")
add_people(2021, "", "src_kpmg_fy21", "Our people define who we are", "more than 236000 partners and employees", "Period-end partners and employees as of 30 September 2021; source provides only a lower-bound rounded value.", original="more than 236,000", low=236000, as_of="2021-09-30", quality_flag="lower_bound")
add_people(2022, 265646, "src_kpmg_fy23", "Headcount table, FY22 comparative", "FY22 total 265646", "Partners and staff employed as of 30 September 2022.", as_of="2022-09-30")
add_people(2023, 273424, "src_kpmg_fy23", "Headcount table", "FY23 total 273424", "Partners and staff employed as of 30 September 2023.", as_of="2023-09-30")
fy24_people_original = add_people(2024, 275288, "src_kpmg_fy24", "Headcount table", "FY24 total 275288", "Partners and staff employed as of 30 September 2024.", as_of="2024-09-30", quality_flag="exclude_from_primary", notes="FY25 release later supplied a restated continuing-operations FY24 comparison.")
add_people(2024, 271230, "src_kpmg_fy25", "Embedded Headcount Region table", "FY24 total 271230", "FY24 headcount restated on a continuing-operations basis.", as_of="2024-09-30", revision_flag="true", supersedes=fy24_people_original, extraction_method="embedded_infogram_json")
add_people(2025, 276030, "src_kpmg_fy25", "Talent section and embedded headcount tables", "FY25 total 276030", "Partners and staff employed as of 30 September 2025.", as_of="2025-09-30", extraction_method="embedded_infogram_json")

# Service-line revenue, FY2015-FY2025.
service_years = {
    2015: ("src_kpmg_ar2015", "PDF p.39, By function", "visual_pdf_table", {"Audit": 10.03, "Tax": 5.31, "Advisory": 9.10}),
    2016: ("src_kpmg_ar2016", "PDF p.36, By function", "manual_web_text", {"Audit": 10.12, "Tax": 5.56, "Advisory": 9.74}),
    2017: ("src_kpmg_ar2017", "PDF p.40, Function", "manual_web_text", {"Audit": 10.39, "Tax": 5.83, "Advisory": 10.18}),
    2018: ("src_kpmg_fy18", "PDF p.4, Functions table", "manual_web_text", {"Audit": 11.15, "Tax": 6.34, "Advisory": 11.47}),
    2019: ("src_kpmg_ar2019", "PDF p.49, function-by-region table", "official_search_index", {"Audit": 11.18, "Tax & Legal": 6.62, "Advisory": 11.95}),
    2020: ("src_kpmg_fy20", "Service-line sections", "manual_web_text", {"Audit": 11.07, "Tax and Legal Services": 6.48, "Advisory": 11.67}),
    2021: ("src_kpmg_fy21", "Revenue table", "manual_web_text", {"Audit": 11.46, "Tax and Legal Services": 7.02, "Advisory": 13.65}),
    2022: ("src_kpmg_fy22", "Notes to editors, Functions table", "manual_web_text", {"Audit": 11.85, "Tax and Legal Services": 7.35, "Advisory": 15.44}),
    2023: ("src_kpmg_fy23", "Notes to editors, Functions table", "manual_web_text", {"Audit": 12.6, "Tax and Legal Services": 7.9, "Advisory": 15.9}),
}
canonical_service = {
    "Audit": "audit_assurance_attest", "Tax": "tax_legal", "Tax & Legal": "tax_legal",
    "Tax and Legal Services": "tax_legal", "Tax & Legal Services": "tax_legal",
    "Advisory": "combined_not_separable",
}
for year, (source, locator, method, values) in service_years.items():
    for label, value in values.items():
        add_money_component(
            "global_revenue_service_line", year, value, source, locator, f"{label} {value:g}",
            service_line=label, canonical_service_line=canonical_service[label], extraction_method=method,
            quality_flag="verify_pdf_on_refresh" if year == 2019 else "",
        )

fy24_service_original: dict[str, str] = {}
for label, value in {"Audit": 13.4, "Tax & Legal Services": 8.7, "Advisory": 16.3}.items():
    fy24_service_original[label] = add_money_component(
        "global_revenue_service_line", 2024, value, "src_kpmg_fy24", "Notes to editors, Functions table",
        f"{label} {value:g}", service_line=label, canonical_service_line=canonical_service[label],
        quality_flag="exclude_from_primary", notes="Original FY24 value later restated on a continuing-operations basis.",
    )
for label, value in {"Audit": 13.3, "Tax & Legal Services": 8.6, "Advisory": 15.9}.items():
    add_money_component(
        "global_revenue_service_line", 2024, value, "src_kpmg_fy25", "Embedded Revenue Function table",
        f"FY24 {label} {value:g}", service_line=label, canonical_service_line=canonical_service[label],
        revision_flag="true", supersedes=fy24_service_original[label], extraction_method="embedded_infogram_json",
        notes="Restated continuing-operations comparison.",
    )
for label, value in {"Audit": 14.1, "Tax & Legal": 9.3, "Advisory": 16.4}.items():
    add_money_component(
        "global_revenue_service_line", 2025, value, "src_kpmg_fy25", "Embedded Revenue Function table",
        f"FY25 {label} {value:g}", service_line=label, canonical_service_line=canonical_service[label],
        extraction_method="embedded_infogram_json",
    )

# Regional revenue, FY2015-FY2025.
region_years = {
    2015: ("src_kpmg_ar2015", "PDF p.38, By region", "visual_pdf_table", {"Americas": 9.34, "Asia Pacific": 3.79, "EMA": 11.31}),
    2016: ("src_kpmg_ar2016", "PDF p.35, By region", "manual_web_text", {"Americas": 10.02, "Asia Pacific": 4.06, "EMA": 11.34}),
    2017: ("src_kpmg_ar2017", "PDF p.40, regional totals", "manual_web_text", {"Americas": 10.48, "Asia Pacific": 4.42, "EMA": 11.50}),
    2018: ("src_kpmg_fy18", "PDF p.4, Regions table", "manual_web_text", {"Americas": 11.10, "Asia Pacific": 4.88, "EMA": 12.98}),
    2019: ("src_kpmg_ar2019", "PDF p.49, regional table", "official_search_index", {"Americas": 11.72, "Asia Pacific": 5.14, "EMA": 12.89}),
    2020: ("src_kpmg_fy20", "Resilient regional performance", "manual_web_text", {"Americas": 11.22, "Asia Pacific": 5.26, "EMA": 12.74}),
    2021: ("src_kpmg_fy21", "Revenue table, Regions", "manual_web_text", {"Americas": 11.88, "Asia Pacific": 5.97, "EMA": 14.28}),
    2022: ("src_kpmg_fy22", "Notes to editors, Regions table", "manual_web_text", {"Americas": 13.71, "Asia Pacific": 6.31, "EMA": 14.62}),
    2023: ("src_kpmg_fy23", "Notes to editors, Regions table", "manual_web_text", {"Americas": 14.6, "Asia Pacific": 6.1, "EMA": 15.7}),
}
canonical_region = {"Americas": "Americas", "Asia Pacific": "Asia-Pacific", "EMA": "Europe; Middle East and Africa"}
for year, (source, locator, method, values) in region_years.items():
    for label, value in values.items():
        add_money_component(
            "global_revenue_region", year, value, source, locator, f"{label} {value:g}",
            geography=label, canonical_geography=canonical_region[label], extraction_method=method,
            quality_flag="verify_pdf_on_refresh" if year == 2019 else "",
        )

fy24_region_original: dict[str, str] = {}
for label, value in {"Americas": 15.2, "Asia Pacific": 6.0, "EMA": 17.2}.items():
    fy24_region_original[label] = add_money_component(
        "global_revenue_region", 2024, value, "src_kpmg_fy24", "Notes to editors, Regions table",
        f"{label} {value:g}", geography=label, canonical_geography=canonical_region[label],
        quality_flag="exclude_from_primary", notes="Original FY24 value; FY25 later restated the continuing-operations perimeter.",
    )
for label, value in {"Americas": 15.2, "Asia Pacific": 6.0, "EMA": 16.6}.items():
    add_money_component(
        "global_revenue_region", 2024, value, "src_kpmg_fy25", "Embedded Revenue Region table",
        f"FY24 {label} {value:g}", geography=label, canonical_geography=canonical_region[label],
        revision_flag="true", supersedes=fy24_region_original[label], extraction_method="embedded_infogram_json",
        notes="Restated continuing-operations comparison.",
    )
for label, value in {"Americas": 15.9, "Asia Pacific": 6.2, "EMA": 17.7}.items():
    add_money_component(
        "global_revenue_region", 2025, value, "src_kpmg_fy25", "Embedded Revenue Region table",
        f"FY25 {label} {value:g}", geography=label, canonical_geography=canonical_region[label],
        extraction_method="embedded_infogram_json",
    )

# Selected physical-scale facts. Combined-country-and-territory values are never relabeled as countries only.
add("global_country_territory_count", 2017, 154, source_id="src_kpmg_ar2017", source_locator="PDF p.46, Where we work", source_excerpt="presence in 154 countries and territories", value_original_text="154 countries and territories", unit_original="countries and territories", unit_canonical="countries_and_territories", as_of_date="2017-09-30", definition="KPMG member-firm presence.")
add("global_country_count", 2018, 153, source_id="src_kpmg_fy18", source_locator="PDF p.5, About KPMG International", source_excerpt="operate in 153 countries", value_original_text="153 countries", unit_original="countries", unit_canonical="countries", as_of_date="2018-09-30", definition="Countries in which KPMG operated.")
add("global_country_territory_count", 2020, 146, source_id="src_kpmg_fy20", source_locator="Highlights", source_excerpt="across 146 countries and territories", value_original_text="146 countries and territories", unit_original="countries and territories", unit_canonical="countries_and_territories", as_of_date="2020-09-30", definition="KPMG global presence.")
add("global_country_territory_count", 2022, 143, source_id="src_kpmg_fy22", source_locator="About KPMG", source_excerpt="operate in 143 countries and territories", value_original_text="143 countries and territories", unit_original="countries and territories", unit_canonical="countries_and_territories", as_of_date="2022-09-30", definition="KPMG member-firm operations.")
add("global_country_territory_count", 2025, 138, source_id="src_kpmg_fy25", source_locator="About KPMG International", source_excerpt="operate in 138 countries and territories", value_original_text="138 countries and territories", unit_original="countries and territories", unit_canonical="countries_and_territories", as_of_date="2025-09-30", definition="KPMG member-firm operations.")


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=OBSERVATION_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} KPMG observations to {OUTPUT}")
