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
	import { boardDraggable } from '$lib/stores/workspace.store';
	import { onDestroy, onMount } from 'svelte';
	import { marked } from 'marked';

	export let content: string;
	export let customStyles: string = '';

	$: isDraggable = !$boardDraggable;

	let wrapper_element: HTMLDivElement;
	let element: HTMLDivElement;
	let editor: Editor;

	let isDragging: boolean = false;
	let offsetX: number = 0;
	let offsetY: number = 0;
	let isEditable: boolean = false;

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
	});

	const handleDoubleClick = () => {
		if (isDraggable && editor) {
			editor.commands.focus();
			editor.setEditable(true);
			isEditable = true;
		}
	};

	const handleMouseDown = (event: MouseEvent) => {
		if (isDraggable) {
			isDragging = true;
			offsetX = event.clientX - (wrapper_element?.offsetLeft || 0);
			offsetY = event.clientY - (wrapper_element?.offsetTop || 0);
		}
	};

	const handleMouseMove = (event: MouseEvent) => {
		if (isDragging && element) {
			wrapper_element.style.position = 'absolute';
			wrapper_element.style.left = `${event.clientX - offsetX}px`;
			wrapper_element.style.top = `${event.clientY - offsetY}px`;
		}
	};

	const handleMouseUp = () => {
		isDragging = false;
	};

	const handleOutsideClick = (event: MouseEvent) => {
		if (editor && editor.isEditable && element && !element.contains(event.target as Node)) {
			editor.setEditable(false);
			isEditable = false;
		}
	};

	const handleWheel = (event: WheelEvent) => {
		event.stopPropagation();
	};
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	style={customStyles}
	id="node-wrapper"
	bind:this={wrapper_element}
	on:dblclick={handleDoubleClick}
	on:mousedown={handleMouseDown}
	on:mousemove={handleMouseMove}
	on:mouseup={handleMouseUp}
	on:wheel={handleWheel}
>
	<div
		id="node"
		class="{isEditable ? 'editable' : ''} {boardDraggable ? 'disable-select' : ''}"
		bind:this={element}
	></div>

	<div id="button-container">
		<button><i class="ri-arrow-down-wide-fill"></i></button>
		<button><i class="ri-delete-bin-7-line"></i></button>
	</div>
</div>

<style lang="scss">
	#node-wrapper {
		position: relative;

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

			&.disable-select {
				user-select: none;
			}

			&.editable {
				cursor: text !important;
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

		#button-container {
			bottom: 0.5rem;
			right: 0.5rem;
			display: flex;
			gap: 0.5rem;
			position: absolute;

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
