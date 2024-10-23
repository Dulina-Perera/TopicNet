<script lang="ts">
</script>

<header>
	<nav>
		<slot />
	</nav>
</header>

<style lang="scss">
	header {
		background-color: var(--theme-body-color);
		border-radius: var(--theme-border-radius-container);
		box-shadow: 0 2px 16px hsla(230, 75%, 32%, 0.15);
		margin-top: 1rem;
		max-width: 1200px;
		min-width: 300px;
		width: 80%;
		position: fixed;
		left: 50%;
		transform: translateX(-50%);
		z-index: var(--theme-z-index-fixed);

		nav {
			align-items: center;
			display: flex;
			height: 3.5rem;
			justify-content: space-between;
			margin-inline: 1.5rem;
		}
	}
</style>
