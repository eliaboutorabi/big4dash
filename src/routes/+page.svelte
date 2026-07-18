<script lang="ts">
	import { onMount } from 'svelte';
	import {
		ArrowRight,
		BookOpenCheck,
		ChartNoAxesCombined,
		Check,
		ChevronRight,
		CircleHelp,
		Database,
		ExternalLink,
		Eye,
		FileCheck2,
		Fingerprint,
		Globe2,
		Info,
		Layers3,
		LayoutDashboard,
		Menu,
		Play,
		ShieldCheck,
		Sparkles,
		TrendingUp,
		UsersRound,
		X
	} from '@lucide/svelte';
	import dashboardData from '$lib/data/dashboard-data.json';
	import CompositionComparison from '$lib/components/CompositionComparison.svelte';
	import EvidenceDrawer from '$lib/components/EvidenceDrawer.svelte';
	import ResearchExplorer from '$lib/components/ResearchExplorer.svelte';
	import TrendChart from '$lib/components/TrendChart.svelte';
	import WorkforceScatter from '$lib/components/WorkforceScatter.svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, fullNumber, percent } from '$lib/data/format';
	import type { DashboardData, FirmName, SeriesPoint } from '$lib/data/types';

	const data = dashboardData as DashboardData;
	const sections = [
		{ id: 'overview', label: 'Overview', icon: LayoutDashboard },
		{ id: 'scale', label: 'Scale & growth', icon: ChartNoAxesCombined },
		{ id: 'mix', label: 'Business mix', icon: Layers3 },
		{ id: 'geography', label: 'Geography', icon: Globe2 },
		{ id: 'workforce', label: 'Workforce', icon: UsersRound },
		{ id: 'evidence', label: 'Evidence ledger', icon: Database }
	];

	let activeSection = $state('overview');
	let selectedMetric = $state<'revenue' | 'people' | 'growth'>('revenue');
	let selectedFirms = $state<FirmName[]>([...FIRMS]);
	let selectedObservationId = $state<string | null>(null);
	let selectedFirm = $state<FirmName | null>(null);
	let researchMode = $state(true);
	let mobileNavOpen = $state(false);

	let selectedObservation = $derived(
		selectedObservationId
			? (data.observations.find((row) => row.id === selectedObservationId) ?? null)
			: null
	);
	let selectedFirmSummary = $derived(
		selectedFirm ? (data.firms.find((row) => row.firm === selectedFirm) ?? null) : null
	);
	let selectedSeries = $derived(
		(selectedMetric === 'revenue'
			? data.revenueSeries
			: selectedMetric === 'people'
				? data.peopleSeries
				: data.growthSeries) as Record<FirmName, SeriesPoint[]>
	);

	function toggleFirm(firm: FirmName) {
		selectedFirms = selectedFirms.includes(firm)
			? selectedFirms.length === 1
				? selectedFirms
				: selectedFirms.filter((item) => item !== firm)
			: [...selectedFirms, firm];
	}

	function openEvidence(observationId: string) {
		selectedFirm = null;
		selectedObservationId = observationId;
	}

	function scrollTo(sectionId: string) {
		activeSection = sectionId;
		mobileNavOpen = false;
		document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}

	async function startTour() {
		const { driver } = await import('driver.js');
		const tour = driver({
			showProgress: true,
			smoothScroll: true,
			animate: true,
			allowClose: true,
			stagePadding: 10,
			stageRadius: 12,
			popoverClass: 'big-four-tour',
			nextBtnText: 'Continue',
			prevBtnText: 'Back',
			doneBtnText: 'Explore the ledger',
			steps: [
				{
					element: '#tour-intro',
					popover: {
						title: 'Your Big Four research cockpit',
						description:
							'Compare the firms at a glance, then move from the headline to its exact source record.',
						side: 'bottom',
						align: 'start'
					}
				},
				{
					element: '#tour-firm-strip',
					popover: {
						title: 'Four firms, one comparison frame',
						description:
							'Select any firm to open its compact profile. Every headline number preserves the firm’s reporting-period caveat.',
						side: 'bottom'
					}
				},
				{
					element: '#tour-trend',
					popover: {
						title: 'Change the question, not the context',
						description:
							'Switch between revenue, workforce and local-currency growth. Hover a point and open the evidence behind it.',
						side: 'top'
					}
				},
				{
					element: '#tour-mix',
					popover: {
						title: 'See how each firm earns',
						description:
							'The composition view respects each network’s disclosed service taxonomy, including nested Deloitte reporting.',
						side: 'top'
					}
				},
				{
					element: '#tour-geography',
					popover: {
						title: 'Regional fingerprints',
						description:
							'Compare Americas, EMEA and Asia-Pacific exposure while keeping the original region labels one click away.',
						side: 'top'
					}
				},
				{
					element: '#tour-workforce',
					popover: {
						title: 'Scale has two dimensions',
						description:
							'This field plots revenue against disclosed people counts. Revenue per person is directional because definitions vary.',
						side: 'top'
					}
				},
				{
					element: '#tour-evidence',
					popover: {
						title: 'The research is the feature',
						description: `Search all ${data.meta.observationCount} observations. Filter by firm, metric family or source grade, then inspect the source locator and excerpt.`,
						side: 'top'
					}
				},
				{
					element: '#tour-research-mode',
					popover: {
						title: 'Choose your level of rigor',
						description:
							'Research mode keeps methodology and caveats in view. Switch it off when you want a cleaner executive scan.',
						side: 'bottom',
						align: 'end'
					}
				}
			]
		});
		tour.drive();
		localStorage.setItem('big-four-tour-seen', 'true');
	}

	onMount(() => {
		let scrollFrame = 0;
		const updateActiveSection = () => {
			cancelAnimationFrame(scrollFrame);
			scrollFrame = requestAnimationFrame(() => {
				let current = sections[0].id;
				for (const section of sections) {
					const element = document.getElementById(section.id);
					if (element && element.getBoundingClientRect().top <= 300) current = section.id;
				}
				activeSection = current;
			});
		};
		window.addEventListener('scroll', updateActiveSection, { passive: true });
		updateActiveSection();

		const shortcut = (event: KeyboardEvent) => {
			if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
				event.preventDefault();
				scrollTo('evidence');
				setTimeout(() => document.getElementById('evidence-search')?.focus(), 500);
			}
		};
		window.addEventListener('keydown', shortcut);

		if (!localStorage.getItem('big-four-tour-seen')) {
			setTimeout(startTour, 900);
		}

		return () => {
			cancelAnimationFrame(scrollFrame);
			window.removeEventListener('scroll', updateActiveSection);
			window.removeEventListener('keydown', shortcut);
		};
	});
</script>

<svelte:head>
	<title>FirmScope — The Big Four, compared</title>
	<meta
		name="description"
		content="An evidence-first interactive comparison of Deloitte, PwC, EY and KPMG across scale, growth, business mix, geography and workforce."
	/>
</svelte:head>

<div class="app-shell" class:research-mode={researchMode}>
	<aside class="sidebar" class:mobile-open={mobileNavOpen}>
		<div class="brand">
			<div class="brand-mark"><span></span><span></span><span></span><span></span></div>
			<div><strong>FirmScope</strong><span>Big Four research</span></div>
			<button
				class="mobile-close"
				aria-label="Close navigation"
				onclick={() => (mobileNavOpen = false)}><X size={18} /></button
			>
		</div>

		<div class="research-status">
			<div><span class="status-pulse"></span><strong>Research current</strong></div>
			<span>Through FY{data.meta.latestCommonYear}</span>
		</div>

		<nav aria-label="Dashboard sections">
			<span class="nav-label">Explore</span>
			{#each sections as section (section.id)}
				<button class:active={activeSection === section.id} onclick={() => scrollTo(section.id)}>
					<section.icon size={16} strokeWidth={activeSection === section.id ? 2.4 : 1.8} />
					<span>{section.label}</span>
					{#if activeSection === section.id}<ChevronRight size={13} />{/if}
				</button>
			{/each}
		</nav>

		<div class="sidebar-brief">
			<BookOpenCheck size={17} />
			<div>
				<strong>{data.meta.sourceCount} primary sources</strong><span
					>{data.meta.observationCount} structured observations</span
				>
			</div>
		</div>

		<div class="sidebar-footer">
			<button onclick={startTour}><Play size={13} fill="currentColor" /> Replay guided tour</button>
			<span>Independent portfolio research</span>
		</div>
	</aside>

	<div
		class="mobile-scrim"
		class:visible={mobileNavOpen}
		role="presentation"
		onclick={() => (mobileNavOpen = false)}
	></div>

	<main>
		<header class="topbar">
			<button
				class="menu-button"
				aria-label="Open navigation"
				onclick={() => (mobileNavOpen = true)}><Menu size={18} /></button
			>
			<div class="topbar-context">
				<span>Comparative intelligence</span>
				<strong>{sections.find((section) => section.id === activeSection)?.label}</strong>
			</div>
			<div class="topbar-actions">
				<span class="cutoff">Research cutoff <strong>18 Jul 2026</strong></span>
				<button
					id="tour-research-mode"
					class="mode-toggle"
					class:active={researchMode}
					onclick={() => (researchMode = !researchMode)}
				>
					<Eye size={14} />
					<span>Research mode</span>
					<i><b></b></i>
				</button>
				<button class="tour-button" onclick={startTour}><Sparkles size={14} /> Take the tour</button
				>
			</div>
		</header>

		<div class="content">
			<section id="overview" class="dashboard-section overview-section">
				<div id="tour-intro" class="overview-intro">
					<div>
						<span class="section-index">01 / Comparative overview</span>
						<h1>The Big Four, seen as one market.</h1>
						<p>
							Four global networks. Different reporting calendars, service taxonomies and geographic
							strengths—compared here without sanding away the caveats.
						</p>
						<div class="intro-actions">
							<button class="primary-action" onclick={() => scrollTo('scale')}
								>Start comparing <ArrowRight size={15} /></button
							>
							<button class="text-action" onclick={() => scrollTo('evidence')}
								>Inspect the research <Database size={14} /></button
							>
						</div>
					</div>
					<div class="market-pulse">
						<div class="pulse-heading">
							<span>Combined FY25 revenue</span><Fingerprint size={17} />
						</div>
						<strong>{currencyShort(data.meta.latestRevenueTotal, 0)}</strong>
						<div class="market-share-bar" aria-label="FY2025 reported revenue market share">
							{#each data.firms as firm (firm.firm)}
								<button
									style:width={`${firm.marketShare}%`}
									style:background={FIRM_COLORS[firm.firm]}
									aria-label={`${firm.firm}: ${percent(firm.marketShare)} market share`}
									onclick={() => (selectedFirm = firm.firm)}
								></button>
							{/each}
						</div>
						<div class="market-share-labels">
							{#each data.firms as firm (firm.firm)}
								<button onclick={() => (selectedFirm = firm.firm)}
									><i style:background={FIRM_COLORS[firm.firm]}></i><span>{firm.firm}</span><b
										>{percent(firm.marketShare, 0)}</b
									></button
								>
							{/each}
						</div>
					</div>
				</div>

				<div class="data-trust-line">
					<div>
						<FileCheck2 size={14} /><strong>{data.meta.reportedObservationCount}</strong><span
							>reported values</span
						>
					</div>
					<div>
						<ShieldCheck size={14} /><strong>{data.meta.qualityPassCount}</strong><span
							>automated QA checks passed</span
						>
					</div>
					<div>
						<Globe2 size={14} /><strong>{data.meta.activeSourceCount}</strong><span
							>live source URLs</span
						>
					</div>
					<div>
						<Info size={14} /><strong>{data.meta.archiveFallbackCount}</strong><span
							>archive fallbacks</span
						>
					</div>
				</div>

				<div id="tour-firm-strip" class="firm-strip">
					{#each data.firms as firm, index (firm.firm)}
						<button class="firm-summary" onclick={() => (selectedFirm = firm.firm)}>
							<div class="firm-summary-head">
								<span class="firm-badge" style:background={FIRM_COLORS[firm.firm]}
									>{firm.firm.slice(0, 1)}</span
								>
								<div><strong>{firm.firm}</strong><span>#{index + 1} by reported revenue</span></div>
								<ExternalLink size={14} />
							</div>
							<div class="firm-main-value">
								<strong>{currencyShort(firm.revenue)}</strong><span>FY25 revenue</span>
							</div>
							<div class="firm-measures">
								<div><span>5Y CAGR</span><strong>{percent(firm.fiveYearCagr)}</strong></div>
								<div><span>People</span><strong>{fullNumber(firm.people)}</strong></div>
								<div><span>Local growth</span><strong>{percent(firm.growth)}</strong></div>
							</div>
							<div class="firm-accent" style:background={FIRM_COLORS[firm.firm]}></div>
						</button>
					{/each}
				</div>

				<div class="insight-deck">
					<div class="insight-intro">
						<span>Research readout</span>
						<h2>What separates the firms right now</h2>
						<p>Three signals worth taking into an interview or strategy discussion.</p>
					</div>
					{#each data.insights as insight, index (insight.id)}
						<button class="insight-item" onclick={() => openEvidence(insight.observationId)}>
							<span class="insight-number">0{index + 1}</span>
							<div>
								<strong>{insight.title}</strong>
								<p>{insight.body}</p>
							</div>
							<ArrowRight size={15} />
						</button>
					{/each}
				</div>
			</section>

			<section id="scale" class="dashboard-section">
				<div class="section-heading">
					<div>
						<span class="section-index">02 / Scale &amp; momentum</span>
						<h2>Follow the shape of growth.</h2>
						<p>
							Switch measures without losing the comparative frame. Every plotted point opens its
							exact evidence record.
						</p>
					</div>
					<div class="section-callout">
						<TrendingUp size={16} /><span><strong>8.2%</strong> highest five-year revenue CAGR</span
						>
					</div>
				</div>

				<div id="tour-trend" class="chart-panel">
					<div class="panel-toolbar">
						<div class="metric-tabs" aria-label="Trend metric">
							<button
								class:active={selectedMetric === 'revenue'}
								onclick={() => (selectedMetric = 'revenue')}>Revenue</button
							>
							<button
								class:active={selectedMetric === 'people'}
								onclick={() => (selectedMetric = 'people')}>Workforce</button
							>
							<button
								class:active={selectedMetric === 'growth'}
								onclick={() => (selectedMetric = 'growth')}>Local growth</button
							>
						</div>
						<div class="firm-filters">
							{#each FIRMS as firm (firm)}
								<button class:active={selectedFirms.includes(firm)} onclick={() => toggleFirm(firm)}
									><i style:background={FIRM_COLORS[firm]}></i>{firm}<Check size={11} /></button
								>
							{/each}
						</div>
					</div>
					<TrendChart
						series={selectedSeries}
						metric={selectedMetric}
						{selectedFirms}
						onSelect={openEvidence}
					/>
					{#if researchMode}
						<div class="method-strip">
							<Info size={13} /><span
								>{selectedMetric === 'growth'
									? 'Growth is shown in locally reported currency where available; it is not derived from USD totals.'
									: selectedMetric === 'people'
										? 'Workforce labels differ by network and year. Use the evidence drawer to inspect the exact disclosed definition.'
										: 'Revenue is normalized to reported USD totals. Fiscal year-end dates differ across networks.'}</span
							>
						</div>
					{/if}
				</div>

				<div class="comparison-readout">
					<div>
						<span>Scale gap</span><strong>$30.7B</strong>
						<p>Deloitte’s FY25 reported revenue lead over KPMG.</p>
					</div>
					<div>
						<span>Growth spread</span><strong>2.4 pts</strong>
						<p>Difference between the fastest and slowest FY25 local growth rates.</p>
					</div>
					<div>
						<span>Common horizon</span><strong>FY20–25</strong>
						<p>Five-year comparison window used for CAGR.</p>
					</div>
				</div>
			</section>

			<section id="mix" class="dashboard-section">
				<div class="section-heading">
					<div>
						<span class="section-index">03 / Business mix</span>
						<h2>How each network earns.</h2>
						<p>
							Reported service lines are shown as a share of each firm’s disclosed service
							revenue—not forced into false equivalence.
						</p>
					</div>
					<div class="section-icon"><Layers3 size={20} /></div>
				</div>
				<div id="tour-mix" class="composition-panel">
					<div class="panel-context">
						<span>FY2025 service composition</span><strong
							>Click any segment to inspect the original classification</strong
						>
					</div>
					<CompositionComparison data={data.serviceMix} mode="service" onSelect={openEvidence} />
				</div>
			</section>

			<section id="geography" class="dashboard-section geography-section">
				<div class="section-heading">
					<div>
						<span class="section-index">04 / Geographic footprint</span>
						<h2>Regional fingerprints.</h2>
						<p>
							Americas is the largest disclosed region for three firms. KPMG’s reported EMA region
							remains its strongest.
						</p>
					</div>
					<div class="region-legend">
						<span><i class="americas"></i>Americas</span><span><i class="emea"></i>EMEA</span><span
							><i class="apac"></i>Asia-Pacific</span
						>
					</div>
				</div>
				<div id="tour-geography" class="geography-layout">
					<div class="composition-panel geography-panel">
						<div class="panel-context">
							<span>FY2025 regional revenue mix</span><strong
								>Normalized shares preserve original region labels in evidence</strong
							>
						</div>
						<CompositionComparison data={data.regionalMix} mode="region" onSelect={openEvidence} />
					</div>
					<aside class="geography-note">
						<Globe2 size={20} />
						<span>Standout</span>
						<strong>Deloitte’s Americas business alone is nearly the scale of KPMG globally.</strong
						>
						<p>$38.8B Americas revenue versus KPMG’s $39.8B total FY2025 revenue.</p>
						<button onclick={() => openEvidence('obs_del_0152')}
							>View supporting record <ArrowRight size={13} /></button
						>
					</aside>
				</div>
			</section>

			<section id="workforce" class="dashboard-section">
				<div class="section-heading">
					<div>
						<span class="section-index">05 / Workforce lens</span>
						<h2>Scale, people and a directional productivity proxy.</h2>
						<p>
							Revenue per disclosed person is useful for orientation—but workforce definitions make
							it a signal, not a verdict.
						</p>
					</div>
					<div class="section-callout">
						<UsersRound size={16} /><span><strong>1.52M</strong> disclosed people combined</span>
					</div>
				</div>
				<div id="tour-workforce" class="workforce-layout">
					<div class="scatter-panel">
						<div class="panel-context">
							<span>Revenue × disclosed workforce</span><strong
								>FY2025 network-level reporting</strong
							>
						</div>
						<WorkforceScatter firms={data.firms} onSelect={openEvidence} />
					</div>
					<div class="productivity-list">
						<div class="productivity-head">
							<span>Directional revenue / person</span><CircleHelp size={14} />
						</div>
						{#each [...data.firms].sort((a, b) => b.revenuePerPerson - a.revenuePerPerson) as firm, index (firm.firm)}
							<button onclick={() => openEvidence(firm.peopleObservationId)}>
								<span class="rank">0{index + 1}</span><i style:background={FIRM_COLORS[firm.firm]}
								></i><strong>{firm.firm}</strong><b>{currencyShort(firm.revenuePerPerson, 0)}</b>
							</button>
						{/each}
						<p>
							Calculated as reported FY25 revenue divided by the network’s disclosed people count.
							Partner, employee and average-vs-year-end definitions vary.
						</p>
					</div>
				</div>
			</section>

			<section id="evidence" class="dashboard-section evidence-section">
				<div class="section-heading">
					<div>
						<span class="section-index">06 / Evidence ledger</span>
						<h2>Interrogate the research.</h2>
						<p>
							Search the complete observation ledger, inspect source excerpts and test the
							comparability behind every claim.
						</p>
					</div>
					<div class="evidence-badge">
						<Database size={16} /><strong>{data.meta.observationCount}</strong><span
							>total records</span
						>
					</div>
				</div>
				<div id="tour-evidence" class="evidence-panel">
					<div class="source-health">
						<div>
							<span class="health-icon success"><Check size={13} /></span><span
								><strong>{data.meta.activeSourceCount} live sources</strong><small
									>Verified at collection</small
								></span
							>
						</div>
						<div>
							<span class="health-icon archive"><BookOpenCheck size={13} /></span><span
								><strong>{data.meta.archiveFallbackCount} archive fallbacks</strong><small
									>Stable evidence retained</small
								></span
							>
						</div>
						<div>
							<span class="health-icon qa"><ShieldCheck size={13} /></span><span
								><strong>{data.meta.qualityPassCount} QA checks</strong><small
									>{data.meta.qualityWarningCount} review warnings</small
								></span
							>
						</div>
					</div>
					<ResearchExplorer observations={data.observations} onSelect={openEvidence} />
				</div>
			</section>

			<footer class="page-footer">
				<div class="brand footer-brand">
					<div class="brand-mark"><span></span><span></span><span></span><span></span></div>
					<div><strong>FirmScope</strong><span>An independent comparison project</span></div>
				</div>
				<p>
					Figures are based on publicly available network-level disclosures. Definitions and
					reporting periods vary; source-level caveats are retained throughout.
				</p>
				<button onclick={startTour}
					><Play size={12} fill="currentColor" /> Tour the dashboard</button
				>
			</footer>
		</div>
	</main>

	<EvidenceDrawer
		observation={selectedObservation}
		onClose={() => (selectedObservationId = null)}
	/>

	{#if selectedFirmSummary}
		<button
			class="drawer-backdrop firm-backdrop"
			aria-label="Close firm profile"
			onclick={() => (selectedFirm = null)}
		></button>
		<aside class="firm-drawer" aria-label={`${selectedFirmSummary.firm} profile`}>
			<header>
				<div class="firm-profile-title">
					<span style:background={FIRM_COLORS[selectedFirmSummary.firm]}
						>{selectedFirmSummary.firm.slice(0, 1)}</span
					>
					<div><small>Firm profile</small><strong>{selectedFirmSummary.firm}</strong></div>
				</div>
				<button aria-label="Close firm profile" onclick={() => (selectedFirm = null)}
					><X size={18} /></button
				>
			</header>
			<div class="firm-profile-body">
				<div class="profile-lead">
					<span>FY2025 reported revenue</span><strong
						>{currencyShort(selectedFirmSummary.revenue)}</strong
					><b>{percent(selectedFirmSummary.marketShare)} of Big Four total</b>
				</div>
				<div class="profile-grid">
					<div>
						<span>Five-year CAGR</span><strong>{percent(selectedFirmSummary.fiveYearCagr)}</strong>
					</div>
					<div>
						<span>FY25 local growth</span><strong>{percent(selectedFirmSummary.growth)}</strong>
					</div>
					<div>
						<span>Disclosed people</span><strong>{fullNumber(selectedFirmSummary.people)}</strong>
					</div>
					<div>
						<span>Revenue / person</span><strong
							>{currencyShort(selectedFirmSummary.revenuePerPerson, 0)}</strong
						>
					</div>
				</div>
				<section>
					<span>Workforce definition</span>
					<p>{selectedFirmSummary.peopleDefinition}</p>
				</section>
				<div class="profile-actions">
					<button onclick={() => openEvidence(selectedFirmSummary!.revenueObservationId)}
						>Revenue evidence <ExternalLink size={13} /></button
					>
					<button onclick={() => openEvidence(selectedFirmSummary!.peopleObservationId)}
						>People evidence <ExternalLink size={13} /></button
					>
				</div>
			</div>
		</aside>
	{/if}
</div>
