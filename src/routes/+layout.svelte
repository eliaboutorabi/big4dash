<script lang="ts">
	import { asset } from '$app/paths';
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="manifest" href={asset('/site.webmanifest')} />
	<meta name="theme-color" content="#101722" />
	<meta name="color-scheme" content="light dark" />
</svelte:head>
{@render children()}
