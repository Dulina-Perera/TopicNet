<script lang="ts">
	import { Tree } from '$lib/components/workspace';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';
</script>

<div id="container">
	<Header>
		<Logo />
		<NavActions>
			<LoginButton />
		</NavActions>
	</Header>
	<Tree />
</div>

<style lang="scss">
	#container {
		position: relative;
	}
</style>
