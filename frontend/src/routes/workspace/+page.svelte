<script lang="ts">
	import type { Writable } from 'svelte/store';
	import { Header, Logo } from '$lib/components';
	import { LoginButton } from '$lib/components/login';
	import { NavActions } from '$lib/components/nav';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	import { Board, Spinner, Node, Toggle } from '$lib/components/workspace';
	import { writable } from 'svelte/store';

	let loading: Writable<boolean> = writable(true);
	let content: Writable<string> = writable(`
# Understanding Cognitive Analytics: Enhancing Decision-Making with Human-Like Intelligence

Cognitive analytics leverages advanced technologies to uncover patterns and connections in data that traditional analytics cannot. By integrating artificial intelligence, machine learning, deep learning, and natural language processing, cognitive analytics mimics human-like intelligence, enabling it to tackle complex problems that fixed programming instructions cannot solve.

Cognitive systems continuously improve through self-learning from interactions with data and users, allowing them to analyze large datasets and provide structured insights from unstructured data. These systems can generate hypotheses from diverse data sources, offering real-time answers and insights that can create a competitive advantage for businesses.

Organizations can utilize cognitive analytics to monitor customer behavior and emerging trends, facilitating predictive analytics that inform future strategies and enhance performance. The adaptive nature of cognitive computing allows it to evolve alongside changing information and requirements, making it a powerful tool for decision-making.

Cognitive systems must be interactive, enabling users to define their needs easily and integrate with various data sources and devices. They
`);

	// let file: File | null = null;
	// $: {
	// 	const pageState = $page?.state as { file: File };
	// 	if (pageState) {
	// 		file = pageState.file;
	// 	}
	// }

	// const processFile: (file: File) => void = async (file) => {
	// 	const formData: FormData = new FormData();
	// 	formData.append('file', file);

	// 	try {
	// 		const response = await fetch('http://localhost:5000/api/v1/summarize', {
	// 			method: 'POST',
	// 			body: formData
	// 		});

	// 		if (response.ok) {
	// 			const responseData: any = await response.json();
	// 			content.set(responseData.summary);
	// 		} else {
	// 			console.error('Failed to process file:', response.statusText);
	// 		}
	// 	} catch (error) {
	// 		console.error(error);
	// 	} finally {
	// 		loading.set(false);
	// 	}
	// };

	// onMount(async () => {
	// 	if (file) {
	// 		await processFile(file);
	// 	}
	// });
</script>

<Header>
	<Logo />
	<NavActions>
		<Toggle />
		<LoginButton />
	</NavActions>
</Header>

<Board />

<!-- {#if $loading}
	<Spinner />
{:else} -->
<Node
	content={$content}
	customStyles="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);"
/>
<!-- {/if} -->
