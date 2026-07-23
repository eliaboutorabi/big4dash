<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="manifest" href="/site.webmanifest" />
	<meta name="theme-color" content="#101722" />
	<meta name="color-scheme" content="light dark" />
</svelte:head>
{@render children()}
