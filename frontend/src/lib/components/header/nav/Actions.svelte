<script lang="ts">
	import { loginVisible, navMenuVisible } from "$lib/stores";

	const showLogin = () => {
		loginVisible.update(() => true);
	};

	const toggleNavMenu = () => {
		navMenuVisible.update((value) => !value);
	};
</script>

<div id="nav-actions">
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<i class="ri-user-line" id="login-btn" on:click={showLogin}></i>

	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div id="nav-toggle" on:click={toggleNavMenu}>
		<i class="ri-menu-line"></i>
	</div>
</div>

<style lang="scss">
	#nav-actions {
		align-items: center;
		column-gap: 1rem;
		display: flex;

		#login-btn,
		#nav-toggle {
			color: var(--theme-title-color);
			cursor: pointer;
			font-size: 1.25rem;
			line-height: 1.75rem;
			transition-duration: 0.4s;
			transition-property: color;
			transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

			&:hover {
				color: var(--theme-primary-color);
			}
		}
	}

	#nav-toggle {
		@media (min-width: 1024px) {
			display: none;
		}
	}
</style>
