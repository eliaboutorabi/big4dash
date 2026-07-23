<script lang="ts">
	import { ArrowUpRight, ScanSearch } from '@lucide/svelte';
	import { FIRM_COLORS, currencyShort, percent } from '$lib/data/format';
	import type { FirmName, FirmSummary } from '$lib/data/types';

	let {
		firms,
		total,
		onselect
	}: {
		firms: FirmSummary[];
		total: number;
		onselect: (firm: FirmName) => void;
	} = $props();

	let upper = $derived(firms.slice(0, 2));
	let lower = $derived(firms.slice(2, 4));
	let upperShare = $derived(upper.reduce((sum, firm) => sum + firm.marketShare, 0));
	let lowerShare = $derived(lower.reduce((sum, firm) => sum + firm.marketShare, 0));
</script>

<div class="market-mosaic">
	<div class="mosaic-heading">
		<div>
			<span>FY25 reported revenue</span>
			<strong>{currencyShort(total, 0)} combined</strong>
		</div>
		<ScanSearch size={18} aria-hidden="true" />
	</div>

	<div
		class="mosaic-plot"
		role="group"
		aria-label={`FY2025 revenue composition across the Big Four, totaling ${currencyShort(total, 0)}`}
	>
		<div class="mosaic-row" style:flex={`${upperShare} 1 0%`}>
			{#each upper as firm, index (firm.firm)}
				<button
					class="mosaic-cell"
					class:light-ink={firm.firm === 'EY'}
					style:flex={`${firm.marketShare / upperShare} 1 0%`}
					style:background={FIRM_COLORS[firm.firm]}
					aria-label={`${firm.firm}: ${currencyShort(firm.revenue)}, ${percent(firm.marketShare)} of combined revenue`}
					onclick={() => onselect(firm.firm)}
				>
					<span>0{index + 1}</span>
					<strong>{firm.firm}</strong>
					<div><b>{currencyShort(firm.revenue)}</b><small>{percent(firm.marketShare, 0)}</small></div>
					<span class="open-icon"><ArrowUpRight size={14} aria-hidden="true" /></span>
				</button>
			{/each}
		</div>
		<div class="mosaic-row" style:flex={`${lowerShare} 1 0%`}>
			{#each lower as firm, index (firm.firm)}
				<button
					class="mosaic-cell"
					class:light-ink={firm.firm === 'EY'}
					style:flex={`${firm.marketShare / lowerShare} 1 0%`}
					style:background={FIRM_COLORS[firm.firm]}
					aria-label={`${firm.firm}: ${currencyShort(firm.revenue)}, ${percent(firm.marketShare)} of combined revenue`}
					onclick={() => onselect(firm.firm)}
				>
					<span>0{index + 3}</span>
					<strong>{firm.firm}</strong>
					<div><b>{currencyShort(firm.revenue)}</b><small>{percent(firm.marketShare, 0)}</small></div>
					<span class="open-icon"><ArrowUpRight size={14} aria-hidden="true" /></span>
				</button>
			{/each}
		</div>
	</div>

	<p>Area represents each network’s share of the four-firm reported total.</p>
</div>

<style>
	.market-mosaic {
		overflow: hidden;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal);
	}

	.mosaic-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 15px 17px;
		border-bottom: 1px solid var(--frame);
		background: var(--accent-wash);
	}

	.mosaic-heading > div {
		display: grid;
		gap: 3px;
	}

	.mosaic-heading span,
	.market-mosaic > p {
		color: var(--text-secondary);
		font-size: 11px;
	}

	.mosaic-heading strong {
		font-family: var(--font-mono);
		font-size: 13px;
	}

	.mosaic-plot {
		display: flex;
		height: 238px;
		flex-direction: column;
		gap: 2px;
		padding: 2px;
		background: var(--frame);
	}

	.mosaic-row {
		display: flex;
		gap: 2px;
		min-height: 0;
	}

	.mosaic-cell {
		position: relative;
		display: grid;
		min-width: 0;
		align-content: space-between;
		padding: 13px 14px;
		overflow: hidden;
		border: 0;
		color: white;
		text-align: left;
		cursor: pointer;
		transition:
			filter 180ms var(--ease-out),
			transform 180ms var(--ease-out);
	}

	.mosaic-cell:hover {
		z-index: 1;
		filter: saturate(1.08) brightness(1.04);
		transform: scale(0.985);
	}

	.mosaic-cell:focus-visible {
		z-index: 2;
		outline: 3px solid var(--surface-base);
		outline-offset: -5px;
	}

	.mosaic-cell.light-ink {
		color: oklch(0.18 0.025 255);
	}

	.mosaic-cell > span {
		font-family: var(--font-mono);
		font-size: 10px;
		font-weight: 700;
		opacity: 0.76;
	}

	.mosaic-cell > strong {
		align-self: end;
		font-size: clamp(16px, 1.7vw, 23px);
		letter-spacing: -0.03em;
	}

	.mosaic-cell > div {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 8px;
	}

	.mosaic-cell b {
		font-family: var(--font-mono);
		font-size: 12px;
	}

	.mosaic-cell small {
		font-family: var(--font-mono);
		font-size: 11px;
		font-weight: 800;
	}

	.open-icon {
		position: absolute;
		top: 13px;
		right: 13px;
	}

	.market-mosaic > p {
		margin: 0;
		padding: 10px 16px;
		border-top: 1px solid var(--frame);
		line-height: 1.45;
	}

	@media (max-width: 560px) {
		.mosaic-plot {
			height: 220px;
		}

		.mosaic-cell {
			padding: 11px;
		}

		.open-icon {
			top: 10px;
			right: 10px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.mosaic-cell {
			transition: none;
		}
	}
</style>
