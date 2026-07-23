<script lang="ts">
	import {
		ExternalLink,
		Globe2,
		LocateFixed,
		Map as MapIcon,
		MapPin,
		ScanSearch
	} from '@lucide/svelte';
	import { SvelteMap } from 'svelte/reactivity';
	import { geoGraticule10, geoNaturalEarth1, geoPath } from 'd3-geo';
	import { feature } from 'topojson-client';
	import type { FeatureCollection } from 'geojson';
	import world from 'world-atlas/countries-110m.json';
	import OfficeGlobe from '$lib/components/OfficeGlobe.svelte';
	import { FIRM_COLORS, FIRMS } from '$lib/data/format';
	import type { FirmName, OfficeLocation } from '$lib/data/types';

	interface Props {
		locations: OfficeLocation[];
	}

	interface ClusterMarker {
		id: string;
		firm: FirmName;
		location: OfficeLocation;
		locationCount: number;
		x: number;
		y: number;
	}

	interface MapCluster {
		id: string;
		x: number;
		y: number;
		locations: OfficeLocation[];
		markers: ClusterMarker[];
	}

	interface OfficeInspection {
		location: OfficeLocation;
		clusterSize: number;
		firmCount: number;
		firmLocationCount: number;
	}

	let { locations }: Props = $props();
	let activeFirms = $state<FirmName[]>(['Deloitte', 'PwC', 'EY', 'KPMG']);
	let inspected = $state<OfficeInspection | null>(null);
	let viewMode = $state<'2d' | '3d'>('2d');

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
		[...locations]
			.filter((location) => activeFirms.includes(location.firm))
			.sort(
				(a, b) =>
					Number(a.coverageTier === 'representative_hub') -
					Number(b.coverageTier === 'representative_hub')
			)
	);
	let directoryCount = $derived(
		visibleLocations.filter((location) => location.coverageTier !== 'representative_hub').length
	);
	let mapClusters = $derived(buildMapClusters(visibleLocations));
	let overlapClusterCount = $derived(
		mapClusters.filter((cluster) => cluster.markers.length > 1).length
	);
	let clusterByLocationId = $derived.by(() => {
		const lookup = new SvelteMap<string, MapCluster>();
		for (const cluster of mapClusters) {
			for (const location of cluster.locations) lookup.set(location.id, cluster);
		}
		return lookup;
	});

	function point(location: OfficeLocation) {
		const projected = projection([location.longitude, location.latitude]);
		if (!projected) return { x: -100, y: -100 };
		return { x: projected[0], y: projected[1] };
	}

	function buildMapClusters(rows: OfficeLocation[]) {
		const collisionDistance = 4.2;
		const cellSize = collisionDistance;
		const clusters: MapCluster[] = [];
		const buckets = new SvelteMap<string, MapCluster[]>();
		const orderedRows = [...rows].sort((a, b) => a.id.localeCompare(b.id));

		for (const location of orderedRows) {
			const position = point(location);
			const cellX = Math.floor(position.x / cellSize);
			const cellY = Math.floor(position.y / cellSize);
			let nearest: MapCluster | undefined;
			let nearestDistance = Number.POSITIVE_INFINITY;

			for (let offsetX = -1; offsetX <= 1; offsetX += 1) {
				for (let offsetY = -1; offsetY <= 1; offsetY += 1) {
					for (const candidate of buckets.get(`${cellX + offsetX}:${cellY + offsetY}`) ?? []) {
						const distance = Math.hypot(candidate.x - position.x, candidate.y - position.y);
						if (distance <= collisionDistance && distance < nearestDistance) {
							nearest = candidate;
							nearestDistance = distance;
						}
					}
				}
			}

			if (nearest) {
				nearest.locations.push(location);
				continue;
			}

			const cluster: MapCluster = {
				id: location.id,
				x: position.x,
				y: position.y,
				locations: [location],
				markers: []
			};
			clusters.push(cluster);
			const bucketKey = `${cellX}:${cellY}`;
			buckets.set(bucketKey, [...(buckets.get(bucketKey) ?? []), cluster]);
		}

		for (const cluster of clusters) {
			const firmGroups = FIRMS.map((firm) => ({
				firm,
				locations: cluster.locations.filter((location) => location.firm === firm)
			})).filter((group) => group.locations.length > 0);
			const isSplit = firmGroups.length > 1;
			const spread = firmGroups.length === 2 ? 3.1 : 3.5;

			cluster.markers = firmGroups.map((group, index) => {
				const angle = -Math.PI / 2 + (index * Math.PI * 2) / firmGroups.length;
				return {
					id: `${cluster.id}-${group.firm}`,
					firm: group.firm,
					location: group.locations[0],
					locationCount: group.locations.length,
					x: cluster.x + (isSplit ? Math.cos(angle) * spread : 0),
					y: cluster.y + (isSplit ? Math.sin(angle) * spread : 0)
				};
			});
		}

		return clusters;
	}

	function inspectClusterMarker(cluster: MapCluster, marker: ClusterMarker) {
		inspected = {
			location: marker.location,
			clusterSize: cluster.locations.length,
			firmCount: cluster.markers.length,
			firmLocationCount: marker.locationCount
		};
	}

	function inspectGlobeLocation(location: OfficeLocation) {
		const cluster = clusterByLocationId.get(location.id);
		const marker = cluster?.markers.find((candidate) => candidate.firm === location.firm);
		if (cluster && marker) inspectClusterMarker(cluster, marker);
		else inspected = { location, clusterSize: 1, firmCount: 1, firmLocationCount: 1 };
	}

	function toggleFirm(firm: FirmName) {
		activeFirms = activeFirms.includes(firm)
			? activeFirms.length === 1
				? activeFirms
				: activeFirms.filter((candidate) => candidate !== firm)
			: [...activeFirms, firm];
		if (inspected && !activeFirms.includes(inspected.location.firm)) inspected = null;
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

	<div class="map-frame" class:globe-mode={viewMode === '3d'}>
		<div class="projection-toggle" aria-label="Map projection">
			<button
				class:active={viewMode === '2d'}
				aria-pressed={viewMode === '2d'}
				onclick={() => (viewMode = '2d')}><MapIcon size={14} /> 2D</button
			>
			<button
				class:active={viewMode === '3d'}
				aria-pressed={viewMode === '3d'}
				onclick={() => (viewMode = '3d')}><Globe2 size={14} /> 3D</button
			>
		</div>
		<div class="map-stamp">
			<span>{viewMode === '2d' ? 'OFFICE ATLAS' : 'SPATIAL GLOBE'}</span><strong
				>{viewMode === '2d' ? 'FLAT PROJECTION' : 'DRAG TO ORBIT'}</strong
			>
		</div>
		<div class="map-layer map-2d" aria-hidden={viewMode === '3d'}>
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
					{#each mapClusters as cluster (cluster.id)}
						{#each cluster.markers as marker (marker.id)}
							<circle
								class="office-marker"
								class:representative={marker.location.coverageTier === 'representative_hub'}
								class:split={cluster.markers.length > 1}
								class:inspected={inspected?.location.id === marker.location.id}
								cx={marker.x}
								cy={marker.y}
								r={marker.location.coverageTier === 'representative_hub' ? 2.35 : 1.95}
								fill={FIRM_COLORS[marker.firm]}
								stroke={FIRM_COLORS[marker.firm]}
								fill-opacity={inspected?.location.id === marker.location.id ? 1 : 0.72}
								stroke-opacity="0.9"
								role="button"
								tabindex="0"
								aria-label={`${marker.firm} office${marker.locationCount > 1 ? ` group of ${marker.locationCount}` : ''} in ${marker.location.city}, ${marker.location.country}${cluster.markers.length > 1 ? `; ${cluster.markers.length} firms share this map position` : ''}`}
								onpointerenter={() => inspectClusterMarker(cluster, marker)}
								onfocus={() => inspectClusterMarker(cluster, marker)}
								onclick={() => inspectClusterMarker(cluster, marker)}
								onkeydown={(event) => {
									if (event.key === 'Enter' || event.key === ' ')
										inspectClusterMarker(cluster, marker);
								}}
							></circle>
						{/each}
					{/each}
				</g>
			</svg>
		</div>
		<div class="map-layer map-3d" aria-hidden={viewMode === '2d'}>
			<OfficeGlobe
				locations={visibleLocations}
				active={viewMode === '3d'}
				onInspect={inspectGlobeLocation}
			/>
		</div>
		<div class="globe-instruction">
			<span>Drag to orbit</span><i></i><span>Scroll to zoom</span>
		</div>
		<div class="coverage-key">
			<span
				><i class="directory-dot"></i>{directoryCount.toLocaleString()} mapped directory records</span
			>
			{#if overlapClusterCount > 0}
				<span
					><i class="split-dot"></i>{overlapClusterCount.toLocaleString()} shared-position clusters split</span
				>
			{/if}
		</div>
	</div>

	<div class="atlas-readout" aria-live="polite">
		{#if inspected}
			<div class="readout-firm">
				<i style:background={FIRM_COLORS[inspected.location.firm]}></i>
				<span>{inspected.location.firm}</span>
				{#if inspected.firmCount > 1 || inspected.firmLocationCount > 1}
					<small
						>{inspected.firmCount > 1
							? `${inspected.firmCount} firms here`
							: 'Shared map position'}{inspected.firmLocationCount > 1
							? ` · ${inspected.firmLocationCount} ${inspected.location.firm} records`
							: ''}</small
					>
				{/if}
			</div>
			<div class="readout-location">
				<MapPin size={18} />
				<div>
					<strong
						>{inspected.location.city}{inspected.location.region
							? `, ${inspected.location.region}`
							: ''}</strong
					>
					<span
						>{inspected.location.country}{inspected.location.address
							? ` · ${inspected.location.address}`
							: ''}</span
					>
				</div>
			</div>
			<div class="readout-quality">
				<span
					>{inspected.clusterSize > 1
						? `Shared position · ${inspected.firmCount} firms · ${inspected.clusterSize} mapped records`
						: inspected.location.coverageTier === 'representative_hub'
							? 'Representative hub · city centroid'
							: inspected.location.coordinatePrecision === 'source_coordinate'
								? 'Official directory · source map coordinate'
								: 'Official directory · city-centroid coordinate'}</span
				>
				<button
					onclick={() =>
						window.open(inspected?.location.sourceUrl, '_blank', 'noopener,noreferrer')}
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
					>{firm === 'Deloitte'
						? 'unique plots from 867 directory entries'
						: firm === 'KPMG'
							? 'from 76 official country directories'
							: 'source directory coordinates'}</small
				>
			</div>
		{/each}
	</div>

	<div class="atlas-method">
		<strong>Coverage note</strong>
		<p>
			Deloitte’s official directory contains 867 entries; 794 carry source-linked coordinates and
			co-located listings collapse to 699 unique plots. KPMG contributes 327 locations normalized
			from 76 official country directories using city centroids. EY and PwC expose structured source
			coordinates. Counts describe mapped records—not comparable audited office totals.
		</p>
	</div>
</div>

<style>
	.atlas-shell {
		border: 1.5px solid var(--frame);
		background: var(--surface-elevated);
		box-shadow: var(--shadow-brutal-sm);
	}

	.atlas-toolbar {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 20px;
		padding: 16px 18px;
		border-bottom: 1px solid var(--frame);
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
		border: 1.5px solid var(--frame);
		background: var(--accent-light);
		color: var(--accent-ink);
		box-shadow: var(--shadow-brutal-xs);
	}

	.atlas-title > div {
		align-items: flex-start;
		flex-direction: column;
		gap: 2px;
	}

	.atlas-title strong {
		font-size: 14px;
	}

	.atlas-title > div > span,
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

	.projection-toggle {
		position: absolute;
		top: 20px;
		right: 20px;
		z-index: 6;
		display: flex;
		padding: 3px;
		border: 1.5px solid var(--frame);
		background: var(--surface-overlay);
		box-shadow: var(--shadow-brutal-xs);
	}

	.projection-toggle button {
		display: inline-flex;
		height: 30px;
		align-items: center;
		gap: 6px;
		padding: 0 10px;
		border: 0;
		background: transparent;
		color: var(--text-on-dark-muted);
		font-size: 11px;
		font-weight: 800;
		cursor: pointer;
		transition:
			background 160ms var(--ease-out),
			color 160ms var(--ease-out);
	}

	.projection-toggle button.active {
		background: var(--accent-light);
		color: oklch(0.18 0.025 255);
	}

	.atlas-filters button {
		display: flex;
		align-items: center;
		gap: 7px;
		min-height: 34px;
		padding: 0 11px;
		border: 1px solid var(--frame);
		background: var(--surface-muted);
		color: var(--text-secondary);
		font-size: 12px;
		font-weight: 750;
		cursor: pointer;
		opacity: 0.5;
		transition: background 150ms var(--ease-out);
	}

	.atlas-filters button.active {
		background: var(--surface-base);
		color: var(--ink);
		opacity: 1;
	}

	.atlas-filters button:hover {
		background: var(--accent-wash);
	}

	.atlas-filters i,
	.readout-firm i,
	.coverage-cards i {
		width: 8px;
		height: 8px;
		border: 1px solid var(--frame);
	}

	.map-frame {
		position: relative;
		overflow: hidden;
		height: clamp(540px, 58vw, 680px);
		--map-ocean: oklch(0.19 0.024 255);
		--map-land: oklch(0.34 0.026 255);
		--map-border: oklch(1 0 0 / 0.3);
		--map-grid: oklch(1 0 0 / 0.07);
		background: var(--surface-dark);
		perspective: 1200px;
	}

	.map-layer {
		position: absolute;
		inset: 0;
		transform-origin: center;
		transition:
			opacity 520ms var(--ease-out),
			transform 820ms cubic-bezier(0.16, 1, 0.3, 1),
			filter 520ms var(--ease-out),
			clip-path 820ms cubic-bezier(0.16, 1, 0.3, 1);
	}

	.map-2d {
		z-index: 1;
		opacity: 1;
		clip-path: circle(100% at 50% 50%);
	}

	.map-3d {
		z-index: 2;
		opacity: 0;
		filter: blur(9px);
		clip-path: circle(0% at 50% 50%);
		transform: scale(0.72) rotateY(-8deg);
		pointer-events: none;
	}

	.map-frame.globe-mode .map-2d {
		opacity: 0;
		filter: blur(5px);
		clip-path: circle(40% at 50% 50%);
		transform: scale(0.88) rotateX(7deg);
		pointer-events: none;
	}

	.map-frame.globe-mode .map-3d {
		opacity: 1;
		filter: none;
		clip-path: circle(100% at 50% 50%);
		transform: scale(1) rotateY(0);
		pointer-events: auto;
	}

	.map-frame svg {
		display: block;
		width: 100%;
		height: 100%;
	}

	.sphere {
		fill: var(--map-ocean);
		stroke: oklch(1 0 0 / 0.16);
	}

	.graticule {
		fill: none;
		stroke: var(--map-grid);
		stroke-width: 0.7;
	}

	.countries path {
		fill: var(--map-land);
		stroke: var(--map-border);
		stroke-width: 0.55;
		vector-effect: non-scaling-stroke;
	}

	.office-points {
		opacity: 1;
	}

	.office-points .office-marker {
		cursor: crosshair;
		stroke-width: 0.8;
		vector-effect: non-scaling-stroke;
		transition:
			r 130ms var(--ease-out),
			fill-opacity 130ms var(--ease-out),
			stroke-width 130ms var(--ease-out);
	}

	.office-points .office-marker.representative {
		stroke-width: 1.35;
	}

	.office-points .office-marker:hover,
	.office-points .office-marker:focus-visible,
	.office-points .office-marker.inspected {
		r: 3.25px;
		fill-opacity: 1;
		stroke-width: 1.55;
		outline: none;
	}

	.map-stamp {
		position: absolute;
		top: 22px;
		left: 24px;
		z-index: 4;
		display: grid;
		gap: 2px;
		padding: 9px 11px;
		border: 1px solid oklch(1 0 0 / 0.3);
		background: oklch(0.17 0.02 255 / 0.8);
		color: var(--text-on-sidebar);
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
		z-index: 4;
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

	.coverage-key .split-dot {
		width: 4px;
		height: 4px;
		margin-right: 5px;
		margin-bottom: 5px;
		background: var(--firm-deloitte);
		box-shadow:
			5px 0 0 var(--firm-pwc),
			0 5px 0 var(--firm-ey),
			5px 5px 0 var(--firm-kpmg);
	}

	.globe-instruction {
		position: absolute;
		bottom: 20px;
		left: 22px;
		z-index: 4;
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 8px 10px;
		border: 1px solid oklch(1 0 0 / 0.24);
		background: oklch(0.13 0.018 255 / 0.84);
		color: var(--text-on-dark-muted);
		font-size: 11px;
		opacity: 0;
		transform: translateY(6px);
		transition:
			opacity 200ms var(--ease-out) 360ms,
			transform 200ms var(--ease-out) 360ms;
		pointer-events: none;
	}

	.globe-instruction i {
		width: 3px;
		height: 3px;
		border-radius: 50%;
		background: var(--accent-light);
	}

	.globe-mode .globe-instruction {
		opacity: 1;
		transform: translateY(0);
	}

	.atlas-readout {
		min-height: 84px;
		display: grid;
		grid-template-columns: 150px minmax(0, 1fr) auto;
		align-items: center;
		gap: 18px;
		padding: 14px 18px;
		border-top: 1px solid var(--frame);
		border-bottom: 1px solid var(--frame);
		background: var(--accent-wash);
	}

	.readout-firm {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 8px;
		font-size: 13px;
		font-weight: 800;
	}

	.readout-firm small {
		width: 100%;
		color: var(--text-secondary);
		font-size: 11px;
		font-weight: 650;
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
		border-right: 1px solid var(--frame);
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
		letter-spacing: -0.035em;
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
		border-top: 1px solid var(--frame);
		background: var(--surface-muted);
	}

	.atlas-method strong {
		font-size: 12px;
	}

	.atlas-method p {
		margin: 0;
		line-height: 1.55;
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
			border-bottom: 1px solid var(--frame);
		}

		.coverage-key {
			display: none;
		}

		.globe-instruction {
			bottom: 12px;
			left: 12px;
		}
	}

	@media (max-width: 520px) {
		.map-frame {
			height: 480px;
		}

		.map-2d svg {
			width: 150%;
			margin-left: -25%;
		}

		.map-layer {
			inset: 0;
		}

		.map-stamp {
			top: 12px;
			left: 12px;
		}

		.projection-toggle {
			top: 12px;
			right: 12px;
		}

		.coverage-cards {
			grid-template-columns: 1fr;
		}

		.coverage-cards > div {
			border-right: 0;
			border-bottom: 1px solid var(--frame);
		}

		.atlas-method {
			grid-template-columns: 1fr;
			gap: 5px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.map-layer,
		.globe-instruction {
			animation: none;
			transition-duration: 0.01ms;
		}
	}
</style>
