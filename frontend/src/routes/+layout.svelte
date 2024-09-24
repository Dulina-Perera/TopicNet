<script lang="ts">
	import "../app.css";
	import Navbar from "$lib/components/Navbar.svelte";
	import Search from "$lib/components/Search.svelte";
</script>

<div class="flex flex-col min-h-screen">
	<Navbar />
	<Search />
	<slot />
</div>
