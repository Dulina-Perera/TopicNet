<script lang="ts">
	import type { Writable } from 'svelte/store';
	import { Board, Spinner, Node, Toggle } from '$lib/components/workspace';
	import { Header } from '$lib/components/header';
	import { Nav, NavLogo } from '$lib/components/header/nav';
	import { NavActions, NavLogin } from '$lib/components/header/nav/actions';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { writable } from 'svelte/store';

	let loading: Writable<boolean> = writable(true);
	let content: Writable<string> = writable('');

	let file: File | null = null;
	$: {
		const pageState = $page?.state as { file: File };
		if (pageState) {
			file = pageState.file;
		}
	}

	const processFile: (file: File) => void = async (file) => {
		const formData: FormData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch('http://localhost:5000/api/v1/summarize', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				const responseData: any = await response.json();
				content.set(responseData.content);
			} else {
				console.error('Failed to process file:', response.statusText);
			}
		} catch (error) {
			console.error(error);
		} finally {
			loading.set(false);
		}
	};

	onMount(async () => {
		if (file) {
			await processFile(file);
		}
	});
</script>

<Header>
	<Nav>
		<NavLogo />
		<NavActions>
			<Toggle />
			<NavLogin />
		</NavActions>
	</Nav>
</Header>

<Board />

{#if $loading}
	<Spinner />
{:else}
	<Node content={$content} customStyles="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);" />
{/if}
