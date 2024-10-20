<script lang="ts">
	import { signupMode } from '$lib/stores';

	$: mode = $signupMode;
</script>

<div class={`${mode ? "sign-up" : ""}`} id="carousel"></div>

<style lang="scss">
	#carousel {
		background-color: #ffe0d2;
		border-radius: var(--theme-border-radius-container);
		height: 100%;
		left: 45%;
		position: absolute;
		top: 0;
		transition: 0.8s ease-in-out;
		width: 55%;

		&.sign-up {
			left: 0;
		}
	}
</style>
