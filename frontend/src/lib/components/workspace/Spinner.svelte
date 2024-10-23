<script lang="ts">
	export let message: string = 'Loading...';
</script>

<div id="loader">
	<svg>
		<filter id="gooey">
			<feGaussianBlur in="SourceGraphic" stdDeviation="5" />
			<feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 20 -10" />
		</filter>
	</svg>

	<div id="spinner">
		<span style="--j:0;" class="rotate"></span>
		<span style="--j:1;" class="rotate"></span>
		<span style="--j:2;" class="rotate"></span>
		<span style="--j:3;" class="rotate"></span>
		<span style="--j:4;" class="rotate"></span>
	</div>

	<div id="message">
		{message}
	</div>
</div>

<style lang="scss">
	#loader {
		align-items: center;
		background-color: var(--theme-body-color);
		border-radius: var(--theme-border-radius-container);
		bottom: 20px;
		box-shadow: 0 2px 16px hsla(230, 75%, 32%, 0.15);
		display: flex;
		padding: 2px 8px;
		position: fixed;
		right: 20px;
		z-index: var(--theme-z-index-fixed);

		svg {
			height: 0;
			width: 0;
		}

		#spinner {
			height: 32px;
			width: 32px;
			filter: url(#gooey);
			position: relative;

			span {
				display: block;
				height: 100%;
				position: absolute;
				width: 100%;

				&.rotate {
					animation: animate 4s ease-in-out infinite;
					animation-delay: calc(-0.2s * var(--j));
				}

				&:before {
					background: linear-gradient(45deg, var(--theme-primary-color), var(--theme-title-color));
					border-radius: 50%;
					box-shadow: 0 0 1px var(--theme-title-color);
					content: '';
					height: 10px;
					left: calc(50% - 5px);
					position: absolute;
					top: 0;
					width: 10px;
				}
			}
		}

		#message {
			color: var(--theme-title-color);
			font-size: 0.75rem;
			font-weight: 600;
			line-height: 1rem;
			margin-left: 4px;
		}
	}

	@keyframes animate {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
