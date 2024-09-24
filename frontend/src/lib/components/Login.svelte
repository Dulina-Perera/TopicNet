<script lang="ts">
	import { loginVisible } from "$lib/stores";

	let isVisible: boolean;
	let email: string = "";
	let password: string = "";

	$: isVisible = $loginVisible;

	const hideLogin = () => {
		email = "";
		password = "";
		loginVisible.set(false);
	};
</script>

<div
	class={`
		${isVisible ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"}
		backdrop-blur-xl bg-[hsla(230, 75%, 15%, 0.1)] fixed h-full left-0 pb-0 pt-32 px-6 sm:pt-40 top-0 transition-opacity w-full z-modal
	`}
	id="login"
>
	<form
		action=""
		class={`
			${isVisible ? "translate-y-0" : "translate-y-[-1rem]"}
			bg-container-color gap-y-5 grid lg:pb-14 lg:pt-12 lg:px-8 pb-10 pt-8 px-6 rounded-2xl shadow-[0_8px_32px_hsla(230,75%,15%,0.2)] sm:max-w-[400px] sm:me-auto sm:ms-auto text-center transition-transform
		`}
	>
		<h2 class="text-h2 text-title-color">Log In</h2>

		<div class="grid gap-y-4">
			<div>
				<label
					for="email"
					class="block font-medium mb-1 text-title-color"
					style="text-align: initial;"
				>Email</label>
				<input
					type="email"
					placeholder="Enter your email"
					bind:value={email}
					class="bg-container-color border-2 border-border-color border-solid p-4 placeholder:text-text-color rounded-lg text-text-color w-full"
					id="email"
				>
			</div>

			<div>
				<label
				for="password"
				class="block font-medium mb-1 text-title-color"
				style="text-align: initial;"
			>Password</label>
				<input
					type="password"
					placeholder="Enter your password"
					bind:value={password}
					class="bg-container-color border-2 border-border-color border-solid p-4 placeholder:text-text-color rounded-lg text-text-color w-full"
					id="password"
				>
			</div>
		</div>

		<div>
			<p class="mb-2">
				<!-- svelte-ignore a11y-invalid-attribute -->
				Do not have an account? <a href="#">Sign up</a>
			</p>

			<!-- svelte-ignore a11y-invalid-attribute -->
			<a
				href="#"
				class="inline-block mb-5 text-first-color"
			>
				Forgot your password?
			</a>

			<button
				type="submit"
				class="bg-first-color cursor-pointer font-semibold hover:shadow-[0_4px_24px_hsla(230,75%,40%,0.4)] inline-block p-4 rounded-lg text-white transition-shadow w-full"
			>Log In</button>
		</div>
	</form>

	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<i
		class="absolute cursor-pointer ri-close-line right-8 sm:inset-x-0 sm:me-auto sm:ms-auto sm:text-3xl sm:top-20 sm:w-max text-2xl text-title-color top-8"
		id="login-close"
		on:click={hideLogin}
	></i>
</div>
