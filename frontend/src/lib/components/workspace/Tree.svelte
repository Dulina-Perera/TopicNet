<script lang="ts">
	import Node from './Node.svelte';
	import { onMount } from 'svelte';

	export let nodeData: any;

	let rootNode = nodeData.find((node: { parent_id: null }) => node.parent_id === null);
	let childNodes = nodeData.filter((node: { parent_id: any }) => node.parent_id === rootNode?.id);

	function centerHorizontalScroll(node: HTMLElement) {
		onMount(() => {
			const hasHorizontalOverflow = node.scrollWidth > node.clientWidth;
			if (hasHorizontalOverflow) {
				node.scrollLeft = (node.scrollWidth - node.clientWidth) / 2;
			}
		});
	}
</script>

<!-- Apply the action to #scroll-wrapper -->
<div id="scroll-wrapper" use:centerHorizontalScroll>
	<div id="tree">
		{#if rootNode}
			<ul>
				<li id={`node-${rootNode.id}`}>
					<Node content={rootNode.topic_and_content} />

					{#if childNodes.length > 0}
						<ul>
							{#each childNodes as childNode}
								<li id={`node-${childNode.id}`}>
									<Node content={childNode.topic_and_content} />
								</li>
							{/each}
						</ul>
					{/if}
				</li>
			</ul>
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
		}
	}
</style>
