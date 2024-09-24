<script lang="ts">
	import { loginVisible, searchVisible } from "$lib/stores";

	let navMenuVisible: boolean = false;

	const showNavMenu = () => {
		navMenuVisible = true;
	};

	const hideNavMenu = () => {
		navMenuVisible = false;
	};

	const showSearch = () => {
		searchVisible.set(true);
	};

	const showLogin = () => {
		loginVisible.set(true);
	};
</script>

<header class="bg-body-color fixed inset-x-16 rounded-lg shadow-[0_2px_16px_hsla(230,75%,32%,0.15)] top-4 w-[calc(100%-8rem)] z-fixed" id="header">
	<nav class="flex h-header items-center justify-between me-6 ms-6">
		<a href="/" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">TopicNet</a>

		<div
			class={`
				${navMenuVisible ? 'top-0' : 'max-lg:top-[-100%]'}
				lg:mx-auto max-lg:bg-body-color max-lg:duration-[0.4s] max-lg:fixed max-lg:left-0 max-lg:pb-16 max-lg:pt-16 max-lg:shadow-[0_8px_16px_hsla(230,75%,32%,0.15)] max-lg:transition-[top] max-lg:w-full
			`}
			id="nav-menu"
		>
			<ul class="flex flex-col gap-y-10 lg:flex-row lg:gap-x-12 text-center">
				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Home</a>
				</li>

				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">About Us</a>
				</li>

				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Services</a>
				</li>

				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Featured</a>
				</li>

				<li>
					<!-- svelte-ignore a11y-invalid-attribute -->
					<a href="#" class="duration-[0.4s] font-semi-bold hover:text-first-color text-title-color transition-[color]">Contact Us</a>
				</li>
			</ul>

			<!-- Close button -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="absolute cursor-pointer duration-[0.4s] lg:hidden right-6 text-title-color text-xl top-5 transition-[color]"
				id="nav-close"
				on:click={hideNavMenu}
			>
				<i class="ri-close-line"></i>
			</div>
		</div>

		<div class="flex gap-x-4 items-center">
			<!-- Search button -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<i
				class="cursor-pointer duration-[0.4s] hover:text-first-color ri-search-line text-title-color text-xl transition-[color]"
				id="search-btn"
				on:click={showSearch}
			></i>

			<!-- Login button -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<i
				class="cursor-pointer duration-[0.4s] hover:text-first-color ri-user-line text-title-color text-xl transition-[color]"
				id="login-btn"
				on:click={showLogin}
			></i>

			<!-- Toggle button -->
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<div
				class="cursor-pointer duration-[0.4s] hover:text-first-color lg:hidden text-title-color text-xl transition-[color]"
				id="nav-toggle"
				on:click={showNavMenu}
			>
					 <i class="ri-menu-line"></i>
				</div>
		</div>
	</nav>
</header>
