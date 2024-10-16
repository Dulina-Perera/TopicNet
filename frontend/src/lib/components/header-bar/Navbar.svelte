<div class="inline-flex items-center">
	<nav>
		<ul class="flex gap-x-12 p-2">
			<li>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a href="#">Home</a>
			</li>
			<li>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a href="#">About Us</a>
			</li>
			<li>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a href="#">Services</a>
			</li>
			<li>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a href="#">Featured</a>
			</li>
			<li>
				<!-- svelte-ignore a11y-invalid-attribute -->
				<a href="#">Contact Us</a>
			</li>
		</ul>
	</nav>
</div>

<style>
	div {
		background-color: var(--color-surface-200);
		border-radius: var(--theme-rounded-container);
		z-index: var(--theme-z-index-fixed);
	}

	a {
		color: var(--color-primary-700);
		font-family: var(--theme-font-family-base);
		font-weight: 700;
	}
</style>
