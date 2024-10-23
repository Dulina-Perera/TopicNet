<script lang="ts">

</script>

<main>
	<div id="box">
		<div id="inner-box">
			<slot />
		</div>
	</div>
</main>

<style lang="scss">
	main {
		align-items: center;
		display: flex;
		justify-content: center;
		min-height: 100vh;
		overflow: hidden;
		padding: 2rem;
		width: 100%;
		z-index: var(--theme-z-index-fixed);

		@media (max-width: 640px) {
			padding: 1rem;
		}
	}

	#box {
		background-color: var(--theme-body-color);
		border-radius: var(--theme-border-radius-base);
		box-shadow: 0 2px 16px hsla(230, 75%, 32%, .15);
		height: 640px;
		max-width: 1024px;
		position: relative;
		width: 100%;

		@media (max-width: 640px) {
			border-radius: 2rem;
		}

		@media (max-width: 768px) {
			height: auto;
			max-width: 640px;
			overflow: hidden;
		}
	}

	#inner-box {
		height: calc(100% - 4.1rem);
		left: 50%;
		position: absolute;
		top: 50%;
		transform: translate(-50%, -50%);
		width: calc(100% - 4.1rem);

		@media (max-width: 640px) {
			padding: 1rem;
		}

		@media (max-width: 768px) {
			height: revert;
			padding: 2rem;
			position: static;
			transform: none;
			width: revert;
		}
	}
</style>
