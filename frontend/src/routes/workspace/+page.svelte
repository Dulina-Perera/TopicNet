<script>
	import { Board } from "$lib/components/workspace";
	import { Header } from "$lib/components/header";
	import { Nav, NavLogo } from "$lib/components/header/nav";
	import { NavActions, NavLogin } from "$lib/components/header/nav/actions";
</script>

<Header>
	<Nav>
		<NavLogo />
		<NavActions>
			<NavLogin />
		</NavActions>
	</Nav>
</Header>
<Board />
