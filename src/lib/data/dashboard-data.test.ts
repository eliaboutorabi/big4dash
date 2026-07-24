import { describe, expect, it } from 'vitest';
import dashboardArtifact from './dashboard-data.json';
import type { DashboardData, FirmName } from './types';

const data = dashboardArtifact as DashboardData;
const firmNames: FirmName[] = ['Deloitte', 'PwC', 'EY', 'KPMG'];

describe('dashboard research contract', () => {
	it('keeps declared metadata reconciled to the artifact', () => {
		expect(data.observations).toHaveLength(data.meta.observationCount);
		expect(data.sources).toHaveLength(data.meta.sourceCount);
		expect(data.observations.filter((row) => row.status === 'reported')).toHaveLength(
			data.meta.reportedObservationCount
		);
		expect(data.firms).toHaveLength(firmNames.length);
		expect(data.meta.latestCommonYear).toBe(2025);
	});

	it('preserves unique identities and complete source lineage', () => {
		const observationIds = data.observations.map((row) => row.id);
		const sourceIds = data.sources.map((source) => source.id);
		const sourceIdSet = new Set(sourceIds);

		expect(new Set(observationIds).size).toBe(observationIds.length);
		expect(new Set(sourceIds).size).toBe(sourceIds.length);
		expect(data.observations.every((row) => sourceIdSet.has(row.sourceId))).toBe(true);
		expect(
			data.observations.every(
				(row) =>
					row.comparabilityScore >= 1 &&
					row.comparabilityScore <= 5 &&
					row.confidenceScore >= 1 &&
					row.confidenceScore <= 5
			)
		).toBe(true);
	});

	it('reconciles the latest market view and five-year growth calculations', () => {
		const revenueTotal = data.firms.reduce((sum, firm) => sum + firm.revenue, 0);
		const marketShareTotal = data.firms.reduce((sum, firm) => sum + firm.marketShare, 0);

		expect(revenueTotal).toBe(data.meta.latestRevenueTotal);
		expect(marketShareTotal).toBeCloseTo(100, 8);

		for (const firm of data.firms) {
			const series = data.revenueSeries[firm.firm];
			const start = series.find((point) => point.year === 2020);
			const end = series.find((point) => point.year === data.meta.latestCommonYear);

			expect(start).toBeDefined();
			expect(end).toBeDefined();
			const expectedCagr = (Math.pow(end!.value / start!.value, 1 / 5) - 1) * 100;
			expect(firm.fiveYearCagr).toBeCloseTo(expectedCagr, 8);
			expect(series.at(-1)?.value).toBe(firm.revenue);
		}
	});

	it('keeps every office location usable and its coverage totals accurate', () => {
		const officeIds = data.officeLocations.map((office) => office.id);

		expect(data.officeLocations).toHaveLength(2206);
		expect(new Set(officeIds).size).toBe(officeIds.length);
		expect(
			data.officeLocations.every(
				(office) =>
					Boolean(office.country) &&
					office.country !== 'Choose a territory' &&
					Number.isFinite(office.latitude) &&
					office.latitude >= -90 &&
					office.latitude <= 90 &&
					Number.isFinite(office.longitude) &&
					office.longitude >= -180 &&
					office.longitude <= 180 &&
					Boolean(office.sourceUrl)
			)
		).toBe(true);

		for (const firm of firmNames) {
			expect(data.officeMeta[firm].count).toBe(
				data.officeLocations.filter((office) => office.firm === firm).length
			);
		}
	});
});
