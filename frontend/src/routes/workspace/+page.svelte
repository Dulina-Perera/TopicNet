<script lang="ts">
	import { Tree } from '$lib/components/workspace';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';
	import { nodes } from '$lib/stores/workspace.store';

	let nodeData: any = [];
	nodes.subscribe((value) => {
		nodeData = value;
	});
</script>

<Header>
	<Logo />
	<NavActions>
		<LoginButton />
	</NavActions>
</Header>
<Tree {nodeData} />

<style lang="scss">

</style>
