<script lang="ts">
	import { onMount, untrack } from 'svelte';
	import type { PageProps } from './$types';
	import SiGithub from '@icons-pack/svelte-simple-icons/icons/SiGithub';
	import {
		ArrowRight,
		Bookmark,
		BookOpenCheck,
		ChartNoAxesCombined,
		Check,
		ChevronRight,
		CircleHelp,
		Database,
		ExternalLink,
		Globe2,
		Info,
		Layers3,
		LayoutDashboard,
		MapPinned,
		Menu,
		Moon,
		Share2,
		ShieldCheck,
		Sparkles,
		Sun,
		TrendingUp,
		UsersRound,
		X
	} from '@lucide/svelte';
	import CompositionComparison from '$lib/components/CompositionComparison.svelte';
	import CoverageMatrix from '$lib/components/CoverageMatrix.svelte';
	import EvidenceDrawer from '$lib/components/EvidenceDrawer.svelte';
	import EvidenceNotebook from '$lib/components/EvidenceNotebook.svelte';
	import GrowthIndex from '$lib/components/GrowthIndex.svelte';
	import MarketMosaic from '$lib/components/MarketMosaic.svelte';
	import MarketShareHistory from '$lib/components/MarketShareHistory.svelte';
	import OfficeAtlas from '$lib/components/OfficeAtlas.svelte';
	import PairwiseCompare from '$lib/components/PairwiseCompare.svelte';
	import ReportingCalendar from '$lib/components/ReportingCalendar.svelte';
	import ResearchExplorer from '$lib/components/ResearchExplorer.svelte';
	import RevisionTrail from '$lib/components/RevisionTrail.svelte';
	import ScenarioStudio from '$lib/components/ScenarioStudio.svelte';
	import TrendChart from '$lib/components/TrendChart.svelte';
	import WorkforceScatter from '$lib/components/WorkforceScatter.svelte';
	import { FIRM_COLORS, FIRMS, currencyShort, fullNumber, percent } from '$lib/data/format';
	import type { DashboardData, FirmName, SeriesPoint } from '$lib/data/types';

	let { data: pageData }: PageProps = $props();
	const data = untrack(() => pageData.dashboardData as DashboardData);
	const rankedFirms = [...data.firms].sort((a, b) => b.revenue - a.revenue);
	const strongestCagr = [...data.firms].sort((a, b) => b.fiveYearCagr - a.fiveYearCagr)[0];
	const revenueScaleGap = rankedFirms[0].revenue - rankedFirms.at(-1)!.revenue;
	const growthSpread =
		Math.max(...data.firms.map((firm) => firm.growth)) -
		Math.min(...data.firms.map((firm) => firm.growth));
	const combinedPeople = data.firms.reduce((sum, firm) => sum + firm.people, 0);
	const deloitteAmericas =
		data.regionalMix.Deloitte.find((region) => region.canonical === 'Americas') ??
		data.regionalMix.Deloitte[0];
	const latestYearLabel = `FY${String(data.meta.latestCommonYear).slice(-2)}`;
	const researchCutoffLabel = new Intl.DateTimeFormat('en-GB', {
		day: '2-digit',
		month: 'short',
		year: 'numeric'
	}).format(new Date(`${data.meta.researchCutoff}T12:00:00Z`));
	const sections = [
		{ id: 'overview', label: 'Overview', icon: LayoutDashboard },
		{ id: 'scale', label: 'Scale & growth', icon: ChartNoAxesCombined },
		{ id: 'mix', label: 'Business mix', icon: Layers3 },
		{ id: 'offices', label: 'Office atlas', icon: MapPinned },
		{ id: 'geography', label: 'Geography', icon: Globe2 },
		{ id: 'workforce', label: 'Workforce', icon: UsersRound },
		{ id: 'evidence', label: 'Evidence ledger', icon: Database }
	];

	let activeSection = $state('overview');
	let selectedMetric = $state<'revenue' | 'people' | 'growth'>('revenue');
	let selectedFirms = $state<FirmName[]>([...FIRMS]);
	let selectedObservationId = $state<string | null>(null);
	let selectedFirm = $state<FirmName | null>(null);
	let savedObservationIds = $state<string[]>([]);
	let notebookOpen = $state(false);
	let viewCopied = $state(false);
	let mobileNavOpen = $state(false);
	let aboutOpen = $state(false);
	let theme = $state<'light' | 'dark'>('light');

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
	let savedObservations = $derived(
		savedObservationIds
			.map((id) => data.observations.find((observation) => observation.id === id))
			.filter((observation): observation is NonNullable<typeof observation> => Boolean(observation))
	);

	function toggleFirm(firm: FirmName) {
		selectedFirms = selectedFirms.includes(firm)
			? selectedFirms.length === 1
				? selectedFirms
				: selectedFirms.filter((item) => item !== firm)
			: [...selectedFirms, firm];
		syncUrlState();
	}

	function openEvidence(observationId: string) {
		selectedFirm = null;
		selectedObservationId = observationId;
		syncUrlState();
	}

	function closeEvidence() {
		selectedObservationId = null;
		syncUrlState();
	}

	function setMetric(metric: 'revenue' | 'people' | 'growth') {
		selectedMetric = metric;
		syncUrlState();
	}

	function toggleSavedObservation(observationId: string) {
		savedObservationIds = savedObservationIds.includes(observationId)
			? savedObservationIds.filter((id) => id !== observationId)
			: [...savedObservationIds, observationId];
		localStorage.setItem('firmscope-evidence-notebook', JSON.stringify(savedObservationIds));
	}

	function toggleTheme() {
		theme = theme === 'light' ? 'dark' : 'light';
		document.documentElement.dataset.theme = theme;
		localStorage.setItem('firmscope-theme', theme);
	}

	function scrollTo(sectionId: string) {
		activeSection = sectionId;
		mobileNavOpen = false;
		document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
		syncUrlState();
	}

	function syncUrlState() {
		if (typeof window === 'undefined') return;
		const url = new URL(window.location.href);
		if (activeSection === 'overview') url.searchParams.delete('section');
		else url.searchParams.set('section', activeSection);
		if (selectedMetric === 'revenue') url.searchParams.delete('metric');
		else url.searchParams.set('metric', selectedMetric);
		if (selectedFirms.length === FIRMS.length) url.searchParams.delete('firms');
		else url.searchParams.set('firms', selectedFirms.join(','));
		if (selectedObservationId) url.searchParams.set('evidence', selectedObservationId);
		else url.searchParams.delete('evidence');
		window.history.replaceState({}, '', url);
	}

	async function shareView() {
		syncUrlState();
		await navigator.clipboard.writeText(window.location.href);
		viewCopied = true;
		window.setTimeout(() => (viewCopied = false), 1800);
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
					element: '#tour-offices',
					popover: {
						title: 'See the physical network',
						description: `Explore ${data.officeLocations.length.toLocaleString()} mapped locations. Source coordinates and city-centroid joins are deliberately encoded differently so coverage is never overstated.`,
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
				}
			]
		});
		tour.drive();
		localStorage.setItem('big-four-tour-seen', 'true');
	}

	onMount(() => {
		theme = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
		const initialUrl = new URL(window.location.href);
		const initialMetric = initialUrl.searchParams.get('metric');
		if (initialMetric === 'people' || initialMetric === 'growth') selectedMetric = initialMetric;
		const initialFirms = (initialUrl.searchParams.get('firms') ?? '')
			.split(',')
			.filter((firm): firm is FirmName => FIRMS.includes(firm as FirmName));
		if (initialFirms.length) selectedFirms = [...new Set(initialFirms)];
		const initialEvidence = initialUrl.searchParams.get('evidence');
		if (
			initialEvidence &&
			data.observations.some((observation) => observation.id === initialEvidence)
		) {
			selectedObservationId = initialEvidence;
		}
		const initialSection = initialUrl.searchParams.get('section');
		if (initialSection && sections.some((section) => section.id === initialSection)) {
			activeSection = initialSection;
			requestAnimationFrame(() => document.getElementById(initialSection)?.scrollIntoView());
		}
		try {
			savedObservationIds = JSON.parse(localStorage.getItem('firmscope-evidence-notebook') ?? '[]');
		} catch {
			savedObservationIds = [];
		}
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
			if (event.key === 'Escape' && aboutOpen) {
				aboutOpen = false;
				return;
			}
			if (event.key === 'Escape' && selectedFirm) {
				selectedFirm = null;
				return;
			}
			if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
				event.preventDefault();
				scrollTo('evidence');
				setTimeout(() => document.getElementById('evidence-search')?.focus(), 500);
			}
		};
		window.addEventListener('keydown', shortcut);

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
	<meta property="og:type" content="website" />
	<meta property="og:site_name" content="FirmScope" />
	<meta property="og:title" content="FirmScope — The Big Four, compared" />
	<meta
		property="og:description"
		content="Traceable comparative intelligence across the world's four largest professional-services networks."
	/>
	<meta name="twitter:card" content="summary" />
	<meta name="twitter:title" content="FirmScope — The Big Four, compared" />
	<meta
		name="twitter:description"
		content="Evidence-first visual intelligence for Deloitte, PwC, EY and KPMG."
	/>
</svelte:head>

<div class="app-shell">
	<aside class="sidebar" class:mobile-open={mobileNavOpen}>
		<div class="brand">
			<button class="brand-button" aria-label="About FirmScope" onclick={() => (aboutOpen = true)}>
				<span class="brand-mark" aria-hidden="true">
					<i></i><i></i><i></i><i></i><b>4</b>
				</span>
				<span class="brand-copy"
					><strong>FirmScope</strong><small>Big Four intelligence</small></span
				>
			</button>
			<button
				class="mobile-close"
				aria-label="Close navigation"
				onclick={() => (mobileNavOpen = false)}><X size={18} /></button
			>
		</div>

		<nav aria-label="Dashboard sections">
			<span class="nav-label">Explore</span>
			<button class:active={activeSection === 'overview'} onclick={() => scrollTo('overview')}>
				<LayoutDashboard size={16} /><span>Overview</span
				>{#if activeSection === 'overview'}<ChevronRight size={13} />{/if}
			</button>
			<button class:active={activeSection === 'scale'} onclick={() => scrollTo('scale')}>
				<ChartNoAxesCombined size={16} /><span>Scale &amp; growth</span
				>{#if activeSection === 'scale'}<ChevronRight size={13} />{/if}
			</button>
			<button class:active={activeSection === 'mix'} onclick={() => scrollTo('mix')}>
				<Layers3 size={16} /><span>Business mix</span>{#if activeSection === 'mix'}<ChevronRight
						size={13}
					/>{/if}
			</button>
			<button class:active={activeSection === 'offices'} onclick={() => scrollTo('offices')}>
				<MapPinned size={16} /><span>Office atlas</span
				>{#if activeSection === 'offices'}<ChevronRight size={13} />{/if}
			</button>
			<button class:active={activeSection === 'geography'} onclick={() => scrollTo('geography')}>
				<Globe2 size={16} /><span>Geography</span>{#if activeSection === 'geography'}<ChevronRight
						size={13}
					/>{/if}
			</button>
			<button class:active={activeSection === 'workforce'} onclick={() => scrollTo('workforce')}>
				<UsersRound size={16} /><span>Workforce</span
				>{#if activeSection === 'workforce'}<ChevronRight size={13} />{/if}
			</button>
			<button class:active={activeSection === 'evidence'} onclick={() => scrollTo('evidence')}>
				<Database size={16} /><span>Evidence ledger</span
				>{#if activeSection === 'evidence'}<ChevronRight size={13} />{/if}
			</button>
		</nav>

		<div class="sidebar-brief">
			<BookOpenCheck size={17} />
			<div>
				<strong>{data.meta.sourceCount} primary sources</strong><span
					>{data.meta.observationCount} structured observations</span
				>
			</div>
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
				<span class="cutoff">Research cutoff <strong>{researchCutoffLabel}</strong></span>
				<button
					class="notebook-button"
					aria-label={`Open evidence notebook with ${savedObservationIds.length} saved ${
						savedObservationIds.length === 1 ? 'record' : 'records'
					}`}
					onclick={() => (notebookOpen = true)}
				>
					<Bookmark size={14} /> Notebook
					<span>{savedObservationIds.length}</span>
				</button>
				<button
					class="share-view-button"
					aria-label={viewCopied ? 'Dashboard link copied' : 'Copy link to current dashboard view'}
					onclick={shareView}
				>
					<Share2 size={14} />
					{viewCopied ? 'Copied' : 'Share view'}
				</button>
				<button class="tour-button" onclick={startTour}><Sparkles size={14} /> Take the tour</button
				>
				<a
					class="icon-button github-button"
					href="https://github.com/eliaboutorabi/big4dash"
					target="_blank"
					rel="noreferrer"
					aria-label="View FirmScope on GitHub"
					title="View FirmScope on GitHub"><SiGithub size={16} title="" /></a
				>
				<button
					class="icon-button theme-toggle"
					aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
					title={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
					onclick={toggleTheme}
				>
					{#if theme === 'light'}<Moon size={15} />{:else}<Sun size={16} />{/if}
				</button>
			</div>
		</header>

		<div class="content">
			<section id="overview" class="dashboard-section overview-section">
				<div id="tour-intro" class="overview-intro">
					<div>
						<h1>Four networks. One market. Every caveat intact.</h1>
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
					<MarketMosaic
						firms={data.firms}
						total={data.meta.latestRevenueTotal}
						onselect={(firm) => (selectedFirm = firm)}
					/>
				</div>

				<div id="tour-firm-strip" class="firm-strip">
					<button class="firm-summary" onclick={() => (selectedFirm = 'Deloitte')}>
						<div class="firm-summary-head">
							<span class="firm-badge" style:background={FIRM_COLORS.Deloitte}>D</span>
							<div><strong>Deloitte</strong><span>#1 by reported revenue</span></div>
							<ExternalLink size={14} />
						</div>
						<div class="firm-main-value">
							<strong>{currencyShort(data.firms[0].revenue)}</strong><span>FY25 revenue</span>
						</div>
						<div class="firm-measures">
							<div><span>5Y CAGR</span><strong>{percent(data.firms[0].fiveYearCagr)}</strong></div>
							<div><span>People</span><strong>{fullNumber(data.firms[0].people)}</strong></div>
							<div><span>Local growth</span><strong>{percent(data.firms[0].growth)}</strong></div>
						</div>
						<div class="firm-accent" style:background={FIRM_COLORS.Deloitte}></div>
					</button>
					<button class="firm-summary" onclick={() => (selectedFirm = 'PwC')}>
						<div class="firm-summary-head">
							<span class="firm-badge" style:background={FIRM_COLORS.PwC}>P</span>
							<div><strong>PwC</strong><span>#2 by reported revenue</span></div>
							<ExternalLink size={14} />
						</div>
						<div class="firm-main-value">
							<strong>{currencyShort(data.firms[1].revenue)}</strong><span>FY25 revenue</span>
						</div>
						<div class="firm-measures">
							<div><span>5Y CAGR</span><strong>{percent(data.firms[1].fiveYearCagr)}</strong></div>
							<div><span>People</span><strong>{fullNumber(data.firms[1].people)}</strong></div>
							<div><span>Local growth</span><strong>{percent(data.firms[1].growth)}</strong></div>
						</div>
						<div class="firm-accent" style:background={FIRM_COLORS.PwC}></div>
					</button>
					<button class="firm-summary" onclick={() => (selectedFirm = 'EY')}>
						<div class="firm-summary-head">
							<span class="firm-badge" style:background={FIRM_COLORS.EY}>E</span>
							<div><strong>EY</strong><span>#3 by reported revenue</span></div>
							<ExternalLink size={14} />
						</div>
						<div class="firm-main-value">
							<strong>{currencyShort(data.firms[2].revenue)}</strong><span>FY25 revenue</span>
						</div>
						<div class="firm-measures">
							<div><span>5Y CAGR</span><strong>{percent(data.firms[2].fiveYearCagr)}</strong></div>
							<div><span>People</span><strong>{fullNumber(data.firms[2].people)}</strong></div>
							<div><span>Local growth</span><strong>{percent(data.firms[2].growth)}</strong></div>
						</div>
						<div class="firm-accent" style:background={FIRM_COLORS.EY}></div>
					</button>
					<button class="firm-summary" onclick={() => (selectedFirm = 'KPMG')}>
						<div class="firm-summary-head">
							<span class="firm-badge" style:background={FIRM_COLORS.KPMG}>K</span>
							<div><strong>KPMG</strong><span>#4 by reported revenue</span></div>
							<ExternalLink size={14} />
						</div>
						<div class="firm-main-value">
							<strong>{currencyShort(data.firms[3].revenue)}</strong><span>FY25 revenue</span>
						</div>
						<div class="firm-measures">
							<div><span>5Y CAGR</span><strong>{percent(data.firms[3].fiveYearCagr)}</strong></div>
							<div><span>People</span><strong>{fullNumber(data.firms[3].people)}</strong></div>
							<div><span>Local growth</span><strong>{percent(data.firms[3].growth)}</strong></div>
						</div>
						<div class="firm-accent" style:background={FIRM_COLORS.KPMG}></div>
					</button>
				</div>

				<PairwiseCompare firms={data.firms} onselect={openEvidence} />

				<div class="insight-deck">
					<div class="insight-intro">
						<span>Research readout</span>
						<h2>What separates the firms right now</h2>
						<p>Three signals worth taking into an interview or strategy discussion.</p>
					</div>
					<button class="insight-item" onclick={() => openEvidence(data.insights[0].observationId)}
						><span class="insight-number">01</span>
						<div>
							<strong>{data.insights[0].title}</strong>
							<p>{data.insights[0].body}</p>
						</div>
						<ArrowRight size={15} /></button
					>
					<button class="insight-item" onclick={() => openEvidence(data.insights[1].observationId)}
						><span class="insight-number">02</span>
						<div>
							<strong>{data.insights[1].title}</strong>
							<p>{data.insights[1].body}</p>
						</div>
						<ArrowRight size={15} /></button
					>
					<button class="insight-item" onclick={() => openEvidence(data.insights[2].observationId)}
						><span class="insight-number">03</span>
						<div>
							<strong>{data.insights[2].title}</strong>
							<p>{data.insights[2].body}</p>
						</div>
						<ArrowRight size={15} /></button
					>
				</div>

				<div class="story-rail" aria-label="Dashboard narrative">
					<div class="story-rail-intro">
						<span>The research arc</span>
						<strong>Read the market in three moves.</strong>
					</div>
					<button onclick={() => scrollTo('scale')}>
						<span>01</span><strong>Measure the race</strong><small
							>Scale, pace and the gap between them</small
						><ArrowRight size={18} />
					</button>
					<button onclick={() => scrollTo('mix')}>
						<span>02</span><strong>Open the engine</strong><small
							>What each network sells and where</small
						><ArrowRight size={18} />
					</button>
					<button onclick={() => scrollTo('offices')}>
						<span>03</span><strong>Enter the footprint</strong><small
							>Offices, regions and people behind scale</small
						><ArrowRight size={18} />
					</button>
				</div>
			</section>

			<section id="scale" class="dashboard-section">
				<div class="section-heading">
					<div>
						<h2>Growth looks different when the denominator is visible.</h2>
						<p>
							Move between revenue, people and local growth without losing the comparative frame.
							Every plotted point opens its exact evidence record.
						</p>
					</div>
					<div class="section-callout">
						<TrendingUp size={16} /><span
							><strong>{percent(strongestCagr.fiveYearCagr)}</strong> highest five-year CAGR ·
							{strongestCagr.firm}</span
						>
					</div>
				</div>

				<ReportingCalendar firms={data.firms} onselect={openEvidence} />

				<div id="tour-trend" class="chart-panel">
					<div class="panel-toolbar">
						<div class="metric-tabs" aria-label="Trend metric">
							<button
								class:active={selectedMetric === 'revenue'}
								onclick={() => setMetric('revenue')}>Revenue</button
							>
							<button class:active={selectedMetric === 'people'} onclick={() => setMetric('people')}
								>Workforce</button
							>
							<button class:active={selectedMetric === 'growth'} onclick={() => setMetric('growth')}
								>Local growth</button
							>
						</div>
						<div class="firm-filters">
							{#each [...FIRMS] as firm (firm)}
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
					<div class="method-strip">
						<Info size={13} /><span
							>{selectedMetric === 'growth'
								? 'Growth is shown in locally reported currency where available; it is not derived from USD totals.'
								: selectedMetric === 'people'
									? 'Workforce labels differ by network and year. Use the evidence drawer to inspect the exact disclosed definition.'
									: 'Revenue is normalized to reported USD totals. Fiscal year-end dates differ across networks.'}</span
						>
					</div>
				</div>

				<div class="comparison-readout">
					<div>
						<span>Scale gap</span><strong>{currencyShort(revenueScaleGap)}</strong>
						<p>
							{rankedFirms[0].firm}’s {latestYearLabel} reported revenue lead over
							{rankedFirms.at(-1)!.firm}.
						</p>
					</div>
					<div>
						<span>Growth spread</span><strong>{growthSpread.toFixed(1)} pts</strong>
						<p>Difference between the fastest and slowest {latestYearLabel} local growth rates.</p>
					</div>
					<div>
						<span>Common horizon</span><strong>FY20–25</strong>
						<p>Five-year comparison window used for CAGR.</p>
					</div>
				</div>
				<GrowthIndex series={data.revenueSeries} onselect={openEvidence} />
				<MarketShareHistory series={data.revenueSeries} onselect={openEvidence} />
				<ScenarioStudio firms={data.firms} onselect={openEvidence} />
			</section>

			<section id="mix" class="dashboard-section">
				<div class="section-heading">
					<div>
						<h2>Revenue is one number. The businesses beneath it are not.</h2>
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

			<section id="offices" class="dashboard-section office-section">
				<div class="section-heading">
					<div>
						<h2>The firms are global. Their disclosed footprints are not identical.</h2>
						<p>
							Explore the physical network behind the financial scale. This atlas preserves the
							difference between source-level coordinates and a representative hub sample.
						</p>
					</div>
					<div class="section-callout office-callout">
						<MapPinned size={17} /><span
							><strong>{data.officeLocations.length.toLocaleString()}</strong> mapped locations</span
						>
					</div>
				</div>
				<div id="tour-offices">
					<OfficeAtlas locations={data.officeLocations} />
				</div>
			</section>

			<section id="geography" class="dashboard-section geography-section">
				<div class="section-heading">
					<div>
						<h2>Regional exposure is the hidden strategy.</h2>
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
						<div class="geography-insight">
							<div class="geography-insight-icon"><Globe2 size={18} /></div>
							<div>
								<span>Scale comparison</span>
								<strong>Deloitte’s Americas business is nearly the scale of KPMG globally.</strong>
								<p>
									{currencyShort(deloitteAmericas.value)} Americas revenue versus KPMG’s
									{currencyShort(data.firms.find((firm) => firm.firm === 'KPMG')!.revenue)} total
									{latestYearLabel} revenue.
								</p>
							</div>
							<button onclick={() => openEvidence(deloitteAmericas.observationId)}
								>View record <ArrowRight size={13} /></button
							>
						</div>
					</div>
				</div>
			</section>

			<section id="workforce" class="dashboard-section">
				<div class="section-heading">
					<div>
						<h2>People turn scale into operating leverage.</h2>
						<p>
							Revenue per disclosed person is useful for orientation—but workforce definitions make
							it a signal, not a verdict.
						</p>
					</div>
					<div class="section-callout">
						<UsersRound size={16} /><span
							><strong>{fullNumber(combinedPeople)}</strong> disclosed people combined</span
						>
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
						<h2>Every conclusion should survive a source check.</h2>
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
					<CoverageMatrix
						coverage={data.coverage}
						observations={data.observations}
						onselect={openEvidence}
					/>
					<RevisionTrail observations={data.observations} onselect={openEvidence} />
					<ResearchExplorer observations={data.observations} onSelect={openEvidence} />
				</div>
			</section>

			<footer class="page-footer">
				<button class="footer-brand" onclick={() => (aboutOpen = true)}>
					<span class="brand-mark" aria-hidden="true">
						<i></i><i></i><i></i><i></i><b>4</b>
					</span>
					<span class="brand-copy"
						><strong>FirmScope</strong><small>Big Four intelligence</small></span
					>
				</button>
				<p>
					Figures are based on publicly available network-level disclosures. Definitions and
					reporting periods vary; source-level caveats are retained throughout.
				</p>
				<a href="https://github.com/eliaboutorabi/big4dash" target="_blank" rel="noreferrer"
					>View repository <ExternalLink size={12} /></a
				>
			</footer>
		</div>
	</main>

	<EvidenceDrawer
		observation={selectedObservation}
		onClose={closeEvidence}
		saved={selectedObservation ? savedObservationIds.includes(selectedObservation.id) : false}
		onToggleSave={toggleSavedObservation}
	/>
	<EvidenceNotebook
		open={notebookOpen}
		observations={savedObservations}
		onclose={() => (notebookOpen = false)}
		onselect={(observationId) => {
			notebookOpen = false;
			openEvidence(observationId);
		}}
		onremove={toggleSavedObservation}
		onclear={() => {
			savedObservationIds = [];
			localStorage.removeItem('firmscope-evidence-notebook');
		}}
	/>

	{#if aboutOpen}
		<button
			class="about-backdrop"
			tabindex="-1"
			aria-hidden="true"
			onclick={() => (aboutOpen = false)}
		></button>
		<dialog open class="about-dialog" aria-modal="true" aria-labelledby="about-title">
			<header>
				<span class="brand-mark about-mark" aria-hidden="true">
					<i></i><i></i><i></i><i></i><b>4</b>
				</span>
				<button aria-label="Close about FirmScope" onclick={() => (aboutOpen = false)}
					><X size={18} /></button
				>
			</header>
			<span class="about-eyebrow">Designed and developed by</span>
			<h2 id="about-title">Elham Aboutorabi</h2>
			<p>
				FirmScope brings public Big Four disclosures into one interactive, evidence-first comparison
				experience.
			</p>
			<div class="about-links">
				<a href="https://github.com/eliaboutorabi" target="_blank" rel="noreferrer"
					><SiGithub size={16} title="" /> GitHub profile <ExternalLink size={13} /></a
				>
				<a href="https://eliaboutorabi.github.io" target="_blank" rel="noreferrer"
					><Globe2 size={16} /> Personal website <ExternalLink size={13} /></a
				>
			</div>
		</dialog>
	{/if}

	{#if selectedFirmSummary}
		<button
			class="drawer-backdrop firm-backdrop"
			tabindex="-1"
			aria-hidden="true"
			onclick={() => (selectedFirm = null)}
		></button>
		<div
			class="firm-drawer"
			role="dialog"
			aria-modal="true"
			aria-label={`${selectedFirmSummary.firm} profile`}
		>
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
		</div>
	{/if}
</div>
