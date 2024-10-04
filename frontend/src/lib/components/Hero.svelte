<script lang="ts">
	import { FileButton } from '@skeletonlabs/skeleton';
</script>

<section class="w-full min-h-screen flex items-center justify-center py-16 px-4 sm:px-6 lg:px-8 bg-white">
  <div class="flex flex-col-reverse lg:flex-row items-center justify-between gap-8 max-w-[90%] mx-auto">
    <!-- Text Content -->
    <div class="hero__content max-w-lg text-center lg:text-left">
      <h1 class="hero__title text-5xl sm:text-6xl font-extrabold tracking-tight text-gray-900">
        TopicNet
      </h1>
      <p class="hero__description mt-6 text-xl sm:text-2xl leading-relaxed text-gray-600">
        Interactively Visualize Unstructured Text Documents as Mindmaps
      </p>
      <div class="mt-8">
        <FileButton name="files" />
      </div>
    </div>

    <!-- Image Content -->
    <div class="hero__image relative flex-shrink-0">
      <!-- svelte-ignore a11y-img-redundant-alt -->
      <img class="w-full max-w-sm lg:max-w-md rounded-3xl shadow-lg transform hover:scale-105 transition-transform duration-300 ease-in-out" src="/hero_img.png" alt="An image depicting the purpose of TopicNet" />

      <!-- Optional overlay gradient for a subtle blend -->
      <div class="absolute inset-0 rounded-3xl bg-gradient-to-t from-gray-900 via-transparent to-transparent opacity-30"></div>
    </div>
  </div>
</section>
