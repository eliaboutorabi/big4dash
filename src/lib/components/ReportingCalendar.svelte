<script lang="ts">
	import { CalendarRange, ExternalLink } from '@lucide/svelte';
	import { FIRM_COLORS } from '$lib/data/format';
	import type { FirmSummary } from '$lib/data/types';

	let {
		firms,
		onselect
	}: {
		firms: FirmSummary[];
		onselect: (observationId: string) => void;
	} = $props();

	const day = 86_400_000;
	const dateValue = (value: string) => new Date(`${value}T12:00:00Z`).getTime();
	let minDate = $derived(Math.min(...firms.map((firm) => dateValue(firm.periodStart))));
	let maxDate = $derived(Math.max(...firms.map((firm) => dateValue(firm.periodEnd))));
	let span = $derived(maxDate - minDate);
	const ticks = [
		'2024-06-01',
		'2024-09-01',
		'2024-12-01',
		'2025-03-01',
		'2025-06-01',
		'2025-09-01'
	];
	const tickLabel = new Intl.DateTimeFormat('en', { month: 'short', year: '2-digit' });
	const periodLabel = new Intl.DateTimeFormat('en', { month: 'short', year: 'numeric' });

	function position(value: string) {
		return ((dateValue(value) - minDate) / span) * 100;
	}

	function width(start: string, end: string) {
		return Math.max(((dateValue(end) - dateValue(start) + day) / span) * 100, 1);
	}
</script>

<div class="reporting-calendar">
	<div class="calendar-intro">
		<div class="calendar-icon"><CalendarRange size={18} aria-hidden="true" /></div>
		<div>
			<strong>Four fiscal calendars, one comparison frame</strong>
			<p>
				The latest reported years overlap, but they do not close together. KPMG’s period ends four
				months after Deloitte’s.
			</p>
		</div>
		<span>Period alignment</span>
	</div>

	<div class="calendar-chart">
		<div class="calendar-axis" aria-hidden="true">
			{#each ticks as tick (tick)}
				<span style:left={`${position(tick)}%`}
					>{tickLabel.format(new Date(`${tick}T12:00:00Z`))}</span
				>
			{/each}
		</div>
		<div class="calendar-rows">
			{#each firms as firm (firm.firm)}
				<div class="calendar-row">
					<strong>{firm.firm}</strong>
					<div class="calendar-track">
						<button
							style:left={`${position(firm.periodStart)}%`}
							style:width={`${width(firm.periodStart, firm.periodEnd)}%`}
							style:--firm-color={FIRM_COLORS[firm.firm]}
							aria-label={`${firm.firm} reporting period: ${periodLabel.format(new Date(`${firm.periodStart}T12:00:00Z`))} to ${periodLabel.format(new Date(`${firm.periodEnd}T12:00:00Z`))}. Open revenue evidence.`}
							onclick={() => onselect(firm.revenueObservationId)}
						>
							<span>{periodLabel.format(new Date(`${firm.periodEnd}T12:00:00Z`))} close</span>
							<ExternalLink size={12} aria-hidden="true" />
						</button>
					</div>
				</div>
			{/each}
		</div>
	</div>
</div>

<style>
	.reporting-calendar {
		display: grid;
		grid-template-columns: minmax(230px, 0.7fr) minmax(440px, 1.3fr);
		margin-bottom: 18px;
		border: 1.5px solid var(--frame);
		background: var(--surface-base);
	}

	.calendar-intro {
		position: relative;
		display: grid;
		grid-template-columns: 38px 1fr;
		gap: 12px;
		align-content: center;
		padding: 21px;
		border-right: 1px solid var(--frame);
	}

	.calendar-icon {
		display: grid;
		width: 36px;
		height: 36px;
		place-items: center;
		background: var(--accent-light);
		color: var(--accent-ink);
		box-shadow: var(--shadow-brutal-xs);
	}

	.calendar-intro strong {
		font-size: 13px;
	}

	.calendar-intro p {
		max-width: 42ch;
		margin: 5px 0 0;
		color: var(--text-secondary);
		font-size: 11px;
		line-height: 1.55;
	}

	.calendar-intro > span {
		position: absolute;
		right: 16px;
		bottom: 10px;
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 9px;
	}

	.calendar-chart {
		min-width: 0;
		padding: 16px 19px 17px;
		background: var(--surface-elevated);
	}

	.calendar-axis {
		position: relative;
		height: 21px;
		margin-left: 70px;
		border-bottom: 1px solid var(--border-subtle);
	}

	.calendar-axis span {
		position: absolute;
		top: 0;
		color: var(--text-tertiary);
		font-family: var(--font-mono);
		font-size: 9px;
		white-space: nowrap;
		transform: translateX(-50%);
	}

	.calendar-axis span:first-child {
		transform: none;
	}

	.calendar-axis span:last-child {
		transform: translateX(-100%);
	}

	.calendar-rows {
		display: grid;
		gap: 8px;
		padding-top: 10px;
	}

	.calendar-row {
		display: grid;
		grid-template-columns: 60px 1fr;
		gap: 10px;
		align-items: center;
	}

	.calendar-row > strong {
		font-size: 10px;
	}

	.calendar-track {
		position: relative;
		height: 25px;
		background: var(--surface-muted);
	}

	.calendar-track::after {
		position: absolute;
		inset: 0;
		border: 1px solid var(--border-subtle);
		content: '';
		pointer-events: none;
	}

	.calendar-track button {
		position: absolute;
		top: 0;
		bottom: 0;
		display: flex;
		align-items: center;
		justify-content: flex-end;
		gap: 6px;
		min-width: 82px;
		padding: 0 8px;
		overflow: hidden;
		border: 0;
		background: color-mix(in oklch, var(--firm-color) 84%, var(--surface-base));
		color: white;
		font-size: 9px;
		font-weight: 750;
		white-space: nowrap;
		cursor: pointer;
		transition: filter 160ms var(--ease-out);
	}

	.calendar-track button:hover {
		filter: brightness(1.08) saturate(1.08);
	}

	.calendar-track button:focus-visible {
		z-index: 1;
		outline: 2px solid var(--ink);
		outline-offset: 2px;
	}

	@media (max-width: 860px) {
		.reporting-calendar {
			grid-template-columns: 1fr;
		}

		.calendar-intro {
			border-right: 0;
			border-bottom: 1px solid var(--frame);
		}
	}

	@media (max-width: 560px) {
		.calendar-chart {
			overflow-x: auto;
			padding-inline: 14px;
		}

		.calendar-axis,
		.calendar-rows {
			width: 540px;
		}
	}
</style>
