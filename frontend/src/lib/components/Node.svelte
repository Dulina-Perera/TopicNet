<script lang="ts">
	import BulletList from "@tiptap/extension-bullet-list";
	import Document from "@tiptap/extension-document";
	import Heading from "@tiptap/extension-heading";
	import ListItem from "@tiptap/extension-list-item";
	import Paragraph from "@tiptap/extension-paragraph";
	import Text from "@tiptap/extension-text";
	import { Editor } from "@tiptap/core";
	import { onDestroy, onMount } from "svelte";
	import { marked } from "marked";

	export let nodeContent: string;

	let element: HTMLDivElement | undefined;
	let editor: Editor | undefined;
	let isDragging: boolean = false;
	let offsetX: number = 0;
	let offsetY: number = 0;

	onMount(() => {
		editor = new Editor({
			element: element,
			content: marked.parse(nodeContent),
			extensions: [
				BulletList,
				Document,
				Heading.configure({
					levels: [1, 2, 3],
				}),
				ListItem,
				Paragraph,
				Text,
			],
			injectCSS: false,
			autofocus: false,
			editable: false,
		});

		document.addEventListener("mousedown", handleOutsideClick);
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();
		}

		if (typeof document !== "undefined") {
			document.removeEventListener("mousedown", handleOutsideClick);
		}
	});

	const handleDoubleClick = () => {
		if (editor) {
			editor.commands.focus();
			editor.setEditable(true);
		}
	};

	const handleMouseDown = (event: MouseEvent) => {
		isDragging = true;
		offsetX = event.clientX - (element?.offsetLeft || 0);
		offsetY = event.clientY - (element?.offsetTop || 0);
	};

	const handleMouseMove = (event: MouseEvent) => {
		if (isDragging && element) {
			element.style.position = "absolute";
			element.style.left = `${event.clientX - offsetX}px`;
			element.style.top = `${event.clientY - offsetY}px`;
		}
	};

	const handleMouseUp = () => {
		isDragging = false;
	};

	const handleOutsideClick = (event: MouseEvent) => {
		if (editor && editor.isEditable && element && !element.contains(event.target as Node)) {
			editor.setEditable(false);
		}
	};
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	class="bg-white pb-4 pt-4 px-4 w-72"
	style="border-radius: var(--theme-rounded-container);"
	bind:this={element}
	on:dblclick={handleDoubleClick}
	on:mousedown={handleMouseDown}
	on:mousemove={handleMouseMove}
	on:mouseup={handleMouseUp}
/>

<style>
	div {
		cursor: grab; /* Visual cue for draggable div */
	}

	div:active {
		cursor: grabbing; /* Visual cue when dragging */
	}
</style>
