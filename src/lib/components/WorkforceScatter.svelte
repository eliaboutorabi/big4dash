<script lang="ts">
	import { FIRM_COLORS, currencyShort, fullNumber } from '$lib/data/format';
	import type { FirmSummary } from '$lib/data/types';

	interface Props {
		firms: FirmSummary[];
		onSelect?: (observationId: string) => void;
	}

	let { firms, onSelect = () => {} }: Props = $props();
	let hovered = $state<FirmSummary | null>(null);

	const width = 700;
	const height = 390;
	const margin = { top: 34, right: 42, bottom: 56, left: 68 };
	const xMin = 240_000;
	const xMax = 500_000;
	const yMin = 35_000_000_000;
	const yMax = 75_000_000_000;
	const xTicks = [250_000, 300_000, 350_000, 400_000, 450_000, 500_000];
	const yTicks = [40_000_000_000, 50_000_000_000, 60_000_000_000, 70_000_000_000];

	function x(value: number) {
		return margin.left + ((value - xMin) / (xMax - xMin)) * (width - margin.left - margin.right);
	}

	function y(value: number) {
		return margin.top + ((yMax - value) / (yMax - yMin)) * (height - margin.top - margin.bottom);
	}
</script>

<div class="scatter">
	<svg
		viewBox={`0 0 ${width} ${height}`}
		role="img"
		aria-label="Revenue and workforce scale comparison for the Big Four"
	>
		<title>Revenue versus disclosed workforce</title>
		<g class="grid">
			{#each yTicks as tick (tick)}
				<line x1={margin.left} x2={width - margin.right} y1={y(tick)} y2={y(tick)} />
				<text x={margin.left - 12} y={y(tick) + 4} text-anchor="end">{currencyShort(tick, 0)}</text>
			{/each}
			{#each xTicks as tick (tick)}
				<line x1={x(tick)} x2={x(tick)} y1={margin.top} y2={height - margin.bottom} />
				<text x={x(tick)} y={height - 24} text-anchor="middle">{Math.round(tick / 1000)}k</text>
			{/each}
		</g>
		<text
			class="axis-label"
			x={(margin.left + width - margin.right) / 2}
			y={height - 2}
			text-anchor="middle">Disclosed workforce</text
		>
		<text
			class="axis-label"
			transform={`translate(15 ${(margin.top + height - margin.bottom) / 2}) rotate(-90)`}
			text-anchor="middle">Revenue (USD)</text
		>

		{#each firms as firm (firm.firm)}
			<g
				class="firm-point"
				class:active={hovered?.firm === firm.firm}
				role="button"
				tabindex="0"
				aria-label={`${firm.firm}: ${currencyShort(firm.revenue)} revenue and ${fullNumber(firm.people)} people. Open evidence.`}
				onpointerenter={() => (hovered = firm)}
				onpointerleave={() => (hovered = null)}
				onfocus={() => (hovered = firm)}
				onblur={() => (hovered = null)}
				onclick={() => onSelect(firm.peopleObservationId)}
				onkeydown={(event) => {
					if (event.key === 'Enter' || event.key === ' ') onSelect(firm.peopleObservationId);
				}}
			>
				<circle
					class="halo"
					cx={x(firm.people)}
					cy={y(firm.revenue)}
					r="28"
					fill={FIRM_COLORS[firm.firm]}
				/>
				<circle cx={x(firm.people)} cy={y(firm.revenue)} r="19" fill={FIRM_COLORS[firm.firm]} />
				<text x={x(firm.people)} y={y(firm.revenue) + 4} text-anchor="middle"
					>{firm.firm.slice(0, 1)}</text
				>
				<text class="point-label" x={x(firm.people) + 27} y={y(firm.revenue) - 20}>{firm.firm}</text
				>
			</g>
		{/each}
	</svg>

	{#if hovered}
		<div class="scatter-tooltip">
			<span>{hovered.firm}</span>
			<strong>{currencyShort(hovered.revenue)} <small>revenue</small></strong>
			<strong>{fullNumber(hovered.people)} <small>people</small></strong>
			<div><b>{currencyShort(hovered.revenuePerPerson, 0)}</b> revenue / person</div>
		</div>
	{/if}
</div>

<style>
	.scatter {
		position: relative;
	}

	svg {
		display: block;
		width: 100%;
		overflow: visible;
	}

	.grid line {
		stroke: var(--border-subtle);
		stroke-dasharray: 2 5;
	}

	.grid text,
	.axis-label {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 10px;
	}

	.axis-label {
		font-family: var(--font-sans);
		font-size: 9px;
		font-weight: 700;
		letter-spacing: 0.03em;
	}

	.firm-point {
		cursor: pointer;
		outline: none;
	}

	.firm-point circle {
		stroke: var(--surface-base);
		stroke-width: 3;
		transition:
			transform 180ms var(--ease-out),
			opacity 180ms var(--ease-out);
		transform-box: fill-box;
		transform-origin: center;
	}

	.firm-point .halo {
		opacity: 0.08;
		stroke: none;
	}

	.firm-point:hover circle,
	.firm-point.active circle,
	.firm-point:focus-visible circle {
		transform: scale(1.12);
	}

	.firm-point text:not(.point-label) {
		fill: var(--surface-base);
		font-size: 11px;
		font-weight: 850;
		pointer-events: none;
	}

	.point-label {
		fill: var(--ink);
		font-size: 10px;
		font-weight: 800;
	}

	.scatter-tooltip {
		position: absolute;
		right: 8px;
		top: 8px;
		display: grid;
		min-width: 178px;
		gap: 4px;
		padding: 13px 14px;
		border-radius: var(--radius-md);
		background: var(--ink);
		color: var(--surface-base);
		box-shadow: var(--shadow-floating);
	}

	.scatter-tooltip > span {
		color: var(--accent-light);
		font-size: 10px;
		font-weight: 800;
	}

	.scatter-tooltip strong {
		font-family: var(--font-mono);
		font-size: 14px;
	}

	.scatter-tooltip small {
		color: var(--text-on-dark-muted);
		font-family: var(--font-sans);
		font-size: 9px;
		font-weight: 500;
	}

	.scatter-tooltip div {
		margin-top: 5px;
		padding-top: 8px;
		border-top: 1px solid var(--border-on-dark);
		color: var(--text-on-dark-muted);
		font-size: 9px;
	}

	.scatter-tooltip b {
		color: var(--surface-base);
		font-family: var(--font-mono);
		font-size: 11px;
	}
</style>
