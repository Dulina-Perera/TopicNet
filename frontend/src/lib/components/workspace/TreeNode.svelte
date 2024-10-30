<script lang="ts">
	import Node from './Node.svelte';
	import { type Writable } from 'svelte/store';

	export let nodes: Writable<App.Node[]>;
	export let treeNode: TreeNode;
	export let isRoot: boolean = false;

	type TreeNode = App.Node & { children?: TreeNode[] };

	function treeNodeToNode(treeNode: TreeNode): App.Node {
		const { children, ...node } = treeNode;
		return node;
	}
</script>

<!-- Each node is wrapped in an <li> -->
<li id={`node-${treeNode.id}`} class="tree-node" class:is-root={isRoot}>
	<div class="node-content">
		<Node node={treeNodeToNode(treeNode)} {nodes} />
	</div>

	{#if treeNode.children && treeNode.children.length > 0}
		<ul class="child-nodes">
			{#each treeNode.children as childNode, index}
				<svelte:self treeNode={childNode} isRoot={false} />
			{/each}
		</ul>
	{/if}
</li>

<style lang="scss">
	.tree-node {
		align-items: center;
		display: inline-flex;
		flex-direction: column;
		list-style-type: none;
		min-width: 100px;
		padding: 10px 20px;
		position: relative;
		transition: all 0.4s;

		&::after,
		&::before {
			border-top: 4px solid var(--theme-border-color);
			content: '';
			position: absolute;
			width: 50%;
			top: 0;
		}

		&::before {
			right: 50%;
		}

		&::after {
			left: 50%;
		}

		&:first-child::before,
		&:last-child::after {
			border-top: none;
		}

		.child-nodes {
			display: flex;
			justify-content: center;
			margin-top: 10px;
			position: relative;
			padding-top: 10px;

			&::before {
				border-left: 4px solid var(--theme-border-color);
				content: '';
				height: 20px;
				left: 50%;
				position: absolute;
				top: -10px;
				transform: translateX(-50%);
				width: 0;
			}
		}
	}
</style>
