<script lang="ts">
	import { goto } from '$app/navigation';

	let isOpen: boolean = false;
	let files: App.Document[] = [];

	async function toggleSidebar() {
		isOpen = !isOpen;

		const filesResponse = await fetch(`http://localhost:5000/api/v1/download/files`, {
			credentials: 'include'
		});

		if (!filesResponse.ok) {
			console.error('Failed to fetch files!');
			return;
		}
		files = await filesResponse.json();
	}

	function navigateToFile(event: MouseEvent, fileId: number) {
		event.preventDefault();
		goto(`/${fileId}`).then(() => location.reload());
	}
</script>

<div id="sidebar-wrapper">
	<div id="sidebar" class:visible={isOpen}>
		{#each files as file}
			<a href="/${file.id}}" on:click={(event) => navigateToFile(event, file.id)}>{file.name}</a>
		{/each}
	</div>

	<button id="toggle-button" class:move-right={isOpen} on:click={toggleSidebar}>
		{#if isOpen}
			<i class="ri-arrow-left-s-line"></i>
		{:else}
			<i class="ri-menu-line"></i>
		{/if}
	</button>
</div>

<style lang="scss">
	#sidebar-wrapper {
		position: fixed;
		top: 0;
		left: 0;
		height: 100vh;
		display: flex;
		align-items: center;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
		z-index: var(--theme-z-index-modal);

		#sidebar {
			position: fixed;
			top: 0;
			left: -200px;
			width: 200px;
			height: 100vh;
			background-color: var(--theme-body-color);
			color: var(--theme-title-color);
			display: flex;
			flex-direction: column;
			padding-top: 2rem;
			gap: 1rem;
			transition: transform 0.3s ease;
			transform: translateX(0);
			box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);

			&.visible {
				transform: translateX(200px);
			}

			a {
				color: var(--theme-title-color);
				text-decoration: none;
				padding: 0.5rem 1rem;
				font-size: 1rem;
				cursor: pointer;

				&:hover {
					background-color: var(--theme-primary-color);
				}
			}
		}

		#toggle-button {
			position: fixed;
			top: 50%;
			transform: translateY(-50%);
			width: 40px;
			height: 40px;
			background-color: var(--theme-body-color);
			color: var(--theme-title-color);
			border: none;
			border-radius: 0 5px 5px 0;
			cursor: pointer;
			font-size: 1.5rem;
			display: flex;
			align-items: center;
			justify-content: center;
			transition:
				background-color 0.2s,
				left 0.3s ease;
			box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
			left: 0;

			&.move-right {
				left: 200px;
			}

			&:hover {
				background-color: var(--theme-primary-color);
			}
		}
	}
</style>
