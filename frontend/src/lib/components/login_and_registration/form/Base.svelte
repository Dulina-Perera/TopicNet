<script lang="ts">
	import { signupMode } from '$lib/stores';

	$: mode = $signupMode;
</script>

<div class={`${mode ? "sign-up" : ""}`} id="form-wrapper">
	<slot />
</div>

<style lang="scss">
	#form-wrapper {
		display: grid;
		grid-template-columns: 1fr;
		grid-template-rows: 1fr;
		height: 100%;
		left: 0;
		position: absolute;
		top: 0;
		transition: 0.8s ease-in-out;
		width: 45%;

		&.sign-up {
			left: 55%;
		}

		@media (max-width: 768px) {
			height: auto;
			position: revert;
			width: 100%;
		}
	}
</style>
