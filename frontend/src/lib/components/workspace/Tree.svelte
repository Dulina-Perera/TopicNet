<script lang="ts">
	import { onMount } from 'svelte';

	// Action to center horizontal scroll on mount
	function centerHorizontalScroll(node: HTMLElement) {
		onMount(() => {
			// Check if content overflows horizontally
			const hasHorizontalOverflow = node.scrollWidth > node.clientWidth;
			if (hasHorizontalOverflow) {
				// Center horizontal scroll position
				node.scrollLeft = (node.scrollWidth - node.clientWidth) / 2;
			}
		});
	}
</script>

<!-- Apply the action to #scroll-wrapper -->
<div id="scroll-wrapper" use:centerHorizontalScroll>
	<div id="tree">
		<slot />
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
	}

	#tree {
		align-items: center;
		display: flex;
		width: max-content;
	}
</style>
