<script lang="ts">
	import { Tree } from '$lib/components/workspace';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';

	export let data: { user: { id: string; username: string; isPermanent: boolean } | null };
</script>

<div id="container">
	<Header>
		<Logo />
		<NavActions>
			<LoginButton user={data.user} />
		</NavActions>
	</Header>
	<Tree />
</div>

<style lang="scss">
	#container {
		position: relative;
	}
</style>
