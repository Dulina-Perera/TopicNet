<script lang="ts">
	import { Editor } from '@tiptap/core';

	export let editor: Editor | null;

	export let customStyles: { top: number; left: number; visible: boolean } = {
		top: 0,
		left: 0,
		visible: false
	};
</script>

{#if editor && customStyles.visible}
	<div
		style="left: {customStyles.left}px; top: {customStyles.top}px; position: absolute;"
		id="toolbar-wrapper"
	>
		<div id="toolbar">
			<!-- Bold Button -->
			<button
				style={editor.isActive('bold')
					? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
					: 'color: var(--theme-title-color);'}
				class="toolbar-button"
				on:click={() => editor.chain().focus().toggleBold().run()}
			>
				<i class="ri-bold"></i>
			</button>

			<!-- Italic Button -->
			<button
				style={editor.isActive('italic')
					? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
					: 'color: var(--theme-title-color);'}
				class="toolbar-button"
				on:click={() => editor.chain().focus().toggleItalic().run()}
			>
				<i class="ri-italic"></i>
			</button>

			<!-- Bullet List Button -->
			<button
				style={editor.isActive('bulletList')
					? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
					: 'color: var(--theme-title-color);'}
				class="toolbar-button"
				on:click={() => editor.chain().focus().toggleBulletList().run()}
			>
				<i class="ri-list-unordered"></i>
			</button>

			<!-- Ordered List Button -->
			<button
				style={editor.isActive('orderedList')
					? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
					: 'color: var(--theme-title-color);'}
				class="toolbar-button"
				on:click={() => editor.chain().focus().toggleOrderedList().run()}
			>
				<i class="ri-list-ordered"></i>
			</button>

			<!-- Heading Buttons -->
			{#each [1, 2, 3] as level}
				<button
					style={editor.isActive('heading', { level })
						? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
						: 'color: var(--theme-title-color);'}
					class="toolbar-button"
					on:click={() => editor.chain().focus().toggleHeading({ level }).run()}
				>
					H{level}
				</button>
			{/each}

			<!-- Link Button -->
			<button
				style={editor.isActive('link')
					? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
					: 'color: var(--theme-title-color);'}
				class="toolbar-button"
				on:click={() => {
					const url = prompt('Enter the URL');
					if (url) {
						editor.chain().focus().setLink({ href: url }).run();
					}
				}}
			>
				<i class="ri-link"></i>
			</button>
		</div>
	</div>
{/if}

<style lang="scss">
	#toolbar-wrapper {
		background-color: var(--theme-body-color);
		border-radius: 0.375rem;
		border: 1px solid var(--theme-border-color);
		padding: 0.75rem 1rem;

		#toolbar {
			display: flex;
			gap: 1rem;

			button {
				background-color: var(--theme-body-color);
				border: none;
				cursor: pointer;
				font-size: 1rem;
				padding: 0.25rem;
				border-radius: 0.375rem;
				transition: background-color 0.2s ease;

				&:hover {
					background-color: var(--theme-title-color);
					color: #fff;
				}
			}
		}
	}
</style>
