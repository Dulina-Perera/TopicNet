<script lang="ts">

</script>

<div id="form-wrapper">
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
		width: 45%;
	}
</style>
