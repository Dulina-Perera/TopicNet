<script lang="ts">
	import Node from './Node.svelte';

	export let treeNode: TreeNode;

	type TreeNode = App.Node & { children?: TreeNode[] };

	function treeNodeToNode(treeNode: TreeNode): App.Node {
		const { children, ...node } = treeNode;
		return node;
	}
</script>

{#if treeNode && treeNode.id == 0}
	<ul>
		<li id={`node-${treeNode.id}`}>
			<Node node={treeNodeToNode(treeNode)} />
		</li>
		{#if treeNode.children && treeNode.children.length > 0}
			<ul>
				{#each treeNode.children as childNode}
					<svelte:self treeNode={childNode} />
				{/each}
			</ul>
		{/if}
	</ul>
{:else}
	<li id={`node-${treeNode.id}`}>
		<Node node={treeNodeToNode(treeNode)} />
	</li>
	{#if treeNode.children && treeNode.children.length > 0}
		<ul>
			{#each treeNode.children as childNode}
				<svelte:self treeNode={childNode} />
			{/each}
		</ul>
	{/if}
{/if}

<style lang="scss">
	ul {
		display: flex;
		flex-wrap: nowrap;
		justify-content: center;
		padding-top: 20px;
		position: relative;
		transition: all 0.4s;

		&:not(:first-of-type)::before {
			border-left: 4px solid var(--theme-border-color);
			content: '';
			height: 20px;
			left: 50%;
			position: absolute;
			top: 0;
			width: 0;
		}
	}

	li {
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

		ul::before {
			border-left: 4px solid var(--theme-border-color);
			content: '';
			height: 20px;
			left: 50%;
			position: absolute;
			top: 0;
			width: 0;
		}

		&:first-child::before,
		&:last-child::after {
			border-top: none;
		}
	}
</style>
