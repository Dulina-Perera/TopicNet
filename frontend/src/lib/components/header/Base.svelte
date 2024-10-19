<script lang="ts">

</script>

<header id="header">
	<slot />
</header>

<style lang="scss">
	#header {
		background-color: var(--theme-body-color);
		border-radius: var(--theme-border-radius-container);
		box-shadow: 0 2px 16px hsla(230, 75%, 32%, .15);
		margin: 0 auto;
		max-width: 1200px;
		min-width: 300px;
		position: sticky;
		margin-top: 1rem;
		width: 80%;
		z-index: var(--theme-z-index-fixed);
	}
</style>
