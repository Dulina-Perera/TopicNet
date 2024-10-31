<script lang="ts">
	import Hero from '$lib/components/Hero.svelte';
	import { About, Contact, Explorer, Featured, Header, Logo, Services } from '$lib/components';
	import { NavActions } from '$lib/components/nav';
	import { NavMenu, NavMenuToggle } from '$lib/components/nav/menu';
	import { ProfileDropdown } from '$lib/components/profile';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	export let data: { user: { id: string; username: string; isPermanent: boolean } | null };

	onMount(() => {
		const loggedOut = $page.url.searchParams.get('loggedOut');
		if (loggedOut) {
			console.log(loggedOut);
			const url = new URL(window.location.href);
			url.searchParams.delete('loggedOut');
			window.history.replaceState({}, document.title, url);
			window.location.reload();
		}
	});
</script>

<Header>
	<Logo />
	<NavMenu />
	<NavActions>
		<ProfileDropdown user={data?.user} />
		<NavMenuToggle />
	</NavActions>
</Header>
<Hero />
<About />
<Services />
<Featured />
{#if data.user}
	<Explorer />
{/if}
