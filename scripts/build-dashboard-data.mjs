import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'csv-parse/sync';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DATA = path.join(ROOT, 'data');
const OUTPUT = path.join(ROOT, 'src/lib/data/dashboard-data.json');
const FIRMS = ['Deloitte', 'PwC', 'EY', 'KPMG'];

function readCsv(name) {
	return parse(fs.readFileSync(path.join(DATA, name), 'utf8'), {
		columns: true,
		skip_empty_lines: true,
		bom: true
	});
}

function number(value) {
	if (value === '' || value == null) return null;
	const parsed = Number(value);
	return Number.isFinite(parsed) ? parsed : null;
}

function yearNumber(label) {
	return Number(String(label).replace('FY', ''));
}

const observations = readCsv('04_observations_long.csv');
const sources = readCsv('03_source_ledger.csv');
const metrics = readCsv('02_metric_dictionary.csv');
const entities = readCsv('01_entity_master.csv');
const qualityChecks = readCsv('27_quality_checks.csv');
const sourceUrlChecks = readCsv('27_source_url_checks.csv');
const searchLog = readCsv('28_search_log.csv');
const coverage = readCsv('05_coverage_matrix.csv');
const serviceCrosswalk = readCsv('06_service_line_crosswalk.csv');
const geographyCrosswalk = readCsv('06_geography_crosswalk.csv');
const workforceCrosswalk = readCsv('06_workforce_crosswalk.csv');
const officeLocations = fs.existsSync(path.join(DATA, '10_office_locations.csv'))
	? readCsv('10_office_locations.csv')
	: [];

const supersededIds = new Set(
	observations.map((row) => row.supersedes_observation_id).filter(Boolean)
);
const primary = observations.filter(
	(row) =>
		row.observation_status === 'reported' &&
		row.quality_flag !== 'exclude_from_primary' &&
		!supersededIds.has(row.observation_id)
);

function preferred(rows) {
	return [...rows].sort((a, b) => {
		const aRevision = a.revision_flag === 'true' ? 1 : 0;
		const bRevision = b.revision_flag === 'true' ? 1 : 0;
		const aExact = a.value_numeric ? 1 : 0;
		const bExact = b.value_numeric ? 1 : 0;
		const aSupplementary = a.quality_flag.includes('supplementary') ? 1 : 0;
		const bSupplementary = b.quality_flag.includes('supplementary') ? 1 : 0;
		return (
			bRevision - aRevision ||
			bExact - aExact ||
			aSupplementary - bSupplementary ||
			a.observation_id.localeCompare(b.observation_id)
		);
	})[0];
}

function observationValue(row, field = 'value_usd_nominal') {
	return number(row?.[field]) ?? number(row?.value_numeric) ?? number(row?.value_low);
}

function series(metricId, valueField = 'value_usd_nominal') {
	return Object.fromEntries(
		FIRMS.map((firm) => {
			const rows = primary.filter((row) => row.firm_network === firm && row.metric_id === metricId);
			const grouped = Map.groupBy(rows, (row) => row.fiscal_year_label);
			const points = [...grouped.entries()]
				.map(([label, matches]) => {
					const row = preferred(matches);
					return {
						year: yearNumber(label),
						label,
						value: observationValue(row, valueField),
						observationId: row.observation_id,
						sourceId: row.source_id,
						periodStart: row.period_start,
						periodEnd: row.period_end,
						valueOriginal: row.value_original_text,
						definition: row.definition_from_source,
						qualityFlag: row.quality_flag
					};
				})
				.filter((point) => point.value != null)
				.sort((a, b) => a.year - b.year);
			return [firm, points];
		})
	);
}

const revenueSeries = series('global_revenue_total');
const peopleSeries = series('global_people_total', 'value_numeric');
const growthSeries = series('global_revenue_growth_local_currency', 'value_numeric');

function latestPoint(points) {
	return points.at(-1) ?? null;
}

function pointForYear(points, year) {
	return points.find((point) => point.year === year) ?? null;
}

function cagr(start, end, years) {
	if (!start || !end || start <= 0 || years <= 0) return null;
	return (Math.pow(end / start, 1 / years) - 1) * 100;
}

const latestYear = 2025;
const latestRevenueTotal = FIRMS.reduce(
	(sum, firm) => sum + (pointForYear(revenueSeries[firm], latestYear)?.value ?? 0),
	0
);

const firmSummaries = FIRMS.map((firm) => {
	const revenue = pointForYear(revenueSeries[firm], latestYear) ?? latestPoint(revenueSeries[firm]);
	const people = pointForYear(peopleSeries[firm], latestYear) ?? latestPoint(peopleSeries[firm]);
	const fiveYearStart = pointForYear(revenueSeries[firm], latestYear - 5);
	const growth = pointForYear(growthSeries[firm], latestYear) ?? latestPoint(growthSeries[firm]);
	return {
		firm,
		revenue: revenue?.value ?? null,
		revenueObservationId: revenue?.observationId ?? null,
		people: people?.value ?? null,
		peopleObservationId: people?.observationId ?? null,
		growth: growth?.value ?? null,
		growthObservationId: growth?.observationId ?? null,
		marketShare: revenue?.value ? (revenue.value / latestRevenueTotal) * 100 : null,
		fiveYearCagr: cagr(fiveYearStart?.value, revenue?.value, 5),
		revenuePerPerson: revenue?.value && people?.value ? revenue.value / people.value : null,
		periodStart: revenue?.periodStart ?? '',
		periodEnd: revenue?.periodEnd ?? '',
		peopleDefinition: people?.definition ?? ''
	};
});

function dimensionRows(metricId) {
	return Object.fromEntries(
		FIRMS.map((firm) => {
			const matches = primary.filter(
				(row) =>
					row.firm_network === firm &&
					row.metric_id === metricId &&
					yearNumber(row.fiscal_year_label) === latestYear
			);
			const dimensionKey =
				metricId === 'global_revenue_service_line' ? 'service_line_original' : 'geography_original';
			const grouped = Map.groupBy(matches, (row) => row[dimensionKey]);
			const rows = [...grouped.entries()].map(([label, candidates]) => {
				const row = preferred(candidates);
				const nested =
					firm === 'Deloitte' &&
					metricId === 'global_revenue_service_line' &&
					['Strategy, Risk & Transactions', 'Technology & Transformation'].includes(label);
				return {
					label,
					canonical:
						metricId === 'global_revenue_service_line'
							? row.service_line_canonical
							: row.geography_canonical,
					value: observationValue(row),
					observationId: row.observation_id,
					sourceId: row.source_id,
					nested,
					parent: nested ? 'Consulting services total' : null
				};
			});
			return [firm, rows.sort((a, b) => (b.value ?? 0) - (a.value ?? 0))];
		})
	);
}

const serviceMix = dimensionRows('global_revenue_service_line');
const regionalMix = dimensionRows('global_revenue_region');

const sourceById = Object.fromEntries(sources.map((row) => [row.source_id, row]));
const metricById = Object.fromEntries(metrics.map((row) => [row.metric_id, row]));
const urlCheckById = Object.fromEntries(sourceUrlChecks.map((row) => [row.source_id, row]));

const compactObservations = observations.map((row) => ({
	id: row.observation_id,
	metricId: row.metric_id,
	metricName: metricById[row.metric_id]?.metric_name_canonical ?? row.metric_id,
	metricFamily: metricById[row.metric_id]?.metric_family ?? '',
	firm: row.firm_network,
	entity: row.entity_name,
	scope: row.entity_scope,
	fiscalYear: row.fiscal_year_label,
	periodStart: row.period_start,
	periodEnd: row.period_end,
	asOfDate: row.as_of_date,
	geographyOriginal: row.geography_original,
	geographyCanonical: row.geography_canonical,
	serviceOriginal: row.service_line_original,
	serviceCanonical: row.service_line_canonical,
	valueOriginal: row.value_original_text,
	valueNumeric: number(row.value_numeric),
	valueLow: number(row.value_low),
	valueHigh: number(row.value_high),
	valueUsd: number(row.value_usd_nominal),
	unitOriginal: row.unit_original,
	unitCanonical: row.unit_canonical,
	scaleOriginal: row.scale_original,
	currencyOriginal: row.currency_original,
	status: row.observation_status,
	valueType: row.reported_calculated_proxy_or_estimate,
	definition: row.definition_from_source,
	formula: row.formula_or_transformation,
	sourceId: row.source_id,
	sourceTitle: sourceById[row.source_id]?.source_title ?? '',
	sourceGrade: sourceById[row.source_id]?.source_grade ?? '',
	sourceUrl: sourceById[row.source_id]?.url ?? '',
	archivedUrl: sourceById[row.source_id]?.archived_url ?? '',
	sourceLocator: row.source_locator,
	sourceExcerpt: row.source_excerpt,
	extractionMethod: row.extraction_method,
	comparabilityScore: number(row.comparability_score),
	confidenceScore: number(row.confidence_score),
	qualityFlag: row.quality_flag,
	revision: row.revision_flag === 'true',
	supersedes: row.supersedes_observation_id,
	notes: row.researcher_notes
}));

const compactSources = sources.map((row) => ({
	id: row.source_id,
	title: row.source_title,
	publisher: row.publisher,
	type: row.document_type,
	url: row.url,
	archivedUrl: row.archived_url,
	publicationDate: row.publication_date,
	periodStart: row.reporting_period_start,
	periodEnd: row.reporting_period_end,
	grade: row.source_grade,
	official: row.official_source_flag === 'true',
	audited: row.audited_flag === 'true',
	urlStatus: urlCheckById[row.source_id]?.check_status ?? 'unchecked',
	notes: row.notes
}));

const compactOfficeLocations = officeLocations
	.map((row) => ({
		id: row.site_id,
		firm: row.firm_network,
		name: row.site_name,
		type: row.office_type,
		address: row.street_address,
		city: row.city,
		region: row.state_province,
		country: row.country,
		countryCode: row.country_iso2,
		latitude: number(row.latitude),
		longitude: number(row.longitude),
		sourceUrl: row.source_url,
		sourceLocator: row.source_locator,
		coordinatePrecision: row.coordinate_precision,
		coverageTier: row.coverage_tier,
		asOfDate: row.as_of_date
	}))
	.filter((row) => row.latitude != null && row.longitude != null);

const officeMeta = Object.fromEntries(
	FIRMS.map((firm) => {
		const rows = compactOfficeLocations.filter((row) => row.firm === firm);
		return [
			firm,
			{
				count: rows.length,
				coverageTier: rows[0]?.coverageTier ?? 'representative_hub',
				coordinatePrecision: rows[0]?.coordinatePrecision ?? 'city_centroid'
			}
		];
	})
);

const firmRevenueSorted = [...firmSummaries].sort((a, b) => (b.revenue ?? 0) - (a.revenue ?? 0));
const firmGrowthSorted = [...firmSummaries].sort(
	(a, b) => (b.fiveYearCagr ?? 0) - (a.fiveYearCagr ?? 0)
);
const firmProductivitySorted = [...firmSummaries].sort(
	(a, b) => (b.revenuePerPerson ?? 0) - (a.revenuePerPerson ?? 0)
);

const payload = {
	meta: {
		researchCutoff: '2026-07-18',
		latestCommonYear: latestYear,
		observationCount: observations.length,
		reportedObservationCount: observations.filter((row) => row.observation_status === 'reported')
			.length,
		sourceCount: sources.length,
		entityCount: entities.length,
		metricCount: metrics.length,
		qualityPassCount: qualityChecks.filter((row) => row.status === 'pass').length,
		qualityWarningCount: qualityChecks.filter((row) => row.status === 'warning').length,
		activeSourceCount: sourceUrlChecks.filter((row) => row.check_status === 'pass').length,
		archiveFallbackCount: sourceUrlChecks.filter((row) => row.check_status === 'warning').length,
		searchGapCount: searchLog.length,
		latestRevenueTotal
	},
	firms: firmSummaries,
	revenueSeries,
	peopleSeries,
	growthSeries,
	serviceMix,
	regionalMix,
	officeLocations: compactOfficeLocations,
	officeMeta,
	insights: [
		{
			id: 'scale-leader',
			title: `${firmRevenueSorted[0].firm} leads on reported scale`,
			body: `${firmRevenueSorted[0].firm} represents ${firmRevenueSorted[0].marketShare.toFixed(1)}% of the Big Four's FY2025 reported revenue in this dataset.`,
			observationId: firmRevenueSorted[0].revenueObservationId,
			tone: 'scale'
		},
		{
			id: 'growth-leader',
			title: `${firmGrowthSorted[0].firm} has the strongest five-year compound growth`,
			body: `Reported revenue grew at approximately ${firmGrowthSorted[0].fiveYearCagr.toFixed(1)}% a year from FY2020 to FY2025.`,
			observationId: firmGrowthSorted[0].revenueObservationId,
			tone: 'growth'
		},
		{
			id: 'productivity-leader',
			title: `${firmProductivitySorted[0].firm} leads the directional productivity proxy`,
			body: `FY2025 reported revenue per disclosed person is about $${Math.round(firmProductivitySorted[0].revenuePerPerson / 1000)}k, with workforce-definition caveats kept visible.`,
			observationId: firmProductivitySorted[0].peopleObservationId,
			tone: 'productivity'
		}
	],
	observations: compactObservations,
	sources: compactSources,
	metrics,
	entities,
	qualityChecks,
	coverage,
	searchLog,
	crosswalks: {
		service: serviceCrosswalk,
		geography: geographyCrosswalk,
		workforce: workforceCrosswalk
	}
};

fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
fs.writeFileSync(OUTPUT, `${JSON.stringify(payload)}\n`);
console.log(`Wrote ${OUTPUT} (${observations.length} observations, ${sources.length} sources)`);
