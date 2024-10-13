<script lang="ts">
	export let logoText: string | undefined = undefined;
</script>

<div
	class="fixed left-4 p-3 top-4 w-fit"
>
	<a href="/" class="text-2xl">{logoText}</a>
</div>

<style>
	div {
		background-color: var(--color-surface-300);
		border-radius: var(--theme-rounded-container);
		z-index: var(--theme-z-index-fixed);
	}

	a {
		color: var(--color-primary-700);
		font-family: var(--theme-font-family-logo);
	}
</style>
