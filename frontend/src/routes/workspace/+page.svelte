<script lang="ts">
	import { Tree } from '$lib/components/workspace';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';
</script>

<Header>
	<Logo />
	<NavActions>
		<LoginButton />
	</NavActions>
</Header>
<Tree />

<style lang="scss">

</style>
