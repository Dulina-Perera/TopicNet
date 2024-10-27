<script lang="ts">
	import Node from './Node.svelte';
	import { type Writable, writable } from 'svelte/store';

	let content: Writable<string> = writable(`
# Understanding Cognitive Analytics: Enhancing Decision-Making with Human-Like Intelligence

Cognitive analytics leverages advanced technologies to uncover patterns and connections in data that traditional analytics cannot. By integrating artificial intelligence, machine learning, deep learning, and natural language processing, cognitive analytics mimics human-like intelligence, enabling it to tackle complex problems that fixed programming instructions cannot solve.

Cognitive systems continuously improve through self-learning from interactions with data and users, allowing them to analyze large datasets and provide structured insights from unstructured data. These systems can generate hypotheses from diverse data sources, offering real-time answers and insights that can create a competitive advantage for businesses.

Organizations can utilize cognitive analytics to monitor customer behavior and emerging trends, facilitating predictive analytics that inform future strategies and enhance performance. The adaptive nature of cognitive computing allows it to evolve alongside changing information and requirements, making it a powerful tool for decision-making.

Cognitive systems must be interactive, enabling users to define their needs easily and integrate with various data sources and devices.
`);
</script>

<div id="tree-container">
	<div id="tree">
		<slot />
	</div>
</div>

<style lang="scss">
	#tree-container {
		align-items: center;
		display: flex;
		height: 100vh;
		justify-content: center;
		position: relative;
		width: 100vw;
	}
</style>
