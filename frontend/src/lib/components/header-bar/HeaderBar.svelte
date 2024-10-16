<script lang="ts">
	// Props for additional configuration
	export let className: string = "";
	export let style: string = "";
</script>

<header class={`fixed left-4 top-4 w-[calc(100%-2rem)] ${className}`} style={style}>
	<div class="flex justify-between">
		<slot />
	</div>
</header>
