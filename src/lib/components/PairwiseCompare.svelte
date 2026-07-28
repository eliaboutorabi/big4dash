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

	function choose(side: 'left' | 'right', firm: FirmName) {
		if (side === 'left') {
			if (firm === rightFirm) rightFirm = leftFirm;
			leftFirm = firm;
		} else {
			if (firm === leftFirm) leftFirm = rightFirm;
			rightFirm = firm;
		}
	}

	function value(firm: FirmSummary, key: (typeof metrics)[number]['key']) {
		return firm[key];
	}
</script>

<div class="pairwise-compare">
	<div class="compare-heading">
		<div class="compare-symbol"><GitCompareArrows size={18} aria-hidden="true" /></div>
		<div>
			<span>Pairwise workbench</span>
			<strong>Put any two networks under the same lens.</strong>
		</div>
		<p>A shared scale reveals the distance between each pair; every value opens its record.</p>
	</div>

	<div class="compare-selectors">
		<strong>Networks</strong>
		<div class="selector-pair">
			<label>
				<span>Network A</span>
				<select
					value={leftFirm}
					aria-label="Choose first network"
					onchange={(event) => choose('left', event.currentTarget.value as FirmName)}
				>
					{#each FIRMS as firm (firm)}<option value={firm}>{firm}</option>{/each}
				</select>
			</label>
			<div class="versus" aria-hidden="true">vs</div>
			<label>
				<span>Network B</span>
				<select
					value={rightFirm}
					aria-label="Choose second network"
					onchange={(event) => choose('right', event.currentTarget.value as FirmName)}
				>
					{#each FIRMS as firm (firm)}<option value={firm}>{firm}</option>{/each}
				</select>
			</label>
		</div>
		<span class="selector-note">Choose any pair</span>
	</div>

	<div class="comparison-table">
		<div class="comparison-head">
			<span>Measure</span>
			<div class="firm-heads">
				<strong style:--firm-color={FIRM_COLORS[leftFirm]}>
					<i class="firm-key firm-key-left"></i>{leftFirm}
				</strong>
				<strong style:--firm-color={FIRM_COLORS[rightFirm]}>
					<i class="firm-key firm-key-right"></i>{rightFirm}
				</strong>
			</div>
			<span>Difference</span>
		</div>
		{#each metrics as metric (metric.key)}
			{@const leftValue = value(left, metric.key)}
			{@const rightValue = value(right, metric.key)}
			{@const maximum = Math.max(leftValue, rightValue, 1)}
			{@const leftPosition = leftValue / maximum}
			{@const rightPosition = rightValue / maximum}
			{@const delta = leftValue - rightValue}
			<div class="comparison-row">
				<strong>{metric.label}</strong>
				<div
					class="metric-pair"
					style:--left-position={leftPosition}
					style:--right-position={rightPosition}
					style:--gap-start={Math.min(leftPosition, rightPosition)}
					style:--gap-size={Math.abs(leftPosition - rightPosition)}
				>
					<div class="pair-values">
						<button
							data-firm={leftFirm}
							style:--firm-color={FIRM_COLORS[leftFirm]}
							onclick={() => onselect(metric.evidence(left))}
							aria-label={`Open ${leftFirm} ${metric.label} evidence: ${metric.format(leftValue)}`}
						>
							<small>{leftFirm}</small>
							<span>{metric.format(leftValue)}</span>
						</button>
						<button
							data-firm={rightFirm}
							style:--firm-color={FIRM_COLORS[rightFirm]}
							onclick={() => onselect(metric.evidence(right))}
							aria-label={`Open ${rightFirm} ${metric.label} evidence: ${metric.format(rightValue)}`}
						>
							<small>{rightFirm}</small>
							<span>{metric.format(rightValue)}</span>
						</button>
					</div>
					<div class="comparison-track" aria-hidden="true">
						<span class="track-rail"></span>
						{#if delta !== 0}<span class="difference-segment"></span>{/if}
						<i class="comparison-marker marker-left" style:--firm-color={FIRM_COLORS[leftFirm]}></i>
						<i class="comparison-marker marker-right" style:--firm-color={FIRM_COLORS[rightFirm]}
						></i>
					</div>
				</div>
				<span class="gap-readout" class:even={delta === 0}>
					<strong>{delta === 0 ? 'Even' : `${delta > 0 ? leftFirm : rightFirm} leads`}</strong>
					<small>
						{metric.key === 'revenue' || metric.key === 'revenuePerPerson'
							? currencyShort(Math.abs(delta), metric.key === 'revenuePerPerson' ? 0 : 1)
							: metric.key === 'people'
								? fullNumber(Math.abs(delta))
								: `${Math.abs(delta).toFixed(1)} pts`}
					</small>
				</span>
			</div>
		{/each}
	</div>

	<div class="period-note">
		<strong>Reporting periods</strong>
		<div>
			<span>{leftFirm}: {left.periodStart} → {left.periodEnd}</span>
			<span>{rightFirm}: {right.periodStart} → {right.periodEnd}</span>
		</div>
	</div>
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
		gap: 2px;
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
		margin: 0;
		color: var(--text-on-dark-muted);
		font-size: 10px;
		line-height: 1.5;
	}

	.compare-selectors {
		display: grid;
		grid-template-columns: 140px minmax(0, 1fr) 110px;
		gap: 16px;
		align-items: center;
		padding: 12px 20px;
		border-bottom: 1px solid var(--border-subtle);
		background: var(--surface-muted);
	}

	.compare-selectors > strong,
	.selector-note {
		color: var(--text-tertiary);
		font-size: 9px;
	}

	.selector-note {
		font-family: var(--font-mono);
		text-align: right;
	}

	.selector-pair {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
		gap: 12px;
		align-items: end;
	}

	.selector-pair label {
		display: grid;
		min-width: 0;
		gap: 4px;
	}

	.selector-pair label span {
		color: var(--text-tertiary);
		font-size: 9px;
		font-weight: 750;
	}

	select {
		width: 100%;
		height: 44px;
		padding: 0 10px;
		border: 1px solid var(--frame);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--ink);
		font-size: 11px;
		font-weight: 800;
	}

	.versus {
		padding-bottom: 12px;
		color: var(--text-tertiary);
		font-family: var(--font-display);
		font-style: italic;
		font-size: 13px;
	}

	.comparison-table {
		padding: 8px 20px;
	}

	.comparison-head,
	.comparison-row {
		display: grid;
		grid-template-columns: 140px minmax(0, 1fr) 110px;
		gap: 16px;
		align-items: center;
	}

	.comparison-head {
		min-height: 30px;
		color: var(--text-tertiary);
		font-size: 9px;
	}

	.firm-heads,
	.pair-values {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 12px;
	}

	.firm-heads strong {
		display: flex;
		align-items: center;
		gap: 8px;
		color: var(--ink);
		font-size: 10px;
	}

	.firm-key {
		display: block;
		width: 9px;
		height: 9px;
		flex: 0 0 auto;
		background: var(--firm-color);
		box-shadow: 0 0 0 1px var(--frame);
	}

	.firm-key-left {
		border-radius: 50%;
	}

	.firm-key-right {
		width: 8px;
		height: 8px;
		transform: rotate(45deg);
	}

	.comparison-row {
		min-height: 72px;
		border-top: 1px solid var(--border-subtle);
	}

	.comparison-row > strong {
		font-size: 11px;
	}

	.metric-pair {
		display: grid;
		gap: 4px;
		min-width: 0;
	}

	.pair-values button {
		display: grid;
		gap: 2px;
		min-width: 0;
		min-height: 44px;
		padding: 4px 8px;
		border: 0;
		background: transparent;
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.pair-values button:last-child {
		text-align: right;
	}

	.pair-values button:hover,
	.pair-values button:focus-visible {
		background: color-mix(in oklab, var(--firm-color) 10%, transparent);
		outline: 1px solid var(--firm-color);
		outline-offset: -1px;
	}

	.pair-values button small {
		overflow: hidden;
		color: var(--text-tertiary);
		font-size: 8px;
		font-weight: 750;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.pair-values button span {
		font-family: var(--font-mono);
		font-size: 13px;
		font-weight: 750;
	}

	.comparison-track {
		position: relative;
		height: 24px;
		margin: 0 8px;
	}

	.track-rail,
	.difference-segment,
	.comparison-marker {
		position: absolute;
	}

	.track-rail {
		top: 11px;
		left: 0;
		width: 100%;
		height: 2px;
		background: var(--border-subtle);
	}

	.track-rail::before,
	.track-rail::after {
		position: absolute;
		top: -2px;
		width: 1px;
		height: 6px;
		background: var(--text-tertiary);
		content: '';
	}

	.track-rail::before {
		left: 0;
	}

	.track-rail::after {
		right: 0;
	}

	.difference-segment {
		top: 10px;
		left: calc(var(--gap-start) * 100%);
		width: max(2px, calc(var(--gap-size) * 100%));
		height: 4px;
		background: var(--ink);
		transition:
			left 220ms var(--ease-out),
			width 220ms var(--ease-out);
	}

	.comparison-marker {
		z-index: 1;
		background: var(--firm-color);
		box-shadow:
			0 0 0 1px var(--surface-base),
			0 0 0 2px var(--frame);
		transition: left 220ms var(--ease-out);
	}

	.marker-left {
		top: 1px;
		left: calc(var(--left-position) * 100%);
		width: 12px;
		height: 12px;
		border-radius: 50%;
		transform: translateX(-50%);
	}

	.marker-right {
		top: 12px;
		left: calc(var(--right-position) * 100%);
		width: 10px;
		height: 10px;
		transform: translateX(-50%) rotate(45deg);
	}

	.gap-readout {
		display: grid;
		gap: 2px;
		color: var(--ink);
		font-family: var(--font-mono);
	}

	.gap-readout strong {
		font-size: 9px;
	}

	.gap-readout small {
		color: var(--text-secondary);
		font-size: 10px;
	}

	.gap-readout.even strong {
		color: var(--text-tertiary);
	}

	.period-note {
		display: grid;
		grid-template-columns: 140px minmax(0, 1fr) 110px;
		gap: 16px;
		align-items: start;
		padding: 8px 20px;
		border-top: 1px solid var(--frame);
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.period-note > strong {
		font-size: 8px;
	}

	.period-note > div {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 12px;
	}

	.period-note > div span:last-child {
		text-align: right;
	}

	@container (max-width: 680px) {
		.compare-heading {
			grid-template-columns: 40px 1fr;
		}

		.compare-heading p {
			grid-column: 2;
		}

		.compare-selectors {
			grid-template-columns: 1fr;
			gap: 8px;
			padding-inline: 16px;
		}

		.compare-selectors > strong,
		.selector-note {
			display: none;
		}

		.comparison-table {
			padding-inline: 16px;
		}

		.comparison-head {
			grid-template-columns: 1fr;
		}

		.comparison-head > span {
			display: none;
		}

		.comparison-row {
			grid-template-columns: minmax(0, 1fr) auto;
			grid-template-areas:
				'metric gap'
				'pair pair';
			gap: 8px 12px;
			padding: 12px 0;
		}

		.comparison-row > strong {
			grid-area: metric;
		}

		.metric-pair {
			grid-area: pair;
		}

		.gap-readout {
			grid-area: gap;
			text-align: right;
		}

		.period-note {
			grid-template-columns: 1fr;
			gap: 4px;
			padding-inline: 16px;
		}
	}

	@container (max-width: 420px) {
		.selector-pair {
			gap: 8px;
		}

		.versus {
			font-size: 10px;
		}

		.period-note > div {
			gap: 8px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.difference-segment,
		.comparison-marker {
			transition: none;
		}
	}
</style>
