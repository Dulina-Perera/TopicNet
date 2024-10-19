<script lang="ts">
	import { signupMode } from '$lib/stores';

	$: mode = $signupMode;

	const moveSlider = (event: MouseEvent) => {
		const images: NodeListOf<Element> = document.querySelectorAll('.image');
		const bullets: NodeListOf<Element> = document.querySelectorAll('#bullets span');

		images.forEach((image) => {
			image.classList.remove('show');
		});

		bullets.forEach((bullet) => {
			bullet.classList.remove('active');
		});

		const bullet: HTMLElement = event.target as HTMLElement;
		const image: HTMLElement = document.querySelector(
			`#image-${bullet.dataset.value}`
		) as HTMLElement;

		bullet.classList.add('active');
		image.classList.add('show');

		const textGroup: HTMLElement = document.querySelector('#text-group') as HTMLElement;
		textGroup.style.transform = `translateY(-${(Number(bullet.dataset.value) - 1) * 2.2}rem)`;
	};
</script>

<div class={`${mode ? 'sign-up' : ''}`} id="carousel">
	<div id="image-wrapper">
		<img src="/login-carousel/image1.png" alt="" class="image show" id="image-1" />
		<img src="/login-carousel/image2.png" alt="" class="image" id="image-2" />
		<img src="/login-carousel/image3.png" alt="" class="image" id="image-3" />
	</div>
	<div id="text-slider">
		<div id="text-wrapper">
			<div id="text-group">
				<h2>Create your own courses</h2>
				<h2>Customize as you like</h2>
				<h2>Invite students to your class</h2>
			</div>
		</div>

		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<!-- svelte-ignore a11y-no-static-element-interactions -->
		<div id="bullets">
			<span class="active" data-value="1" on:click={moveSlider}></span>
			<span data-value="2" on:click={moveSlider}></span>
			<span data-value="3" on:click={moveSlider}></span>
		</div>
	</div>
</div>

<style lang="scss">
	#carousel {
		background-color: #ffe0d2;
		border-radius: var(--theme-border-radius-container);
		display: grid;
		grid-template-rows: auto 1fr;
		height: 100%;
		left: 45%;
		overflow: hidden;
		padding-bottom: 2rem;
		position: absolute;
		top: 0;
		transition: 0.8s ease-in-out;
		width: 55%;

		&.sign-up {
			left: 0;
		}

		@media (max-width: 640px) {
			border-radius: 1.6rem;
			padding: 1.5rem 1rem;
		}

		@media (max-width: 768px) {
			display: flex;
			height: auto;
			padding: 3rem 2rem;
			position: revert;
			width: 100%;
		}
	}

	#image-wrapper {
		display: grid;
		grid-template-columns: 1fr;
		grid-template-rows: 1fr;

		@media (max-width: 768px) {
			display: none;
		}
	}

	.image {
		grid-column: 1 / 2;
		grid-row: 1 / 2;
		opacity: 0;
		transition:
			opacity 0.3s,
			transform 0.5s;
		width: 100%;
	}

	#image-1 {
		transform: translate(0, -50px);

		&:global(.show) {
			opacity: 1;
			transform: none;
		}
	}

	#image-2 {
		transform: scale(0.4, 0.5);

		&:global(.show) {
			opacity: 1;
			transform: none;
		}
	}

	#image-3 {
		transform: scale(0.3) rotate(-20deg);

		&:global(.show) {
			opacity: 1;
			transform: none;
		}
	}

	#text-slider {
		align-items: center;
		display: flex;
		flex-direction: column;
		justify-content: center;

		@media (max-width: 768px) {
			width: 100%;
		}
	}

	#text-wrapper {
		margin-bottom: 2.5rem;
		max-height: 2.2rem;
		overflow: hidden;

		@media (max-width: 640px) {
			margin-bottom: 1rem;
		}
	}

	#text-group {
		display: flex;
		flex-direction: column;
		text-align: center;
		transform: translateY(0);
		transition: 0.5s;

		h2 {
			color: var(--theme-title-color);
			font-size: 1.6rem;
			font-weight: 600;
			line-height: 2.2rem;

			@media (max-width: 640px) {
				font-size: 1.2rem;
			}
		}
	}

	#bullets {
		align-items: center;
		display: flex;
		justify-content: center;

		span {
			background-color: var(--theme-border-color);
			border-radius: 50%;
			cursor: pointer;
			display: block;
			height: 0.5rem;
			margin: 0 0.25rem;
			transition: 0.4s;
			width: 0.5rem;

			&.active {
				background-color: var(--theme-title-color);
				border-radius: 1rem;
				width: 1.1rem;
			}
		}
	}
</style>
