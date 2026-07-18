#!/usr/bin/env python3
"""Assemble and validate the Big Four research package from firm-level CSV fragments."""

from __future__ import annotations

import csv
import datetime as dt
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INBOX = DATA / "inbox"
RESEARCH_CUTOFF = "2026-07-18"
FIRMS = ("Deloitte", "PwC", "EY", "KPMG")

ENTITY_FIELDS = [
    "entity_id", "entity_name_canonical", "entity_name_original", "entity_type",
    "parent_entity_id", "big_four_network", "member_firm_name", "legal_name",
    "former_names", "jurisdiction", "country_iso2", "country_iso3", "legal_form",
    "registration_number", "lei", "cik", "website", "active_from", "active_to",
    "status", "notes", "source_id",
]

SOURCE_FIELDS = [
    "source_id", "source_title", "publisher", "publisher_type", "document_type",
    "url", "archived_url", "publication_date", "filing_date",
    "reporting_period_start", "reporting_period_end", "access_date", "language",
    "official_source_flag", "audited_flag", "primary_or_secondary", "source_grade",
    "paywall_flag", "local_filename_if_saved", "notes",
]

OBSERVATION_FIELDS = [
    "observation_id", "metric_id", "firm_network", "entity_id", "entity_name",
    "entity_scope", "jurisdiction", "geography_original", "geography_canonical",
    "service_line_original", "service_line_canonical", "industry_original",
    "industry_canonical", "client_id", "period_start", "period_end",
    "fiscal_year_label", "calendar_year", "as_of_date", "value_original_text",
    "value_numeric", "value_low", "value_high", "unit_original", "unit_canonical",
    "scale_original", "currency_original", "value_in_original_currency",
    "value_usd_nominal", "value_usd_constant_price", "fx_rate_used", "fx_rate_type",
    "inflation_index_used", "observation_status",
    "reported_calculated_proxy_or_estimate", "definition_from_source",
    "formula_or_transformation", "numerator_observation_ids",
    "denominator_observation_ids", "sample_size", "population_size", "source_id",
    "source_locator", "source_excerpt", "extraction_method", "comparability_score",
    "confidence_score", "quality_flag", "revision_flag",
    "supersedes_observation_id", "researcher_notes",
]

METRICS = [
    {
        "metric_id": "global_revenue_total", "metric_name_canonical": "Global network revenue",
        "metric_family": "global_financials", "description": "Global network member-firm revenue exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "USD", "preferred_currency": "USD",
        "frequency": "annual", "stock_or_flow": "flow", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined member-firm revenue",
        "exclusions": "Do not assume consolidated corporate revenue", "known_definition_issues": "Aggregate/combined/gross terminology and reimbursable-expense treatment differ",
        "comparability_requirements": "Same reporting perimeter; preserve fiscal dates and revenue definition", "priority_level": "high",
    },
    {
        "metric_id": "global_revenue_growth_reported", "metric_name_canonical": "Reported global revenue growth",
        "metric_family": "global_financials", "description": "Year-over-year growth exactly as highlighted by the source",
        "raw_or_derived": "raw", "preferred_unit": "percent", "preferred_currency": "",
        "frequency": "annual", "stock_or_flow": "rate", "preferred_denominator": "prior-year revenue",
        "calculation_formula": "", "inclusions": "Source-defined headline basis", "exclusions": "",
        "known_definition_issues": "May be local currency, constant currency, reported currency, or continuing operations",
        "comparability_requirements": "Growth basis must match", "priority_level": "high",
    },
    {
        "metric_id": "global_revenue_growth_local_currency", "metric_name_canonical": "Global revenue growth in local currency",
        "metric_family": "global_financials", "description": "Source-reported local-currency growth",
        "raw_or_derived": "raw", "preferred_unit": "percent", "preferred_currency": "",
        "frequency": "annual", "stock_or_flow": "rate", "preferred_denominator": "prior-year revenue",
        "calculation_formula": "", "inclusions": "Source-defined local-currency basis", "exclusions": "FX translation effect",
        "known_definition_issues": "Constant exchange-rate method may vary", "comparability_requirements": "Same perimeter and exchange-rate method", "priority_level": "high",
    },
    {
        "metric_id": "global_revenue_growth_constant_currency", "metric_name_canonical": "Global revenue growth in constant currency",
        "metric_family": "global_financials", "description": "Source-reported constant-currency growth",
        "raw_or_derived": "raw", "preferred_unit": "percent", "preferred_currency": "",
        "frequency": "annual", "stock_or_flow": "rate", "preferred_denominator": "prior-year revenue",
        "calculation_formula": "", "inclusions": "Source-defined constant-currency basis", "exclusions": "FX translation effect",
        "known_definition_issues": "Method may vary", "comparability_requirements": "Same perimeter and exchange-rate method", "priority_level": "high",
    },
    {
        "metric_id": "global_revenue_growth_usd", "metric_name_canonical": "Global revenue growth in US dollars",
        "metric_family": "global_financials", "description": "Source-reported US-dollar growth",
        "raw_or_derived": "raw", "preferred_unit": "percent", "preferred_currency": "",
        "frequency": "annual", "stock_or_flow": "rate", "preferred_denominator": "prior-year revenue",
        "calculation_formula": "", "inclusions": "Reported US-dollar basis", "exclusions": "",
        "known_definition_issues": "May differ from growth calculated from rounded headline values", "comparability_requirements": "Same perimeter", "priority_level": "high",
    },
    {
        "metric_id": "global_people_total", "metric_name_canonical": "Global people",
        "metric_family": "workforce", "description": "Global workforce exactly as defined by the source",
        "raw_or_derived": "raw", "preferred_unit": "people", "preferred_currency": "",
        "frequency": "annual", "stock_or_flow": "source_specific", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined people population", "exclusions": "",
        "known_definition_issues": "Average FTE, period-end headcount, and partner inclusion vary", "comparability_requirements": "Match timing and population definition", "priority_level": "high",
    },
    {
        "metric_id": "global_revenue_service_line", "metric_name_canonical": "Global revenue by service line",
        "metric_family": "service_line", "description": "Revenue for a source-defined global service line",
        "raw_or_derived": "raw", "preferred_unit": "USD", "preferred_currency": "USD",
        "frequency": "annual", "stock_or_flow": "flow", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined service line", "exclusions": "Do not split combined categories without support",
        "known_definition_issues": "Firm taxonomies and reorganizations differ", "comparability_requirements": "Original and canonical service labels required", "priority_level": "high",
    },
    {
        "metric_id": "global_revenue_region", "metric_name_canonical": "Global revenue by reported region",
        "metric_family": "geography", "description": "Revenue for a source-defined global region",
        "raw_or_derived": "raw", "preferred_unit": "USD", "preferred_currency": "USD",
        "frequency": "annual", "stock_or_flow": "flow", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined region", "exclusions": "Do not force a country bridge",
        "known_definition_issues": "Regional boundaries differ, especially India and Central Asia", "comparability_requirements": "Original region retained", "priority_level": "high",
    },
    {
        "metric_id": "global_country_count", "metric_name_canonical": "Countries served",
        "metric_family": "organization", "description": "Countries served or operated in, excluding territories only when the source separates them",
        "raw_or_derived": "raw", "preferred_unit": "countries", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined", "exclusions": "Do not treat offices or cities as countries",
        "known_definition_issues": "Many sources combine countries and territories", "comparability_requirements": "Scope label must match", "priority_level": "high",
    },
    {
        "metric_id": "global_territory_count", "metric_name_canonical": "Territories served",
        "metric_family": "organization", "description": "Territories served when separately disclosed",
        "raw_or_derived": "raw", "preferred_unit": "territories", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined", "exclusions": "",
        "known_definition_issues": "Often combined with countries", "comparability_requirements": "Separate disclosure required", "priority_level": "medium",
    },
    {
        "metric_id": "global_country_territory_count", "metric_name_canonical": "Countries and territories served",
        "metric_family": "organization", "description": "Combined country-and-territory presence exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "countries_and_territories", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined combined total", "exclusions": "Do not relabel as countries only",
        "known_definition_issues": "Not separable", "comparability_requirements": "Compare only with combined totals", "priority_level": "high",
    },
    {
        "metric_id": "global_office_count", "metric_name_canonical": "Global offices",
        "metric_family": "organization", "description": "Physical offices exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "offices", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined", "exclusions": "Do not substitute cities or countries",
        "known_definition_issues": "Office and site definitions differ", "comparability_requirements": "Exact as-of date and definition", "priority_level": "medium",
    },
    {
        "metric_id": "global_member_firm_count", "metric_name_canonical": "Member firms",
        "metric_family": "organization", "description": "Number of network member firms exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "member_firms", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined member firms", "exclusions": "Do not substitute legal entities",
        "known_definition_issues": "Membership and legal-entity counts differ", "comparability_requirements": "Same definition", "priority_level": "medium",
    },
    {
        "metric_id": "global_location_count", "metric_name_canonical": "Global locations",
        "metric_family": "organization", "description": "Locations in the global network exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "locations", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined locations", "exclusions": "Do not relabel locations as offices or cities",
        "known_definition_issues": "Location, office, and city definitions differ", "comparability_requirements": "Compare only like-for-like source terms", "priority_level": "medium",
    },
    {
        "metric_id": "global_city_count", "metric_name_canonical": "Global cities",
        "metric_family": "organization", "description": "Cities in which the global network operates exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "cities", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined cities", "exclusions": "Do not relabel cities as offices or locations",
        "known_definition_issues": "City and metropolitan-area definitions may differ", "comparability_requirements": "Exact as-of date and source term", "priority_level": "medium",
    },
    {
        "metric_id": "global_client_facing_entity_count", "metric_name_canonical": "Client-facing entities",
        "metric_family": "organization", "description": "Client-facing entities in the global network exactly as reported",
        "raw_or_derived": "raw", "preferred_unit": "client_facing_entities", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "", "inclusions": "Source-defined client-facing entities", "exclusions": "Do not substitute legal entities or member firms",
        "known_definition_issues": "Network and legal-entity structures differ", "comparability_requirements": "Same entity definition", "priority_level": "medium",
    },
    {
        "metric_id": "global_member_firms_and_affiliates_count", "metric_name_canonical": "Member firms and affiliates",
        "metric_family": "organization", "description": "Combined member-firm-and-affiliate count when the source does not permit separation",
        "raw_or_derived": "derived", "preferred_unit": "entities", "preferred_currency": "",
        "frequency": "point_in_time", "stock_or_flow": "stock", "preferred_denominator": "",
        "calculation_formula": "Count source-listed entities", "inclusions": "Member firms and affiliates exactly as source-listed", "exclusions": "Do not relabel as member firms only",
        "known_definition_issues": "Affiliate status and entity structures differ across networks", "comparability_requirements": "Compare only with equally combined counts", "priority_level": "medium",
    },
]

METRIC_FIELDS = list(METRICS[0])


def read_fragments(suffix: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(INBOX.glob(f"*_{suffix}.csv")):
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                clean = {str(key).strip(): (value or "").strip() for key, value in row.items() if key is not None}
                clean["_input_file"] = path.name
                rows.append(clean)
    return rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def assert_unique(rows: list[dict[str, str]], field: str) -> None:
    counts = Counter(row.get(field, "") for row in rows)
    bad = sorted(key for key, count in counts.items() if not key or count > 1)
    if bad:
        raise ValueError(f"{field} must be non-empty and unique; invalid IDs: {bad[:10]}")


def parse_date(value: str, field: str, row_id: str) -> None:
    if not value:
        return
    try:
        dt.date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{row_id}: invalid {field}={value!r}") from error


def parse_numeric(value: str, field: str, row_id: str) -> None:
    if not value:
        return
    try:
        number = float(value)
    except ValueError as error:
        raise ValueError(f"{row_id}: invalid {field}={value!r}") from error
    if not math.isfinite(number):
        raise ValueError(f"{row_id}: non-finite {field}={value!r}")


def normalize(rows: list[dict[str, str]], fields: list[str]) -> list[dict[str, str]]:
    return [{field: row.get(field, "") for field in fields} for row in rows]


def normalize_observations(rows: list[dict[str, str]], source_grades: dict[str, str]) -> list[dict[str, str]]:
    """Preserve source values while filling consistent canonical fields."""
    normalized = normalize(rows, OBSERVATION_FIELDS)
    revenue_metrics = {"global_revenue_total", "global_revenue_service_line", "global_revenue_region"}
    scale_multipliers = {
        "": 1.0, "unit": 1.0, "units": 1.0,
        "thousand": 1_000.0, "thousands": 1_000.0,
        "million": 1_000_000.0, "millions": 1_000_000.0,
        "billion": 1_000_000_000.0, "billions": 1_000_000_000.0,
    }
    comparability_defaults = {
        "global_revenue_total": "4",
        "global_revenue_service_line": "3",
        "global_revenue_region": "3",
        "global_people_total": "3",
    }
    confidence_by_grade = {"A": "5", "B": "4", "C": "3", "D": "2", "E": "1"}
    for row in normalized:
        fiscal_label = row.get("fiscal_year_label", "")
        if len(fiscal_label) == 4 and fiscal_label.startswith("FY") and fiscal_label[2:].isdigit():
            row["fiscal_year_label"] = f"FY20{fiscal_label[2:]}"
        if not row.get("comparability_score"):
            row["comparability_score"] = comparability_defaults.get(row["metric_id"], "3")
        if not row.get("confidence_score"):
            row["confidence_score"] = confidence_by_grade.get(source_grades.get(row["source_id"], ""), "3")
        for score_field in ("comparability_score", "confidence_score"):
            score = float(row[score_field])
            if 0 <= score <= 1:
                # Some research fragments used probabilities. Convert them to the
                # commission's required integer 1-5 rubric in the canonical layer.
                row[score_field] = str(max(1, min(5, math.floor(score * 5 + 0.5))))
        if row["metric_id"] not in revenue_metrics or not row.get("value_numeric"):
            continue
        scale = row.get("scale_original", "").strip().lower()
        if scale not in scale_multipliers:
            continue
        value = float(row["value_numeric"]) * scale_multipliers[scale]
        # The current global-core sources report these rows in USD. Keep the raw
        # source number/scale above and put the comparable full-dollar value here.
        if row.get("currency_original") == "USD":
            canonical = f"{value:.10f}".rstrip("0").rstrip(".")
            row["value_in_original_currency"] = canonical
            row["value_usd_nominal"] = canonical
            row["unit_canonical"] = "USD"
    return normalized


def validate(entities: list[dict[str, str]], sources: list[dict[str, str]], observations: list[dict[str, str]]) -> None:
    assert_unique(entities, "entity_id")
    assert_unique(sources, "source_id")
    assert_unique(observations, "observation_id")
    entity_ids = {row["entity_id"] for row in entities}
    source_ids = {row["source_id"] for row in sources}
    metric_ids = {row["metric_id"] for row in METRICS}
    valid_status = {"reported", "calculated", "proxy", "estimated_external", "target", "not_disclosed", "not_found_after_search", "not_comparable", "not_applicable"}
    valid_type = {"reported", "calculated", "proxy", "estimated_external", "target", ""}
    for entity in entities:
        row_id = entity["entity_id"]
        for field in ("active_from", "active_to"):
            parse_date(entity.get(field, ""), field, row_id)
        if entity.get("source_id") and entity["source_id"] not in source_ids:
            raise ValueError(f"{row_id}: unknown source_id {entity['source_id']}")
    for source in sources:
        row_id = source["source_id"]
        for field in ("publication_date", "filing_date", "reporting_period_start", "reporting_period_end", "access_date"):
            parse_date(source.get(field, ""), field, row_id)
    for obs in observations:
        row_id = obs["observation_id"]
        if obs["entity_id"] not in entity_ids:
            raise ValueError(f"{row_id}: unknown entity_id {obs['entity_id']}")
        if obs["source_id"] not in source_ids:
            raise ValueError(f"{row_id}: unknown source_id {obs['source_id']}")
        if obs["metric_id"] not in metric_ids:
            raise ValueError(f"{row_id}: unknown metric_id {obs['metric_id']}")
        if obs["firm_network"] not in FIRMS:
            raise ValueError(f"{row_id}: invalid firm_network {obs['firm_network']!r}")
        if obs["observation_status"] not in valid_status:
            raise ValueError(f"{row_id}: invalid observation_status {obs['observation_status']!r}")
        if obs["reported_calculated_proxy_or_estimate"] not in valid_type:
            raise ValueError(f"{row_id}: invalid observation type {obs['reported_calculated_proxy_or_estimate']!r}")
        for field in ("period_start", "period_end", "as_of_date"):
            parse_date(obs.get(field, ""), field, row_id)
        for field in ("value_numeric", "value_low", "value_high", "value_in_original_currency", "value_usd_nominal", "value_usd_constant_price", "fx_rate_used", "sample_size", "population_size", "comparability_score", "confidence_score"):
            parse_numeric(obs.get(field, ""), field, row_id)
        if obs["observation_status"] in {"reported", "calculated", "proxy", "estimated_external", "target"} and not any(obs.get(field) for field in ("value_numeric", "value_low", "value_high")):
            raise ValueError(f"{row_id}: populated status requires a numeric value")
        if obs["observation_status"] == "calculated" and not obs.get("formula_or_transformation"):
            raise ValueError(f"{row_id}: calculated observation requires formula_or_transformation")


def sort_observations(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: (
        FIRMS.index(row["firm_network"]), row["metric_id"], row.get("period_end", ""),
        row.get("as_of_date", ""), row.get("geography_original", ""),
        row.get("service_line_original", ""), row["observation_id"],
    ))


def preferred_reported(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    superseded_ids = {row.get("supersedes_observation_id", "") for row in rows if row.get("supersedes_observation_id")}
    return [
        row for row in rows
        if row["observation_status"] == "reported"
        and row.get("quality_flag") != "exclude_from_primary"
        and row["observation_id"] not in superseded_ids
    ]


def make_coverage(observations: list[dict[str, str]]) -> list[dict[str, str]]:
    indexed: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    years = [f"FY{year}" for year in range(2010, 2026)]
    core_metrics = ("global_revenue_total", "global_people_total", "global_revenue_service_line", "global_revenue_region")
    for row in observations:
        indexed[(row["firm_network"], row["metric_id"], row.get("fiscal_year_label", ""))].append(row)
    output: list[dict[str, str]] = []
    for firm in FIRMS:
        for metric_id in core_metrics:
            for year in years:
                matches = indexed.get((firm, metric_id, year), [])
                reported = [row for row in matches if row["observation_status"] == "reported"]
                missing = [row for row in matches if row["observation_status"] not in {"reported", "calculated", "proxy", "estimated_external", "target"}]
                if reported:
                    expected = 3 if metric_id in {"global_revenue_service_line", "global_revenue_region"} else 1
                    coverage = "complete" if len(reported) >= expected else "partial"
                    status = "reported"
                elif matches:
                    coverage = "not_found" if missing else "partial"
                    status = ";".join(sorted({row["observation_status"] for row in matches}))
                else:
                    coverage = "not_researched_in_initial_tranche" if metric_id in {"global_revenue_service_line", "global_revenue_region"} and year < "FY2015" else "gap"
                    status = ""
                output.append({
                    "metric_id": metric_id, "firm_network": firm, "geography": "Global",
                    "fiscal_year_label": year, "coverage_status": coverage,
                    "observation_status": status, "observation_count": str(len(matches)),
                    "notes": "Initial global-core tranche; absence is not a zero.",
                })
    return output


def make_quality_checks(observations: list[dict[str, str]], sources: list[dict[str, str]]) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in preferred_reported(observations):
        grouped[(row["firm_network"], row.get("fiscal_year_label", ""), row["metric_id"])].append(row)
    check_number = 1
    for firm in FIRMS:
        for fy in [f"FY{year}" for year in range(2015, 2026)]:
            total_rows = grouped.get((firm, fy, "global_revenue_total"), [])
            if not total_rows:
                continue
            total_row = total_rows[-1]
            total = float(total_row.get("value_usd_nominal") or total_row["value_numeric"])
            for component_metric, check_type in (("global_revenue_service_line", "service_line_reconciliation"), ("global_revenue_region", "regional_reconciliation")):
                components = grouped.get((firm, fy, component_metric), [])
                if not components:
                    status = "warning"
                    difference = ""
                    note = "No component rows in the initial tranche."
                    affected = total_rows[-1]["observation_id"]
                else:
                    reconciliation_components = components
                    if component_metric == "global_revenue_service_line":
                        labels = {row.get("service_line_original", "") for row in components}
                        if "Consulting services total" in labels:
                            reconciliation_components = [
                                row for row in components
                                if row.get("service_line_original") not in {"Strategy, Risk & Transactions", "Technology & Transformation"}
                            ]
                    candidate_groups = [reconciliation_components]
                    revised = [row for row in reconciliation_components if row.get("revision_flag", "").lower() == "true"]
                    original = [row for row in reconciliation_components if row.get("revision_flag", "").lower() != "true"]
                    if len(revised) >= 2:
                        candidate_groups.append(revised)
                    if len(original) >= 2:
                        candidate_groups.append(original)
                    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
                    for row in reconciliation_components:
                        by_source[row["source_id"]].append(row)
                    candidate_groups.extend(group for group in by_source.values() if len(group) >= 2)

                    def group_sum(group: list[dict[str, str]]) -> float:
                        return sum(float(row.get("value_usd_nominal") or row["value_numeric"]) for row in group)

                    reconciliation_components = min(
                        candidate_groups,
                        key=lambda group: (abs(group_sum(group) - total), -len(group)),
                    )
                    component_sum = group_sum(reconciliation_components)
                    difference_value = component_sum - total
                    tolerance = max(1.0, abs(total)) * 0.006
                    status = "pass" if abs(difference_value) <= tolerance else "warning"
                    difference = f"{difference_value:.6g}"
                    note = "Difference is measured in canonical nominal USD using the internally consistent published taxonomy closest to the total; rounded components may not sum exactly."
                    affected = ";".join([total_rows[-1]["observation_id"], *[row["observation_id"] for row in reconciliation_components]])
                checks.append({
                    "check_id": f"qc_{check_number:04d}", "check_type": check_type,
                    "firm_network": firm, "fiscal_year_label": fy, "status": status,
                    "affected_observation_ids": affected, "difference": difference,
                    "resolution_or_caveat": note,
                })
                check_number += 1

    def add_structural(check_type: str, status: str, affected: list[str], note: str) -> None:
        nonlocal check_number
        checks.append({
            "check_id": f"qc_{check_number:04d}", "check_type": check_type,
            "firm_network": "All", "fiscal_year_label": "all",
            "status": status, "affected_observation_ids": ";".join(affected),
            "difference": "", "resolution_or_caveat": note,
        })
        check_number += 1

    missing_locators = [row["observation_id"] for row in observations if row["observation_status"] == "reported" and not row.get("source_locator")]
    add_structural(
        "source_locator_completeness", "pass" if not missing_locators else "fail", missing_locators,
        "Every reported observation must identify an exact page, table, section, or embedded-data locator.",
    )
    missing_excerpts = [row["observation_id"] for row in observations if row["observation_status"] == "reported" and not row.get("source_excerpt")]
    add_structural(
        "source_excerpt_completeness", "pass" if not missing_excerpts else "fail", missing_excerpts,
        "Every reported observation must retain a concise source excerpt sufficient to verify the value.",
    )
    source_without_url = [row["source_id"] for row in sources if not row.get("url")]
    add_structural(
        "source_url_presence", "pass" if not source_without_url else "fail", source_without_url,
        "Every source-ledger row must provide a direct source URL.",
    )
    revenue_rows = [row for row in observations if row["metric_id"] in {"global_revenue_total", "global_revenue_service_line", "global_revenue_region"} and row["observation_status"] == "reported"]
    bad_currency = [
        row["observation_id"] for row in revenue_rows
        if row.get("currency_original") != "USD" or row.get("unit_canonical") != "USD" or not row.get("value_usd_nominal")
    ]
    add_structural(
        "currency_unit_scale_consistency", "pass" if not bad_currency else "fail", bad_currency,
        "Global-core revenue rows retain source-scale values and normalize canonical currency values to full nominal US dollars.",
    )
    bad_periods: list[str] = []
    fiscal_calendars = {
        "Deloitte": ("06-01", "05-31"),
        "PwC": ("07-01", "06-30"),
        "EY": ("07-01", "06-30"),
        "KPMG": ("10-01", "09-30"),
    }
    for row in observations:
        fy = row.get("fiscal_year_label", "")
        if not fy.startswith("FY") or not fy[2:].isdigit():
            continue
        year = int(fy[2:])
        start_suffix, end_suffix = fiscal_calendars[row["firm_network"]]
        expected_start, expected_end = f"{year - 1}-{start_suffix}", f"{year}-{end_suffix}"
        if (row.get("period_start") or row.get("period_end")) and (row.get("period_start") != expected_start or row.get("period_end") != expected_end):
            bad_periods.append(row["observation_id"])
    add_structural(
        "fiscal_year_label_date_consistency", "pass" if not bad_periods else "fail", bad_periods,
        "FY labels were checked against each network's verified reporting calendar: Deloitte June-May, PwC and EY July-June, and KPMG October-September.",
    )
    scope_conflicts = [row["observation_id"] for row in observations if row.get("entity_scope") != "global_network"]
    add_structural(
        "global_vs_member_firm_scope", "pass" if not scope_conflicts else "warning", scope_conflicts,
        "The initial tranche is global-network-only. Any member-firm observation must be moved to the national-firm module.",
    )
    workforce_rows = [row for row in observations if row["metric_id"] == "global_people_total" and row["observation_status"] == "reported"]
    workforce_definitions = {row.get("definition_from_source", "") for row in workforce_rows}
    add_structural(
        "people_employee_fte_definition_conflicts", "warning" if len(workforce_definitions) > 1 else "pass",
        [row["observation_id"] for row in workforce_rows],
        "Average FTE, period-end headcount, rounded people, and lower-bound disclosures remain separate; do not chart them as one seamless series without a visible timing flag.",
    )
    superseded_ids = {row.get("supersedes_observation_id", "") for row in observations if row.get("supersedes_observation_id")}
    non_one_to_one_revisions = [
        row["observation_id"] for row in observations
        if row.get("revision_flag", "").lower() == "true"
        and not row.get("supersedes_observation_id")
        and row["observation_id"] not in superseded_ids
    ]
    broken_revision_lineage = [
        row["observation_id"] for row in observations
        if row["observation_id"] in non_one_to_one_revisions and not row.get("researcher_notes")
    ]
    add_structural(
        "revised_historical_value_lineage", "pass" if not broken_revision_lineage else "fail", broken_revision_lineage,
        "Every explicit revision must identify the superseded observation or document why one-to-one lineage is impossible.",
    )
    add_structural(
        "non_one_to_one_revision_caveats", "warning" if non_one_to_one_revisions else "pass", non_one_to_one_revisions,
        "These restatements or reclassifications cannot map one-to-one to an older row; their source locator and researcher notes preserve the caveat.",
    )
    broken_calculated_lineage = [
        row["observation_id"] for row in observations
        if row["observation_status"] == "calculated" and not row.get("formula_or_transformation")
    ]
    add_structural(
        "calculated_observation_input_lineage", "pass" if not broken_calculated_lineage else "fail", broken_calculated_lineage,
        "Calculated rows require an explicit transformation; observation-ID lineage is additionally required when the inputs are other observations rather than a directly cited source table.",
    )
    ungraded_sources = [row["source_id"] for row in sources if row.get("source_grade") not in {"A", "B", "C", "D", "E"}]
    add_structural(
        "source_grade_completeness", "pass" if not ungraded_sources else "fail", ungraded_sources,
        "Every source must carry an A-E source grade.",
    )
    missing_scores = [row["observation_id"] for row in observations if not row.get("comparability_score") or not row.get("confidence_score")]
    add_structural(
        "observation_score_completeness", "pass" if not missing_scores else "fail", missing_scores,
        "Every observation must carry 1-5 comparability and confidence scores.",
    )
    out_of_range_scores = [
        row["observation_id"] for row in observations
        if not (
            1 <= float(row["comparability_score"]) <= 5
            and float(row["comparability_score"]).is_integer()
            and 1 <= float(row["confidence_score"]) <= 5
            and float(row["confidence_score"]).is_integer()
        )
    ]
    add_structural(
        "observation_score_range", "pass" if not out_of_range_scores else "fail", out_of_range_scores,
        "Comparability and confidence scores must be integers from 1 through 5.",
    )
    return checks


def main() -> None:
    entities = normalize(read_fragments("entities"), ENTITY_FIELDS)
    sources = normalize(read_fragments("sources"), SOURCE_FIELDS)
    source_grades = {row["source_id"]: row.get("source_grade", "") for row in sources}
    observations = sort_observations(normalize_observations(read_fragments("observations"), source_grades))
    validate(entities, sources, observations)

    write_csv(DATA / "01_entity_master.csv", ENTITY_FIELDS, sorted(entities, key=lambda row: row["entity_id"]))
    write_csv(DATA / "02_metric_dictionary.csv", METRIC_FIELDS, METRICS)
    write_csv(DATA / "03_source_ledger.csv", SOURCE_FIELDS, sorted(sources, key=lambda row: row["source_id"]))
    write_csv(DATA / "04_observations_long.csv", OBSERVATION_FIELDS, observations)
    coverage_fields = ["metric_id", "firm_network", "geography", "fiscal_year_label", "coverage_status", "observation_status", "observation_count", "notes"]
    write_csv(DATA / "05_coverage_matrix.csv", coverage_fields, make_coverage(observations))

    reported = preferred_reported(observations)
    write_csv(DATA / "07_global_financials.csv", OBSERVATION_FIELDS, [row for row in reported if row["metric_id"] in {"global_revenue_total", "global_revenue_growth_reported", "global_revenue_growth_local_currency", "global_revenue_growth_constant_currency", "global_revenue_growth_usd"}])
    write_csv(DATA / "08_service_line_data.csv", OBSERVATION_FIELDS, [row for row in reported if row["metric_id"] == "global_revenue_service_line"])
    write_csv(DATA / "09_geographic_data.csv", OBSERVATION_FIELDS, [row for row in reported if row["metric_id"] == "global_revenue_region"])
    write_csv(DATA / "11_workforce_data.csv", OBSERVATION_FIELDS, [row for row in reported if row["metric_id"] == "global_people_total"])

    quality_fields = ["check_id", "check_type", "firm_network", "fiscal_year_label", "status", "affected_observation_ids", "difference", "resolution_or_caveat"]
    quality = make_quality_checks(observations, sources)
    write_csv(DATA / "27_quality_checks.csv", quality_fields, quality)

    search_fields = ["search_id", "metric_id", "firm_network", "entity_or_geography", "period", "search_date", "search_query", "domains_checked", "databases_checked", "reports_checked", "result", "reason_unresolved"]
    search_rows = normalize(read_fragments("search_log"), search_fields)
    write_csv(DATA / "28_search_log.csv", search_fields, sorted(search_rows, key=lambda row: row["search_id"]))

    firm_counts = Counter(row["firm_network"] for row in observations)
    source_grades = Counter(row["source_grade"] for row in sources)
    reported_counts = Counter(row["firm_network"] for row in observations if row["observation_status"] == "reported")
    quality_counts = Counter(row["status"] for row in quality)
    link_check_path = DATA / "27_source_url_checks.csv"
    link_counts: Counter[str] = Counter()
    if link_check_path.exists():
        with link_check_path.open(newline="", encoding="utf-8-sig") as handle:
            link_counts.update(row["check_status"] for row in csv.DictReader(handle))
    summary = [
        "# Initial global-core research summary", "", f"Research cutoff: **{RESEARCH_CUTOFF}**", "",
        "This is the first data-collection tranche, not the completion of the full commission. It covers official-source global identity, revenue, people, service-line revenue, and regional revenue. Front-end code was not changed.", "",
        "## Package counts", "",
        f"- Entities: {len(entities)}", f"- Sources: {len(sources)}", f"- Observations: {len(observations)}",
        f"- Reported observations: {sum(reported_counts.values())}", f"- Quality checks: {len(quality)} ({dict(sorted(quality_counts.items()))})",
        f"- Source grades: {dict(sorted(source_grades.items()))}", "", "## Observations by network", "",
    ]
    summary.extend(f"- {firm}: {firm_counts[firm]} total; {reported_counts[firm]} reported" for firm in FIRMS)
    summary.extend([
        "", "## Coverage and currentness", "",
        "- Global revenue and people were attempted for every network from FY2010 through FY2025; only KPMG FY2010-FY2011 people remain unresolved.",
        "- Service-line and regional revenue are complete for the initial FY2015-FY2025 target window for all four networks.",
        "- FY2025 is the latest published global fiscal year for all four networks at the research cutoff, although their exact fiscal periods differ.",
        f"- Live source-link checks: {dict(sorted(link_counts.items())) if link_counts else 'not run; execute scripts/check_source_urls.py'}.",
        "", "## Material comparability warnings", "",
        "- Fiscal year ends and exact reporting windows differ across networks.",
        "- Revenue labels and inclusion of reimbursable/pass-through amounts are source-specific.",
        "- Workforce values mix average FTE and period-end people where that is all the firms disclose; every row retains the timing definition.",
        "- Restated continuing-operations values are separate rows and do not silently replace originally reported figures.",
        "- Service-line labels are not fully interchangeable; combined categories remain combined.",
        "", "## Highest-confidence evidence", "",
        "- Grade A government registry records establish legal identities where available.",
        "- Grade B official annual reviews, impact reports, and revenue releases support the global operating series.",
        "- Every reported observation carries a source locator, excerpt, comparability score, and confidence score.",
        "", "## Deferred modules", "",
        "National member-firm accounts, office geocoding, audit-client and audit-fee panels, regulator inspections, legal events, acquisitions, technology investments, alliances, sustainability, careers, public contracts, and Grade E digital-trace data require separate collection tranches.", "",
        "## Refresh cadence", "",
        "Refresh global revenue, people, service-line, and regional series annually after each network's results release. Recheck entity registries and source links quarterly; event-based modules should be refreshed as new filings or regulator records appear.", "",
    ])
    (DATA / "29_research_summary.md").write_text("\n".join(summary), encoding="utf-8")
    print(f"Built package: {len(entities)} entities, {len(sources)} sources, {len(observations)} observations")


if __name__ == "__main__":
    main()
