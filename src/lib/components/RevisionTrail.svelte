<script lang="ts">
	import { ArrowRight, FileClock, History, SearchCheck } from '@lucide/svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, fullNumber } from '$lib/data/format';
	import type { DashboardObservation, FirmName } from '$lib/data/types';

	let {
		observations,
		onselect
	}: {
		observations: DashboardObservation[];
		onselect: (observationId: string) => void;
	} = $props();

	type RevisionPair = {
		key: string;
		firm: FirmName;
		metric: string;
		fiscalYear: string;
		original: DashboardObservation;
		revised: DashboardObservation;
		originalValue: number | null;
		revisedValue: number | null;
		delta: number | null;
		percentageChange: number | null;
	};

	let selectedFirm = $state<'All' | FirmName>('All');
	let selectedKey = $state('');
	let revisionRecords = $derived(observations.filter((observation) => observation.revision));
	let pairs = $derived.by(() => {
		const byId = new Map(observations.map((observation) => [observation.id, observation]));
		return observations
			.filter((observation) => Boolean(observation.supersedes && byId.has(observation.supersedes)))
			.map((revised): RevisionPair => {
				const original = byId.get(revised.supersedes)!;
				const originalValue = original.valueUsd ?? original.valueNumeric;
				const revisedValue = revised.valueUsd ?? revised.valueNumeric;
				const delta =
					originalValue != null && revisedValue != null ? revisedValue - originalValue : null;
				const percentageChange =
					delta != null && originalValue ? (delta / Math.abs(originalValue)) * 100 : null;
				return {
					key: `${original.id}:${revised.id}`,
					firm: revised.firm,
					metric: revised.metricName,
					fiscalYear: revised.fiscalYear,
					original,
					revised,
					originalValue,
					revisedValue,
					delta,
					percentageChange
				};
			})
			.sort(
				(a, b) =>
					Math.abs(b.percentageChange ?? 0) - Math.abs(a.percentageChange ?? 0) ||
					b.fiscalYear.localeCompare(a.fiscalYear)
			);
	});
	let filteredPairs = $derived(
		selectedFirm === 'All' ? pairs : pairs.filter((pair) => pair.firm === selectedFirm)
	);
	let selectedPair = $derived(
		filteredPairs.find((pair) => pair.key === selectedKey) ?? filteredPairs[0]
	);

	const revisionCount = (firm: FirmName) =>
		revisionRecords.filter((observation) => observation.firm === firm).length;
	const displayValue = (observation: DashboardObservation, value: number | null) => {
		if (value == null) return observation.valueOriginal || 'Not disclosed';
		const unit = observation.unitCanonical || observation.unitOriginal;
		return unit === 'USD' || observation.valueUsd != null
			? currencyShort(value, value >= 1_000_000_000 ? 3 : 1)
			: fullNumber(value);
	};
	const displayDelta = (pair: RevisionPair) => {
		if (pair.delta == null) return 'Value not numerically comparable';
		if (pair.delta === 0) return 'Value carried forward unchanged';
		const formatted =
			(pair.revised.unitCanonical || pair.revised.unitOriginal) === 'USD' ||
			pair.revised.valueUsd != null
				? currencyShort(Math.abs(pair.delta), Math.abs(pair.delta) >= 1_000_000_000 ? 3 : 1)
				: fullNumber(Math.abs(pair.delta));
		return `${pair.delta > 0 ? '+' : '−'}${formatted} · ${Math.abs(pair.percentageChange ?? 0).toFixed(2)}%`;
	};
</script>

<div class="revision-trail">
	<div class="revision-heading">
		<div class="revision-symbol"><History size={18} aria-hidden="true" /></div>
		<div>
			<span>Audit trail</span>
			<h3>Later disclosures changed earlier numbers.</h3>
		</div>
		<p>
			FirmScope never silently overwrites a historical fact. Original and later comparative
			disclosures stay linked so reclassifications and restatements remain inspectable.
		</p>
	</div>

	<div class="revision-summary">
		<div class="revision-total">
			<strong>{revisionRecords.length}</strong>
			<span>records marked as revisions</span>
		</div>
		<div class="firm-revision-tabs" aria-label="Filter revision trail by firm">
			<button class:active={selectedFirm === 'All'} onclick={() => (selectedFirm = 'All')}>
				All <b>{pairs.length}</b>
			</button>
			{#each FIRMS as firm (firm)}
				<button class:active={selectedFirm === firm} onclick={() => (selectedFirm = firm)}>
					<i style:background={FIRM_COLORS[firm]}></i>{firm}<b>{revisionCount(firm)}</b>
				</button>
			{/each}
		</div>
		<div class="lineage-count">
			<SearchCheck size={14} aria-hidden="true" />
			<span><strong>{pairs.length}</strong> explicit original → later links</span>
		</div>
	</div>

	{#if selectedPair}
		<div class="revision-workbench">
			<div class="revision-list">
				<div class="list-heading">
					<span>{selectedFirm === 'All' ? 'All networks' : selectedFirm}</span>
					<strong>{filteredPairs.length} linked comparisons</strong>
				</div>
				<div class="revision-scroll">
					{#each filteredPairs as pair (pair.key)}
						<button
							class:selected={selectedPair.key === pair.key}
							onclick={() => (selectedKey = pair.key)}
						>
							<i style:background={FIRM_COLORS[pair.firm]}></i>
							<span>{pair.firm} · {pair.fiscalYear}</span>
							<strong>{pair.metric}</strong>
							<small class:unchanged={pair.delta === 0}>{displayDelta(pair)}</small>
						</button>
					{/each}
				</div>
			</div>

			<div class="lineage-inspector" aria-live="polite">
				<div class="inspector-heading">
					<span>{selectedPair.firm} · {selectedPair.fiscalYear}</span>
					<strong>{selectedPair.metric}</strong>
					<small>{selectedPair.revised.sourceTitle}</small>
				</div>

				<div class="revision-flow">
					<button onclick={() => onselect(selectedPair.original.id)}>
						<span>Original record</span>
						<strong>{displayValue(selectedPair.original, selectedPair.originalValue)}</strong>
						<small>{selectedPair.original.id}</small>
					</button>
					<div class="flow-arrow">
						<span class="flow-icon"><ArrowRight size={18} aria-hidden="true" /></span>
						<span>later comparative</span>
					</div>
					<button onclick={() => onselect(selectedPair.revised.id)}>
						<span>Revised record</span>
						<strong>{displayValue(selectedPair.revised, selectedPair.revisedValue)}</strong>
						<small>{selectedPair.revised.id}</small>
					</button>
				</div>

				<div class="delta-band">
					<span>Recorded movement</span>
					<strong class:negative={(selectedPair.delta ?? 0) < 0}
						>{displayDelta(selectedPair)}</strong
					>
				</div>

				<div class="lineage-note">
					<FileClock size={16} aria-hidden="true" />
					<p>
						The primary chart series uses the supported comparative where the source establishes a
						revision. Both records remain in the ledger with their own source wording and lineage.
					</p>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.revision-trail {
		margin-top: 20px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
		box-shadow: var(--shadow-brutal-sm);
	}

	.revision-heading {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr) minmax(280px, 0.82fr);
		align-items: center;
		gap: 18px;
		padding: 22px;
		border-bottom: 1px solid var(--frame);
	}

	.revision-symbol {
		display: grid;
		width: 38px;
		height: 38px;
		place-items: center;
		background: var(--accent);
		color: var(--accent-ink);
		box-shadow: 3px 3px 0 var(--frame);
	}

	.revision-heading span {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.revision-heading h3 {
		margin: 4px 0 0;
		font-family: var(--font-display);
		font-size: 25px;
		font-weight: 620;
		letter-spacing: -0.03em;
		line-height: 1.05;
	}

	.revision-heading p {
		max-width: 54ch;
		margin: 0;
		color: var(--text-secondary);
		font-size: 10px;
		line-height: 1.55;
	}

	.revision-summary {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr) auto;
		align-items: stretch;
		border-bottom: 1px solid var(--frame);
		background: var(--surface-subtle);
	}

	.revision-total,
	.lineage-count {
		display: flex;
		align-items: center;
		gap: 9px;
		padding: 12px 16px;
	}

	.revision-total {
		border-right: 1px solid var(--frame);
	}

	.revision-total strong {
		font-family: var(--font-mono);
		font-size: 19px;
	}

	.revision-total span,
	.lineage-count span {
		color: var(--text-secondary);
		font-size: 9px;
	}

	.lineage-count {
		border-left: 1px solid var(--frame);
	}

	.firm-revision-tabs {
		display: flex;
		align-items: stretch;
	}

	.firm-revision-tabs button {
		display: flex;
		flex: 1;
		align-items: center;
		justify-content: center;
		gap: 6px;
		min-width: 0;
		padding: 0 11px;
		border: 0;
		border-right: 1px solid var(--frame);
		background: transparent;
		color: var(--text-secondary);
		font-size: 9px;
		font-weight: 750;
		cursor: pointer;
	}

	.firm-revision-tabs button:last-child {
		border-right: 0;
	}

	.firm-revision-tabs button.active {
		background: var(--ink);
		color: var(--surface-base);
	}

	.firm-revision-tabs i {
		width: 6px;
		height: 13px;
	}

	.firm-revision-tabs b {
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.revision-workbench {
		display: grid;
		grid-template-columns: minmax(270px, 0.72fr) minmax(0, 1.4fr);
		min-height: 470px;
	}

	.revision-list {
		border-right: 1px solid var(--frame);
	}

	.list-heading {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 10px;
		padding: 13px 15px;
		border-bottom: 1px solid var(--frame);
	}

	.list-heading span {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.list-heading strong {
		font-size: 9px;
	}

	.revision-scroll {
		max-height: 430px;
		overflow-y: auto;
	}

	.revision-scroll button {
		display: grid;
		width: 100%;
		grid-template-columns: 6px minmax(0, 1fr);
		gap: 2px 9px;
		padding: 13px 15px;
		border: 0;
		border-bottom: 1px solid var(--border-soft);
		background: transparent;
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.revision-scroll button:hover {
		background: var(--surface-subtle);
	}

	.revision-scroll button.selected {
		background: var(--accent-soft);
	}

	.revision-scroll button > i {
		grid-row: 1 / 4;
		width: 6px;
		height: 100%;
		min-height: 42px;
	}

	.revision-scroll button span {
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.revision-scroll button strong {
		font-size: 10px;
	}

	.revision-scroll button small {
		color: var(--accent-strong);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.revision-scroll button small.unchanged {
		color: var(--text-tertiary);
	}

	.lineage-inspector {
		display: grid;
		align-content: start;
		padding: 27px;
		background: var(--inverse-surface);
		color: var(--inverse-text);
	}

	.inspector-heading {
		display: grid;
		gap: 4px;
	}

	.inspector-heading span,
	.inspector-heading small {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.inspector-heading strong {
		font-family: var(--font-display);
		font-size: 23px;
		font-weight: 620;
	}

	.inspector-heading small {
		max-width: 65ch;
	}

	.revision-flow {
		display: grid;
		grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
		align-items: stretch;
		margin-top: 28px;
	}

	.revision-flow > button {
		display: grid;
		align-content: center;
		min-height: 135px;
		padding: 18px;
		border: 1px solid var(--border-on-dark);
		background: color-mix(in oklch, var(--inverse-text) 3%, transparent);
		color: var(--inverse-text);
		text-align: left;
		cursor: pointer;
	}

	.revision-flow > button:hover {
		background: color-mix(in oklch, var(--inverse-text) 7%, transparent);
	}

	.revision-flow button span,
	.revision-flow button small {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.revision-flow button strong {
		margin: 7px 0;
		font-family: var(--font-mono);
		font-size: clamp(18px, 2.3vw, 28px);
	}

	.flow-arrow {
		display: grid;
		width: 92px;
		place-content: center;
		justify-items: center;
		gap: 5px;
		color: var(--accent);
	}

	.flow-arrow span {
		color: var(--text-on-dark-muted);
		font-family: var(--font-mono);
		font-size: 7px;
	}

	.flow-arrow .flow-icon {
		display: flex;
		color: var(--accent);
	}

	.delta-band {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		padding: 13px 16px;
		border: 1px solid var(--border-on-dark);
		border-top: 0;
	}

	.delta-band span {
		color: var(--text-on-dark-muted);
		font-size: 9px;
	}

	.delta-band strong {
		color: var(--success);
		font-family: var(--font-mono);
		font-size: 11px;
	}

	.delta-band strong.negative {
		color: var(--accent);
	}

	.lineage-note {
		display: flex;
		align-items: flex-start;
		gap: 9px;
		margin-top: 28px;
		color: var(--text-on-dark-muted);
	}

	.lineage-note p {
		max-width: 62ch;
		margin: 0;
		font-size: 9px;
		line-height: 1.55;
	}

	@media (max-width: 980px) {
		.revision-heading {
			grid-template-columns: auto 1fr;
		}

		.revision-heading p {
			grid-column: 2;
		}

		.revision-summary {
			grid-template-columns: auto 1fr;
		}

		.lineage-count {
			grid-column: 1 / 3;
			border-top: 1px solid var(--frame);
			border-left: 0;
		}
	}

	@media (max-width: 740px) {
		.revision-heading {
			padding: 18px;
		}

		.revision-heading p {
			grid-column: 1 / 3;
		}

		.revision-summary,
		.revision-workbench {
			grid-template-columns: 1fr;
		}

		.revision-total {
			border-right: 0;
			border-bottom: 1px solid var(--frame);
		}

		.firm-revision-tabs {
			overflow-x: auto;
		}

		.firm-revision-tabs button {
			min-height: 40px;
			min-width: 82px;
		}

		.lineage-count {
			grid-column: auto;
		}

		.revision-list {
			border-right: 0;
			border-bottom: 1px solid var(--frame);
		}

		.revision-scroll {
			max-height: 280px;
		}

		.lineage-inspector {
			padding: 20px;
		}

		.revision-flow {
			grid-template-columns: 1fr;
		}

		.flow-arrow {
			width: auto;
			height: 62px;
		}

		.flow-arrow .flow-icon {
			transform: rotate(90deg);
		}
	}
</style>
