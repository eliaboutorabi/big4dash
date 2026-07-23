<script lang="ts">
	import { Check, CircleDashed, SearchX } from '@lucide/svelte';
	import { FIRM_COLORS, FIRMS } from '$lib/data/format';
	import type { DashboardObservation, FirmName } from '$lib/data/types';

	type CoverageRow = Record<string, string>;
	type MetricId =
		| 'global_revenue_total'
		| 'global_people_total'
		| 'global_revenue_service_line'
		| 'global_revenue_region';

	let {
		coverage,
		observations,
		onselect
	}: {
		coverage: CoverageRow[];
		observations: DashboardObservation[];
		onselect: (observationId: string) => void;
	} = $props();

	const metrics: Array<{ id: MetricId; label: string; short: string }> = [
		{ id: 'global_revenue_total', label: 'Total revenue', short: 'Revenue' },
		{ id: 'global_people_total', label: 'People', short: 'People' },
		{ id: 'global_revenue_service_line', label: 'Service lines', short: 'Services' },
		{ id: 'global_revenue_region', label: 'Regional revenue', short: 'Regions' }
	];
	const years = Array.from({ length: 16 }, (_, index) => `FY${2010 + index}`);
	let selectedMetric = $state<MetricId>('global_revenue_total');

	function record(firm: FirmName, year: string) {
		return coverage.find(
			(row) =>
				row.metric_id === selectedMetric &&
				row.firm_network === firm &&
				row.fiscal_year_label === year
		);
	}

	function observationId(firm: FirmName, year: string) {
		return observations.find(
			(row) => row.metricId === selectedMetric && row.firm === firm && row.fiscalYear === year
		)?.id;
	}

	function statusLabel(status = '') {
		if (status === 'complete') return 'reported';
		if (status === 'not_found') return 'searched, not found';
		return 'not researched in the initial tranche';
	}
</script>

<div class="coverage-matrix">
	<div class="coverage-copy">
		<div>
			<span>Research completeness</span>
			<h3>What is known—and where the record stops.</h3>
		</div>
		<p>
			Absence is never treated as zero. Switch metrics to see the researched horizon and open any
			reported year directly.
		</p>
	</div>

	<div class="coverage-controls" aria-label="Coverage metric">
		{#each metrics as metric (metric.id)}
			<button
				class:active={selectedMetric === metric.id}
				aria-label={`Show coverage for ${metric.label}`}
				onclick={() => (selectedMetric = metric.id)}
			>
				{metric.short}
			</button>
		{/each}
	</div>

	<div class="matrix-scroll">
		<div class="matrix-grid">
			<div class="year-row" aria-hidden="true">
				<span></span>
				{#each years as year (year)}<b>{year.slice(2)}</b>{/each}
			</div>
			{#each FIRMS as firm (firm)}
				<div class="firm-row">
					<strong><i style:background={FIRM_COLORS[firm]}></i>{firm}</strong>
					{#each years as year (year)}
						{@const entry = record(firm, year)}
						{@const evidenceId = observationId(firm, year)}
						<button
							class:complete={entry?.coverage_status === 'complete'}
							class:not-found={entry?.coverage_status === 'not_found'}
							class:not-researched={entry?.coverage_status === 'not_researched_in_initial_tranche'}
							style:--firm-color={FIRM_COLORS[firm]}
							disabled={!evidenceId}
							aria-label={`${firm} ${year} ${metrics.find((metric) => metric.id === selectedMetric)?.label}: ${statusLabel(entry?.coverage_status)}`}
							onclick={() => evidenceId && onselect(evidenceId)}
						>
							{#if entry?.coverage_status === 'complete'}
								<Check size={11} aria-hidden="true" />
							{:else if entry?.coverage_status === 'not_found'}
								<SearchX size={11} aria-hidden="true" />
							{:else}
								<CircleDashed size={11} aria-hidden="true" />
							{/if}
						</button>
					{/each}
				</div>
			{/each}
		</div>
	</div>

	<div class="coverage-legend">
		<span><i class="legend-complete"><Check size={10} /></i>Reported</span>
		<span><i class="legend-search"><SearchX size={10} /></i>Searched, not found</span>
		<span><i><CircleDashed size={10} /></i>Outside initial tranche</span>
	</div>
</div>

<style>
	.coverage-matrix {
		margin-bottom: 22px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.coverage-copy {
		display: grid;
		grid-template-columns: minmax(260px, 1fr) minmax(280px, 0.8fr);
		gap: 30px;
		align-items: end;
		padding: 22px 24px 18px;
		border-bottom: 1px solid var(--frame);
	}

	.coverage-copy span {
		color: var(--accent-strong);
		font-family: var(--font-mono);
		font-size: 10px;
		font-weight: 700;
	}

	.coverage-copy h3 {
		max-width: 20ch;
		margin: 7px 0 0;
		font-family: var(--font-display);
		font-size: 30px;
		font-weight: 620;
		line-height: 1;
		letter-spacing: -0.035em;
	}

	.coverage-copy p {
		max-width: 55ch;
		margin: 0;
		color: var(--text-secondary);
		font-size: 11px;
		line-height: 1.6;
	}

	.coverage-controls {
		display: flex;
		padding: 8px;
		border-bottom: 1px solid var(--frame);
		background: var(--surface-muted);
	}

	.coverage-controls button {
		min-height: 34px;
		padding: 0 13px;
		border: 0;
		border-right: 1px solid var(--border-subtle);
		background: transparent;
		color: var(--text-secondary);
		font-size: 10px;
		font-weight: 750;
		cursor: pointer;
	}

	.coverage-controls button.active {
		background: var(--accent-light);
		color: var(--accent-ink);
	}

	.matrix-scroll {
		overflow-x: auto;
		padding: 17px 20px 18px;
	}

	.matrix-grid {
		min-width: 820px;
	}

	.year-row,
	.firm-row {
		display: grid;
		grid-template-columns: 100px repeat(16, minmax(30px, 1fr));
		gap: 3px;
	}

	.year-row {
		margin-bottom: 5px;
	}

	.year-row b {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
		font-weight: 600;
		text-align: center;
	}

	.firm-row {
		margin-bottom: 3px;
	}

	.firm-row > strong {
		display: flex;
		align-items: center;
		gap: 7px;
		font-size: 10px;
	}

	.firm-row > strong i {
		width: 7px;
		height: 7px;
	}

	.firm-row > button {
		display: grid;
		height: 28px;
		place-items: center;
		border: 1px solid var(--border-subtle);
		background: var(--surface-muted);
		color: var(--text-tertiary);
		cursor: pointer;
		transition:
			filter 150ms var(--ease-out),
			transform 150ms var(--ease-out);
	}

	.firm-row > button.complete {
		border-color: color-mix(in oklch, var(--firm-color) 72%, var(--frame));
		background: color-mix(in oklch, var(--firm-color) 72%, var(--surface-base));
		color: white;
	}

	.firm-row > button.not-found {
		border-color: var(--accent-strong);
		background: var(--accent-wash);
		color: var(--accent-strong);
	}

	.firm-row > button.not-researched {
		background: transparent;
	}

	.firm-row > button:disabled {
		cursor: default;
		opacity: 0.78;
	}

	.firm-row > button:not(:disabled):hover {
		filter: brightness(1.08) saturate(1.08);
		transform: translateY(-1px);
	}

	.coverage-legend {
		display: flex;
		flex-wrap: wrap;
		gap: 16px;
		padding: 10px 20px;
		border-top: 1px solid var(--border-subtle);
		color: var(--text-secondary);
		font-size: 9px;
	}

	.coverage-legend span {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.coverage-legend i {
		display: grid;
		width: 18px;
		height: 18px;
		place-items: center;
		border: 1px solid var(--border-subtle);
		background: var(--surface-muted);
		color: var(--text-tertiary);
	}

	.coverage-legend .legend-complete {
		background: var(--success);
		color: white;
	}

	.coverage-legend .legend-search {
		background: var(--accent-wash);
		color: var(--accent-strong);
	}

	@media (max-width: 700px) {
		.coverage-copy {
			grid-template-columns: 1fr;
			gap: 12px;
		}

		.coverage-controls {
			overflow-x: auto;
		}
	}
</style>
