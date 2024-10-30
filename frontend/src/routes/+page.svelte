<script lang="ts">
	import Hero from '$lib/components/Hero.svelte';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';
	import { NavMenu, NavMenuToggle } from '$lib/components/nav/menu';

	export let data: { user: { id: string; username: string; isPermanent: boolean } | null };
	console.log(data);
</script>

<Header>
	<Logo />
	<NavMenu />
	<NavActions>
		<LoginButton user={data.user} />
		<NavMenuToggle />
	</NavActions>
</Header>
<Hero />
