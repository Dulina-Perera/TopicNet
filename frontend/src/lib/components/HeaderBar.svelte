<header class="bottom-0 bg-neutral-900 md:pb-0 md:pt-2 md:top-0 pb-2 px-2 sticky w-full">
	<div class="!outline !outline-neutral-700 bg-neutral-800 container dark:!outline-none flex h-14 items-center outline-2 text-white">
		<slot />
	</div>
</header>

<style lang="scss">
	header {
		@media (min-width: 768px) {
			bottom: unset;
		}

		z-index: var(--theme-z-index-fixed);
	}

	div {
		border-radius: var(--theme-rounded-container);
	}
</style>
