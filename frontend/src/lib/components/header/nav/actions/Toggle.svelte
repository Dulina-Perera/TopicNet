<script lang="ts">
	import { navMenuVisible } from "$lib/stores";

	const toggleNavMenu = () => {
		navMenuVisible.update((value) => !value);
	};
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div id="nav-toggle" on:click={toggleNavMenu}>
	<i class="ri-menu-line"></i>
</div>

<style lang="scss">
	#nav-toggle {
		color: var(--theme-title-color);
		cursor: pointer;
		font-size: 1.25rem;
		line-height: 1.75rem;
		transition-duration: 0.4s;
		transition-property: color;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

		@media (min-width: 1024px) {
			display: none;
		}

		&:hover {
			color: var(--theme-primary-color);
		}
	}
</style>
