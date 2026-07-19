<script lang="ts">
	import {
		ArrowUpRight,
		CalendarDays,
		Check,
		FileText,
		Gauge,
		ShieldCheck,
		X
	} from '@lucide/svelte';
	import { displayObservationValue, formatDate } from '$lib/data/format';
	import type { DashboardObservation } from '$lib/data/types';

	interface Props {
		observation: DashboardObservation | null;
		onClose?: () => void;
	}

	let { observation, onClose = () => {} }: Props = $props();

	function closeOnEscape(event: KeyboardEvent) {
		if (event.key === 'Escape' && observation) onClose();
	}

	function openSource() {
		if (!observation) return;
		window.open(observation.sourceUrl || observation.archivedUrl, '_blank', 'noopener,noreferrer');
	}
</script>

<svelte:window onkeydown={closeOnEscape} />

{#if observation}
	<button class="drawer-backdrop" aria-label="Close evidence drawer" onclick={onClose}></button>
	<aside class="evidence-drawer" aria-label="Evidence detail" aria-live="polite">
		<header>
			<div>
				<span class="record-id">{observation.id}</span>
				<strong>Evidence record</strong>
			</div>
			<button class="icon-button" aria-label="Close evidence drawer" onclick={onClose}
				><X size={18} /></button
			>
		</header>

		<div class="drawer-body">
			<div class="firm-line">
				<span class="firm-marker firm-{observation.firm.toLowerCase()}"
					>{observation.firm.slice(0, 1)}</span
				>
				<div>
					<span>{observation.firm} · {observation.fiscalYear}</span>
					<h2>{observation.metricName}</h2>
				</div>
			</div>

			<div class="record-value">{displayObservationValue(observation)}</div>

			<div class="confidence-grid">
				<div>
					<Gauge size={15} />
					<span>Comparability</span>
					<strong>{observation.comparabilityScore}/5</strong>
					<i><b style:width={`${observation.comparabilityScore * 20}%`}></b></i>
				</div>
				<div>
					<ShieldCheck size={15} />
					<span>Confidence</span>
					<strong>{observation.confidenceScore}/5</strong>
					<i><b style:width={`${observation.confidenceScore * 20}%`}></b></i>
				</div>
			</div>

			<section class="detail-block">
				<div class="detail-heading"><FileText size={15} /><span>What was reported</span></div>
				<p>{observation.definition || 'No additional definition was provided in the source.'}</p>
				{#if observation.sourceExcerpt}
					<blockquote>“{observation.sourceExcerpt}”</blockquote>
				{/if}
			</section>

			<section class="source-card">
				<div class="source-grade">Grade {observation.sourceGrade}</div>
				<div>
					<span>Primary source</span>
					<strong>{observation.sourceTitle}</strong>
				</div>
				{#if observation.sourceUrl || observation.archivedUrl}
					<button class="source-link" onclick={openSource}>
						Open source <ArrowUpRight size={14} />
					</button>
				{/if}
			</section>

			<dl class="metadata">
				<div>
					<dt><CalendarDays size={14} /> Reporting period</dt>
					<dd>{formatDate(observation.periodStart)} — {formatDate(observation.periodEnd)}</dd>
				</div>
				<div>
					<dt><Check size={14} /> Source locator</dt>
					<dd>{observation.sourceLocator || 'Document-level source'}</dd>
				</div>
				<div>
					<dt>Service / geography</dt>
					<dd>{observation.serviceOriginal || observation.geographyOriginal || 'Global total'}</dd>
				</div>
				<div>
					<dt>Quality status</dt>
					<dd>{observation.qualityFlag || 'Passed canonical checks'}</dd>
				</div>
			</dl>

			{#if observation.notes}
				<section class="note">
					<strong>Research note</strong>
					<p>{observation.notes}</p>
				</section>
			{/if}
		</div>
	</aside>
{/if}

<style>
	.drawer-backdrop {
		position: fixed;
		inset: 0;
		z-index: var(--z-overlay);
		width: 100%;
		padding: 0;
		border: 0;
		background: oklch(0.14 0.025 255 / 0.32);
		backdrop-filter: blur(2px);
		animation: fade-in 180ms var(--ease-out);
	}

	.evidence-drawer {
		position: fixed;
		top: 0;
		right: 0;
		bottom: 0;
		z-index: var(--z-drawer);
		width: min(470px, 100vw);
		overflow-y: auto;
		border-left: 2px solid var(--ink);
		background: var(--surface-base);
		box-shadow: -20px 0 60px oklch(0.16 0.02 255 / 0.2);
		animation: slide-in 240ms var(--ease-out);
	}

	header {
		position: sticky;
		top: 0;
		z-index: 2;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 18px 22px;
		border-bottom: 2px solid var(--ink);
		background: oklch(1 0 0 / 0.9);
		backdrop-filter: blur(12px);
	}

	header > div {
		display: grid;
		gap: 2px;
	}

	header strong {
		font-size: 12px;
	}

	.record-id {
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 12px;
	}

	.icon-button {
		display: grid;
		width: 34px;
		height: 34px;
		place-items: center;
		padding: 0;
		border: 1.5px solid var(--ink);
		border-radius: 0;
		background: var(--surface-base);
		color: var(--ink);
		cursor: pointer;
	}

	.drawer-body {
		display: grid;
		gap: 24px;
		padding: 26px 24px 40px;
	}

	.firm-line {
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.firm-marker {
		display: grid;
		width: 36px;
		height: 36px;
		place-items: center;
		border: 1.5px solid var(--ink);
		border-radius: 0;
		color: var(--surface-base);
		font-weight: 850;
	}

	.firm-deloitte {
		background: var(--firm-deloitte);
	}
	.firm-pwc {
		background: var(--firm-pwc);
	}
	.firm-ey {
		background: var(--firm-ey);
		color: var(--ink);
	}
	.firm-kpmg {
		background: var(--firm-kpmg);
	}

	.firm-line div {
		display: grid;
		gap: 2px;
	}

	.firm-line span:not(.firm-marker) {
		color: var(--text-tertiary);
		font-size: 12px;
	}

	h2 {
		margin: 0;
		font-size: 15px;
		letter-spacing: -0.02em;
	}

	.record-value {
		margin-top: -8px;
		font-family: var(--font-mono);
		font-size: clamp(30px, 6vw, 46px);
		font-weight: 650;
		letter-spacing: -0.06em;
		line-height: 1;
	}

	.confidence-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 10px;
	}

	.confidence-grid > div {
		display: grid;
		grid-template-columns: auto 1fr auto;
		gap: 7px;
		align-items: center;
		padding: 13px;
		border: 1.5px solid var(--ink);
		border-radius: 0;
	}

	.confidence-grid span,
	.confidence-grid strong {
		font-size: 12px;
	}

	.confidence-grid strong {
		font-family: var(--font-mono);
	}

	.confidence-grid i {
		grid-column: 1 / -1;
		height: 3px;
		overflow: hidden;
		border-radius: 2px;
		background: var(--surface-muted);
	}

	.confidence-grid i b {
		display: block;
		height: 100%;
		background: var(--accent-strong);
	}

	.detail-block {
		display: grid;
		gap: 10px;
	}

	.detail-heading {
		display: flex;
		align-items: center;
		gap: 7px;
		font-size: 12px;
		font-weight: 800;
	}

	.detail-block p,
	.note p {
		margin: 0;
		color: var(--text-secondary);
		font-size: 12px;
		line-height: 1.7;
	}

	blockquote {
		margin: 0;
		padding: 14px 16px;
		border: 1px solid var(--ink);
		border-left: 6px solid var(--accent);
		background: var(--accent-wash);
		color: var(--text-secondary);
		font-size: 11px;
		font-style: italic;
		line-height: 1.65;
	}

	.source-card {
		display: grid;
		grid-template-columns: auto minmax(0, 1fr);
		gap: 10px 12px;
		align-items: center;
		padding: 15px;
		border: 2px solid var(--ink);
		border-radius: 0;
		box-shadow: 4px 4px 0 var(--accent);
		background: var(--ink);
		color: var(--surface-base);
	}

	.source-grade {
		display: grid;
		width: 42px;
		height: 42px;
		place-items: center;
		border: 1px solid var(--border-on-dark);
		border-radius: 50%;
		color: var(--accent-light);
		font-family: var(--font-mono);
		font-size: 12px;
		font-weight: 800;
	}

	.source-card > div:nth-child(2) {
		display: grid;
		gap: 3px;
	}

	.source-card span {
		color: var(--text-on-dark-muted);
		font-size: 12px;
	}

	.source-card strong {
		font-size: 11px;
		line-height: 1.4;
	}

	.source-card .source-link {
		grid-column: 2;
		display: inline-flex;
		align-items: center;
		gap: 5px;
		width: max-content;
		padding: 0;
		border: 0;
		background: transparent;
		color: var(--accent-light);
		font: inherit;
		font-size: 12px;
		font-weight: 800;
		text-decoration: none;
	}

	.metadata {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 18px 14px;
		margin: 0;
	}

	.metadata div {
		display: grid;
		gap: 5px;
	}

	.metadata dt {
		display: flex;
		align-items: center;
		gap: 5px;
		color: var(--text-tertiary);
		font-size: 12px;
	}

	.metadata dd {
		margin: 0;
		font-size: 12px;
		line-height: 1.5;
	}

	.note {
		display: grid;
		gap: 5px;
		padding-top: 18px;
		border-top: 1px solid var(--border-subtle);
	}

	.note strong {
		font-size: 12px;
	}

	@keyframes fade-in {
		from {
			opacity: 0;
		}
	}
	@keyframes slide-in {
		from {
			transform: translateX(100%);
		}
	}

	@media (max-width: 520px) {
		.metadata,
		.confidence-grid {
			grid-template-columns: 1fr;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.drawer-backdrop,
		.evidence-drawer {
			animation: none;
		}
	}
</style>
