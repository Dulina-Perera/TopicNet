<script lang="ts">
    import Contact from '$lib/components/Contact.svelte';
    import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';
	import { NavMenu, NavMenuToggle } from '$lib/components/nav/menu';
</script>

<Header>
	<Logo />
	<NavMenu />
	<NavActions>
		<LoginButton />
		<NavMenuToggle />
	</NavActions>
</Header>

<Contact />