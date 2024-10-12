<script lang="ts">
	import { FileButton } from '@skeletonlabs/skeleton';
</script>

<section class="relative w-full h-screen flex items-center">
	<div
		class="flex flex-col lg:flex-row max-w-8xl items-start justify-between gap-12 px-6 lg:px-12"
	>
		<div class="lg:max-w-lg text-left">
			<h1 class="font-extrabold leading-tight text-8xl text-title-color tracking-tight">
				TopicNet
			</h1>
			<p class="mt-6 text-lg sm:text-xl lg:text-2xl leading-relaxed text-gray-600">
				Interactively Visualize Unstructured Text Documents as Mindmaps
			</p>
			<div class="mt-8">
				<FileButton name="files" />
			</div>
		</div>

		<div
			class="absolute bottom-8 pointer-events-none right-8 select-none lg:w-auto w-full h-[90vh]"
		>
			<!-- svelte-ignore a11y-img-redundant-alt -->
			<img class="h-full w-full" src="/hero_img.svg" alt="Hero Image" />
		</div>
	</div>
</section>
