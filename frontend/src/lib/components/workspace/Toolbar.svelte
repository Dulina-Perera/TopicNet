<script lang="ts">
	import { Editor } from '@tiptap/core';

	export let editor: Editor | null;
	export let content: string;

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
			<button
				style={editor.isActive('bold')
					? 'background-color: var(--theme-primary-color); border-radius: 0.5rem; color: #fff; padding: 0.5rem;'
					: 'color: var(--theme-title-color);'}
				class="toolbar-button"
				on:click={() => editor.chain().focus().toggleBold().run()}><i class="ri-bold"></i></button
			>
		</div>
	</div>
{/if}

<style lang="scss">
	#toolbar-wrapper {
		align-items: start;
		background-color: var(--theme-body-color);
		border-radius: 0.375rem;
		border: 1px solid var(--theme-border-color);
		display: flex;
		flex-wrap: wrap;
		gap: 1.25rem;
		justify-content: space-between;
		padding: 0.75rem 1rem;
		width: 100%;

		#toolbar {
			align-items: center;
			display: flex;
			flex-wrap: wrap;
			gap: 1.25rem;
			justify-content: start;
			width: 100%;

			@media screen and (min-width: 1024px) {
				width: 83.333333%;
			}

			button {
				background-color: var(--theme-body-color);
			}
		}
	}
</style>
