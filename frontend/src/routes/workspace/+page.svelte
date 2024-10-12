<script lang="ts">
	import Board from "$lib/components/Board.svelte";
	import Node from "$lib/components/Node.svelte";
	// import Toolbar from "$lib/components/Toolbar.svelte";

	let content = `
# Welcome to TopicNet
## The interactive way to visualize unstructured text documents
### Why should you use TopicNet?
- **Interactive**: Visualize your text data in a way that is easy to understand
- **Customizable**: Choose from a variety of layouts and themes to suit your needs
- **Collaborative**: Share your work with others and work together in real-time
- **Open-source**: Contribute to the project and make it better for everyone
<br>
	`
</script>

<!-- <Board /> -->
<Node nodeContent={content} />
<!-- <Toolbar /> -->
