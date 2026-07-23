<script lang="ts">
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { ArrowLeft, SearchX } from '@lucide/svelte';
</script>

<svelte:head>
	<title>{page.status} — FirmScope</title>
	<meta name="robots" content="noindex" />
</svelte:head>

<main class="error-stage">
	<a class="error-brand" href={resolve('/')} aria-label="Return to FirmScope">
		<span class="error-mark" aria-hidden="true">
			<i></i><i></i><i></i><i></i><b>4</b>
		</span>
		<span><strong>FirmScope</strong><small>Big Four intelligence</small></span>
	</a>

	<section>
		<div class="error-code"><SearchX size={20} /> {page.status}</div>
		<h1>{page.status === 404 ? 'This evidence trail ends here.' : 'The analysis hit an exception.'}</h1>
		<p>
			{page.status === 404
				? 'The requested page is not part of the current research instrument.'
				: page.error?.message || 'FirmScope could not complete this request.'}
		</p>
		<a class="return-link" href={resolve('/')}><ArrowLeft size={16} /> Return to the dashboard</a>
	</section>
</main>

<style>
	.error-stage {
		display: grid;
		min-height: 100vh;
		align-content: space-between;
		padding: clamp(24px, 5vw, 72px);
		background:
			linear-gradient(90deg, transparent 49.95%, oklch(1 0 0 / 0.08) 50%, transparent 50.05%),
			oklch(0.13 0.018 255);
		color: oklch(0.96 0.006 255);
	}

	.error-brand {
		display: flex;
		width: fit-content;
		align-items: center;
		gap: 12px;
		color: inherit;
		text-decoration: none;
	}

	.error-brand > span:last-child {
		display: grid;
		gap: 2px;
	}

	.error-brand strong {
		font-size: 14px;
	}

	.error-brand small {
		color: oklch(0.72 0.012 255);
		font-size: 11px;
	}

	.error-mark {
		position: relative;
		display: grid;
		width: 38px;
		height: 38px;
		grid-template-columns: repeat(2, 1fr);
		overflow: hidden;
	}

	.error-mark i:nth-child(1) {
		background: oklch(0.52 0.13 147);
	}
	.error-mark i:nth-child(2) {
		background: oklch(0.65 0.18 43);
	}
	.error-mark i:nth-child(3) {
		background: oklch(0.83 0.165 95);
	}
	.error-mark i:nth-child(4) {
		background: oklch(0.51 0.165 255);
	}
	.error-mark b {
		position: absolute;
		inset: 0;
		display: grid;
		place-items: center;
		font-size: 24px;
		text-shadow: 0 1px 0 oklch(0.08 0.006 255);
	}

	section {
		width: min(760px, 100%);
		padding-bottom: min(14vh, 120px);
	}

	.error-code {
		display: flex;
		align-items: center;
		gap: 9px;
		color: oklch(0.82 0.15 90);
		font-family: 'JetBrains Mono Variable', monospace;
		font-size: 13px;
	}

	h1 {
		max-width: 10ch;
		margin: 22px 0 18px;
		font-family: 'Newsreader Variable', Georgia, serif;
		font-size: clamp(3rem, 8vw, 6rem);
		font-weight: 520;
		line-height: 0.93;
		letter-spacing: -0.035em;
		text-wrap: balance;
	}

	p {
		max-width: 58ch;
		margin: 0 0 30px;
		color: oklch(0.76 0.012 255);
		font-size: 15px;
		line-height: 1.7;
	}

	.return-link {
		display: inline-flex;
		align-items: center;
		gap: 9px;
		padding: 12px 15px;
		border: 1px solid oklch(0.9 0.006 255);
		background: oklch(0.9 0.16 92);
		color: oklch(0.16 0.025 255);
		font-size: 13px;
		font-weight: 800;
		text-decoration: none;
		box-shadow: 4px 4px 0 oklch(0.9 0.006 255);
		transition:
			transform 160ms cubic-bezier(0.2, 0.75, 0.2, 1),
			box-shadow 160ms cubic-bezier(0.2, 0.75, 0.2, 1);
	}

	.return-link:hover {
		transform: translate(2px, 2px);
		box-shadow: 2px 2px 0 oklch(0.9 0.006 255);
	}

	.return-link:focus-visible,
	.error-brand:focus-visible {
		outline: 2px solid oklch(0.9 0.16 92);
		outline-offset: 4px;
	}
</style>
