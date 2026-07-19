<script lang="ts">
	import { FIRM_COLORS, currencyShort, fullNumber } from '$lib/data/format';
	import type { FirmSummary } from '$lib/data/types';

	interface Props {
		firms: FirmSummary[];
		onSelect?: (observationId: string) => void;
	}

	let { firms, onSelect = () => {} }: Props = $props();
	let hovered = $state<FirmSummary | null>(null);
	let inspected = $derived(
		hovered ?? firms.find((firm) => firm.firm === 'Deloitte') ?? firms[0] ?? null
	);

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

		<g class="quadrants" aria-hidden="true">
			<line x1={x(365_000)} x2={x(365_000)} y1={margin.top} y2={height - margin.bottom} />
			<line
				x1={margin.left}
				x2={width - margin.right}
				y1={y(56_000_000_000)}
				y2={y(56_000_000_000)}
			/>
			<text x={margin.left + 12} y={margin.top + 18}>HIGH REVENUE / LEANER BASE</text>
			<text x={width - margin.right - 12} y={height - margin.bottom - 12} text-anchor="end"
				>LARGER PEOPLE PLATFORM</text
			>
		</g>

		{#each firms as firm (firm.firm)}
			<g
				class="firm-point"
				class:active={inspected?.firm === firm.firm}
				role="button"
				tabindex="0"
				aria-label={`${firm.firm}: ${currencyShort(firm.revenue)} revenue and ${fullNumber(firm.people)} people. Open evidence.`}
				onpointerenter={() => (hovered = firm)}
				onfocus={() => (hovered = firm)}
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

	<div class="scatter-readout" aria-live="polite">
		{#if inspected}
			<div class="readout-firm">
				<i style:background={FIRM_COLORS[inspected.firm]}></i><strong>{inspected.firm}</strong><span
					>selected</span
				>
			</div>
			<div><span>Revenue</span><strong>{currencyShort(inspected.revenue)}</strong></div>
			<div><span>People</span><strong>{fullNumber(inspected.people)}</strong></div>
			<div class="readout-proxy">
				<span>Directional revenue / person</span><strong
					>{currencyShort(inspected.revenuePerPerson, 0)}</strong
				>
			</div>
		{/if}
	</div>
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
		stroke: var(--border-strong);
		stroke-dasharray: 2 5;
	}

	.grid text,
	.axis-label {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 16px;
	}

	.axis-label {
		font-family: var(--font-sans);
		font-size: 14px;
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
		opacity: 0.13;
		stroke: none;
		animation: point-pulse 3.2s ease-in-out infinite;
	}

	.firm-point:hover circle,
	.firm-point.active circle,
	.firm-point:focus-visible circle {
		transform: scale(1.12);
	}

	.firm-point text:not(.point-label) {
		fill: var(--surface-base);
		font-size: 14px;
		font-weight: 850;
		pointer-events: none;
	}

	.point-label {
		fill: var(--ink);
		font-size: 15px;
		font-weight: 800;
	}

	.quadrants line {
		stroke: var(--ink);
		stroke-dasharray: 4 7;
		stroke-width: 1;
		opacity: 0.3;
	}

	.quadrants text {
		fill: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 12px;
		font-weight: 700;
		letter-spacing: 0.06em;
	}

	.scatter-readout {
		display: grid;
		grid-template-columns: 1.1fr repeat(3, minmax(0, 1fr));
		min-height: 74px;
		margin-top: 10px;
		border: 1.5px solid var(--ink);
		background: var(--accent-wash);
	}

	.scatter-readout > div {
		display: grid;
		align-content: center;
		gap: 4px;
		padding: 12px 14px;
		border-right: 1px solid var(--ink);
	}

	.scatter-readout > div:last-child {
		border: 0;
	}

	.scatter-readout span {
		color: var(--text-secondary);
		font-size: 12px;
	}

	.scatter-readout strong {
		font-family: var(--font-mono);
		font-size: 14px;
	}

	.readout-firm {
		grid-template-columns: 10px auto;
		column-gap: 8px !important;
	}

	.readout-firm i {
		width: 10px;
		height: 10px;
		border: 1px solid var(--ink);
	}

	.readout-firm span {
		grid-column: 2;
	}

	@keyframes point-pulse {
		50% {
			transform: scale(1.16);
			opacity: 0.05;
		}
	}

	@media (max-width: 620px) {
		.scatter-readout {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}

		.scatter-readout > div:nth-child(2) {
			border-right: 0;
		}

		.scatter-readout > div:nth-child(-n + 2) {
			border-bottom: 1px solid var(--ink);
		}
	}
</style>
