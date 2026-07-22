<script lang="ts">
	import { ChevronDown, ExternalLink } from '@lucide/svelte';
	import { onMount } from 'svelte';
	import { FIRMS } from '$lib/data/format';
	import type { DimensionPoint, FirmName } from '$lib/data/types';

	interface Props {
		data: Record<FirmName, DimensionPoint[]>;
		mode: 'service' | 'region';
		onSelect?: (observationId: string) => void;
	}

	let { data, mode, onSelect = () => {} }: Props = $props();
	let compositionElement: HTMLDivElement;
	let expanded = $state(false);
	let hovered = $state<{ firm: FirmName; point: DimensionPoint; share: number } | null>(null);
	let tooltipPosition = $state({ left: 0, top: 0, below: false });
	let barProgress = $state(1);
	let animationReady = $state(false);
	let animationFrame = 0;
	let animationKey = $derived(
		`${mode}-${Object.values(data)
			.flat()
			.map((point) => point.observationId)
			.join('-')}`
	);

	onMount(() => {
		animationReady = true;
		return () => cancelAnimationFrame(animationFrame);
	});

	$effect(() => {
		if (!animationReady || !animationKey) return;
		cancelAnimationFrame(animationFrame);
		if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
			barProgress = 1;
			return;
		}
		barProgress = 0;
		const startedAt = performance.now();
		const duration = 380;
		const tick = (now: number) => {
			const elapsed = Math.min(1, (now - startedAt) / duration);
			barProgress = 1 - Math.pow(1 - elapsed, 4);
			if (elapsed < 1) animationFrame = requestAnimationFrame(tick);
		};
		animationFrame = requestAnimationFrame(tick);
		return () => cancelAnimationFrame(animationFrame);
	});

	const serviceColors: Record<string, string> = {
		audit_assurance_attest: 'var(--mix-audit)',
		assurance: 'var(--mix-audit)',
		consulting: 'var(--mix-consulting)',
		consulting_transformation_implementation: 'var(--mix-consulting)',
		combined_not_separable: 'var(--mix-advisory)',
		tax: 'var(--mix-tax)',
		tax_legal: 'var(--mix-tax)',
		strategy_and_transactions: 'var(--mix-strategy)'
	};

	const regionColors: Record<string, string> = {
		americas: 'var(--region-americas)',
		emeia: 'var(--region-emea)',
		asia_pacific: 'var(--region-apac)'
	};

	function normalizedKey(point: DimensionPoint) {
		const value = `${point.canonical} ${point.label}`.toLowerCase();
		if (value.includes('america')) return 'americas';
		if (value.includes('asia')) return 'asia_pacific';
		if (value.includes('eme') || value.includes('europe')) return 'emeia';
		return point.canonical;
	}

	function colorFor(point: DimensionPoint) {
		return mode === 'service'
			? (serviceColors[point.canonical] ?? 'var(--mix-other)')
			: (regionColors[normalizedKey(point)] ?? 'var(--mix-other)');
	}

	function visiblePoints(firm: FirmName) {
		return data[firm].filter((point) => !point.nested);
	}

	function detailPoints(firm: FirmName) {
		return data[firm].filter((point) => point.nested);
	}

	function totalFor(firm: FirmName) {
		return visiblePoints(firm).reduce((sum, point) => sum + point.value, 0);
	}

	function shareFor(firm: FirmName, point: DimensionPoint) {
		return (point.value / totalFor(firm)) * 100;
	}

	function showTooltip(
		event: PointerEvent | FocusEvent,
		firm: FirmName,
		point: DimensionPoint,
		share: number
	) {
		const segment = event.currentTarget as HTMLButtonElement;
		const compositionBounds = compositionElement.getBoundingClientRect();
		const segmentBounds = segment.getBoundingClientRect();
		const tooltipWidth = 196;
		const segmentCenter = segmentBounds.left + segmentBounds.width / 2 - compositionBounds.left;
		const segmentTop = segmentBounds.top - compositionBounds.top;
		tooltipPosition = {
			left: Math.max(
				tooltipWidth / 2 + 8,
				Math.min(compositionBounds.width - tooltipWidth / 2 - 8, segmentCenter)
			),
			top: segmentTop,
			below: segmentTop < 104
		};
		hovered = { firm, point, share };
	}
</script>

<div class="composition" data-mode={mode} bind:this={compositionElement}>
	{#each FIRMS as firm (firm)}
		<div class="firm-row">
			<div class="firm-label">
				<strong>{firm}</strong>
				<span>{mode === 'service' ? 'FY25 revenue mix' : 'Reported revenue footprint'}</span>
			</div>
			<div class="bar-shell">
				<div class="bar-frame">
					<div class="bar" aria-label={`${firm} ${mode} composition`}>
						{#each visiblePoints(firm) as point (point.observationId)}
							{@const share = shareFor(firm, point)}
							<button
								class="segment"
								style:width={`${share * barProgress}%`}
								style:background={colorFor(point)}
								aria-label={`${firm} ${point.label}: ${share.toFixed(1)}%. Open evidence.`}
								onpointerenter={(event) => showTooltip(event, firm, point, share)}
								onpointerleave={() => (hovered = null)}
								onfocus={(event) => showTooltip(event, firm, point, share)}
								onblur={() => (hovered = null)}
								onclick={() => onSelect(point.observationId)}
							></button>
						{/each}
					</div>
				</div>
				<div class="labels">
					{#each visiblePoints(firm) as point (point.observationId)}
						<button onclick={() => onSelect(point.observationId)}>
							<span class="dot" style:background={colorFor(point)}></span>
							<span>{point.label}</span>
							<strong>{shareFor(firm, point).toFixed(0)}%</strong>
						</button>
					{/each}
				</div>
			</div>
		</div>
	{/each}

	{#if mode === 'service' && detailPoints('Deloitte').length}
		<div class="method-note">
			<div>
				<strong>Deloitte reporting hierarchy</strong>
				<span
					>Technology &amp; Transformation and Strategy, Risk &amp; Transactions roll into its
					consulting total.</span
				>
			</div>
			<button aria-expanded={expanded} onclick={() => (expanded = !expanded)}>
				{expanded ? 'Hide detail' : 'Show detail'}
				<ChevronDown size={15} class={expanded ? 'rotated' : ''} />
			</button>
		</div>
		{#if expanded}
			<div class="nested-detail">
				{#each detailPoints('Deloitte') as point (point.observationId)}
					<button onclick={() => onSelect(point.observationId)}>
						<span class="nested-kicker">Consulting component</span>
						<strong>{point.label}</strong>
						<span>${(point.value / 1_000_000_000).toFixed(1)}B</span>
						<ExternalLink size={14} />
					</button>
				{/each}
			</div>
		{/if}
	{/if}

	{#if hovered}
		<div
			class="composition-tooltip"
			class:below={tooltipPosition.below}
			style:left={`${tooltipPosition.left}px`}
			style:top={`${tooltipPosition.top}px`}
		>
			<span>{hovered.firm}</span>
			<strong>{hovered.point.label}</strong>
			<b>{hovered.share.toFixed(1)}%</b>
			<small>Click segment for evidence</small>
		</div>
	{/if}
</div>

<style>
	.composition {
		position: relative;
		display: grid;
		gap: 24px;
	}

	.firm-row {
		display: grid;
		grid-template-columns: 116px minmax(0, 1fr);
		gap: 20px;
		align-items: start;
	}

	.firm-label {
		display: grid;
		gap: 3px;
		padding-top: 2px;
	}

	.firm-label strong {
		font-size: 14px;
	}

	.firm-label span {
		color: var(--text-tertiary);
		font-size: 12px;
		line-height: 1.35;
	}

	.bar-shell {
		min-width: 0;
	}

	.bar-frame {
		height: 38px;
		overflow: hidden;
		border: 1.5px solid var(--frame);
		border-radius: 0;
		background: var(--surface-muted);
		box-shadow: var(--shadow-brutal-xs);
	}

	.bar {
		display: flex;
		height: 100%;
	}

	.segment {
		position: relative;
		min-width: 0;
		padding: 0;
		border: 0;
		border-right: 1px solid color-mix(in oklab, var(--frame) 72%, transparent);
		cursor: pointer;
		transition:
			filter 160ms var(--ease-out),
			transform 160ms var(--ease-out);
	}

	.segment:last-child {
		border-right: 0;
	}

	.segment:hover,
	.segment:focus-visible {
		z-index: 1;
		filter: brightness(1.1) saturate(1.06);
		outline: 2px solid var(--frame);
		outline-offset: -2px;
	}

	.labels {
		display: flex;
		flex-wrap: wrap;
		gap: 6px 14px;
		margin-top: 9px;
	}

	.labels button {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 0;
		border: 0;
		background: none;
		color: var(--text-secondary);
		font: inherit;
		font-size: 12px;
		cursor: pointer;
	}

	.labels button:hover span:nth-child(2) {
		color: var(--ink);
		text-decoration: underline;
		text-underline-offset: 3px;
	}

	.labels strong {
		color: var(--ink);
		font-family: var(--font-mono);
		font-size: 12px;
	}

	.dot {
		width: 9px;
		height: 9px;
		border: 1px solid var(--frame);
		border-radius: 0;
	}

	.method-note {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 20px;
		padding: 14px 16px;
		border: 1.5px solid var(--frame);
		background: var(--accent-wash);
	}

	.method-note > div {
		display: grid;
		gap: 3px;
	}

	.method-note strong {
		font-size: 11px;
	}

	.method-note span {
		color: var(--text-secondary);
		font-size: 12px;
	}

	.method-note button {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		flex: 0 0 auto;
		padding: 6px 8px;
		border: 0;
		background: transparent;
		color: var(--ink);
		font: inherit;
		font-size: 12px;
		font-weight: 750;
		cursor: pointer;
	}

	.method-note :global(svg) {
		transition: transform 160ms var(--ease-out);
	}

	.method-note :global(svg.rotated) {
		transform: rotate(180deg);
	}

	.nested-detail {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 10px;
		margin-top: -14px;
	}

	.nested-detail button {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto;
		gap: 4px 12px;
		align-items: center;
		padding: 13px 15px;
		border: 1.5px solid var(--frame);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.nested-detail button:hover {
		border-color: var(--border-strong);
	}

	.nested-detail strong {
		font-size: 11px;
	}

	.nested-detail span:not(.nested-kicker) {
		grid-column: 1;
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 11px;
	}

	.nested-kicker {
		grid-column: 1 / -1;
		color: var(--text-tertiary);
		font-size: 12px;
	}

	.nested-detail :global(svg) {
		grid-column: 2;
		grid-row: 2 / 4;
	}

	.composition-tooltip {
		position: absolute;
		z-index: var(--z-tooltip);
		display: grid;
		width: 196px;
		gap: 4px;
		padding: 12px;
		border: 1.5px solid var(--frame);
		border-radius: 0;
		background: var(--surface-overlay);
		color: var(--ink);
		box-shadow: var(--shadow-brutal-sm);
		transform: translate(-50%, calc(-100% - 12px));
		pointer-events: none;
	}

	.composition-tooltip.below {
		transform: translate(-50%, 14px);
	}

	.composition-tooltip::after {
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

	.composition-tooltip.below::after {
		top: -6px;
		bottom: auto;
		border: 0;
		border-top: 1.5px solid var(--frame);
		border-left: 1.5px solid var(--frame);
	}

	.composition-tooltip span,
	.composition-tooltip small {
		color: var(--text-secondary);
		font-size: 12px;
	}

	.composition-tooltip strong {
		font-size: 11px;
	}

	.composition-tooltip b {
		font-family: var(--font-mono);
		font-size: 20px;
	}

	@media (max-width: 640px) {
		.firm-row {
			grid-template-columns: 1fr;
			gap: 8px;
		}

		.firm-label {
			display: flex;
			align-items: baseline;
			justify-content: space-between;
		}

		.nested-detail {
			grid-template-columns: 1fr;
		}

		.method-note {
			align-items: flex-start;
		}
	}
</style>
