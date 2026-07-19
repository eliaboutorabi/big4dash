<script lang="ts">
	import { ExternalLink, LocateFixed, MapPin, ScanSearch } from '@lucide/svelte';
	import { geoGraticule10, geoNaturalEarth1, geoPath } from 'd3-geo';
	import { feature } from 'topojson-client';
	import type { FeatureCollection } from 'geojson';
	import world from 'world-atlas/countries-110m.json';
	import { FIRM_COLORS, FIRMS } from '$lib/data/format';
	import type { FirmName, OfficeLocation } from '$lib/data/types';

	interface Props {
		locations: OfficeLocation[];
	}

	let { locations }: Props = $props();
	let activeFirms = $state<FirmName[]>(['Deloitte', 'PwC', 'EY', 'KPMG']);
	let inspected = $state<OfficeLocation | null>(null);

	const width = 1120;
	const height = 540;
	const projection = geoNaturalEarth1()
		.rotate([-10, 0])
		.fitExtent(
			[
				[24, 26],
				[width - 24, height - 22]
			],
			{ type: 'Sphere' }
		);
	const path = geoPath(projection);
	const countries = feature(
		world as never,
		world.objects.countries as never
	) as unknown as FeatureCollection;
	const graticule = geoGraticule10();

	let visibleLocations = $derived(
		[...locations].filter((location) => activeFirms.includes(location.firm))
	);
	let directoryCount = $derived(
		visibleLocations.filter((location) => location.coverageTier === 'directory_complete').length
	);
	let hubCount = $derived(visibleLocations.length - directoryCount);

	function point(location: OfficeLocation) {
		const projected = projection([location.longitude, location.latitude]);
		if (!projected) return { x: -100, y: -100 };
		const firmOffset: Record<FirmName, [number, number]> = {
			Deloitte: [-3, -2],
			PwC: [3, -2],
			EY: [-3, 2],
			KPMG: [3, 2]
		};
		const [dx, dy] = firmOffset[location.firm];
		return { x: projected[0] + dx, y: projected[1] + dy };
	}

	function toggleFirm(firm: FirmName) {
		activeFirms = activeFirms.includes(firm)
			? activeFirms.length === 1
				? activeFirms
				: activeFirms.filter((candidate) => candidate !== firm)
			: [...activeFirms, firm];
		if (inspected && !activeFirms.includes(inspected.firm)) inspected = null;
	}
</script>

<div class="atlas-shell">
	<div class="atlas-toolbar">
		<div class="atlas-title">
			<span class="atlas-icon"><LocateFixed size={18} /></span>
			<div>
				<strong>Global office signal</strong><span
					>{visibleLocations.length.toLocaleString()} visible locations</span
				>
			</div>
		</div>
		<div class="atlas-filters" aria-label="Filter office locations by firm">
			{#each [...FIRMS] as firm (firm)}
				<button class:active={activeFirms.includes(firm)} onclick={() => toggleFirm(firm)}>
					<i style:background={FIRM_COLORS[firm]}></i>{firm}
				</button>
			{/each}
		</div>
	</div>

	<div class="map-frame">
		<div class="map-stamp"><span>OFFICE ATLAS</span><strong>WORLD / 2026</strong></div>
		<svg
			viewBox={`0 0 ${width} ${height}`}
			role="img"
			aria-label="World map showing mapped Big Four office locations"
		>
			<title>Mapped Big Four office locations</title>
			<path class="sphere" d={path({ type: 'Sphere' }) ?? ''}></path>
			<path class="graticule" d={path(graticule) ?? ''}></path>
			<g class="countries">
				{#each countries.features as country, countryIndex (countryIndex)}
					<path d={path(country) ?? ''}></path>
				{/each}
			</g>
			<g class="office-points">
				{#each visibleLocations as location (location.id)}
					{@const position = point(location)}
					<circle
						class:representative={location.coverageTier === 'representative_hub'}
						class:inspected={inspected?.id === location.id}
						class={`firm-${location.firm.toLowerCase()}`}
						cx={position.x}
						cy={position.y}
						r={location.coverageTier === 'representative_hub' ? 7 : 3.2}
						fill={FIRM_COLORS[location.firm]}
						role="button"
						tabindex="0"
						aria-label={`${location.firm} office in ${location.city}, ${location.country}`}
						onpointerenter={() => (inspected = location)}
						onfocus={() => (inspected = location)}
						onclick={() => (inspected = location)}
						onkeydown={(event) => {
							if (event.key === 'Enter' || event.key === ' ') inspected = location;
						}}
					></circle>
				{/each}
			</g>
		</svg>
		<div class="map-scan"></div>
		<div class="coverage-key">
			<span><i class="directory-dot"></i>{directoryCount.toLocaleString()} source coordinates</span>
			<span><i class="hub-dot"></i>{hubCount} representative hubs</span>
		</div>
	</div>

	<div class="atlas-readout" aria-live="polite">
		{#if inspected}
			<div class="readout-firm">
				<i style:background={FIRM_COLORS[inspected.firm]}></i>
				<span>{inspected.firm}</span>
			</div>
			<div class="readout-location">
				<MapPin size={18} />
				<div>
					<strong>{inspected.city}{inspected.region ? `, ${inspected.region}` : ''}</strong>
					<span>{inspected.country}{inspected.address ? ` · ${inspected.address}` : ''}</span>
				</div>
			</div>
			<div class="readout-quality">
				<span
					>{inspected.coverageTier === 'directory_complete'
						? 'Official directory coordinate'
						: 'Representative hub · city centroid'}</span
				>
				<button onclick={() => window.open(inspected?.sourceUrl, '_blank', 'noopener,noreferrer')}
					>Source <ExternalLink size={13} /></button
				>
			</div>
		{:else}
			<div class="readout-empty">
				<ScanSearch size={20} />
				<div>
					<strong>Inspect the network</strong><span
						>Move across a point to identify the office and its coordinate provenance.</span
					>
				</div>
			</div>
		{/if}
	</div>

	<div class="coverage-cards">
		{#each FIRMS as firm (firm)}
			{@const rows = locations.filter((location) => location.firm === firm)}
			<div>
				<span><i style:background={FIRM_COLORS[firm]}></i>{firm}</span>
				<strong>{rows.length}</strong>
				<small
					>{rows[0]?.coverageTier === 'directory_complete'
						? 'directory coordinates'
						: 'representative global hubs'}</small
				>
			</div>
		{/each}
	</div>

	<div class="atlas-method">
		<strong>Coverage note</strong>
		<p>
			EY and PwC expose structured public coordinates suitable for a directory-level map. Deloitte
			and KPMG are shown as a sourced representative hub sample because their public global
			directories do not expose an equivalent bulk coordinate feed. Counts should not be compared as
			office totals across all four firms.
		</p>
	</div>
</div>

<style>
	.atlas-shell {
		border: 2px solid var(--ink);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.atlas-toolbar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 20px;
		padding: 16px 18px;
		border-bottom: 2px solid var(--ink);
	}

	.atlas-title,
	.atlas-title > div,
	.readout-location,
	.readout-empty {
		display: flex;
		align-items: center;
	}

	.atlas-title {
		gap: 11px;
	}

	.atlas-icon {
		display: grid;
		width: 36px;
		height: 36px;
		place-items: center;
		border: 2px solid var(--ink);
		background: var(--accent-light);
		box-shadow: 3px 3px 0 var(--ink);
	}

	.atlas-title > div {
		align-items: flex-start;
		flex-direction: column;
		gap: 2px;
	}

	.atlas-title strong {
		font-size: 14px;
	}

	.atlas-title span,
	.atlas-method p,
	.readout-location span {
		color: var(--text-secondary);
		font-size: 12px;
	}

	.atlas-filters {
		display: flex;
		flex-wrap: wrap;
		gap: 7px;
	}

	.atlas-filters button {
		display: flex;
		align-items: center;
		gap: 7px;
		min-height: 34px;
		padding: 0 11px;
		border: 1.5px solid var(--ink);
		background: var(--surface-muted);
		color: var(--text-secondary);
		font-size: 12px;
		font-weight: 750;
		cursor: pointer;
		opacity: 0.5;
		transition:
			transform 150ms var(--ease-out),
			background 150ms var(--ease-out);
	}

	.atlas-filters button.active {
		background: var(--surface-base);
		color: var(--ink);
		opacity: 1;
	}

	.atlas-filters button:hover {
		transform: translate(-1px, -1px);
	}

	.atlas-filters i,
	.readout-firm i,
	.coverage-cards i {
		width: 8px;
		height: 8px;
		border: 1px solid var(--ink);
	}

	.map-frame {
		position: relative;
		overflow: hidden;
		padding: 8px;
		background: var(--surface-dark);
	}

	.map-frame svg {
		display: block;
		width: 100%;
	}

	.sphere {
		fill: oklch(0.19 0.024 255);
		stroke: oklch(1 0 0 / 0.16);
	}

	.graticule {
		fill: none;
		stroke: oklch(1 0 0 / 0.07);
		stroke-width: 0.7;
	}

	.countries path {
		fill: oklch(0.34 0.026 255);
		stroke: oklch(1 0 0 / 0.3);
		stroke-width: 0.55;
		vector-effect: non-scaling-stroke;
	}

	.office-points {
		opacity: 1;
	}

	.office-points circle {
		cursor: crosshair;
		stroke: var(--surface-dark);
		stroke-width: 0.9;
		vector-effect: non-scaling-stroke;
		transition:
			r 130ms var(--ease-out),
			opacity 130ms var(--ease-out),
			stroke-width 130ms var(--ease-out);
	}

	.office-points circle.representative {
		fill: transparent;
		stroke-width: 2.2;
	}

	.office-points circle:hover,
	.office-points circle:focus-visible,
	.office-points circle.inspected {
		r: 8px;
		stroke: var(--surface-base);
		stroke-width: 2.2;
		outline: none;
	}

	.map-stamp {
		position: absolute;
		top: 22px;
		left: 24px;
		z-index: 2;
		display: grid;
		gap: 2px;
		padding: 9px 11px;
		border: 1px solid oklch(1 0 0 / 0.3);
		background: oklch(0.17 0.02 255 / 0.8);
		color: var(--surface-base);
		font-family: var(--font-mono);
		pointer-events: none;
	}

	.map-stamp span {
		color: var(--accent-light);
		font-size: 11px;
		letter-spacing: 0.1em;
	}

	.map-stamp strong {
		font-size: 12px;
	}

	.coverage-key {
		position: absolute;
		right: 22px;
		bottom: 20px;
		display: flex;
		gap: 14px;
		padding: 9px 11px;
		border: 1px solid oklch(1 0 0 / 0.26);
		background: oklch(0.17 0.02 255 / 0.88);
		color: var(--text-on-dark-muted);
		font-size: 11px;
		pointer-events: none;
	}

	.coverage-key span {
		display: flex;
		align-items: center;
		gap: 6px;
	}

	.coverage-key i {
		display: block;
		width: 8px;
		height: 8px;
		background: var(--accent-light);
	}

	.coverage-key .hub-dot {
		border: 2px solid var(--accent-light);
		background: transparent;
	}

	.map-scan {
		position: absolute;
		top: 0;
		bottom: 0;
		left: -20%;
		width: 14%;
		background: linear-gradient(90deg, transparent, oklch(0.84 0.125 74 / 0.08), transparent);
		transform: skewX(-9deg);
		animation: map-scan 8s ease-in-out infinite;
		pointer-events: none;
	}

	.atlas-readout {
		min-height: 84px;
		display: grid;
		grid-template-columns: 150px minmax(0, 1fr) auto;
		align-items: center;
		gap: 18px;
		padding: 14px 18px;
		border-top: 2px solid var(--ink);
		border-bottom: 1px solid var(--ink);
		background: var(--accent-wash);
	}

	.readout-firm {
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 13px;
		font-weight: 800;
	}

	.readout-location {
		gap: 10px;
		min-width: 0;
	}

	.readout-location > div {
		display: grid;
		min-width: 0;
		gap: 2px;
	}

	.readout-location strong {
		font-size: 15px;
	}

	.readout-location span {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.readout-quality {
		display: grid;
		justify-items: end;
		gap: 4px;
	}

	.readout-quality span,
	.readout-quality button {
		font-size: 11px;
	}

	.readout-quality span {
		color: var(--text-secondary);
	}

	.readout-quality button {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		padding: 0;
		border: 0;
		background: transparent;
		color: var(--ink);
		font: inherit;
		font-weight: 800;
		cursor: pointer;
	}

	.readout-empty {
		grid-column: 1 / -1;
		gap: 10px;
	}

	.readout-empty > div {
		display: grid;
		gap: 2px;
	}

	.readout-empty strong {
		font-size: 14px;
	}

	.readout-empty span {
		color: var(--text-secondary);
		font-size: 12px;
	}

	.coverage-cards {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
	}

	.coverage-cards > div {
		display: grid;
		gap: 4px;
		padding: 15px 18px;
		border-right: 1px solid var(--ink);
	}

	.coverage-cards > div:last-child {
		border: 0;
	}

	.coverage-cards span {
		display: flex;
		align-items: center;
		gap: 7px;
		font-size: 12px;
		font-weight: 800;
	}

	.coverage-cards strong {
		font: 650 27px var(--font-mono);
		letter-spacing: -0.05em;
	}

	.coverage-cards small {
		color: var(--text-secondary);
		font-size: 11px;
	}

	.atlas-method {
		display: grid;
		grid-template-columns: 130px minmax(0, 1fr);
		gap: 18px;
		padding: 14px 18px;
		border-top: 1px solid var(--ink);
		background: var(--surface-muted);
	}

	.atlas-method strong {
		font-size: 12px;
	}

	.atlas-method p {
		margin: 0;
		line-height: 1.55;
	}

	@keyframes map-scan {
		0%,
		22% {
			transform: translateX(0) skewX(-9deg);
			opacity: 0;
		}
		35% {
			opacity: 1;
		}
		72%,
		100% {
			transform: translateX(850%) skewX(-9deg);
			opacity: 0;
		}
	}

	@media (max-width: 820px) {
		.atlas-toolbar,
		.atlas-readout {
			align-items: flex-start;
			grid-template-columns: 1fr;
			flex-direction: column;
		}

		.atlas-filters {
			width: 100%;
		}

		.atlas-readout {
			gap: 10px;
		}

		.readout-quality {
			justify-items: start;
		}

		.coverage-cards {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}

		.coverage-cards > div:nth-child(2) {
			border-right: 0;
		}

		.coverage-cards > div:nth-child(-n + 2) {
			border-bottom: 1px solid var(--ink);
		}

		.coverage-key {
			display: none;
		}
	}

	@media (max-width: 520px) {
		.map-frame {
			padding: 0;
		}

		.map-frame svg {
			width: 150%;
			margin-left: -25%;
		}

		.map-stamp {
			top: 12px;
			left: 12px;
		}

		.coverage-cards {
			grid-template-columns: 1fr;
		}

		.coverage-cards > div {
			border-right: 0;
			border-bottom: 1px solid var(--ink);
		}

		.atlas-method {
			grid-template-columns: 1fr;
			gap: 5px;
		}
	}
</style>
