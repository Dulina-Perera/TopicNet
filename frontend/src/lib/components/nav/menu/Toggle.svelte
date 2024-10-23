<script lang="ts">
	import { isVisible } from "$lib/stores/nav-menu.store";

	const toggleNavMenu = () => {
		isVisible.update((value) => !value);
	};
</script>

<button id="nav-toggle" on:click={toggleNavMenu}>
	<i class="ri-menu-line"></i>
</button>

<style lang="scss">
	#nav-toggle {
		background-color: transparent;
		color: var(--theme-title-color);
		cursor: pointer;
		font-size: 1.25rem;
		line-height: 1.75rem;
		transition-duration: 0.4s;
		transition-property: color;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

		@media (min-width: 768px) {
			display: none;
		}

		&:hover {
			color: var(--theme-primary-color);
		}
	}
</style>
