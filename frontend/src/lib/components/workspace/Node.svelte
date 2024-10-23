<script lang="ts">
	import Bold from '@tiptap/extension-bold';
	import BulletList from '@tiptap/extension-bullet-list';
	import Document from '@tiptap/extension-document';
	import Heading from '@tiptap/extension-heading';
	import Italic from '@tiptap/extension-italic';
	import Link from '@tiptap/extension-link';
	import ListItem from '@tiptap/extension-list-item';
	import OrderedList from '@tiptap/extension-ordered-list';
	import Paragraph from '@tiptap/extension-paragraph';
	import Text from '@tiptap/extension-text';
	import { Editor } from '@tiptap/core';
	import { onDestroy, onMount } from 'svelte';
	import { marked } from 'marked';

	export let content: string;
	export let customStyles: string = '';

	let editor: Editor | undefined;
	let element: HTMLDivElement | undefined;

	let isDragging: boolean = false;
	let offsetX: number = 0;
	let offsetY: number = 0;

	onMount(() => {
		editor = new Editor({
			element: element,
			content: marked.parse(content), // Convert markdown to HTML.
			extensions: [
				Bold,
				BulletList,
				Document,
				Heading.configure({
					levels: [1, 2, 3]
				}),
				Italic,
				Link.configure({
					autolink: true,
					defaultProtocol: 'https',
					openOnClick: true
				}),
				ListItem,
				OrderedList,
				Paragraph,
				Text
			],
			injectCSS: false
		});

		document.addEventListener('mousedown', handleOutsideClick);
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();
		}

		if (typeof document !== 'undefined') {
			document.removeEventListener('mousedown', handleOutsideClick);
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
			element.style.position = 'absolute';
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
	style={customStyles}
	id="node"
	bind:this={element}
	on:dblclick={handleDoubleClick}
	on:mousedown={handleMouseDown}
	on:mousemove={handleMouseMove}
	on:mouseup={handleMouseUp}
>
	<div id="button-container">
		<button><i class="ri-arrow-down-wide-fill"></i></button>
		<button><i class="ri-delete-bin-7-line"></i></button>
	</div>
</div>

<style lang="scss">
	#node {
		background-color: var(--theme-body-color);
		border-radius: var(--theme-border-radius-container);
		box-shadow: 0 2px 16px hsla(230, 75%, 32%, 0.15);
		cursor: grab;
		font-size: 0.875rem;
		line-height: 1.5rem;
		max-height: 16rem;
		overflow-y: auto;
		padding: 0.5rem;
		width: 16rem;
		position: relative;

		&::-webkit-scrollbar {
			width: 6px;
		}
		&::-webkit-scrollbar-track {
			background: transparent;
		}
		&::-webkit-scrollbar-thumb {
			background-color: var(--theme-title-color);
			border-radius: 10px;
		}
		&::-webkit-scrollbar-thumb:hover {
			background-color: var(--theme-primary-color);
		}

		#button-container {
			bottom: 0.5rem;
			display: flex;
			gap: 0.5rem;
			position: fixed;
			right: 0.5rem;

			button {
				background-color: var(--theme-title-color);
				border: none;
				border-radius: 50%;
				color: #fff;
				cursor: pointer;
				display: none;
				font-size: 0.875rem;
				font-weight: 800;
				padding: 0.3rem 0.6rem;

				&:hover {
					background-color: var(--theme-primary-color);
				}
			}
		}

		&:active {
			cursor: grabbing;
		}

		&:hover {
			#button-container button {
				display: block;
			}
		}
	}

	:global(h1) {
		font-size: 1.125rem;
		color: var(--theme-title-color);
	}

	:global(h2) {
		font-size: 1rem;
		color: var(--theme-title-color);
	}

	:global(h3) {
		font-size: 0.875rem;
		color: var(--theme-title-color);
	}

	:global(p) {
		color: var(--theme-title-color);
		display: inline;
	}

	:global(ol) {
		color: var(--theme-title-color);
		list-style-position: inside;
		list-style-type: decimal;
	}

	:global(ul) {
		color: var(--theme-title-color);
		list-style-position: inside;
		list-style-type: disc;
	}
</style>
