<script>
	import Hero from "$lib/components/Hero.svelte";
	import { Header } from "$lib/components/header";
	import { Nav, NavLogo, NavMenu } from "$lib/components/header/nav";
	import { NavActions, NavLogin, NavToggle } from "$lib/components/header/nav/actions";
</script>

<Header>
	<Nav>
		<NavLogo />
		<NavMenu />
		<NavActions>
			<NavLogin />
			<NavToggle />
		</NavActions>
	</Nav>
</Header>
<Hero />
