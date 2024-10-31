<script lang="ts">
	import { isVisible } from '$lib/stores/nav-menu.store';

	const hideNavMenu: () => void = () => {
		isVisible.set(false);
	};
</script>

<div class={`${$isVisible ? 'is-visible' : ''}`} id="nav-menu">
	<!-- svelte-ignore a11y-invalid-attribute -->
	<ul id="nav-list">
		<li><a href="/about" id="nav-link">About Us</a></li>
		<li><a href="/services" id="nav-link">Services</a></li>
		<li><a href="/featured" id="nav-link">Featured</a></li>
		<li><a href="/contact" id="nav-link">Contact Me</a></li>
	</ul>

	<button id="nav-close" on:click={hideNavMenu}><i class="ri-close-line"></i></button>
</div>

<style lang="scss">
	#nav-menu {
		@media screen and (max-width: 768px) {
			background-color: var(--theme-body-color);
			box-shadow: 0 8px 16px hsla(230, 75%, 32%, 0.15);
			left: 0;
			padding-block: 4.5rem 4rem;
			position: fixed;
			top: -1000%;
			transition: top 0.4s cubic-bezier(0.4, 0, 0.2, 1);
			width: 100%;
		}

		&.is-visible {
			top: 0;
		}

		#nav-list {
			display: flex;
			flex-direction: column;
			row-gap: 2.5rem;
			text-align: center;

			@media screen and (min-width: 768px) {
				column-gap: 3rem;
				flex-direction: row;
			}

			#nav-link {
				color: var(--theme-title-color);
				font-weight: 600;
				transition: color 0.4s cubic-bezier(0.4, 0, 0.2, 1);

				&:hover {
					color: var(--theme-primary-color);
				}
			}
		}

		#nav-close {
			background-color: transparent;
			color: var(--theme-title-color);
			cursor: pointer;
			font-size: 1.25rem;
			line-height: 1.75rem;
			position: absolute;
			right: 1.5rem;
			top: 1.15rem;
			transition: color 0.4s cubic-bezier(0.4, 0, 0.2, 1);

			@media screen and (min-width: 768px) {
				display: none;
			}
		}
	}
</style>
