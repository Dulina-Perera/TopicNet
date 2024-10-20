<script lang="ts">
	import { navMenuVisible } from "$lib/stores";

	$: isVisible = $navMenuVisible;

	const hideNavMenu = () => {
		navMenuVisible.update(() => false);
	};
</script>

<div class={`${isVisible ? "is-visible" : ""}`} id="nav-menu">
	<ul id="nav-list">
		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" id="nav-link">About Us</a>
		</li>

		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" id="nav-link">Services</a>
		</li>

		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" id="nav-link">Featured</a>
		</li>

		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" id="nav-link">Contact Me</a>
		</li>
	</ul>

	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div id="nav-close" on:click={hideNavMenu}>
		<i class="ri-close-line"></i>
	</div>
</div>

<style lang="scss">
	#nav-menu {
		@media (min-width: 1024px) {
			margin-left: auto;
			margin-right: auto;
		}

		@media not all and (min-width: 1024px) {
			background-color: var(--theme-body-color);
			box-shadow: 0 8px 16px hsla(230, 75%, 32%, .15);
			left: 0;
			padding-bottom: 4rem;
			padding-top: 4rem;
			position: fixed;
			top: -100%;
			transition-duration: 0.4s;
			transition-property: top;
    	transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
			width: 100%;
		}

		&.is-visible {
			top: 0;
		}
	}

	#nav-list {
		display: flex;
		flex-direction: column;
		row-gap: 2.5rem;
		text-align: center;

		@media (min-width: 1024px) {
			column-gap: 3rem;
			flex-direction: row;
		}
	}

	#nav-link {
		color: var(--theme-title-color);
		font-weight: 600;
		transition-duration: 0.4s;
		transition-property: color;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

		&:hover {
			color: var(--theme-primary-color);
		}
	}

	#nav-close {
		color: var(--theme-title-color);
		cursor: pointer;
		font-size: 1.25rem;
		line-height: 1.75rem;
		position: absolute;
		right: 1.5rem;
		top: 1.25rem;
		transition-duration: 0.4s;
		transition-property: color;
		transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

		@media (min-width: 1024px) {
			display: none;
		}
	}
</style>
