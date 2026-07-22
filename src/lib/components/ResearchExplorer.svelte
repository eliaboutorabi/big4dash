<script lang="ts">
	import {
		ArrowDown,
		ArrowUpRight,
		Database,
		Filter,
		Search,
		SlidersHorizontal
	} from '@lucide/svelte';
	import { displayObservationValue, FIRM_COLORS, FIRMS } from '$lib/data/format';
	import type { DashboardObservation, FirmName } from '$lib/data/types';

	interface Props {
		observations: DashboardObservation[];
		onSelect?: (observationId: string) => void;
	}

	let { observations, onSelect = () => {} }: Props = $props();
	let query = $state('');
	let firm = $state<'All' | FirmName>('All');
	let family = $state('All metrics');
	let grade = $state('All grades');
	let visibleCount = $state(12);
	let sortNewest = $state(true);

	let families = $derived([
		'All metrics',
		...new Set(observations.map((row) => row.metricFamily).filter(Boolean))
	]);
	let grades = $derived([
		'All grades',
		...new Set(observations.map((row) => row.sourceGrade).filter(Boolean))
	]);
	let filtered = $derived.by(() => {
		const needle = query.trim().toLowerCase();
		return observations
			.filter((row) => row.status !== 'superseded')
			.filter((row) => firm === 'All' || row.firm === firm)
			.filter((row) => family === 'All metrics' || row.metricFamily === family)
			.filter((row) => grade === 'All grades' || row.sourceGrade === grade)
			.filter((row) => {
				if (!needle) return true;
				return [
					row.metricName,
					row.firm,
					row.fiscalYear,
					row.serviceOriginal,
					row.geographyOriginal,
					row.sourceTitle,
					row.valueOriginal
				]
					.join(' ')
					.toLowerCase()
					.includes(needle);
			})
			.sort((a, b) => {
				const statusDelta = Number(b.status === 'reported') - Number(a.status === 'reported');
				if (statusDelta) return statusDelta;
				const dateDelta = (b.periodEnd || b.asOfDate).localeCompare(a.periodEnd || a.asOfDate);
				return sortNewest ? dateDelta : -dateDelta;
			});
	});
	let visible = $derived(filtered.slice(0, visibleCount));

	function resetVisible() {
		visibleCount = 12;
	}
</script>

<div class="explorer">
	<div class="explorer-toolbar">
		<label class="search-field">
			<Search size={16} />
			<input
				id="evidence-search"
				bind:value={query}
				oninput={resetVisible}
				placeholder="Search metrics, sources, services…"
			/>
			<kbd>⌘ K</kbd>
		</label>
		<div class="filter-row">
			<label>
				<Filter size={13} />
				<select bind:value={firm} onchange={resetVisible} aria-label="Filter by firm">
					<option value="All">All firms</option>
					{#each FIRMS as option (option)}<option value={option}>{option}</option>{/each}
				</select>
			</label>
			<label>
				<SlidersHorizontal size={13} />
				<select bind:value={family} onchange={resetVisible} aria-label="Filter by metric family">
					{#each families as option (option)}<option value={option}>{option}</option>{/each}
				</select>
			</label>
			<label>
				<select bind:value={grade} onchange={resetVisible} aria-label="Filter by source grade">
					{#each grades as option (option)}<option value={option}>{option}</option>{/each}
				</select>
			</label>
		</div>
	</div>

	<div class="result-meta">
		<div><Database size={14} /><strong>{filtered.length}</strong> matching records</div>
		<button onclick={() => (sortNewest = !sortNewest)}>
			{sortNewest ? 'Newest reporting period' : 'Oldest reporting period'}
			{#if sortNewest}<ArrowDown size={13} />{:else}<ArrowDown size={13} class="reversed" />{/if}
		</button>
	</div>

	<div class="research-table" role="table" aria-label="Research observations">
		<div class="table-head" role="row">
			<span>Firm / period</span>
			<span>Metric</span>
			<span>Reported value</span>
			<span>Evidence quality</span>
			<span></span>
		</div>
		{#each visible as row (row.id)}
			<button class="table-row" role="row" onclick={() => onSelect(row.id)}>
				<span class="firm-cell" role="cell">
					<i style:background={FIRM_COLORS[row.firm]}>{row.firm.slice(0, 1)}</i>
					<span><strong>{row.firm}</strong><small>{row.fiscalYear || 'As of date'}</small></span>
				</span>
				<span class="metric-cell" role="cell">
					<strong>{row.metricName}</strong>
					<small>{row.serviceOriginal || row.geographyOriginal || row.scope}</small>
				</span>
				<span class="value-cell" role="cell">{displayObservationValue(row)}</span>
				<span class="quality-cell" role="cell">
					<b>Grade {row.sourceGrade}</b>
					<small>{row.confidenceScore}/5 confidence</small>
				</span>
				<span class="open-cell" role="cell"><ArrowUpRight size={15} /></span>
			</button>
		{/each}
	</div>

	{#if filtered.length === 0}
		<div class="empty-state">
			<Search size={22} /><strong>No matching records</strong><span
				>Try a broader metric or source term.</span
			>
		</div>
	{:else if visible.length < filtered.length}
		<button class="load-more" onclick={() => (visibleCount += 12)}>
			Load 12 more <span>{filtered.length - visible.length} remaining</span>
		</button>
	{/if}
</div>

<style>
	.explorer {
		display: grid;
		gap: 16px;
	}

	.explorer-toolbar {
		display: grid;
		grid-template-columns: minmax(260px, 1fr) auto;
		gap: 12px;
	}

	.search-field,
	.filter-row label {
		display: flex;
		align-items: center;
		gap: 8px;
		min-height: 44px;
		padding: 0 12px;
		border: 1px solid var(--frame);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--text-tertiary);
	}

	.search-field:focus-within,
	.filter-row label:focus-within {
		border-color: var(--accent-strong);
		box-shadow: 0 0 0 3px var(--accent-wash);
	}

	.search-field input {
		width: 100%;
		border: 0;
		outline: none;
		background: transparent;
		color: var(--ink);
		font: inherit;
		font-size: 11px;
	}

	kbd {
		padding: 2px 6px;
		border: 1px solid var(--frame);
		border-bottom-width: 2px;
		border-radius: 0;
		color: var(--text-tertiary);
		font: 11px var(--font-sans);
	}

	.filter-row {
		display: flex;
		gap: 8px;
	}

	.filter-row label {
		padding-right: 8px;
	}

	select {
		max-width: 150px;
		border: 0;
		outline: 0;
		background: transparent;
		color: var(--text-secondary);
		font: inherit;
		font-size: 12px;
		font-weight: 650;
	}

	.result-meta {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		color: var(--text-tertiary);
		font-size: 12px;
	}

	.result-meta > div,
	.result-meta button {
		display: inline-flex;
		align-items: center;
		gap: 6px;
	}

	.result-meta strong {
		color: var(--ink);
		font-family: var(--font-mono);
	}

	.result-meta button {
		padding: 0;
		border: 0;
		background: transparent;
		color: var(--text-tertiary);
		font: inherit;
		cursor: pointer;
	}

	.result-meta :global(.reversed) {
		transform: rotate(180deg);
	}

	.research-table {
		overflow: hidden;
		border: 1.5px solid var(--frame);
		border-radius: 0;
		background: var(--surface-elevated);
		box-shadow: var(--shadow-brutal-sm);
	}

	.table-head,
	.table-row {
		display: grid;
		grid-template-columns: 145px minmax(220px, 1.5fr) minmax(150px, 0.8fr) 120px 24px;
		gap: 14px;
		align-items: center;
	}

	.table-head {
		padding: 12px 14px;
		border-bottom: 1px solid var(--frame);
		background: var(--accent-light);
		color: var(--ink);
		font-size: 11px;
		font-weight: 750;
		letter-spacing: 0.04em;
		text-transform: uppercase;
	}

	.table-row {
		width: 100%;
		padding: 14px;
		border: 0;
		border-bottom: 1px solid var(--frame);
		background: var(--surface-elevated);
		color: var(--ink);
		font: inherit;
		text-align: left;
		cursor: pointer;
		transition: background 140ms var(--ease-out);
	}

	.table-row:last-child {
		border-bottom: 0;
	}
	.table-row:hover {
		background: var(--accent-wash);
	}

	.firm-cell,
	.metric-cell,
	.quality-cell {
		display: flex;
		align-items: center;
		gap: 9px;
		min-width: 0;
	}

	.firm-cell i {
		display: grid;
		width: 28px;
		height: 28px;
		flex: 0 0 auto;
		place-items: center;
		border: 1px solid var(--frame);
		border-radius: 0;
		color: oklch(0.98 0.01 80);
		font-size: 12px;
		font-style: normal;
		font-weight: 850;
	}

	.firm-cell > span,
	.metric-cell,
	.quality-cell {
		flex-direction: column;
		align-items: flex-start;
		gap: 3px;
	}

	.firm-cell strong,
	.metric-cell strong {
		max-width: 100%;
		overflow: hidden;
		font-size: 12px;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.table-row small {
		max-width: 100%;
		overflow: hidden;
		color: var(--text-tertiary);
		font-size: 11px;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.value-cell {
		overflow: hidden;
		font-family: var(--font-mono);
		font-size: 12px;
		font-weight: 600;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.quality-cell b {
		padding: 2px 6px;
		border: 1px solid currentColor;
		border-radius: 0;
		background: var(--success-wash);
		color: var(--success);
		font-size: 11px;
	}

	.open-cell {
		color: var(--text-tertiary);
	}

	.load-more {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 7px;
		width: 100%;
		padding: 11px;
		border: 1px solid var(--frame);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--ink);
		font: inherit;
		font-size: 12px;
		font-weight: 750;
		cursor: pointer;
	}

	.load-more span {
		color: var(--text-tertiary);
		font-weight: 500;
	}

	.empty-state {
		display: grid;
		place-items: center;
		gap: 7px;
		padding: 42px;
		border: 1px dashed var(--border-strong);
		border-radius: var(--radius-md);
		color: var(--text-tertiary);
		font-size: 12px;
	}

	.empty-state strong {
		color: var(--ink);
	}

	@media (max-width: 860px) {
		.explorer-toolbar {
			grid-template-columns: 1fr;
		}
		.filter-row {
			overflow-x: auto;
		}
		.table-head {
			display: none;
		}
		.table-row {
			grid-template-columns: 120px minmax(160px, 1fr) minmax(120px, 0.7fr) 20px;
		}
		.quality-cell {
			display: none;
		}
	}

	@media (max-width: 600px) {
		.table-row {
			grid-template-columns: 104px minmax(0, 1fr) 20px;
		}
		.value-cell {
			display: none;
		}
		kbd {
			display: none;
		}
	}
</style>
