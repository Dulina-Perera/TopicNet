<script lang="ts">
	import Logo from './Logo.svelte';
	import { enhance } from '$app/forms';
	import { signupMode } from '$lib/stores';

	$: mode = $signupMode;

	const onFocus = (event: FocusEvent) => {
		const target = event.target as HTMLInputElement;
		target.classList.add('active');
	};

	const onBlur = (event: FocusEvent) => {
		const target = event.target as HTMLInputElement;
		if (target.value === '') {
			target.classList.remove('active');
		}
	};
</script>

<form class={`${mode ? 'sign-up' : ''}`} action="?/login" method="post" use:enhance>
	<Logo />

	<div id="heading">
		<h2>Welcome Back!</h2>
		<h6>Not registered yet?</h6>
		<!-- svelte-ignore a11y-invalid-attribute -->
		<!-- svelte-ignore a11y-missing-content -->
		<a href="#" id="toggle" on:click={() => signupMode.set(true)}>Sign up</a>
	</div>

	<div id="actual-form">
		<div class="input-wrapper">
			<input
				type="text"
				name="username"
				minlength="4"
				required
				id="username"
				class="input-field"
				on:focus={onFocus}
				on:blur={onBlur}
			/>
			<label for="username">Username</label>
		</div>
		<div class="input-wrapper">
			<input
				type="password"
				name="password"
				minlength="16"
				maxlength="64"
				required
				id="password"
				class="input-field"
				on:focus={onFocus}
				on:blur={onBlur}
			/>
			<label for="password">Password</label>
		</div>

		<input type="submit" value="Sign In" id="submit-btn" />

		<p class="text">
			Forgotten your username or password?
			<br />
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#">Get help</a> signing in.
		</p>
	</div>
</form>

<style lang="scss">
	form {
		display: flex;
		flex-direction: column;
		grid-column: 1 / 2;
		grid-row: 1 / 2;
		height: 100%;
		justify-content: space-evenly;
		margin: 0 auto;
		max-width: 260px;
		transition: opacity 0.02s 0.4s;
		width: 100%;

		&.sign-up {
			opacity: 0;
			pointer-events: none;

			@media (max-width: 768px) {
				transform: translateX(-100%);
			}
		}

		@media (max-width: 640px) {
			padding: 1rem 2rem 1.5rem;
		}

		@media (max-width: 768px) {
			max-width: revert;
			padding: 1.5rem 2.5rem 2rem;
			transition:
				opacity 0.45s linear,
				transform 0.8s ease-in-out;
		}
	}

	#heading {
		@media (max-width: 768px) {
			margin: 2rem 0;
		}

		h2 {
			color: var(--theme-title-color);
			font-size: 2.1rem;
			font-weight: 600;
		}

		h6 {
			color: var(--theme-text-color);
			display: inline;
			font-size: 0.75rem;
			font-weight: 400;
		}
	}

	#toggle {
		color: var(--theme-title-color);
		cursor: pointer;
		font-size: 0.75rem;
		font-weight: 500;
		text-decoration: none;
		transition: 0.4s;

		&:hover {
			color: var(--theme-primary-color);
		}
	}

	.input-wrapper {
		height: 37px;
		margin-bottom: 2rem;
		position: relative;

		.input-field {
			background: none;
			border: none;
			border-bottom: 1px solid var(--theme-border-color);
			color: var(--theme-title-color);
			font-size: 0.95rem;
			height: 100%;
			padding: 0;
			position: absolute;
			transition: 0.4s;
			outline: none;
			width: 100%;

			&:global(.active) {
				border-bottom: 1px solid var(--theme-title-color);

				+ label {
					font-size: 0.75rem;
					top: -2px;
				}
			}
		}

		label {
			color: var(--theme-border-color);
			font-size: 0.95rem;
			left: 0;
			pointer-events: none;
			position: absolute;
			top: 50%;
			transform: translateY(-50%);
			transition: 0.4s;
		}
	}

	#submit-btn {
		background-color: var(--theme-title-color);
		border: none;
		border-radius: var(--theme-border-radius-container);
		cursor: pointer;
		color: #fff;
		display: inline-block;
		font-size: 0.8rem;
		height: 43px;
		margin-bottom: 2rem;
		transition: 0.4s;
		width: 100%;

		&:hover {
			background-color: var(--theme-primary-color);
		}
	}

	.text {
		color: var(--theme-text-color);
		font-size: 0.7rem;

		a {
			text-decoration: underline;
			transition: 0.4s;

			&:hover {
				color: var(--theme-primary-color);
			}
		}
	}
</style>
