export type FirmName = 'Deloitte' | 'PwC' | 'EY' | 'KPMG';

export interface SeriesPoint {
	year: number;
	label: string;
	value: number;
	observationId: string;
	sourceId: string;
	periodStart: string;
	periodEnd: string;
	valueOriginal: string;
	definition: string;
	qualityFlag: string;
}

export interface FirmSummary {
	firm: FirmName;
	revenue: number;
	revenueObservationId: string;
	people: number;
	peopleObservationId: string;
	growth: number;
	growthObservationId: string;
	marketShare: number;
	fiveYearCagr: number;
	revenuePerPerson: number;
	periodStart: string;
	periodEnd: string;
	peopleDefinition: string;
}

export interface DimensionPoint {
	label: string;
	canonical: string;
	value: number;
	observationId: string;
	sourceId: string;
	nested: boolean;
	parent: string | null;
}

export interface DashboardObservation {
	id: string;
	metricId: string;
	metricName: string;
	metricFamily: string;
	firm: FirmName;
	entity: string;
	scope: string;
	fiscalYear: string;
	periodStart: string;
	periodEnd: string;
	asOfDate: string;
	geographyOriginal: string;
	geographyCanonical: string;
	serviceOriginal: string;
	serviceCanonical: string;
	valueOriginal: string;
	valueNumeric: number | null;
	valueLow: number | null;
	valueHigh: number | null;
	valueUsd: number | null;
	unitOriginal: string;
	unitCanonical: string;
	scaleOriginal: string;
	currencyOriginal: string;
	status: string;
	valueType: string;
	definition: string;
	formula: string;
	sourceId: string;
	sourceTitle: string;
	sourceGrade: string;
	sourceUrl: string;
	archivedUrl: string;
	sourceLocator: string;
	sourceExcerpt: string;
	extractionMethod: string;
	comparabilityScore: number;
	confidenceScore: number;
	qualityFlag: string;
	revision: boolean;
	supersedes: string;
	notes: string;
}

export interface DashboardSource {
	id: string;
	title: string;
	publisher: string;
	type: string;
	url: string;
	archivedUrl: string;
	publicationDate: string;
	periodStart: string;
	periodEnd: string;
	grade: string;
	official: boolean;
	audited: boolean;
	urlStatus: string;
	notes: string;
}

export interface OfficeLocation {
	id: string;
	firm: FirmName;
	name: string;
	type: string;
	address: string;
	city: string;
	region: string;
	country: string;
	countryCode: string;
	latitude: number;
	longitude: number;
	sourceUrl: string;
	sourceLocator: string;
	coordinatePrecision: 'source_coordinate' | 'city_centroid';
	coverageTier: 'directory_complete' | 'directory_mapped' | 'representative_hub';
	asOfDate: string;
}

export interface DashboardData {
	meta: {
		researchCutoff: string;
		latestCommonYear: number;
		observationCount: number;
		reportedObservationCount: number;
		sourceCount: number;
		entityCount: number;
		metricCount: number;
		qualityPassCount: number;
		qualityWarningCount: number;
		activeSourceCount: number;
		archiveFallbackCount: number;
		searchGapCount: number;
		latestRevenueTotal: number;
	};
	firms: FirmSummary[];
	revenueSeries: Record<FirmName, SeriesPoint[]>;
	peopleSeries: Record<FirmName, SeriesPoint[]>;
	growthSeries: Record<FirmName, SeriesPoint[]>;
	serviceMix: Record<FirmName, DimensionPoint[]>;
	regionalMix: Record<FirmName, DimensionPoint[]>;
	officeLocations: OfficeLocation[];
	officeMeta: Record<
		FirmName,
		{
			count: number;
			coverageTier: 'directory_complete' | 'directory_mapped' | 'representative_hub';
			coordinatePrecision: 'source_coordinate' | 'city_centroid';
		}
	>;
	insights: Array<{
		id: string;
		title: string;
		body: string;
		observationId: string;
		tone: string;
	}>;
	observations: DashboardObservation[];
	sources: DashboardSource[];
	metrics: Array<Record<string, string>>;
	entities: Array<Record<string, string>>;
	qualityChecks: Array<Record<string, string>>;
	coverage: Array<Record<string, string>>;
	searchLog: Array<Record<string, string>>;
	crosswalks: {
		service: Array<Record<string, string>>;
		geography: Array<Record<string, string>>;
		workforce: Array<Record<string, string>>;
	};
}
