<script lang="ts">
	import "../app.css";

	import Login from "$lib/components/Login.svelte";
	import Navbar from "$lib/components/Navbar.svelte";
	import Search from "$lib/components/Search.svelte";
	import Hero from "$lib/components/Hero.svelte";
</script>

<div class="flex flex-col min-h-screen">
	<Navbar />
	<Search />
	<Login />
	<Hero />
	<slot />
</div>
