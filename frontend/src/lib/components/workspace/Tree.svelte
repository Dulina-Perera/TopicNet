<script lang="ts">
	import TreeNode from './TreeNode.svelte';
	import { derived, type Readable } from 'svelte/store';
	import { onMount } from 'svelte';
	import { type Writable } from 'svelte/store';

	export let nodes: Writable<App.Node[]>;

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
			<ul>
				<TreeNode {nodes} treeNode={$treeData} isRoot={true} />
			</ul>
		{/if}
	</div>
</div>

<style lang="scss">
	#scroll-wrapper {
		align-items: start;
		display: flex;
		height: 100vh;
		justify-content: start;
		left: 0;
		overflow-x: auto;
		position: absolute;
		top: 5rem;

		#tree {
			align-items: center;
			display: flex;
			justify-content: center;
		}
	}
</style>
