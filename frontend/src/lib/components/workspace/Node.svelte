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
	import Toolbar from './Toolbar.svelte';
	import TurndownService from 'turndown';
	import pkg from 'lodash';
	import { Editor } from '@tiptap/core';
	import { boardDraggable } from '$lib/stores/workspace.store';
	import { get } from 'svelte/store';
	import { marked } from 'marked';
	import { onDestroy, onMount } from 'svelte';
	import { type Writable } from 'svelte/store';

	const { debounce } = pkg;

	// Props
	export let node: App.Node;
	export let nodes: Writable<App.Node[]>;
	export let customStyles: string = '';

	// Stores
	$: isDraggable = !$boardDraggable;

	// Variables
	let wrapper_element: HTMLDivElement;
	let element: HTMLDivElement;
	let editor: Editor;

	let isDragging: boolean = false;
	let offsetX: number = 0;
	let offsetY: number = 0;
	let isEditable: boolean = false;

	const turndownService: TurndownService = new TurndownService();

	let toolbarProps: { top: number; left: number; visible: boolean } = {
		top: 0,
		left: 0,
		visible: false
	};

	// Lifecycle methods
	onMount(() => {
		editor = new Editor({
			element: element,
			content: marked.parse(node.topic_and_content), // Convert markdown to HTML.
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

		editor.on(
			'update',
			debounce(async () => {
				const html_content: string = editor.getHTML();
				const markdown_content: string = turndownService.turndown(html_content);

				if (markdown_content !== node.topic_and_content) {
					const response: Response = await fetch(
						`http://localhost:5000/api/v1/update/node?document_id=${node.document_id}&node_id=${node.id}`,
						{
							method: 'PUT',
							headers: {
								'Content-Type': 'application/json'
							},
							body: JSON.stringify({ content: markdown_content })
						}
					);
				}
			}, 1000)
		);

		document.addEventListener('mousedown', handleOutsideClick);
		document.addEventListener('selectionchange', handleSelectionChange);
	});

	onDestroy(() => {
		if (editor) {
			editor.destroy();

			document.removeEventListener('mousedown', handleOutsideClick);
			document.removeEventListener('selectionchange', handleSelectionChange);
		}
	});

	// Event handlers
	const handleMouseDown: (event: MouseEvent) => void = (event: MouseEvent) => {
		if (isEditable) {
			toolbarProps.visible = false;
		}
	};

	const handleDoubleClick: () => void = () => {
		if (!isEditable) {
			editor.commands.focus();
			editor.setEditable(true);
			isEditable = true;
		}
		updateToolbarPosition();
	};

	const handleOutsideClick: (event: MouseEvent) => void = (event: MouseEvent) => {
		if (isEditable && element && !element.contains(event.target as Node)) {
			editor.setEditable(false);
			isEditable = false;

			toolbarProps.visible = false;
		}
	};

	function handleSelectionChange() {
		const selection: Selection | null = document.getSelection();

		if (selection && selection.rangeCount > 0 && selection.toString().length > 0 && isEditable) {
			updateToolbarPosition();
		} else {
			toolbarProps.visible = false;
		}
	}

	// Functions
	const updateToolbarPosition: () => void = () => {
		const selection: Selection | null = document.getSelection();
		if (selection && selection.rangeCount > 0) {
			const range: Range = selection.getRangeAt(0);
			const rect: DOMRect = range.getBoundingClientRect();
			const parentRect: DOMRect = wrapper_element.getBoundingClientRect();

			// Calculate top position within bounds
			const toolbarTop: number = rect.top - parentRect.top - 50;
			const clampedTop = Math.max(0, Math.min(toolbarTop, wrapper_element.offsetHeight - 50));

			toolbarProps = {
				top: clampedTop,
				left: rect.left - parentRect.left,
				visible: true
			};
		} else {
			toolbarProps.visible = false;
		}
	};

	async function extendNode() {
		// Check if the node has child nodes.
		const childNodes: App.Node[] = get(nodes).filter((n) => n.parent_id === node.id);
		const hasChildNodes: boolean = childNodes.length > 0;

		// If the node has child nodes, do nothing.
		if (hasChildNodes) return;

		// Else, create child nodes for the node.
		const response: Response = await fetch(
			`http://localhost:5000/api/v1/generate/extend?document_id=${node.document_id}&node_id=${node.id}`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);

		// If the request is successful, update the nodes store.
		if (response.ok) {
			const newNodes: App.Node[] = await response.json();
			nodes.update((n) => [...n, ...newNodes]);
		} else {
			console.error('Failed to extend node.');
		}
	}

	async function destroyDescendantNodes() {
		console.log($nodes);
		// Check if the node has child nodes.
		const childNodes: App.Node[] = get(nodes).filter((n) => n.parent_id === node.id);
		const hasChildNodes: boolean = childNodes.length > 0;

		// If the node has no child nodes, do nothing.
		if (!hasChildNodes) return;

		// Else, destroy the child nodes of the node.
		const response: Response = await fetch(
			`http://localhost:5000/api/v1/destroy?document_id=${node.document_id}&node_id=${node.id}`,
			{
				method: 'DELETE'
			}
		);

		// If the request is successful, update the nodes store.
		if (response.ok) {
			const destroyedNodeIds: number[] = await response.json();
			nodes.update((n) => n.filter((node) => !destroyedNodeIds.includes(node.id)));
		} else {
			console.error('Failed to destroy descendant nodes.');
		}
	}
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	style={customStyles}
	id="node-wrapper"
	bind:this={wrapper_element}
	on:dblclick={handleDoubleClick}
	on:mousedown={handleMouseDown}
>
	{#if isEditable && toolbarProps.visible}
		<Toolbar {editor} content={node.topic_and_content} customStyles={toolbarProps} />
	{/if}

	<div
		id="node"
		class="{isEditable ? 'editable' : ''} {boardDraggable ? 'disable-select' : ''}"
		bind:this={element}
	></div>

	<div id="button-container">
		<button on:click={extendNode}><i class="ri-arrow-down-wide-fill"></i></button>
		<button on:click={destroyDescendantNodes}><i class="ri-delete-bin-7-line"></i></button>
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
				display: none;
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
			#node::-webkit-scrollbar {
				display: block;
			}

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

	:global(.tiptap h1) {
		font-size: 1.125rem;
		color: var(--theme-title-color);
	}

	:global(.tiptap h2) {
		font-size: 1rem;
		color: var(--theme-title-color);
	}

	:global(.tiptap h3) {
		font-size: 0.875rem;
		color: var(--theme-title-color);
	}

	:global(.tiptap p) {
		color: var(--theme-title-color);
		display: inline;
	}

	:global(.tiptap ol) {
		color: var(--theme-title-color);
		list-style-position: inside;
		list-style-type: decimal;
	}

	:global(.tiptap ul) {
		color: var(--theme-title-color);
		list-style-position: inside;
		list-style-type: disc;
	}
</style>
