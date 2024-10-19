<script>
	import { Github, Moon, Sun } from "$lib/components/icon";
	import { onMount } from "svelte";
	import { theme } from "$lib/stores";
</script>

<nav class="flex font-semibold items-center leading-8 text-sm">
	<ul class="hidden md:flex space-x-8">
		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" class="hover:text-magnum-500 transition-colors"> About us </a>
		</li>
		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" class="hover:text-magnum-500 transition-colors"> Services </a>
		</li>
		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" class="hover:text-magnum-500 transition-colors"> Features </a>
		</li>
		<li>
			<!-- svelte-ignore a11y-invalid-attribute -->
			<a href="#" class="hover:text-magnum-500 transition-colors"> Contact us </a>
		</li>
	</ul>

	<div class="border-neutral-700 flex gap-6 items-center md:border-l sm:ml-6 sm:pl-6 text-neutral-400">
		<a href="https://github.com/Dulina-Perera/TopicNet" target="_blank" rel="noopener noreferrer" class="transition-colors hover:text-neutral-50">
			<Github className="h-5 w-5" />
			<span class="sr-only">View the TopicNet Github repository</span>
		</a>

		<div>
			<button class="focus:outline-none" aria-label="Toggle dark mode">
				<Sun className="h-5 w-5" />
				<Moon className="h-5 w-5" />
			</button>
		</div>
	</div>
</nav>
