<script lang="ts">
	import Hero from '$lib/components/Hero.svelte';
	import { Header, Logo } from '$lib/components';
	import { NavActions } from '$lib/components/nav';
	import { NavMenu, NavMenuToggle } from '$lib/components/nav/menu';
	import { ProfileDropdown } from '$lib/components/profile';

	export let data: { user: { id: string; username: string; isPermanent: boolean } | null };
</script>

<Header>
	<Logo />
	<NavMenu />
	<NavActions>
		<ProfileDropdown user={data.user} />
		<NavMenuToggle />
	</NavActions>
</Header>
<Hero />
