<script lang="ts">
	import { Tree } from '$lib/components/workspace';
	import { Header, Logo } from '$lib/components';
	import { NavActions } from '$lib/components/nav';
	import { ProfileDropdown } from '$lib/components/profile';

	export let data: { user: { id: string; username: string; isPermanent: boolean } | null };
</script>

<div id="container">
	<Header>
		<Logo />
		<NavActions>
			<ProfileDropdown user={data.user} />
		</NavActions>
	</Header>
	<Tree />
</div>

<style lang="scss">
	#container {
		position: relative;
	}
</style>
