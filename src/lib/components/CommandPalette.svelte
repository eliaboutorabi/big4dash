<script lang="ts">
	import { BarChart3, Building2, Command, Compass, Database, Search, X } from '@lucide/svelte';
	import type { DashboardObservation, FirmName } from '$lib/data/types';

	let {
		open = $bindable(false),
		sections,
		observations,
		onnavigate,
		onmetric,
		onfirm,
		onevidence
	}: {
		open: boolean;
		sections: Array<{ id: string; label: string }>;
		observations: DashboardObservation[];
		onnavigate: (sectionId: string) => void;
		onmetric: (metric: 'revenue' | 'people' | 'growth') => void;
		onfirm: (firm: FirmName) => void;
		onevidence: (observationId: string) => void;
	} = $props();

	type PaletteResult = {
		id: string;
		group: 'Navigate' | 'Analyze' | 'Firm' | 'Evidence';
		title: string;
		subtitle: string;
		keywords: string;
		run: () => void;
	};

	let query = $state('');
	let activeIndex = $state(0);
	let inputElement = $state<HTMLInputElement>();
	let paletteElement = $state<HTMLElement>();
	let baseResults = $derived.by(() => {
		const navigation: PaletteResult[] = sections.map((section) => ({
			id: `section-${section.id}`,
			group: 'Navigate',
			title: section.label,
			subtitle: `Jump to the ${section.label.toLowerCase()} chapter`,
			keywords: `${section.id} section chapter`,
			run: () => onnavigate(section.id)
		}));
		const metrics: PaletteResult[] = [
			{
				id: 'metric-revenue',
				group: 'Analyze',
				title: 'Compare reported revenue',
				subtitle: 'Open the historical revenue series',
				keywords: 'money sales fees scale financials trend',
				run: () => onmetric('revenue')
			},
			{
				id: 'metric-people',
				group: 'Analyze',
				title: 'Compare disclosed workforce',
				subtitle: 'Open the people series and definitions',
				keywords: 'people headcount employees staff fte',
				run: () => onmetric('people')
			},
			{
				id: 'metric-growth',
				group: 'Analyze',
				title: 'Compare local growth',
				subtitle: 'Open the locally reported growth series',
				keywords: 'pace percentage change yoy',
				run: () => onmetric('growth')
			}
		];
		const firms = (['Deloitte', 'PwC', 'EY', 'KPMG'] as FirmName[]).map((firm): PaletteResult => ({
			id: `firm-${firm}`,
			group: 'Firm',
			title: firm,
			subtitle: `Open the ${firm} network profile`,
			keywords: 'network profile company',
			run: () => onfirm(firm)
		}));
		return [...navigation, ...metrics, ...firms];
	});
	let results = $derived.by(() => {
		const normalized = query.trim().toLowerCase();
		const tokens = normalized.split(/\s+/).filter(Boolean);
		const matches = (value: string) => tokens.every((token) => value.toLowerCase().includes(token));
		const fixed = normalized
			? baseResults.filter((result) =>
					matches(`${result.title} ${result.subtitle} ${result.keywords}`)
				)
			: baseResults;
		if (normalized.length < 2) return fixed;
		const relevance = (observation: DashboardObservation) => {
			const primary =
				`${observation.firm} ${observation.metricName} ${observation.fiscalYear}`.toLowerCase();
			const secondary =
				`${observation.serviceOriginal} ${observation.geographyOriginal} ${observation.valueOriginal}`.toLowerCase();
			return tokens.reduce(
				(score, token) => score + (primary.includes(token) ? 4 : secondary.includes(token) ? 2 : 1),
				0
			);
		};
		const evidence = observations
			.filter((observation) => {
				const searchable = [
					observation.firm,
					observation.metricName,
					observation.fiscalYear,
					observation.serviceOriginal,
					observation.geographyOriginal,
					observation.sourceTitle,
					observation.valueOriginal,
					observation.qualityFlag,
					observation.sourceExcerpt
				]
					.join(' ')
					.toLowerCase();
				return matches(searchable);
			})
			.sort(
				(a, b) =>
					relevance(b) - relevance(a) ||
					(b.periodEnd || b.asOfDate).localeCompare(a.periodEnd || a.asOfDate)
			)
			.slice(0, 8)
			.map((observation): PaletteResult => ({
				id: `evidence-${observation.id}`,
				group: 'Evidence',
				title: `${observation.firm} · ${observation.metricName}`,
				subtitle: `${observation.fiscalYear || 'As of date'} · ${
					observation.valueOriginal || observation.sourceTitle
				}`,
				keywords: '',
				run: () => onevidence(observation.id)
			}));
		return [...fixed, ...evidence];
	});

	function closePalette() {
		open = false;
		query = '';
		activeIndex = 0;
	}

	function execute(result: PaletteResult | undefined) {
		if (!result) return;
		closePalette();
		result.run();
	}

	function handleQuery(value: string) {
		query = value;
		activeIndex = 0;
	}

	function handleKeyboard(event: KeyboardEvent) {
		if (!open && (event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
			event.preventDefault();
			open = true;
			return;
		}
		if (!open) return;
		if (event.key === 'Escape') {
			event.preventDefault();
			closePalette();
			return;
		}
		if (event.key === 'ArrowDown') {
			event.preventDefault();
			activeIndex = results.length ? (activeIndex + 1) % results.length : 0;
			return;
		}
		if (event.key === 'ArrowUp') {
			event.preventDefault();
			activeIndex = results.length ? (activeIndex - 1 + results.length) % results.length : 0;
			return;
		}
		if (event.key === 'Enter') {
			event.preventDefault();
			execute(results[activeIndex]);
			return;
		}
		if (event.key !== 'Tab' || !paletteElement) return;
		const focusable = [
			...paletteElement.querySelectorAll<HTMLElement>(
				'input, button:not([disabled]), [tabindex]:not([tabindex="-1"])'
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
		queueMicrotask(() => inputElement?.focus());
		return () => {
			document.body.style.overflow = previousOverflow;
			previousFocus?.focus();
		};
	});
</script>

<svelte:window onkeydown={handleKeyboard} />

{#if open}
	<button class="palette-backdrop" tabindex="-1" aria-hidden="true" onclick={closePalette}></button>
	<div
		class="command-palette"
		bind:this={paletteElement}
		role="dialog"
		aria-modal="true"
		aria-labelledby="palette-title"
	>
		<header>
			<div class="palette-title">
				<span><Command size={13} aria-hidden="true" /> Research command</span>
				<h2 id="palette-title">Go anywhere. Find any fact.</h2>
			</div>
			<button aria-label="Close command palette" onclick={closePalette}><X size={17} /></button>
		</header>

		<label class="palette-search">
			<Search size={17} aria-hidden="true" />
			<input
				bind:this={inputElement}
				value={query}
				placeholder="Search chapters, firms, metrics or evidence…"
				aria-label="Search dashboard commands and evidence"
				aria-controls="palette-results"
				aria-activedescendant={results[activeIndex]?.id}
				oninput={(event) => handleQuery(event.currentTarget.value)}
			/>
			<kbd>esc</kbd>
		</label>

		<div id="palette-results" class="palette-results" role="listbox">
			{#if results.length}
				{#each results as result, index (result.id)}
					{@const previousGroup = results[index - 1]?.group}
					{#if index === 0 || result.group !== previousGroup}
						<div class="result-group">{result.group}</div>
					{/if}
					<button
						id={result.id}
						class:active={index === activeIndex}
						role="option"
						aria-selected={index === activeIndex}
						onmouseenter={() => (activeIndex = index)}
						onclick={() => execute(result)}
					>
						<span class="result-icon">
							{#if result.group === 'Navigate'}
								<Compass size={15} aria-hidden="true" />
							{:else if result.group === 'Analyze'}
								<BarChart3 size={15} aria-hidden="true" />
							{:else if result.group === 'Firm'}
								<Building2 size={15} aria-hidden="true" />
							{:else}
								<Database size={15} aria-hidden="true" />
							{/if}
						</span>
						<span>
							<strong>{result.title}</strong>
							<small>{result.subtitle}</small>
						</span>
						{#if index === activeIndex}<kbd>↵</kbd>{/if}
					</button>
				{/each}
			{:else}
				<div class="palette-empty">
					<Database size={20} aria-hidden="true" />
					<strong>No matching command or evidence.</strong>
					<span>Try a firm, fiscal year, metric, source title or reported value.</span>
				</div>
			{/if}
		</div>

		<footer>
			<span><kbd>↑</kbd><kbd>↓</kbd> move</span>
			<span><kbd>↵</kbd> open</span>
			<span><kbd>esc</kbd> close</span>
		</footer>
	</div>
{/if}

<style>
	.palette-backdrop {
		position: fixed;
		inset: 0;
		z-index: calc(var(--z-overlay) + 10);
		width: 100%;
		padding: 0;
		border: 0;
		background: oklch(0.1 0.018 255 / 0.62);
		backdrop-filter: blur(3px);
	}

	.command-palette {
		position: fixed;
		top: min(14vh, 120px);
		left: 50%;
		z-index: calc(var(--z-drawer) + 10);
		display: grid;
		width: min(700px, calc(100vw - 34px));
		max-height: min(720px, 76vh);
		grid-template-rows: auto auto minmax(0, 1fr) auto;
		transform: translateX(-50%);
		border: 1.5px solid var(--frame);
		background: var(--surface-overlay);
		box-shadow: var(--shadow-overlay);
		animation: palette-in 180ms var(--ease-out);
	}

	header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 18px;
		padding: 17px 19px;
		border-bottom: 1px solid var(--frame);
	}

	.palette-title {
		display: grid;
		gap: 3px;
	}

	.palette-title > span {
		display: flex;
		align-items: center;
		gap: 6px;
		color: var(--text-secondary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.palette-title h2 {
		margin: 0;
		font-family: var(--font-display);
		font-size: 21px;
		font-weight: 620;
		letter-spacing: -0.03em;
	}

	header > button {
		display: grid;
		width: 32px;
		height: 32px;
		place-items: center;
		padding: 0;
		border: 1px solid var(--frame);
		background: var(--surface-base);
		color: var(--ink);
		cursor: pointer;
	}

	.palette-search {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 10px;
		padding: 14px 18px;
		border-bottom: 1px solid var(--frame);
		background: var(--accent-soft);
	}

	.palette-search input {
		min-width: 0;
		height: 34px;
		padding: 0;
		border: 0;
		outline: 0;
		background: transparent;
		color: var(--ink);
		font: 600 13px var(--font-sans);
	}

	.palette-search input::placeholder {
		color: var(--text-secondary);
		opacity: 1;
	}

	kbd {
		padding: 2px 5px;
		border: 1px solid var(--border-subtle);
		background: var(--surface-base);
		color: var(--text-secondary);
		font: 8px var(--font-mono);
	}

	.palette-results {
		overflow-y: auto;
		padding: 8px;
	}

	.result-group {
		padding: 10px 10px 6px;
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 8px;
	}

	.palette-results > button {
		display: grid;
		width: 100%;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 10px;
		min-height: 52px;
		padding: 8px 10px;
		border: 1px solid transparent;
		background: transparent;
		color: var(--ink);
		text-align: left;
		cursor: pointer;
	}

	.palette-results > button:hover,
	.palette-results > button.active {
		border-color: var(--frame);
		background: var(--surface-subtle);
	}

	.result-icon {
		display: grid;
		width: 30px;
		height: 30px;
		place-items: center;
		border: 1px solid var(--border-subtle);
		background: var(--surface-base);
	}

	.palette-results button > span:nth-child(2) {
		display: grid;
		gap: 2px;
		min-width: 0;
	}

	.palette-results strong {
		overflow: hidden;
		font-size: 10px;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.palette-results small {
		overflow: hidden;
		color: var(--text-secondary);
		font-size: 9px;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.palette-empty {
		display: grid;
		min-height: 200px;
		place-content: center;
		justify-items: center;
		gap: 7px;
		color: var(--text-secondary);
		text-align: center;
	}

	.palette-empty strong {
		color: var(--ink);
		font-size: 11px;
	}

	.palette-empty span {
		font-size: 9px;
	}

	footer {
		display: flex;
		gap: 16px;
		padding: 10px 18px;
		border-top: 1px solid var(--frame);
		color: var(--text-secondary);
		font-size: 8px;
	}

	footer span {
		display: flex;
		align-items: center;
		gap: 4px;
	}

	@keyframes palette-in {
		from {
			transform: translate(-50%, -10px);
			opacity: 0;
		}
	}

	@media (max-width: 620px) {
		.command-palette {
			top: 12px;
			width: calc(100vw - 24px);
			max-height: calc(100dvh - 24px);
		}

		.palette-title h2 {
			font-size: 18px;
		}

		footer {
			display: none;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		.command-palette {
			animation: none;
		}
	}
</style>
