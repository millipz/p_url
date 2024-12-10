<script>
    import { onMount } from 'svelte';
    import { env } from '$env/dynamic/public';
  
    let longUrl = '';
    let shortUrl = '';
    let error = '';
  
    const API_ENDPOINT = env.PUBLIC_API_ENDPOINT;
    const BASE_URL = env.PUBLIC_BASE_URL || 'http://localhost:5000';
  
    onMount(() => {
      const urlParams = new URLSearchParams(window.location.search);
      const short = urlParams.get('go');
      if (short) {
        getLongUrl(short);
      }
    });
  
    async function getLongUrl(shortPath) {
      const apiUrl = `${API_ENDPOINT}/${shortPath}`;
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        if (data.long_url) {
          window.location.href = data.long_url;
        } else {
          error = 'Long URL not found';
        }
      } catch (e) {
        error = `Error fetching long URL: ${e.message}`;
      }
    }
  
    async function createShortUrl() {
      try {
        const response = await fetch(API_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: longUrl })
        });
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        shortUrl = `${BASE_URL}/?go=${data.short_url}`;
      } catch (e) {
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
      <p>Here's your new shiny short URL! <a href={shortUrl}>{shortUrl.split('://')[1]}</a></p>
      <hr />
      <h3>API response (for debugging)</h3>
      <pre>{JSON.stringify({ short_url: shortUrl }, null, 2)}</pre>
    {/if}
  </main>
  
  <style>
    .error {
      color: red;
    }
  </style>