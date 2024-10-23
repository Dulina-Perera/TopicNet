<script lang="ts">
	import { boardDraggable } from "$lib/stores";
	import { onDestroy, onMount } from "svelte";

	let isOpen: boolean = false;
	let selectedOption: string = 'select';

	const options: { name: string; icon: string }[] = [
		{ name: 'select', icon: 'ri-cursor-line' },
		{ name: 'move', icon: 'ri-hand' }
	];

	const toggleDropdown: () => void = () => {
		isOpen = !isOpen;
	};

	const selectOption: (option: { name: string; icon: string }) => void = (option) => {
		selectedOption = option.name;
		isOpen = false;

		if (selectedOption === 'select') {
			boardDraggable.update(() => false);
		} else if (selectedOption === 'move') {
			boardDraggable.update(() => true);
		}
	};

	const handleClickOutside: (event: MouseEvent) => void = (event) => {
		const target = event.target as HTMLElement;

		if (!target.closest('#toggle-component')) {
			isOpen = false;
		}
	};

	onMount(() => {
		document.addEventListener('click', handleClickOutside);
	});
</script>

<div id="toggle-component">
	<button id="toggle-button" on:click={toggleDropdown} type="button" aria-label="Toggle Dropdown">
		<i class={selectedOption === 'select' ? 'ri-cursor-line' : 'ri-hand'}></i>
		<i class={isOpen ? 'ri-arrow-up-s-line' : 'ri-arrow-down-s-line'}></i>
	</button>

	{#if isOpen}
		<div id="toggle-dropdown">
			{#each options as option}
				<button
					on:click={() => selectOption(option)}
					type="button"
					aria-label={option.name}
					class="dropdown-option"
				>
					<i class={option.icon}></i>
					<span>{option.name.charAt(0).toUpperCase() + option.name.slice(1)}</span>
				</button>
			{/each}
		</div>
	{/if}
</div>

<style lang="scss">
	#toggle-component {
		position: relative;

		#toggle-button {
			align-items: center;
			cursor: pointer;
			display: flex;
			background-color: var(--theme-body-color);

			i {
				color: var(--theme-title-color);
				cursor: pointer;
				font-size: 0.875rem;
				line-height: 1.25rem;
				transition: color 0.4s cubic-bezier(0.4, 0, 0.2, 1);
			}

			:first-child {
				font-size: 1.25rem;
				line-height: 1.75rem;
			}
		}

		#toggle-dropdown {
			background-color: var(--theme-body-color);
			border-radius: var(--theme-border-radius-container);
			box-shadow: 0 2px 16px hsla(230, 75%, 32%, 0.15);
			margin-top: 0.5rem;
			position: absolute;
			z-index: var(--theme-z-index-modal);

			.dropdown-option {
				align-items: center;
				background-color: transparent;
				cursor: pointer;
				display: flex;
				justify-content: center;
				padding: 0.5rem 0.5rem;
				transition: border-left 0.4s cubic-bezier(0.4, 0, 0.2, 1);

				i {
					color: var(--theme-title-color);
					font-size: 1.25rem;
					line-height: 1.75rem;
					margin-right: 0.5rem;
				}

				span {
					color: var(--theme-title-color);
					font-size: 1rem;
				}

				/* Hover effect to highlight the option */
				&:hover {
					border-left: 3px solid var(--theme-border-color);
				}
			}
		}
	}
</style>
