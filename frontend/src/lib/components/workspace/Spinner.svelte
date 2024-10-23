<script lang="ts">
</script>

<section>
	<svg>
		<filter id="gooey">
			<feGaussianBlur in="SourceGraphic" stdDeviation="10" />
			<feColorMatrix
				values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 20 -10"
			/>
		</filter>
	</svg>

	<div id="spinner">
		<span style="--i:1;"></span>
		<span style="--i:2;"></span>
		<span style="--i:3;"></span>
		<span style="--i:4;"></span>
		<span style="--i:5;"></span>
		<span style="--i:6;"></span>
		<span style="--i:7;"></span>
		<span style="--i:8;"></span>

		<span style="--j:0;" class="rotate"></span>
		<span style="--j:1;" class="rotate"></span>
		<span style="--j:2;" class="rotate"></span>
		<span style="--j:3;" class="rotate"></span>
		<span style="--j:4;" class="rotate"></span>
	</div>
</section>

<style lang="scss">
	section {
		align-items: center;
		background-color: #0c1b21;
		display: flex;
		justify-content: center;
		min-height: 100vh;

		svg {
			height: 0;
			width: 0;
		}

		#spinner {
			height: 250px;
			filter: url(#gooey);
			position: relative;
			width: 250px;

			span {
				display: block;
				height: 100%;
				left: 0;
				position: absolute;
				top: 0;
				transform: rotate(calc(45deg * var(--i)));
				width: 100%;

				&.rotate {
					animation: animate 4s ease-in-out infinite;
					animation-delay: calc(-0.2s * var(--j));
				}

				&:before {
					background: linear-gradient(45deg, #c7eeff, #03a9f4);
					border-radius: 50%;
					box-shadow: 0 0 30px #00bcd4;
					content: '';
					height: 40px;
					left: calc(50% - 20px);
					position: absolute;
					top: 0;
					width: 40px;
				}
			}
		}
	}

	@keyframes animate {
		0% {
			transform: rotate(90deg);
		}
		100% {
			transform: rotate(450deg);
		}
	}
</style>
