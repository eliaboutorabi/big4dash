<script lang="ts">
	import { Calculator, RotateCcw, TrendingUp } from '@lucide/svelte';
	import { untrack } from 'svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, percent } from '$lib/data/format';
	import type { FirmName, FirmSummary } from '$lib/data/types';

	let {
		firms,
		onselect
	}: {
		firms: FirmSummary[];
		onselect: (observationId: string) => void;
	} = $props();

	type ScenarioMode = 'cagr' | 'latest' | 'custom';
	let mode = $state<ScenarioMode>('cagr');
	let horizon = $state<1 | 3 | 5>(5);
	let customRates = $state(
		untrack(
			() =>
				Object.fromEntries(firms.map((firm) => [firm.firm, firm.fiveYearCagr])) as Record<
					FirmName,
					number
				>
		)
	);

	const rateFor = (firm: FirmSummary) =>
		mode === 'cagr' ? firm.fiveYearCagr : mode === 'latest' ? firm.growth : customRates[firm.firm];
	let projections = $derived(
		firms
			.map((firm) => {
				const rate = rateFor(firm);
				const projected = firm.revenue * Math.pow(1 + rate / 100, horizon);
				return {
					...firm,
					rate,
					projected,
					added: projected - firm.revenue
				};
			})
			.sort((a, b) => b.projected - a.projected)
	);
	let maximum = $derived(Math.max(...projections.map((firm) => firm.projected)));
	let projectedTotal = $derived(projections.reduce((sum, firm) => sum + firm.projected, 0));
	let currentTotal = $derived(firms.reduce((sum, firm) => sum + firm.revenue, 0));
	let largestContributor = $derived([...projections].sort((a, b) => b.added - a.added)[0]);

	function setCustomRate(firm: FirmName, value: number) {
		customRates = { ...customRates, [firm]: value };
	}

	function resetCustomRates() {
		customRates = Object.fromEntries(firms.map((firm) => [firm.firm, firm.fiveYearCagr])) as Record<
			FirmName,
			number
		>;
	}
</script>

<div class="scenario-studio">
	<div class="scenario-heading">
		<div class="scenario-symbol"><Calculator size={19} aria-hidden="true" /></div>
		<div>
			<span>Scenario—not forecast</span>
			<h3>Compound the assumptions, then inspect the distance.</h3>
		</div>
		<p>
			Straight-line compounding isolates the consequence of a growth assumption. It does not model
			currency, acquisitions, capacity or economic cycles.
		</p>
	</div>

	<div class="scenario-controls">
		<div class="control-block">
			<span>Growth assumption</span>
			<div class="mode-tabs" aria-label="Choose scenario assumption">
				<button class:active={mode === 'cagr'} onclick={() => (mode = 'cagr')}>5Y CAGR</button>
				<button class:active={mode === 'latest'} onclick={() => (mode = 'latest')}>FY25 pace</button
				>
				<button class:active={mode === 'custom'} onclick={() => (mode = 'custom')}>Custom</button>
			</div>
		</div>
		<div class="control-block horizon-control">
			<span>Compounding horizon</span>
			<div class="horizon-tabs" aria-label="Choose scenario horizon">
				{#each [1, 3, 5] as years (years)}
					<button class:active={horizon === years} onclick={() => (horizon = years as 1 | 3 | 5)}>
						{years}Y
					</button>
				{/each}
			</div>
		</div>
		<div class="scenario-date">
			<span>Illustrative endpoint</span>
			<strong>FY{2025 + horizon}</strong>
		</div>
	</div>

	{#if mode === 'custom'}
		<div class="custom-assumptions">
			{#each FIRMS as firm (firm)}
				<label>
					<span><i style:background={FIRM_COLORS[firm]}></i>{firm}</span>
					<input
						type="range"
						min="-2"
						max="14"
						step="0.1"
						value={customRates[firm]}
						aria-label={`${firm} annual growth assumption`}
						oninput={(event) => setCustomRate(firm, Number(event.currentTarget.value))}
					/>
					<strong>{customRates[firm].toFixed(1)}%</strong>
				</label>
			{/each}
			<button class="reset-assumptions" onclick={resetCustomRates}>
				<RotateCcw size={12} aria-hidden="true" /> Reset to five-year CAGR
			</button>
		</div>
	{/if}

	<div class="scenario-stage">
		<div class="scenario-readout">
			<span>Illustrative four-firm value pool</span>
			<strong>{currencyShort(projectedTotal, 1)}</strong>
			<p>
				{currencyShort(projectedTotal - currentTotal, 1)} above the FY2025 reported baseline after
				{horizon}
				{horizon === 1 ? 'year' : 'years'}.
			</p>
			<div>
				<TrendingUp size={14} aria-hidden="true" />
				<span
					><b>{largestContributor.firm}</b> contributes the largest modeled increase:
					{currencyShort(largestContributor.added, 1)}.</span
				>
			</div>
		</div>

		<div class="projection-bars">
			<div class="projection-axis">
				<span>FY2025 baseline</span>
				<span>Modeled FY{2025 + horizon}</span>
			</div>
			{#each projections as firm, index (firm.firm)}
				<button onclick={() => onselect(firm.revenueObservationId)}>
					<div class="projection-label">
						<span>{String(index + 1).padStart(2, '0')}</span>
						<strong>{firm.firm}</strong>
						<small>{percent(firm.rate)} annual assumption</small>
					</div>
					<div class="bar-track">
						<i
							class="current-bar"
							style:--bar-scale={firm.revenue / maximum}
							style:background={FIRM_COLORS[firm.firm]}
						></i>
						<i
							class="projected-bar"
							style:--bar-scale={firm.projected / maximum}
							style:background={FIRM_COLORS[firm.firm]}
						></i>
					</div>
					<div class="projection-values">
						<span>{currencyShort(firm.revenue, 1)}</span>
						<strong>{currencyShort(firm.projected, 1)}</strong>
						<small>+{currencyShort(firm.added, 1)}</small>
					</div>
				</button>
			{/each}
		</div>
	</div>

	<div class="scenario-method">
		<strong>Method</strong>
		<span>
			FY2025 reported revenue × (1 + annual assumption)<sup>{horizon}</sup>. FY25 pace uses each
			network’s locally reported growth rate against a USD baseline and is therefore a directional
			sensitivity—not a currency-consistent forecast.
		</span>
	</div>
</div>

<style>
	.scenario-studio {
		margin-top: 22px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.scenario-heading {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr) minmax(260px, 0.8fr);
		align-items: center;
		gap: 18px;
		padding: 22px;
		border-bottom: 1px solid var(--frame);
	}

	.scenario-symbol {
		display: grid;
		width: 38px;
		height: 38px;
		place-items: center;
		background: var(--accent);
		color: var(--accent-ink);
		box-shadow: 3px 3px 0 var(--frame);
	}

	.scenario-heading span,
	.control-block > span,
	.scenario-date span {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.scenario-heading h3 {
		margin: 4px 0 0;
		font-family: var(--font-display);
		font-size: 24px;
		font-weight: 620;
		letter-spacing: -0.03em;
		line-height: 1.05;
		text-wrap: balance;
	}

	.scenario-heading p {
		max-width: 52ch;
		margin: 0;
		color: var(--text-secondary);
		font-size: 10px;
		line-height: 1.55;
	}

	.scenario-controls {
		display: grid;
		grid-template-columns: minmax(320px, 1fr) minmax(210px, 0.58fr) auto;
		gap: 18px;
		padding: 14px 22px;
		border-bottom: 1px solid var(--frame);
		background: var(--surface-subtle);
	}

	.control-block {
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: center;
		gap: 12px;
	}

	.mode-tabs,
	.horizon-tabs {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		border: 1px solid var(--frame);
	}

	.mode-tabs button,
	.horizon-tabs button {
		min-height: 34px;
		border: 0;
		border-right: 1px solid var(--frame);
		background: var(--surface-base);
		color: var(--text-secondary);
		font-size: 9px;
		font-weight: 750;
		cursor: pointer;
	}

	.mode-tabs button:last-child,
	.horizon-tabs button:last-child {
		border-right: 0;
	}

	.mode-tabs button.active,
	.horizon-tabs button.active {
		background: var(--ink);
		color: var(--surface-base);
	}

	.scenario-date {
		display: grid;
		align-content: center;
		justify-items: end;
	}

	.scenario-date strong {
		font-family: var(--font-mono);
		font-size: 16px;
	}

	.custom-assumptions {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr)) auto;
		gap: 14px;
		padding: 15px 22px;
		border-bottom: 1px solid var(--frame);
		background: var(--accent-soft);
	}

	.custom-assumptions label {
		display: grid;
		grid-template-columns: 1fr auto;
		align-items: center;
		gap: 7px;
	}

	.custom-assumptions label > span {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 9px;
		font-weight: 750;
	}

	.custom-assumptions label i {
		width: 6px;
		height: 13px;
	}

	.custom-assumptions input {
		grid-column: 1 / 3;
		width: 100%;
		accent-color: var(--ink);
	}

	.custom-assumptions label strong {
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.reset-assumptions {
		align-self: end;
		min-height: 32px;
		padding: 0 10px;
		border: 1px solid var(--frame);
		background: var(--surface-base);
		color: var(--ink);
		font-size: 9px;
		font-weight: 750;
		cursor: pointer;
	}

	.scenario-stage {
		display: grid;
		grid-template-columns: minmax(220px, 0.58fr) minmax(0, 1.55fr);
		min-height: 390px;
		background: var(--inverse-surface);
		color: var(--inverse-text);
	}

	.scenario-readout {
		display: grid;
		align-content: start;
		padding: 28px;
		border-right: 1px solid var(--border-on-dark);
	}

	.scenario-readout > span {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.scenario-readout > strong {
		margin: 10px 0 6px;
		font-family: var(--font-mono);
		font-size: clamp(32px, 4vw, 50px);
		line-height: 1;
	}

	.scenario-readout > p {
		max-width: 30ch;
		margin: 0;
		color: var(--text-on-dark-muted);
		font-size: 10px;
		line-height: 1.55;
	}

	.scenario-readout > div {
		display: flex;
		align-items: flex-start;
		gap: 8px;
		margin-top: 38px;
		padding-top: 16px;
		border-top: 1px solid var(--border-on-dark);
		color: var(--text-on-dark-muted);
		font-size: 9px;
		line-height: 1.5;
	}

	.scenario-readout b {
		color: var(--inverse-text);
	}

	.projection-bars {
		padding: 23px 26px 26px;
	}

	.projection-axis {
		display: flex;
		justify-content: space-between;
		margin-bottom: 12px;
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.projection-bars > button {
		display: grid;
		width: 100%;
		grid-template-columns: 128px minmax(0, 1fr) 114px;
		align-items: center;
		gap: 15px;
		padding: 15px 0;
		border: 0;
		border-top: 1px solid var(--border-on-dark);
		background: transparent;
		color: var(--inverse-text);
		text-align: left;
		cursor: pointer;
	}

	.projection-bars > button:hover {
		background: color-mix(in oklch, var(--inverse-text) 4%, transparent);
	}

	.projection-label {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 2px 7px;
	}

	.projection-label > span {
		grid-row: 1 / 3;
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.projection-label strong {
		font-size: 10px;
	}

	.projection-label small {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.bar-track {
		position: relative;
		height: 21px;
		border-left: 1px solid var(--border-on-dark);
	}

	.bar-track i {
		position: absolute;
		left: 0;
		display: block;
		width: 100%;
		transform: scaleX(var(--bar-scale));
		transform-origin: left;
	}

	.current-bar {
		top: 2px;
		height: 5px;
		opacity: 0.38;
	}

	.projected-bar {
		bottom: 1px;
		height: 10px;
		transition: transform 220ms var(--ease-out);
	}

	.projection-values {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 1px 7px;
		font-family: var(--font-mono);
		text-align: right;
	}

	.projection-values span {
		color: var(--text-on-dark-muted);
		font-size: 8px;
	}

	.projection-values strong {
		font-size: 11px;
	}

	.projection-values small {
		grid-column: 1 / 3;
		color: var(--accent);
		font-size: 8px;
	}

	.scenario-method {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 12px;
		padding: 12px 22px;
		border-top: 1px solid var(--frame);
		color: var(--text-secondary);
		font-size: 9px;
		line-height: 1.5;
	}

	.scenario-method strong {
		color: var(--ink);
		font-family: var(--font-mono);
	}

	@media (max-width: 940px) {
		.scenario-heading {
			grid-template-columns: auto 1fr;
		}

		.scenario-heading p {
			grid-column: 2;
		}

		.scenario-controls {
			grid-template-columns: 1fr 1fr;
		}

		.scenario-date {
			grid-column: 1 / 3;
			justify-items: start;
		}

		.custom-assumptions {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
	}

	@media (max-width: 720px) {
		.scenario-heading {
			grid-template-columns: auto 1fr;
			padding: 18px;
		}

		.scenario-heading p {
			grid-column: 1 / 3;
		}

		.scenario-controls,
		.scenario-stage {
			grid-template-columns: 1fr;
		}

		.scenario-date {
			grid-column: auto;
		}

		.control-block {
			grid-template-columns: 1fr;
		}

		.scenario-readout {
			border-right: 0;
			border-bottom: 1px solid var(--border-on-dark);
		}

		.projection-bars > button {
			grid-template-columns: 96px minmax(0, 1fr);
		}

		.projection-values {
			grid-column: 1 / 3;
			grid-template-columns: auto auto 1fr;
			text-align: left;
		}

		.projection-values small {
			grid-column: auto;
			text-align: right;
		}
	}

	@media (max-width: 480px) {
		.custom-assumptions {
			grid-template-columns: 1fr;
		}

		.projection-bars {
			padding: 18px;
		}

		.projection-bars > button {
			grid-template-columns: 82px minmax(0, 1fr);
			gap: 10px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.projected-bar {
			transition: none;
		}
	}
</style>
