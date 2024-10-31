<script lang="ts">
	import type { PageData } from './$types';
	import { Explorer, Header, Logo } from '$lib/components';
	import { NavActions } from '$lib/components/nav';
	import { ProfileDropdown } from '$lib/components/profile';
	import { Tree } from '$lib/components/workspace';
	import { type Writable, writable } from 'svelte/store';

	export let data: PageData;

	const nodes: Writable<App.Node[]> = writable(data.nodes);
</script>

<div id="container">
	<Header>
		<Logo />
		<NavActions>
			<!-- Access data.user directly instead of userMetadata -->
			<ProfileDropdown user={data?.user} />
		</NavActions>
	</Header>
	<Tree {nodes} />
</div>
<Explorer />

<style lang="scss">
	#container {
		position: relative;
	}
</style>
