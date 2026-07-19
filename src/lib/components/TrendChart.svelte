<script lang="ts">
	import { ArrowUpRight } from '@lucide/svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, numberShort, percent } from '$lib/data/format';
	import type { FirmName, SeriesPoint } from '$lib/data/types';

	interface Props {
		series: Record<FirmName, SeriesPoint[]>;
		metric: 'revenue' | 'people' | 'growth';
		selectedFirms?: FirmName[];
		onSelect?: (observationId: string) => void;
	}

	let { series, metric, selectedFirms = FIRMS, onSelect = () => {} }: Props = $props();
	let hovered = $state<{ firm: FirmName; point: SeriesPoint } | null>(null);

	const width = 980;
	const height = 430;
	const margin = { top: 28, right: 88, bottom: 50, left: 72 };
	const plotWidth = width - margin.left - margin.right;
	const plotHeight = height - margin.top - margin.bottom;

	let visibleSeries = $derived(
		Object.fromEntries(selectedFirms.map((firm) => [firm, series[firm] ?? []])) as Record<
			FirmName,
			SeriesPoint[]
		>
	);
	let allPoints = $derived(Object.values(visibleSeries).flat());
	let years = $derived([...new Set(allPoints.map((point) => point.year))].sort((a, b) => a - b));
	let yMax = $derived(Math.max(...allPoints.map((point) => point.value), 1) * 1.08);
	let yMin = $derived(
		metric === 'growth' ? Math.min(0, ...allPoints.map((point) => point.value)) : 0
	);
	let yTicks = $derived(
		Array.from({ length: 5 }, (_, index) => yMin + ((yMax - yMin) * index) / 4)
	);

	function x(year: number) {
		if (years.length <= 1) return margin.left;
		return margin.left + ((year - years[0]) / (years.at(-1)! - years[0])) * plotWidth;
	}

	function y(value: number) {
		return margin.top + plotHeight - ((value - yMin) / (yMax - yMin)) * plotHeight;
	}

	function pathFor(points: SeriesPoint[]) {
		return points
			.map((point, index) => `${index === 0 ? 'M' : 'L'} ${x(point.year)} ${y(point.value)}`)
			.join(' ');
	}

	function displayValue(value: number) {
		if (metric === 'revenue') return currencyShort(value);
		if (metric === 'people') return numberShort(value, 0);
		return percent(value);
	}

	function endLabelOffset(firm: FirmName) {
		if (metric !== 'growth') return 0;
		return { Deloitte: 4, PwC: 0, EY: 18, KPMG: -13 }[firm];
	}

	function activatePoint(event: KeyboardEvent, observationId: string) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onSelect(observationId);
		}
	}
</script>

<div class="trend-chart" data-metric={metric}>
	<svg
		viewBox={`0 0 ${width} ${height}`}
		role="img"
		aria-label={`Big Four ${metric} trend from ${years[0]} to ${years.at(-1)}`}
	>
		<title>Big Four {metric} trend</title>
		<g class="grid">
			{#each yTicks as tick (tick)}
				<line x1={margin.left} x2={width - margin.right} y1={y(tick)} y2={y(tick)} />
				<text x={margin.left - 14} y={y(tick) + 4} text-anchor="end">{displayValue(tick)}</text>
			{/each}
		</g>

		<g class="years">
			{#each years as year, index (year)}
				{#if index === 0 || index === years.length - 1 || index % 3 === 0}
					<text x={x(year)} y={height - 17} text-anchor="middle">FY{String(year).slice(-2)}</text>
				{/if}
			{/each}
		</g>

		{#each selectedFirms as firm (firm)}
			{@const points = visibleSeries[firm]}
			{#if points.length}
				<path class="series-line underlay" d={pathFor(points)} />
				<path class="series-line" d={pathFor(points)} style:stroke={FIRM_COLORS[firm]} />
				{#each points as point (point.observationId)}
					<circle
						class:active={hovered?.point.observationId === point.observationId}
						cx={x(point.year)}
						cy={y(point.value)}
						r={hovered?.point.observationId === point.observationId ? 7 : 4}
						fill={FIRM_COLORS[firm]}
						role="button"
						tabindex="0"
						aria-label={`${firm} FY${point.year}: ${displayValue(point.value)}. Open evidence.`}
						onpointerenter={() => (hovered = { firm, point })}
						onpointerleave={() => (hovered = null)}
						onfocus={() => (hovered = { firm, point })}
						onblur={() => (hovered = null)}
						onclick={() => onSelect(point.observationId)}
						onkeydown={(event) => activatePoint(event, point.observationId)}
					></circle>
				{/each}
				{@const last = points.at(-1)!}
				<text
					class="end-label"
					x={x(last.year) + 13}
					y={y(last.value) + 4 + endLabelOffset(firm)}
					fill={FIRM_COLORS[firm]}>{firm}</text
				>
			{/if}
		{/each}
	</svg>

	{#if hovered}
		<div
			class="chart-tooltip"
			style:left={`${(x(hovered.point.year) / width) * 100}%`}
			style:top={`${(y(hovered.point.value) / height) * 100}%`}
		>
			<div class="tooltip-heading">
				<span class="firm-swatch" style:background={FIRM_COLORS[hovered.firm]}></span>
				<strong>{hovered.firm}</strong>
				<span>FY{hovered.point.year}</span>
			</div>
			<div class="tooltip-value">{displayValue(hovered.point.value)}</div>
			<div class="tooltip-action">Click point for evidence <ArrowUpRight size={14} /></div>
		</div>
	{/if}
</div>

<style>
	.trend-chart {
		position: relative;
		min-width: 0;
	}

	svg {
		display: block;
		width: 100%;
		overflow: visible;
	}

	.grid line {
		stroke: var(--border-strong);
		stroke-width: 1;
		stroke-dasharray: 2 5;
	}

	.grid text,
	.years text {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 14px;
		font-variant-numeric: tabular-nums;
	}

	.series-line {
		fill: none;
		stroke-linecap: round;
		stroke-linejoin: round;
		stroke-width: 3;
		vector-effect: non-scaling-stroke;
		stroke-dasharray: 1400;
		stroke-dashoffset: 1400;
		animation: line-draw 1.1s var(--ease-out) forwards;
	}

	.series-line.underlay {
		stroke: var(--surface-base);
		stroke-width: 7;
	}

	circle {
		cursor: pointer;
		stroke: var(--surface-base);
		stroke-width: 2;
		transition:
			r 160ms var(--ease-out),
			opacity 160ms var(--ease-out);
		vector-effect: non-scaling-stroke;
		animation: point-enter 420ms var(--ease-out) both;
	}

	circle:not(.active) {
		opacity: 0.82;
	}

	circle:focus-visible {
		outline: none;
		stroke: var(--ink);
		stroke-width: 4;
	}

	.end-label {
		font-size: 14px;
		font-weight: 800;
	}

	.chart-tooltip {
		position: absolute;
		z-index: var(--z-tooltip);
		width: 190px;
		padding: 12px;
		border: 1.5px solid var(--ink);
		border-radius: 0;
		background: var(--ink);
		color: var(--surface-base);
		box-shadow: var(--shadow-floating);
		transform: translate(-50%, calc(-100% - 14px));
		pointer-events: none;
	}

	.tooltip-heading {
		display: flex;
		align-items: center;
		gap: 7px;
		font-size: 12px;
	}

	.tooltip-heading span:last-child {
		margin-left: auto;
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
	}

	.firm-swatch {
		width: 7px;
		height: 7px;
		border-radius: 50%;
	}

	.tooltip-value {
		margin: 8px 0 10px;
		font-family: var(--font-mono);
		font-size: 20px;
		font-weight: 650;
		letter-spacing: -0.03em;
	}

	.tooltip-action {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		padding: 0;
		color: var(--accent-light);
		font-size: 11px;
		font-weight: 700;
	}

	@keyframes line-draw {
		to {
			stroke-dashoffset: 0;
		}
	}

	@keyframes point-enter {
		from {
			opacity: 0;
			transform: scale(0);
			transform-origin: center;
			transform-box: fill-box;
		}
	}

	@media (max-width: 720px) {
		.end-label {
			display: none;
		}

		.chart-tooltip {
			width: 160px;
		}
	}
</style>
