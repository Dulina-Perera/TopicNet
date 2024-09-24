<script lang="ts">
	import { searchVisible } from "$lib/stores";

	let isVisible: boolean;
	let searchQuery: string = "";

	$: isVisible = $searchVisible;

	const hideSearch = () => {
		searchQuery = "";
		searchVisible.set(false);
	};
</script>

<div
	class={`
		${isVisible ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"}
		backdrop-blur-xl bg-[hsla(230, 75%, 15%, .1)] fixed left-0 pb-0 pt-32 px-6 sm:pt-40 top-0 transition-opacity w-full z-modal
	`}
	id="search"
>
	<form
		action=""
		class={`
			${isVisible ? "translate-y-0" : "translate-y-[-1rem]"}
			bg-container-color flex gap-x-2 items-center pe-4 ps-4 rounded-lg shadow-[0_8px_32px_hsla(230,75%,15%,0.2)] sm:max-w-[450px] sm:me-auto sm:ms-auto transition-transform
		`}
	>
		<i class="ri-search-line text-title-color text-xl"></i>
		<input
			type="search"
			placeholder="What are you looking for?"
			bind:value={searchQuery}
			class="bg-container-color placeholder:text-text-color py-4 text-text-color w-full"
		>
	</form>

	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<i
		class="absolute ri-close-line cursor-pointer right-8 sm:inset-x-0 sm:me-auto sm:ms-auto sm:text-[2rem] sm:top-20 sm:w-max text-2xl text-title-color top-8"
		id="search-close"
		on:click={hideSearch}
	></i>
</div>
