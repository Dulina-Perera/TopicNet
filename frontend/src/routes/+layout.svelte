<script lang="ts">
	import "../app.css";
	import Navbar from "$lib/components/Navbar.svelte";
	import Search from "$lib/components/Search.svelte";
	import Login from "$lib/components/Login.svelte";
</script>

<div class="flex flex-col min-h-screen">
	<Navbar />
	<Search />
	<Login />
	<slot />
</div>
