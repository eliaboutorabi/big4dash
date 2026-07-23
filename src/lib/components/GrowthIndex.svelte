<script lang="ts">
	import { ArrowUpRight, Gauge, RotateCcw } from '@lucide/svelte';
	import { curveMonotoneX, line } from 'd3-shape';
	import { FIRM_COLORS, FIRMS } from '$lib/data/format';
	import type { FirmName, SeriesPoint } from '$lib/data/types';

	let {
		series,
		onselect
	}: {
		series: Record<FirmName, SeriesPoint[]>;
		onselect: (observationId: string) => void;
	} = $props();

	const plot = { left: 64, right: 844, top: 40, bottom: 282 };
	let baseYear = $state<2015 | 2020>(2020);
	let years = $derived(
		Array.from({ length: 2025 - baseYear + 1 }, (_, index) => baseYear + index)
	);
	let indexed = $derived.by(() => {
		const result = {} as Record<
			FirmName,
			Array<{ year: number; index: number; observationId: string }>
		>;
		for (const firm of FIRMS) {
			const base = series[firm].find((point) => point.year === baseYear)?.value ?? 1;
			result[firm] = series[firm]
				.filter((point) => point.year >= baseYear && point.year <= 2025)
				.map((point) => ({
					year: point.year,
					index: (point.value / base) * 100,
					observationId: point.observationId
				}));
		}
		return result;
	});
	let maxIndex = $derived(
		Math.ceil(
			Math.max(...FIRMS.flatMap((firm) => indexed[firm].map((point) => point.index))) / 10
		) * 10
	);
	let gridValues = $derived(
		Array.from({ length: Math.max((maxIndex - 100) / 10 + 1, 2) }, (_, index) => 100 + index * 10)
	);

	const x = (year: number) =>
		plot.left + ((year - baseYear) / Math.max(2025 - baseYear, 1)) * (plot.right - plot.left);
	const y = (value: number) =>
		plot.bottom - ((value - 95) / Math.max(maxIndex - 95, 1)) * (plot.bottom - plot.top);
	const pathFor = (firm: FirmName) =>
		line<{ year: number; index: number }>()
			.x((point) => x(point.year))
			.y((point) => y(point.index))
			.curve(curveMonotoneX)(indexed[firm]) ?? '';
	const finalPoint = (firm: FirmName) => indexed[firm].at(-1)!;
</script>

<div class="growth-index">
	<div class="growth-copy">
		<div class="growth-symbol"><Gauge size={19} aria-hidden="true" /></div>
		<span>Normalized growth</span>
		<h3>Who compounded fastest?</h3>
		<p>
			Each network begins at 100. The view removes absolute scale and isolates cumulative reported
			revenue growth.
		</p>
		<div class="base-switch" aria-label="Choose index base year">
			<button class:active={baseYear === 2020} onclick={() => (baseYear = 2020)}>2020 = 100</button>
			<button class:active={baseYear === 2015} onclick={() => (baseYear = 2015)}>2015 = 100</button>
		</div>
		<button class="reset-button" onclick={() => (baseYear = 2020)}>
			<RotateCcw size={12} aria-hidden="true" /> Reset frame
		</button>
	</div>

	<div class="index-chart">
		<div class="chart-caption">
			<strong>Reported revenue index</strong>
			<span>{baseYear}–2025 · USD-reported totals</span>
		</div>
		<svg viewBox="0 0 960 330" role="img" aria-labelledby="index-title index-desc">
			<title id="index-title">Indexed Big Four revenue growth from {baseYear} to 2025</title>
			<desc id="index-desc">
				Every firm begins at an index value of 100. Direct labels show its ending index value.
			</desc>
			{#each gridValues as value (value)}
				<line
					class:baseline={value === 100}
					x1={plot.left}
					x2={plot.right}
					y1={y(value)}
					y2={y(value)}
				/>
				<text class="axis-label" x={plot.left - 12} y={y(value) + 4} text-anchor="end">
					{value}
				</text>
			{/each}
			{#each years as year (year)}
				<text class="year-label" x={x(year)} y={plot.bottom + 28} text-anchor="middle">
					{year}
				</text>
			{/each}
			{#each [...FIRMS].reverse() as firm (firm)}
				<path class="index-line underlay" d={pathFor(firm)} />
				<path class="index-line" d={pathFor(firm)} stroke={FIRM_COLORS[firm]} />
				{#each indexed[firm] as point (point.year)}
					<g
						role="button"
						tabindex="0"
						aria-label={`${firm} ${point.year}: revenue index ${point.index.toFixed(1)}. Open evidence.`}
						onclick={() => onselect(point.observationId)}
						onkeydown={(event) => {
							if (event.key === 'Enter' || event.key === ' ') onselect(point.observationId);
						}}
					>
						<circle class="point-target" cx={x(point.year)} cy={y(point.index)} r="10" />
						<circle
							class="index-point"
							cx={x(point.year)}
							cy={y(point.index)}
							r={point.year === 2025 ? 5 : 3}
							fill={FIRM_COLORS[firm]}
						/>
						<title>{firm} · {point.year} · {point.index.toFixed(1)}</title>
					</g>
				{/each}
				<g class="end-label" transform={`translate(${plot.right + 14} ${y(finalPoint(firm).index)})`}>
					<circle r="4" fill={FIRM_COLORS[firm]} />
					<text x="10" y="-2">{firm}</text>
					<text class="end-value" x="10" y="12">{finalPoint(firm).index.toFixed(0)}</text>
					<ArrowUpRight x="48" y="-11" size={13} aria-hidden="true" />
				</g>
			{/each}
		</svg>
		<div class="index-note">
			<span>100</span> marks each firm’s own starting revenue—not a common dollar value.
		</div>
	</div>
</div>

<style>
	.growth-index {
		display: grid;
		grid-template-columns: minmax(230px, 0.62fr) minmax(0, 1.65fr);
		margin-top: 22px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.growth-copy {
		display: grid;
		align-content: start;
		padding: 25px;
		border-right: 1px solid var(--frame);
		background: var(--inverse-surface);
		color: var(--inverse-text);
	}

	.growth-symbol {
		display: grid;
		width: 38px;
		height: 38px;
		margin-bottom: 42px;
		place-items: center;
		background: var(--accent);
		color: var(--accent-ink);
		box-shadow: 3px 3px 0 var(--inverse-text);
	}

	.growth-copy > span {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 10px;
	}

	.growth-copy h3 {
		max-width: 8ch;
		margin: 9px 0 13px;
		font-family: var(--font-display);
		font-size: 34px;
		font-weight: 620;
		letter-spacing: -0.035em;
		line-height: 0.97;
	}

	.growth-copy p {
		max-width: 32ch;
		margin: 0 0 22px;
		color: var(--text-on-dark-muted);
		font-size: 11px;
		line-height: 1.6;
	}

	.base-switch {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		border: 1px solid var(--border-on-dark);
	}

	.base-switch button,
	.reset-button {
		min-height: 36px;
		border: 0;
		background: transparent;
		color: var(--text-on-dark-muted);
		font-size: 10px;
		font-weight: 750;
		cursor: pointer;
	}

	.base-switch button:first-child {
		border-right: 1px solid var(--border-on-dark);
	}

	.base-switch button.active {
		background: var(--accent);
		color: var(--accent-ink);
	}

	.reset-button {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		width: fit-content;
		margin-top: 10px;
		padding: 0;
	}

	.index-chart {
		min-width: 0;
		padding: 21px 22px 15px;
		background: var(--surface-elevated);
	}

	.chart-caption {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 12px;
		padding: 0 6px 7px;
	}

	.chart-caption strong {
		font-size: 12px;
	}

	.chart-caption span {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	svg {
		display: block;
		width: 100%;
		overflow: visible;
	}

	svg line {
		stroke: var(--border-subtle);
		stroke-dasharray: 2 5;
		stroke-width: 1;
	}

	svg line.baseline {
		stroke: var(--ink);
		stroke-dasharray: none;
		stroke-width: 1.5;
	}

	.axis-label,
	.year-label {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 10px;
	}

	.index-line {
		fill: none;
		stroke-linecap: round;
		stroke-linejoin: round;
		stroke-width: 3;
	}

	.index-line.underlay {
		stroke: var(--surface-base);
		stroke-width: 7;
	}

	.point-target {
		fill: transparent;
		cursor: pointer;
	}

	.index-point {
		stroke: var(--surface-base);
		stroke-width: 2;
		pointer-events: none;
	}

	g[role='button']:focus-visible .index-point {
		stroke: var(--ink);
		stroke-width: 4;
	}

	.end-label {
		fill: var(--ink);
		font-size: 10px;
		font-weight: 800;
	}

	.end-value {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.index-note {
		display: flex;
		align-items: center;
		gap: 7px;
		color: var(--text-secondary);
		font-size: 10px;
	}

	.index-note span {
		display: inline-grid;
		width: 30px;
		height: 21px;
		place-items: center;
		background: var(--accent-light);
		color: var(--accent-ink);
		font-family: var(--font-mono);
		font-weight: 800;
	}

	@media (max-width: 900px) {
		.growth-index {
			grid-template-columns: 1fr;
		}

		.growth-copy {
			grid-template-columns: 48px 1fr;
			column-gap: 13px;
			border-right: 0;
			border-bottom: 1px solid var(--frame);
		}

		.growth-symbol {
			grid-row: span 3;
			margin: 0;
		}

		.growth-copy h3 {
			max-width: none;
			font-size: 28px;
		}

		.growth-copy p {
			max-width: 62ch;
		}

		.base-switch,
		.reset-button {
			grid-column: 2;
		}
	}

	@media (max-width: 560px) {
		.index-chart {
			overflow-x: auto;
		}

		.index-chart svg {
			width: 700px;
		}

		.chart-caption,
		.index-note {
			width: 700px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.base-switch button {
			transition: none;
		}
	}
</style>
