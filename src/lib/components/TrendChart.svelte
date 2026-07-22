<script lang="ts">
	import { ArrowUpRight } from '@lucide/svelte';
	import { curveMonotoneX, line as shapeLine } from 'd3-shape';
	import { onMount } from 'svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, numberShort, percent } from '$lib/data/format';
	import type { FirmName, SeriesPoint } from '$lib/data/types';

	interface Props {
		series: Record<FirmName, SeriesPoint[]>;
		metric: 'revenue' | 'people' | 'growth';
		selectedFirms?: FirmName[];
		onSelect?: (observationId: string) => void;
	}

	let { series, metric, selectedFirms = FIRMS, onSelect = () => {} }: Props = $props();
	let chartElement: HTMLDivElement;
	let hovered = $state<{ firm: FirmName; point: SeriesPoint } | null>(null);
	let tooltipPosition = $state({ left: 0, top: 0, below: false });
	let animationProgress = $state(1);
	let animationReady = $state(false);
	let animationFrame = 0;

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
	let animationKey = $derived(`${metric}-${selectedFirms.join('-')}`);

	onMount(() => {
		animationReady = true;
		return () => cancelAnimationFrame(animationFrame);
	});

	$effect(() => {
		if (!animationReady || !animationKey) return;
		cancelAnimationFrame(animationFrame);
		if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
			animationProgress = 1;
			return;
		}
		animationProgress = 0;
		const startedAt = performance.now();
		const duration = 420;
		const tick = (now: number) => {
			const elapsed = Math.min(1, (now - startedAt) / duration);
			animationProgress = 1 - Math.pow(1 - elapsed, 4);
			if (elapsed < 1) animationFrame = requestAnimationFrame(tick);
		};
		animationFrame = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(animationFrame);
	});

	function x(year: number) {
		if (years.length <= 1) return margin.left;
		return margin.left + ((year - years[0]) / (years.at(-1)! - years[0])) * plotWidth;
	}

	function y(value: number) {
		return margin.top + plotHeight - ((value - yMin) / (yMax - yMin)) * plotHeight;
	}

	function animatedY(value: number) {
		return y(0) + (y(value) - y(0)) * animationProgress;
	}

	function pathFor(points: SeriesPoint[]) {
		return (
			shapeLine<SeriesPoint>()
				.x((point) => x(point.year))
				.y((point) => animatedY(point.value))
				.curve(curveMonotoneX)(points) ?? ''
		);
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

	function showTooltip(event: PointerEvent | FocusEvent, firm: FirmName, point: SeriesPoint) {
		const marker = event.currentTarget as SVGCircleElement;
		const chartBounds = chartElement.getBoundingClientRect();
		const markerBounds = marker.getBoundingClientRect();
		const tooltipWidth = chartBounds.width <= 720 ? 168 : 198;
		const markerCenter = markerBounds.left + markerBounds.width / 2 - chartBounds.left;
		const markerTop = markerBounds.top - chartBounds.top;
		tooltipPosition = {
			left: Math.max(
				tooltipWidth / 2 + 8,
				Math.min(chartBounds.width - tooltipWidth / 2 - 8, markerCenter)
			),
			top: markerTop,
			below: markerTop < 112
		};
		hovered = { firm, point };
	}
</script>

<div class="trend-chart" data-metric={metric} bind:this={chartElement}>
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

		<g class="series-geometry">
			{#each selectedFirms as firm (firm)}
				{@const points = visibleSeries[firm]}
				{#if points.length}
					<path class="series-line" d={pathFor(points)} style:stroke={FIRM_COLORS[firm]} />
					{#each points as point (point.observationId)}
						<circle
							class:active={hovered?.point.observationId === point.observationId}
							cx={x(point.year)}
							cy={animatedY(point.value)}
							r={hovered?.point.observationId === point.observationId ? 5 : 3}
							fill={FIRM_COLORS[firm]}
							stroke={FIRM_COLORS[firm]}
							role="button"
							tabindex="0"
							aria-label={`${firm} FY${point.year}: ${displayValue(point.value)}. Open evidence.`}
							onpointerenter={(event) => showTooltip(event, firm, point)}
							onpointerleave={() => (hovered = null)}
							onfocus={(event) => showTooltip(event, firm, point)}
							onblur={() => (hovered = null)}
							onclick={() => onSelect(point.observationId)}
							onkeydown={(event) => activatePoint(event, point.observationId)}
						></circle>
					{/each}
					{@const last = points.at(-1)!}
					<text
						class="end-label"
						x={x(last.year) + 13}
						y={animatedY(last.value) + 4 + endLabelOffset(firm)}
						style:opacity={Math.max(0, (animationProgress - 0.82) / 0.18)}
						fill={FIRM_COLORS[firm]}>{firm}</text
					>
				{/if}
			{/each}
		</g>
	</svg>

	{#if hovered}
		<div
			class="chart-tooltip"
			class:below={tooltipPosition.below}
			style:left={`${tooltipPosition.left}px`}
			style:top={`${tooltipPosition.top}px`}
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
		stroke-width: 2.25;
		stroke-opacity: 0.66;
		vector-effect: non-scaling-stroke;
	}

	circle {
		cursor: pointer;
		fill-opacity: 0.64;
		stroke-opacity: 0.26;
		stroke-width: 1;
		transition:
			r 160ms var(--ease-out),
			fill-opacity 160ms var(--ease-out),
			stroke-opacity 160ms var(--ease-out);
		vector-effect: non-scaling-stroke;
	}

	circle.active {
		fill-opacity: 0.92;
		stroke-opacity: 0.72;
	}

	circle:focus-visible {
		outline: none;
		stroke-opacity: 1;
		stroke-width: 2.5;
	}

	.end-label {
		font-size: 14px;
		font-weight: 800;
		transition: opacity 120ms linear;
	}

	.chart-tooltip {
		position: absolute;
		z-index: var(--z-tooltip);
		width: 198px;
		padding: 12px;
		border: 1.5px solid var(--frame);
		border-radius: 0;
		background: var(--surface-overlay);
		color: var(--ink);
		box-shadow: var(--shadow-brutal-sm);
		transform: translate(-50%, calc(-100% - 12px));
		pointer-events: none;
	}

	.chart-tooltip.below {
		transform: translate(-50%, 14px);
	}

	.chart-tooltip::after {
		position: absolute;
		bottom: -6px;
		left: calc(50% - 5px);
		width: 9px;
		height: 9px;
		border-right: 1.5px solid var(--frame);
		border-bottom: 1.5px solid var(--frame);
		background: var(--surface-overlay);
		content: '';
		transform: rotate(45deg);
	}

	.chart-tooltip.below::after {
		top: -6px;
		bottom: auto;
		border: 0;
		border-top: 1.5px solid var(--frame);
		border-left: 1.5px solid var(--frame);
	}

	.tooltip-heading {
		display: flex;
		align-items: center;
		gap: 7px;
		font-size: 12px;
	}

	.tooltip-heading span:last-child {
		margin-left: auto;
		color: var(--text-tertiary);
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
		color: var(--text-secondary);
		font-size: 11px;
		font-weight: 700;
	}

	@media (max-width: 720px) {
		.end-label {
			display: none;
		}

		.chart-tooltip {
			width: 168px;
		}
	}
</style>
