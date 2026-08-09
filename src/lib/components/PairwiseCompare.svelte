<script lang="ts">
	import { GitCompareArrows } from '@lucide/svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, fullNumber, percent } from '$lib/data/format';
	import type { FirmName, FirmSummary } from '$lib/data/types';

	let {
		firms,
		onselect
	}: {
		firms: FirmSummary[];
		onselect: (observationId: string) => void;
	} = $props();

	let leftFirm = $state<FirmName>('Deloitte');
	let rightFirm = $state<FirmName>('KPMG');
	let left = $derived(firms.find((firm) => firm.firm === leftFirm)!);
	let right = $derived(firms.find((firm) => firm.firm === rightFirm)!);

	const metrics = [
		{
			label: 'Reported revenue',
			key: 'revenue',
			format: (value: number) => currencyShort(value),
			evidence: (firm: FirmSummary) => firm.revenueObservationId
		},
		{
			label: 'Disclosed people',
			key: 'people',
			format: (value: number) => fullNumber(value),
			evidence: (firm: FirmSummary) => firm.peopleObservationId
		},
		{
			label: 'Local growth',
			key: 'growth',
			format: (value: number) => percent(value),
			evidence: (firm: FirmSummary) => firm.growthObservationId
		},
		{
			label: 'Five-year CAGR',
			key: 'fiveYearCagr',
			format: (value: number) => percent(value),
			evidence: (firm: FirmSummary) => firm.revenueObservationId
		},
		{
			label: 'Revenue / person',
			key: 'revenuePerPerson',
			format: (value: number) => currencyShort(value, 0),
			evidence: (firm: FirmSummary) => firm.peopleObservationId
		}
	] as const;

	type Metric = (typeof metrics)[number];

	function value(firm: FirmSummary, key: Metric['key']) {
		return firm[key];
	}

	function formatGap(metric: Metric, delta: number) {
		const gap = Math.abs(delta);
		if (metric.key === 'revenue') return currencyShort(gap, 1);
		if (metric.key === 'revenuePerPerson') return currencyShort(gap, 0);
		if (metric.key === 'people') return fullNumber(gap);
		return `${gap.toFixed(1)} pts`;
	}
</script>

<div class="pairwise-compare">
	<header class="compare-heading">
		<div class="compare-symbol"><GitCompareArrows size={18} aria-hidden="true" /></div>
		<div>
			<span>Pairwise workbench</span>
			<strong>Read the two networks as a vertical ledger.</strong>
		</div>
		<p>Each metric stacks the firms on one scale; every reported value opens its source record.</p>
	</header>

	<div class="network-controls">
		<label class="network-control" style:--firm-color={FIRM_COLORS[leftFirm]}>
			<span class="network-label">
				<i></i>
				<span><small>Upper row</small><strong>Network A</strong></span>
			</span>
			<select bind:value={leftFirm} aria-label="Choose first network">
				{#each FIRMS as firm (firm)}
					<option value={firm} disabled={firm === rightFirm}>{firm}</option>
				{/each}
			</select>
			<span class="network-period">{left.periodStart} → {left.periodEnd}</span>
		</label>

		<div class="vertical-versus" aria-hidden="true"><span>versus</span></div>

		<label class="network-control" style:--firm-color={FIRM_COLORS[rightFirm]}>
			<span class="network-label">
				<i></i>
				<span><small>Lower row</small><strong>Network B</strong></span>
			</span>
			<select bind:value={rightFirm} aria-label="Choose second network">
				{#each FIRMS as firm (firm)}
					<option value={firm} disabled={firm === leftFirm}>{firm}</option>
				{/each}
			</select>
			<span class="network-period">{right.periodStart} → {right.periodEnd}</span>
		</label>
	</div>

	<div class="comparison-table">
		<div class="ledger-heading">
			<div>
				<strong>Vertical comparison ledger</strong>
				<span>Adjacent endpoints make narrow differences easier to judge.</span>
			</div>
			<span>Click any row for evidence</span>
		</div>

		{#each metrics as metric (metric.key)}
			{@const leftValue = value(left, metric.key)}
			{@const rightValue = value(right, metric.key)}
			{@const maximum = Math.max(leftValue, rightValue, 1)}
			{@const delta = leftValue - rightValue}
			<section class="comparison-row">
				<div class="metric-heading">
					<strong>{metric.label}</strong>
					<span class="gap-readout" class:even={delta === 0}>
						{#if delta === 0}
							Even
						{:else}
							<strong>{delta > 0 ? leftFirm : rightFirm}</strong>
							<span>leads by {formatGap(metric, delta)}</span>
						{/if}
					</span>
				</div>

				<div class="firm-stack">
					<button
						class="firm-row"
						class:winner={leftValue > rightValue}
						data-firm={leftFirm}
						style:--firm-color={FIRM_COLORS[leftFirm]}
						style:--bar-scale={leftValue / maximum}
						onclick={() => onselect(metric.evidence(left))}
						aria-label={`Open ${leftFirm} ${metric.label} evidence: ${metric.format(leftValue)}`}
					>
						<span class="firm-identity">
							<i></i>
							<span><small>Network A</small><strong>{leftFirm}</strong></span>
						</span>
						<span class="bar-track" aria-hidden="true"><i></i></span>
						<strong class="metric-value">{metric.format(leftValue)}</strong>
						<small class="evidence-cue">View record</small>
					</button>

					<button
						class="firm-row"
						class:winner={rightValue > leftValue}
						data-firm={rightFirm}
						style:--firm-color={FIRM_COLORS[rightFirm]}
						style:--bar-scale={rightValue / maximum}
						onclick={() => onselect(metric.evidence(right))}
						aria-label={`Open ${rightFirm} ${metric.label} evidence: ${metric.format(rightValue)}`}
					>
						<span class="firm-identity">
							<i></i>
							<span><small>Network B</small><strong>{rightFirm}</strong></span>
						</span>
						<span class="bar-track" aria-hidden="true"><i></i></span>
						<strong class="metric-value">{metric.format(rightValue)}</strong>
						<small class="evidence-cue">View record</small>
					</button>
				</div>
			</section>
		{/each}
	</div>

	<footer class="comparison-note">
		<strong>How to read</strong>
		<span
			>Bars share a scale within each metric only. Compare exact values—not bar lengths—across
			metrics.</span
		>
	</footer>
</div>

<style>
	.pairwise-compare {
		container-type: inline-size;
		margin-top: 24px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.compare-heading {
		display: grid;
		grid-template-columns: 40px minmax(240px, 1fr) minmax(260px, 0.8fr);
		gap: 12px;
		align-items: center;
		padding: 16px 20px;
		border-bottom: 1px solid var(--frame);
		background: var(--inverse-surface);
		color: var(--inverse-text);
	}

	.compare-symbol {
		display: grid;
		width: 38px;
		height: 38px;
		place-items: center;
		background: var(--accent);
		color: var(--accent-ink);
	}

	.compare-heading > div:nth-child(2) {
		display: grid;
		gap: 4px;
	}

	.compare-heading span {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.compare-heading strong {
		font-size: 13px;
	}

	.compare-heading p {
		max-width: 58ch;
		margin: 0;
		color: var(--text-on-dark-muted);
		font-size: 10px;
		line-height: 1.5;
	}

	.network-controls {
		padding: 16px 20px;
		border-bottom: 1px solid var(--frame);
		background: var(--surface-muted);
	}

	.network-control {
		display: grid;
		grid-template-columns: 132px minmax(220px, 1fr) minmax(180px, auto);
		gap: 16px;
		align-items: center;
		min-height: 56px;
	}

	.network-label,
	.firm-identity {
		display: flex;
		align-items: center;
		gap: 8px;
		min-width: 0;
	}

	.network-label > i,
	.firm-identity > i {
		display: block;
		width: 10px;
		height: 10px;
		flex: 0 0 auto;
		background: var(--firm-color);
		box-shadow: 0 0 0 1px var(--frame);
	}

	.network-label > span,
	.firm-identity > span {
		display: grid;
		gap: 4px;
		min-width: 0;
	}

	.network-label small,
	.firm-identity small {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
		font-weight: 650;
	}

	.network-label strong,
	.firm-identity strong {
		overflow: hidden;
		color: var(--ink);
		font-size: 10px;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	select {
		width: 100%;
		height: 44px;
		padding: 0 12px;
		border: 1px solid var(--frame);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--ink);
		font-size: 12px;
		font-weight: 800;
	}

	.network-period {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
		text-align: right;
	}

	.vertical-versus {
		display: flex;
		align-items: center;
		gap: 12px;
		height: 24px;
		color: var(--text-tertiary);
		font-family: var(--font-display);
		font-size: 11px;
		font-style: italic;
	}

	.vertical-versus::before,
	.vertical-versus::after {
		height: 1px;
		flex: 1;
		background: var(--border-subtle);
		content: '';
	}

	.comparison-table {
		padding: 0 20px 16px;
	}

	.ledger-heading {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 24px;
		padding: 16px 0 12px;
	}

	.ledger-heading > div {
		display: grid;
		gap: 4px;
	}

	.ledger-heading strong {
		font-size: 11px;
	}

	.ledger-heading span {
		color: var(--text-tertiary);
		font-size: 9px;
	}

	.ledger-heading > span {
		font-family: var(--font-mono);
		text-align: right;
	}

	.comparison-row {
		padding: 16px 0;
		border-top: 1px solid var(--border-subtle);
	}

	.metric-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 24px;
		margin-bottom: 12px;
	}

	.metric-heading > strong {
		color: var(--ink);
		font-size: 12px;
	}

	.gap-readout {
		display: flex;
		align-items: baseline;
		gap: 8px;
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 9px;
		text-align: right;
	}

	.gap-readout > strong {
		color: var(--ink);
		font-size: 9px;
	}

	.gap-readout.even {
		color: var(--text-tertiary);
	}

	.firm-stack {
		display: grid;
		gap: 4px;
	}

	.firm-row {
		display: grid;
		grid-template-columns: minmax(112px, 140px) minmax(160px, 1fr) minmax(80px, 112px) 64px;
		gap: 12px;
		align-items: center;
		width: 100%;
		min-height: 48px;
		padding: 8px;
		border: 0;
		background: transparent;
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.firm-row:hover,
	.firm-row:focus-visible {
		background: color-mix(in oklab, var(--firm-color) 9%, transparent);
		outline: 1px solid var(--firm-color);
		outline-offset: -1px;
	}

	.firm-row.winner .metric-value {
		font-weight: 850;
	}

	.firm-row:not(.winner) .bar-track > i {
		opacity: 0.72;
	}

	.bar-track {
		position: relative;
		display: block;
		height: 10px;
		overflow: hidden;
		background: var(--surface-muted);
		box-shadow: inset 0 0 0 1px var(--border-subtle);
	}

	.bar-track > i {
		display: block;
		width: max(2px, calc(var(--bar-scale) * 100%));
		height: 100%;
		background: var(--firm-color);
		transition: width 220ms var(--ease-out);
	}

	.metric-value {
		font-family: var(--font-mono);
		font-size: 12px;
		font-weight: 750;
		text-align: right;
		white-space: nowrap;
	}

	.evidence-cue {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
		text-align: right;
	}

	.comparison-note {
		display: grid;
		grid-template-columns: 132px minmax(0, 1fr);
		gap: 16px;
		padding: 12px 20px;
		border-top: 1px solid var(--frame);
		color: var(--text-tertiary);
		font-size: 9px;
		line-height: 1.5;
	}

	.comparison-note strong {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	@container (max-width: 720px) {
		.compare-heading {
			grid-template-columns: 40px 1fr;
		}

		.compare-heading p {
			grid-column: 2;
		}

		.network-controls,
		.comparison-table {
			padding-inline: 16px;
		}

		.network-control {
			grid-template-columns: 104px minmax(0, 1fr);
			gap: 12px;
		}

		.network-period {
			grid-column: 2;
			text-align: left;
		}

		.firm-row {
			grid-template-columns: minmax(96px, 120px) minmax(100px, 1fr) auto;
		}

		.evidence-cue {
			display: none;
		}
	}

	@container (max-width: 440px) {
		.compare-heading {
			padding-inline: 16px;
		}

		.compare-heading p {
			grid-column: 1 / -1;
		}

		.network-control {
			grid-template-columns: 1fr;
			gap: 8px;
			padding: 4px 0;
		}

		.network-period {
			grid-column: auto;
		}

		.ledger-heading {
			align-items: flex-start;
			flex-direction: column;
			gap: 8px;
		}

		.ledger-heading > span {
			text-align: left;
		}

		.metric-heading {
			align-items: flex-start;
			flex-direction: column;
			gap: 4px;
		}

		.gap-readout {
			text-align: left;
		}

		.firm-row {
			grid-template-columns: minmax(92px, 0.8fr) minmax(0, 1.2fr);
			grid-template-areas:
				'identity value'
				'bar bar';
			gap: 8px 12px;
		}

		.firm-identity {
			grid-area: identity;
		}

		.bar-track {
			grid-area: bar;
		}

		.metric-value {
			grid-area: value;
		}

		.comparison-note {
			grid-template-columns: 1fr;
			gap: 4px;
			padding-inline: 16px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.bar-track > i {
			transition: none;
		}
	}
</style>
