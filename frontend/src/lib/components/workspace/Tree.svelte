<script lang="ts">
	import TreeNode from './TreeNode.svelte';
	import { derived, type Readable } from 'svelte/store';
	import { nodes } from '$lib/stores/workspace.store';
	import { onMount } from 'svelte';

	type TreeNode = App.Node & { children?: TreeNode[] };

	const treeData: Readable<TreeNode | null> = derived(nodes, ($nodes: App.Node[]) => {
		function buildTree(parentId: number | null): TreeNode[] {
			return $nodes
				.filter((node) => node.parent_id === parentId)
				.map((node) => ({
					...node,
					children: buildTree(node.id)
				}));
		}

		const rootNode = $nodes.find((node) => node.parent_id === null);

		return rootNode ? { ...rootNode, children: buildTree(rootNode.id) } : null;
	});

	function centerHorizontalScroll(node: HTMLElement) {
		onMount(() => {
			const hasHorizontalOverflow = node.scrollWidth > node.clientWidth;
			if (hasHorizontalOverflow) {
				node.scrollLeft = (node.scrollWidth - node.clientWidth) / 2;
			}
		});
	}
</script>

<div id="scroll-wrapper" use:centerHorizontalScroll>
	<div id="tree">
		{#if $treeData}
			<TreeNode treeNode={$treeData} />
		{/if}
	</div>
</div>

<style lang="scss">
	#scroll-wrapper {
		align-items: center;
		display: flex;
		height: 100vh;
		justify-content: center;
		overflow-x: auto; /* Allow horizontal scroll if needed */
		width: 100vw;

		#tree {
			align-items: center;
			display: flex;
			width: max-content;
		}
	}
</style>
