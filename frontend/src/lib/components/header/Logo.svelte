<script lang="ts">
	export let logoText: string | undefined = undefined;
</script>

<div class="inline-flex items-center p-1">
	<a href="/" class="text-xl">{logoText}</a>
</div>

<style>
	div {
		background-color: var(--color-surface-200);
		border-radius: var(--theme-rounded-container);
		z-index: var(--theme-z-index-fixed);
	}

	a {
		color: var(--color-primary-700);
		font-family: var(--theme-font-family-logo);
	}
</style>
