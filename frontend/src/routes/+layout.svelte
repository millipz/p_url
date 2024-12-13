<script>
	import { onMount } from 'svelte';
	import { env } from '$env/dynamic/public';

	let longUrl = '';
	let shortUrl = '';
	let error = '';

	const API_ENDPOINT = env.PUBLIC_API_ENDPOINT;
	const BASE_URL = env.PUBLIC_BASE_URL || 'http://localhost:5000';

	console.log('API_ENDPOINT:', API_ENDPOINT);

	onMount(() => {
		const urlParams = new URLSearchParams(window.location.search);
		const short = urlParams.get('go');
		if (short) {
			getLongUrl(short);
		}
	});

	async function getLongUrl(shortPath) {
		error = '';
		const apiUrl = `${API_ENDPOINT}/${shortPath}`;
		try {
			const response = await fetch(apiUrl);
			if (response.status === 404) {
				error = 'Short URL not found';
				return;
			}
			if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
			const data = await response.json();
			if (data.long_url) {
				window.location.href = data.long_url;
			} else {
				error = 'Invalid response from server';
			}
		} catch (e) {
			error = `Error fetching long URL: ${e.message}`;
		}
	}

	async function createShortUrl() {
		error = '';
		if (!longUrl.trim()) {
			error = 'Please enter a URL';
			return;
		}

		try {
			const response = await fetch(API_ENDPOINT, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ url: longUrl })
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => null);
				throw new Error(errorData?.message || `HTTP error! status: ${response.status}`);
			}

			const data = await response.json();
			console.log('API Response:', data);

			if (!data.short_url) {
				throw new Error('Missing short_url in API response');
			}

			shortUrl = `${BASE_URL}/?go=${data.short_url}`;
		} catch (e) {
			console.error('Full error:', e);
			error = `Error creating short URL: ${e.message}`;
		}
	}
</script>

<main>
	<h1>p_url short'ner</h1>

	{#if error}
		<p class="error">{error}</p>
	{/if}

	<input bind:value={longUrl} placeholder="Enter a long URL" />
	<button on:click={createShortUrl}>Shorten URL</button>

	{#if shortUrl}
		<p>Here's your new shiny short URL! <a href={shortUrl}>{shortUrl}</a></p>
		<hr />
		<h3>API response (for debugging)</h3>
		<pre>{JSON.stringify({ long_url: longUrl, short_url: shortUrl }, null, 2)}</pre>
	{/if}
</main>

<style>
	.error {
		color: red;
	}
</style>
