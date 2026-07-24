<script lang="ts">
	import { Scale, ScanLine } from '@lucide/svelte';
	import { area, curveMonotoneX } from 'd3-shape';
	import { FIRM_COLORS, FIRMS, currencyShort } from '$lib/data/format';
	import type { FirmName, SeriesPoint } from '$lib/data/types';

	let {
		series,
		onselect
	}: {
		series: Record<FirmName, SeriesPoint[]>;
		onselect: (observationId: string) => void;
	} = $props();

	const plot = { left: 34, right: 724, top: 22, bottom: 292 };
	let selectedYear = $state(2025);
	let chart = $derived.by(() => {
		const years = series.Deloitte.map((point) => point.year);
		const rows = years.map((year) => {
			const points = FIRMS.map((firm) => series[firm].find((point) => point.year === year)!);
			const total = points.reduce((sum, point) => sum + point.value, 0);
			let cumulative = 0;
			const firms = FIRMS.map((firm, index) => {
				const point = points[index];
				const share = (point.value / total) * 100;
				const lower = cumulative;
				cumulative += share;
				return {
					firm,
					year,
					value: point.value,
					share,
					lower,
					upper: cumulative,
					observationId: point.observationId
				};
			});
			return { year, total, firms };
		});
		const x = (year: number) =>
			plot.left +
			((year - years[0]) / Math.max(years.at(-1)! - years[0], 1)) * (plot.right - plot.left);
		const y = (share: number) => plot.bottom - (share / 100) * (plot.bottom - plot.top);
		const paths = FIRMS.map((firm) => {
			const points = rows.map((row) => row.firms.find((entry) => entry.firm === firm)!);
			return {
				firm,
				path:
					area<(typeof points)[number]>()
						.x((point) => x(point.year))
						.y0((point) => y(point.lower))
						.y1((point) => y(point.upper))
						.curve(curveMonotoneX)(points) ?? ''
			};
		});
		return { years, rows, paths, x, y };
	});
	let selected = $derived(
		chart.rows.find((row) => row.year === selectedYear) ?? chart.rows.at(-1)!
	);
	let baseline = $derived(chart.rows[0]);
	let ranked = $derived(
		[...selected.firms]
			.sort((a, b) => b.share - a.share)
			.map((firm) => ({
				...firm,
				change:
					firm.share - baseline.firms.find((baselineFirm) => baselineFirm.firm === firm.firm)!.share
			}))
	);
	let effectivePeers = $derived(
		1 / selected.firms.reduce((sum, firm) => sum + Math.pow(firm.share / 100, 2), 0)
	);
	const focusYear = (year: number) => {
		selectedYear = year;
	};
</script>

<div class="share-history">
	<div class="share-copy">
		<div class="share-symbol"><Scale size={18} aria-hidden="true" /></div>
		<span>Within-four share</span>
		<h3>Scale moved. So did the balance of power.</h3>
		<p>
			Each band is a network’s share of the four firms’ combined reported revenue. Scrub the
			timeline to see who gained ground.
		</p>
		<div class="balance-readout">
			<strong>{effectivePeers.toFixed(2)}</strong>
			<span>revenue-equivalent peers in {selectedYear}</span>
		</div>
		<small>Within-four measure only—not total professional-services market share.</small>
	</div>

	<div class="share-chart">
		<div class="chart-caption">
			<div>
				<ScanLine size={14} aria-hidden="true" />
				<strong>Reported revenue share</strong>
			</div>
			<span>{selectedYear} · {currencyShort(selected.total, 1)} combined</span>
		</div>
		<div class="plot-scroll">
			<svg viewBox="0 0 780 330" role="img" aria-labelledby="share-title share-desc">
				<title id="share-title">Big Four share of combined reported revenue, 2010 to 2025</title>
				<desc id="share-desc">
					Stacked bands show each firm’s percentage of the four-network reported revenue total. Use
					the year targets to update the detailed readout.
				</desc>
				{#each [25, 50, 75] as share (share)}
					<line
						class="share-grid"
						x1={plot.left}
						x2={plot.right}
						y1={chart.y(share)}
						y2={chart.y(share)}
					/>
					<text class="axis-label" x={plot.left - 8} y={chart.y(share) + 4} text-anchor="end">
						{share}
					</text>
				{/each}
				{#each chart.paths as item (item.firm)}
					<path
						class="share-area"
						class:selected={ranked[0].firm === item.firm}
						d={item.path}
						fill={FIRM_COLORS[item.firm]}
					/>
				{/each}
				<line
					class="selected-rule"
					x1={chart.x(selectedYear)}
					x2={chart.x(selectedYear)}
					y1={plot.top}
					y2={plot.bottom}
				/>
				{#each chart.years as year, index (year)}
					<g
						role="button"
						tabindex="0"
						aria-label={`Show reported revenue share for ${year}`}
						onmouseenter={() => focusYear(year)}
						onfocus={() => focusYear(year)}
						onclick={() => focusYear(year)}
						onkeydown={(event) => {
							if (event.key === 'Enter' || event.key === ' ') focusYear(year);
						}}
					>
						<rect
							class="year-target"
							x={chart.x(year) - 22}
							y={plot.top}
							width="44"
							height={plot.bottom - plot.top}
						/>
						{#if year === 2010 || year === 2015 || year === 2020 || year === 2025}
							<text class="year-label" x={chart.x(year)} y={plot.bottom + 25} text-anchor="middle">
								{year}
							</text>
						{/if}
						{#if index === chart.years.length - 1}
							<title>Move across the chart to inspect each year</title>
						{/if}
					</g>
				{/each}
			</svg>
		</div>

		<div class="share-ranking" aria-live="polite">
			{#each ranked as item, index (item.firm)}
				<button onclick={() => onselect(item.observationId)}>
					<span class="rank">{String(index + 1).padStart(2, '0')}</span>
					<i style:background={FIRM_COLORS[item.firm]}></i>
					<strong>{item.firm}</strong>
					<b>{item.share.toFixed(1)}%</b>
					<small class:negative={item.change < 0}>
						{item.change >= 0 ? '+' : ''}{item.change.toFixed(1)} pts since 2010
					</small>
				</button>
			{/each}
		</div>
	</div>
</div>

<style>
	.share-history {
		display: grid;
		grid-template-columns: minmax(230px, 0.68fr) minmax(0, 1.65fr);
		margin-top: 22px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.share-copy {
		display: grid;
		align-content: start;
		padding: 25px;
		border-right: 1px solid var(--frame);
		background: var(--accent-soft);
	}

	.share-symbol {
		display: grid;
		width: 38px;
		height: 38px;
		margin-bottom: 42px;
		place-items: center;
		border: 1px solid var(--frame);
		background: var(--accent);
		color: var(--accent-ink);
		box-shadow: 3px 3px 0 var(--frame);
	}

	.share-copy > span {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 10px;
	}

	.share-copy h3 {
		max-width: 12ch;
		margin: 9px 0 13px;
		font-family: var(--font-display);
		font-size: 31px;
		font-weight: 620;
		letter-spacing: -0.035em;
		line-height: 1;
		text-wrap: balance;
	}

	.share-copy p {
		max-width: 34ch;
		margin: 0;
		color: var(--text-secondary);
		font-size: 11px;
		line-height: 1.6;
	}

	.balance-readout {
		display: grid;
		grid-template-columns: auto 1fr;
		align-items: end;
		gap: 9px;
		margin-top: 28px;
		padding-top: 18px;
		border-top: 1px solid var(--frame);
	}

	.balance-readout strong {
		font-family: var(--font-mono);
		font-size: 27px;
		line-height: 1;
	}

	.balance-readout span,
	.share-copy small {
		color: var(--text-secondary);
		font-size: 9px;
		line-height: 1.45;
	}

	.share-copy small {
		margin-top: 10px;
	}

	.share-chart {
		min-width: 0;
		padding: 22px;
	}

	.chart-caption {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 18px;
		margin-bottom: 8px;
	}

	.chart-caption div {
		display: flex;
		align-items: center;
		gap: 7px;
	}

	.chart-caption strong {
		font-size: 11px;
	}

	.chart-caption > span {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.plot-scroll {
		overflow-x: auto;
	}

	svg {
		display: block;
		width: 100%;
	}

	.share-grid {
		stroke: var(--chart-grid);
		stroke-dasharray: 2 4;
	}

	.axis-label,
	.year-label {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.share-area {
		opacity: 0.76;
		stroke: var(--surface-base);
		stroke-width: 1.5;
		transition: opacity 180ms var(--ease-out);
	}

	.share-area.selected {
		opacity: 0.92;
	}

	.selected-rule {
		pointer-events: none;
		stroke: var(--ink);
		stroke-dasharray: 3 4;
		stroke-width: 1.5;
	}

	.year-target {
		fill: transparent;
		cursor: crosshair;
	}

	g:focus-visible .year-target {
		stroke: var(--focus-ring);
		stroke-width: 2;
	}

	.share-ranking {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		border: 1px solid var(--frame);
	}

	.share-ranking button {
		display: grid;
		grid-template-columns: auto 7px 1fr auto;
		align-items: center;
		gap: 7px;
		min-width: 0;
		padding: 11px;
		border: 0;
		border-right: 1px solid var(--frame);
		background: var(--surface-base);
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.share-ranking button:last-child {
		border-right: 0;
	}

	.share-ranking button:hover {
		background: var(--surface-subtle);
	}

	.rank {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.share-ranking i {
		width: 7px;
		height: 18px;
	}

	.share-ranking strong {
		overflow: hidden;
		font-size: 10px;
		text-overflow: ellipsis;
	}

	.share-ranking b {
		font-family: var(--font-mono);
		font-size: 10px;
	}

	.share-ranking small {
		grid-column: 3 / 5;
		color: var(--success);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.share-ranking small.negative {
		color: var(--accent-strong);
	}

	@media (max-width: 900px) {
		.share-history {
			grid-template-columns: 1fr;
		}

		.share-copy {
			border-right: 0;
			border-bottom: 1px solid var(--frame);
		}

		.share-symbol {
			margin-bottom: 24px;
		}
	}

	@media (max-width: 680px) {
		.share-chart {
			padding: 16px;
		}

		.chart-caption {
			align-items: flex-start;
			flex-direction: column;
			gap: 5px;
		}

		.share-ranking {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}

		.share-ranking button:nth-child(2) {
			border-right: 0;
		}

		.share-ranking button:nth-child(-n + 2) {
			border-bottom: 1px solid var(--frame);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.share-area {
			transition: none;
		}
	}
</style>
