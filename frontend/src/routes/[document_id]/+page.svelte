<script lang="ts">
	import { Header, Logo } from '$lib/components';
	import { NavActions } from '$lib/components/nav';
	import type { PageData } from './$types';
	import { ProfileDropdown } from '$lib/components/profile';
	import { Tree } from '$lib/components/workspace';
	import { type Writable, writable } from 'svelte/store';

	export let data: PageData;
	export let userMetadata: { user: { id: string; username: string; isPermanent: boolean } | null };

	const nodes: Writable<App.Node[]> = writable(data.nodes);
</script>

<div id="container">
	<Header>
		<Logo />
		<NavActions>
			<ProfileDropdown user={userMetadata?.user} />
		</NavActions>
	</Header>
	<Tree {nodes} />
</div>

<style lang="scss">
	#container {
		position: relative;
	}
</style>
