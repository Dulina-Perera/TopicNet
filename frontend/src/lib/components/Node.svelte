<script lang="ts">
	import { Editor } from "@tiptap/core";
	import { onDestroy, onMount } from "svelte";
	import { marked } from "marked";
	import Document from "@tiptap/extension-document";
	import BulletList from "@tiptap/extension-bullet-list";
	import ListItem from "@tiptap/extension-list-item";
	import Heading from "@tiptap/extension-heading";
	import Paragraph from "@tiptap/extension-paragraph";
	import Text from "@tiptap/extension-text";

	export let content: string;

	let element: HTMLDivElement | undefined;
	let editor: Editor | undefined;

	onMount(() => {
		editor = new Editor({
			element: element,
			content: marked.parse(content),
			extensions: [
				BulletList,
				Document,
				Heading.configure({
					levels: [1, 2, 3]
				}),
				ListItem,
				Paragraph,
				Text,
			],
			injectCSS: false,
			autofocus: true,
			editable: true,
		});
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();
		}
	});
</script>

<div
	class="bg-white pb-4 pt-4 px-4 w-72"
	style="border-radius: var(--theme-rounded-container);"
	bind:this={element}
/>
