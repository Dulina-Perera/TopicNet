<script lang="ts">
	import { loginVisible } from "$lib/stores";

	export let user: { id: string; username: string; isPermanent: boolean } | null;

	const showLogin = () => {
		loginVisible.update(() => true);
	};
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<i class={user ? "ri-user-line" : "ri-ghost-smile-line"} id="login-btn" on:click={showLogin}></i>

<style lang="scss">
	#login-btn {
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
</style>
