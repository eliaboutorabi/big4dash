<script lang="ts">
	import { ArrowDownRight, ArrowUpRight, GitCompareArrows } from '@lucide/svelte';
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
		<p>Bars compare direction and magnitude; each value opens its supporting record.</p>
	</div>

	<div class="compare-selectors">
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
		<div class="versus">versus</div>
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

	<div class="comparison-table">
		<div class="comparison-head">
			<span>Measure</span>
			<strong style:--firm-color={FIRM_COLORS[leftFirm]}>{leftFirm}</strong>
			<strong style:--firm-color={FIRM_COLORS[rightFirm]}>{rightFirm}</strong>
			<span>Gap</span>
		</div>
		{#each metrics as metric (metric.key)}
			{@const leftValue = value(left, metric.key)}
			{@const rightValue = value(right, metric.key)}
			{@const maximum = Math.max(leftValue, rightValue)}
			{@const delta = leftValue - rightValue}
			<div class="comparison-row">
				<strong>{metric.label}</strong>
				<button data-firm={leftFirm} onclick={() => onselect(metric.evidence(left))}>
					<span>{metric.format(leftValue)}</span>
					<i style:--bar-scale={leftValue / maximum} style:background={FIRM_COLORS[leftFirm]}></i>
				</button>
				<button data-firm={rightFirm} onclick={() => onselect(metric.evidence(right))}>
					<span>{metric.format(rightValue)}</span>
					<i style:--bar-scale={rightValue / maximum} style:background={FIRM_COLORS[rightFirm]}></i>
				</button>
				<span class:negative={delta < 0}>
					{#if delta >= 0}<ArrowUpRight size={12} />{:else}<ArrowDownRight size={12} />{/if}
					{metric.key === 'revenue' || metric.key === 'revenuePerPerson'
						? currencyShort(Math.abs(delta), metric.key === 'revenuePerPerson' ? 0 : 1)
						: metric.key === 'people'
							? fullNumber(Math.abs(delta))
							: `${Math.abs(delta).toFixed(1)} pts`}
				</span>
			</div>
		{/each}
	</div>

	<div class="period-note">
		<span>{leftFirm}: {left.periodStart} → {left.periodEnd}</span>
		<span>{rightFirm}: {right.periodStart} → {right.periodEnd}</span>
	</div>
</div>

<style>
	.pairwise-compare {
		margin-top: 22px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.compare-heading {
		display: grid;
		grid-template-columns: 40px minmax(240px, 1fr) minmax(260px, 0.8fr);
		gap: 13px;
		align-items: center;
		padding: 17px 20px;
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
		grid-template-columns: 1fr auto 1fr;
		gap: 13px;
		align-items: end;
		padding: 13px 20px;
		border-bottom: 1px solid var(--border-subtle);
		background: var(--surface-muted);
	}

	.compare-selectors label {
		display: grid;
		gap: 5px;
	}

	.compare-selectors label span {
		color: var(--text-tertiary);
		font-size: 9px;
		font-weight: 750;
	}

	select {
		width: 100%;
		height: 36px;
		padding: 0 10px;
		border: 1px solid var(--frame);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--ink);
		font-size: 11px;
		font-weight: 800;
	}

	.versus {
		padding-bottom: 10px;
		color: var(--text-tertiary);
		font-family: var(--font-display);
		font-style: italic;
		font-size: 13px;
	}

	.comparison-table {
		padding: 10px 20px 8px;
	}

	.comparison-head,
	.comparison-row {
		display: grid;
		grid-template-columns: 140px repeat(2, minmax(130px, 1fr)) 115px;
		gap: 14px;
		align-items: center;
	}

	.comparison-head {
		min-height: 30px;
		color: var(--text-tertiary);
		font-size: 9px;
	}

	.comparison-head strong {
		position: relative;
		padding-left: 11px;
		color: var(--ink);
		font-size: 10px;
	}

	.comparison-head strong::before {
		position: absolute;
		top: 4px;
		left: 0;
		width: 6px;
		height: 6px;
		background: var(--firm-color);
		content: '';
	}

	.comparison-row {
		min-height: 48px;
		border-top: 1px solid var(--border-subtle);
	}

	.comparison-row > strong {
		font-size: 10px;
	}

	.comparison-row button {
		display: grid;
		gap: 5px;
		padding: 0;
		border: 0;
		background: transparent;
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.comparison-row button span {
		font-family: var(--font-mono);
		font-size: 11px;
		font-weight: 750;
	}

	.comparison-row button i {
		display: block;
		width: 100%;
		height: 4px;
		min-width: 3px;
		transform: scaleX(var(--bar-scale));
		transform-origin: left;
		transition: transform 220ms var(--ease-out);
	}

	.comparison-row > span {
		display: flex;
		align-items: center;
		gap: 5px;
		color: var(--success);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.comparison-row > span.negative {
		color: var(--accent-strong);
	}

	.period-note {
		display: flex;
		justify-content: space-between;
		gap: 12px;
		padding: 9px 20px;
		border-top: 1px solid var(--frame);
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	@media (max-width: 760px) {
		.compare-heading {
			grid-template-columns: 40px 1fr;
		}

		.compare-heading p {
			grid-column: 2;
		}

		.comparison-head {
			display: none;
		}

		.comparison-row {
			grid-template-columns: repeat(2, minmax(0, 1fr));
			grid-template-areas:
				'metric metric'
				'left right'
				'gap gap';
			gap: 9px 12px;
			padding: 13px 0;
		}

		.comparison-row > strong {
			grid-area: metric;
		}

		.comparison-row > button:nth-child(2) {
			grid-area: left;
		}

		.comparison-row > button:nth-child(3) {
			grid-area: right;
		}

		.comparison-row > span {
			grid-area: gap;
		}

		.comparison-row button::before {
			color: var(--text-tertiary);
			font-size: 8px;
			font-weight: 750;
			content: attr(data-firm);
		}
	}

	@media (max-width: 480px) {
		.compare-selectors {
			grid-template-columns: 1fr;
		}

		.versus {
			display: none;
		}

		.period-note {
			align-items: flex-start;
			flex-direction: column;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.comparison-row button i {
			transition: none;
		}
	}
</style>
