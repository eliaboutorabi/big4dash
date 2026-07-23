<script lang="ts">
	import { BookmarkCheck, Database, FileDown, FileSpreadsheet, Trash2, X } from '@lucide/svelte';
	import { displayObservationValue } from '$lib/data/format';
	import type { DashboardObservation } from '$lib/data/types';

	let {
		open,
		observations,
		onclose,
		onselect,
		onremove,
		onclear
	}: {
		open: boolean;
		observations: DashboardObservation[];
		onclose: () => void;
		onselect: (observationId: string) => void;
		onremove: (observationId: string) => void;
		onclear: () => void;
	} = $props();
	let notebookElement = $state<HTMLElement>();
	let closeButton = $state<HTMLButtonElement>();

	function downloadFile(filename: string, content: string, type: string) {
		const url = URL.createObjectURL(new Blob([content], { type }));
		const anchor = document.createElement('a');
		anchor.href = url;
		anchor.download = filename;
		anchor.click();
		URL.revokeObjectURL(url);
	}

	function csvCell(value: unknown) {
		let text = String(value ?? '');
		if (/^[=+\-@]/.test(text)) text = `'${text}`;
		return `"${text.replaceAll('"', '""')}"`;
	}

	function exportCsv() {
		const headers = [
			'Observation ID',
			'Firm',
			'Fiscal year',
			'Metric',
			'Reported value',
			'Definition',
			'Source',
			'Source URL',
			'Source locator',
			'Comparability score',
			'Confidence score',
			'Quality flag',
			'Notes'
		];
		const rows = observations.map((observation) => [
			observation.id,
			observation.firm,
			observation.fiscalYear,
			observation.metricName,
			displayObservationValue(observation),
			observation.definition,
			observation.sourceTitle,
			observation.sourceUrl || observation.archivedUrl,
			observation.sourceLocator,
			observation.comparabilityScore,
			observation.confidenceScore,
			observation.qualityFlag,
			observation.notes
		]);
		const csv = [headers, ...rows].map((row) => row.map(csvCell).join(',')).join('\r\n');
		downloadFile(
			`firmscope-evidence-${new Date().toISOString().slice(0, 10)}.csv`,
			`\ufeff${csv}`,
			'text/csv;charset=utf-8'
		);
	}

	function markdownCell(value: string) {
		return value.replaceAll('|', '\\|').replaceAll('\n', ' ').trim();
	}

	function exportBriefing() {
		const generated = new Intl.DateTimeFormat('en-US', {
			dateStyle: 'long',
			timeStyle: 'short'
		}).format(new Date());
		const records = observations
			.map((observation, index) => {
				const sourceUrl = observation.sourceUrl || observation.archivedUrl;
				const source = sourceUrl
					? `[${markdownCell(observation.sourceTitle)}](${sourceUrl})`
					: markdownCell(observation.sourceTitle);
				return [
					`## ${index + 1}. ${observation.firm} — ${markdownCell(observation.metricName)}`,
					'',
					`- **Period:** ${observation.fiscalYear || observation.asOfDate || 'Not stated'}`,
					`- **Reported value:** ${markdownCell(displayObservationValue(observation))}`,
					`- **Definition:** ${markdownCell(observation.definition || 'Not separately stated')}`,
					`- **Evidence quality:** comparability ${observation.comparabilityScore}/5; confidence ${observation.confidenceScore}/5`,
					`- **Source:** ${source}`,
					`- **Locator:** ${markdownCell(observation.sourceLocator || 'Document-level source')}`,
					observation.notes ? `- **Research note:** ${markdownCell(observation.notes)}` : '',
					`- **Observation ID:** \`${observation.id}\``
				]
					.filter(Boolean)
					.join('\n');
			})
			.join('\n\n');
		const markdown = [
			'# FirmScope evidence briefing',
			'',
			`Generated ${generated} from ${observations.length} saved ${
				observations.length === 1 ? 'record' : 'records'
			}.`,
			'',
			'> Figures preserve source-specific periods, definitions and caveats. This export does not make non-comparable disclosures equivalent.',
			'',
			records
		].join('\n');
		downloadFile(
			`firmscope-briefing-${new Date().toISOString().slice(0, 10)}.md`,
			markdown,
			'text/markdown;charset=utf-8'
		);
	}

	function closeOnEscape(event: KeyboardEvent) {
		if (!open) return;
		if (event.key === 'Escape') {
			onclose();
			return;
		}
		if (event.key !== 'Tab') return;
		if (!notebookElement) return;
		const focusable = [
			...notebookElement.querySelectorAll<HTMLElement>(
				'button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])'
			)
		];
		const first = focusable[0];
		const last = focusable.at(-1);
		if (event.shiftKey && document.activeElement === first) {
			event.preventDefault();
			last?.focus();
		} else if (!event.shiftKey && document.activeElement === last) {
			event.preventDefault();
			first?.focus();
		}
	}

	$effect(() => {
		if (!open) return;
		const previousFocus = document.activeElement as HTMLElement | null;
		const previousOverflow = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		queueMicrotask(() => closeButton?.focus());
		return () => {
			document.body.style.overflow = previousOverflow;
			previousFocus?.focus();
		};
	});
</script>

<svelte:window onkeydown={closeOnEscape} />

{#if open}
	<button class="notebook-backdrop" tabindex="-1" aria-hidden="true" onclick={onclose}></button>
	<div
		class="notebook"
		bind:this={notebookElement}
		role="dialog"
		aria-modal="true"
		aria-labelledby="notebook-title"
	>
		<header>
			<div class="notebook-title">
				<span><BookmarkCheck size={15} /> Research collection</span>
				<h2 id="notebook-title">Evidence notebook</h2>
			</div>
			<button
				class="close-button"
				bind:this={closeButton}
				aria-label="Close evidence notebook"
				onclick={onclose}><X size={18} /></button
			>
		</header>

		<div class="notebook-summary">
			<div class="saved-count">
				<strong>{observations.length}</strong>
				<span>saved {observations.length === 1 ? 'record' : 'records'}</span>
			</div>
			{#if observations.length}
				<div class="summary-actions">
					<button aria-label="Download saved evidence as CSV" onclick={exportCsv}>
						<FileSpreadsheet size={12} /> CSV
					</button>
					<button
						aria-label="Download saved evidence briefing as Markdown"
						onclick={exportBriefing}
					>
						<FileDown size={12} /> Brief
					</button>
					<button aria-label="Clear evidence notebook" onclick={onclear}>
						<Trash2 size={12} /> Clear
					</button>
				</div>
			{/if}
		</div>

		<div class="notebook-body">
			{#if observations.length}
				{#each observations as observation, index (observation.id)}
					<article>
						<button class="record-open" onclick={() => onselect(observation.id)}>
							<span class="record-index">{String(index + 1).padStart(2, '0')}</span>
							<div>
								<span>{observation.firm} · {observation.fiscalYear}</span>
								<strong>{observation.metricName}</strong>
								<b>{displayObservationValue(observation)}</b>
							</div>
						</button>
						<button
							class="record-remove"
							aria-label={`Remove ${observation.firm} ${observation.metricName} from notebook`}
							onclick={() => onremove(observation.id)}
						>
							<X size={14} />
						</button>
					</article>
				{/each}
			{:else}
				<div class="notebook-empty">
					<div><Database size={22} aria-hidden="true" /></div>
					<strong>Build a source-backed argument.</strong>
					<p>
						Open any chart mark or ledger record, then save it here. Your collection persists on
						this device.
					</p>
				</div>
			{/if}
		</div>

		<footer>
			<span>Portable research state</span>
			<p>Exports preserve source lineage and never alter the underlying dataset.</p>
		</footer>
	</div>
{/if}

<style>
	.notebook-backdrop {
		position: fixed;
		inset: 0;
		z-index: var(--z-overlay);
		width: 100%;
		padding: 0;
		border: 0;
		background: oklch(0.11 0.022 255 / 0.45);
		backdrop-filter: blur(2px);
	}

	.notebook {
		position: fixed;
		top: 0;
		right: 0;
		bottom: 0;
		z-index: var(--z-drawer);
		display: grid;
		width: min(430px, 100vw);
		grid-template-rows: auto auto 1fr auto;
		border-left: 1.5px solid var(--frame);
		background: var(--surface-overlay);
		box-shadow: var(--shadow-drawer);
		animation: notebook-in 220ms var(--ease-out);
	}

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 18px 20px;
		border-bottom: 1px solid var(--frame);
	}

	.notebook-title {
		display: grid;
		gap: 3px;
	}

	.notebook-title > span {
		display: flex;
		align-items: center;
		gap: 6px;
		color: var(--accent-strong);
		font-size: 9px;
		font-weight: 800;
	}

	h2 {
		margin: 0;
		font-size: 14px;
	}

	.close-button {
		display: grid;
		width: 36px;
		height: 36px;
		place-items: center;
		padding: 0;
		border: 1px solid var(--frame);
		background: var(--surface-base);
		color: var(--ink);
		cursor: pointer;
	}

	.notebook-summary {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 14px;
		padding: 13px 20px;
		border-bottom: 1px solid var(--frame);
		background: var(--accent-wash);
	}

	.saved-count {
		display: flex;
		align-items: baseline;
		gap: 7px;
	}

	.notebook-summary strong {
		font-family: var(--font-mono);
		font-size: 21px;
	}

	.notebook-summary span {
		color: var(--text-secondary);
		font-size: 10px;
	}

	.notebook-summary button {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		padding: 6px;
		border: 0;
		background: transparent;
		color: var(--text-secondary);
		font-size: 9px;
		cursor: pointer;
	}

	.summary-actions {
		display: flex;
		align-items: center;
	}

	.summary-actions button {
		border-left: 1px solid var(--border-subtle);
	}

	.summary-actions button:first-child {
		border-left: 0;
	}

	.notebook-body {
		overflow-y: auto;
		padding: 18px 20px 28px;
	}

	article {
		position: relative;
		display: grid;
		grid-template-columns: 1fr auto;
		border-top: 1px solid var(--frame);
	}

	article:last-child {
		border-bottom: 1px solid var(--frame);
	}

	.record-open {
		display: grid;
		grid-template-columns: 26px 1fr;
		gap: 10px;
		padding: 15px 5px;
		border: 0;
		background: transparent;
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.record-open:hover {
		background: var(--surface-muted);
	}

	.record-index {
		color: var(--accent-strong);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.record-open > div {
		display: grid;
		gap: 3px;
	}

	.record-open div span {
		color: var(--text-tertiary);
		font-size: 9px;
	}

	.record-open strong {
		font-size: 11px;
	}

	.record-open b {
		margin-top: 4px;
		font-family: var(--font-mono);
		font-size: 16px;
	}

	.record-remove {
		width: 34px;
		padding: 0;
		border: 0;
		background: transparent;
		color: var(--text-tertiary);
		cursor: pointer;
	}

	.record-remove:hover {
		color: var(--accent-strong);
	}

	.notebook-empty {
		display: grid;
		justify-items: center;
		padding: 58px 26px;
		text-align: center;
	}

	.notebook-empty > div {
		display: grid;
		width: 48px;
		height: 48px;
		margin-bottom: 16px;
		place-items: center;
		background: var(--accent-light);
		color: var(--accent-ink);
		box-shadow: var(--shadow-brutal-xs);
	}

	.notebook-empty strong {
		font-family: var(--font-display);
		font-size: 22px;
	}

	.notebook-empty p {
		max-width: 34ch;
		margin: 8px 0 0;
		color: var(--text-secondary);
		font-size: 11px;
		line-height: 1.6;
	}

	footer {
		padding: 12px 20px;
		border-top: 1px solid var(--frame);
		background: var(--inverse-surface);
		color: var(--inverse-text);
	}

	footer span {
		color: var(--accent-light);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	footer p {
		margin: 3px 0 0;
		color: var(--text-on-dark-muted);
		font-size: 9px;
	}

	@keyframes notebook-in {
		from {
			transform: translateX(100%);
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.notebook {
			animation: none;
		}
	}
</style>
