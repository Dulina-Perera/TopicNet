<script lang="ts">
	import { onMount } from 'svelte';

	export let title: string;
	export let content: string;

	let textareaEl: HTMLTextAreaElement | null = null;
	let maxHeight: number = 360; // Maximum height (in pixels) before scroll appears

	// Expand textarea based on content.
	const autoResize = () => {
		if (textareaEl) {
			// Reset height to 'auto' to allow shrinking.
			textareaEl.style.height = 'auto';

			// Calculate the new height.
			const newHeight: number = Math.min(textareaEl.scrollHeight, maxHeight);
			textareaEl.style.height = `${newHeight}px`;

			// Toggle overflow when max height is reached.
			if (textareaEl.scrollHeight > maxHeight) {
				textareaEl.style.overflowY = 'auto';
			} else {
				textareaEl.style.overflowY = 'hidden';
			}
		}
	};

	// Handle focus and blur for changing border color.
	const handleFocus = (e: FocusEvent) => {
		const target = e.target as HTMLTextAreaElement;
		target.style.borderColor = 'var(--color-primary-700)';
	};

	const handleBlur = (e: FocusEvent) => {
		const target = e.target as HTMLTextAreaElement;
		target.style.borderColor = 'var(--color-secondary-300)';
		// Reset scroll position to the top
		target.scrollTop = 0;
	};

	// Trigger autoResize when the component is mounted to handle initial content.
	onMount(() => {
		autoResize();
	});
</script>

<div class="pk bg-white pb-4 pt-4 px-4 w-72" style="border-radius: var(--theme-rounded-container);">
	<h2 class="text-sm text-center" style="color: var(--color-primary-700);">{title}</h2>

	<textarea
		bind:this={textareaEl}
		class="border mt-3 outline-none overflow-hidden p-2 resize-none text-xs w-full"
		style="
			border-color: var(--color-secondary-300);
			border-radius: var(--theme-rounded-container);
			border-width: var(--theme-border-base);
			max-height: {maxHeight}px;
			transition: height 0.2s ease, border-color 0.2s ease;
		"
		rows="1"
		on:input={autoResize}
		on:focus={handleFocus}
		on:blur={handleBlur}>{content}</textarea
	>
</div>

<style>
	textarea {
		scrollbar-color: var(--color-secondary-300) transparent;
		scrollbar-gutter: stable;
		scrollbar-width: thin;
	}

	textarea::-webkit-scrollbar-thumb {
		border-radius: 10px;
	}
</style>
