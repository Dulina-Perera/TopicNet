<script lang="ts">
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';

	export let user: { id: string; username: string; isPermanent: boolean } | null;

	const showLogin = () => {
		if (!user) {
			goto('/login');
		}
	};
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-invalid-attribute -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div id="dropdown">
	<i class={user ? 'ri-user-line' : 'ri-ghost-smile-line'} id="avatar" on:click={showLogin}></i>

	{#if user}
		<div id="menu">
			<a href="#" id="menu-item">Profile</a>
			<a href="#" id="menu-item">Settings</a>
			<form method="post" action="?/logout" use:enhance>
				<button id="menu-item" type="submit">Logout</button>
			</form>
		</div>
	{/if}
</div>

<style lang="scss">
	#dropdown {
		display: inline-block;
		position: relative;

		#avatar {
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

		#menu {
			background-color: var(--theme-body-color);
			border-radius: var(--theme-border-radius-container);
			box-shadow: 0 2px 16px hsla(230, 75%, 32%, 0.15);
			display: none;
			padding: 0.5rem 0;
			position: absolute;
			right: 0;
			width: 8rem;
			z-index: var(--theme-z-index-modal);

			#menu-item {
				background-color: var(--theme-body-color);
				color: var(--theme-title-color);
				display: block;
				font-size: 0.875rem;
				line-height: 1.25rem;
				font-weight: 600;
				padding: 0.5rem 1rem;
				text-decoration: none;
				transition: background-color 0.3s ease;

				&:hover {
					color: var(--theme-primary-color);
				}
			}
		}

		&:hover #menu {
			display: block;
		}
	}
</style>
