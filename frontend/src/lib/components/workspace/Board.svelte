<script lang="ts">
	import { boardClickedPos, boardDraggable, boardGrabbing, boardScale } from "$lib/stores/workspace.store";
	import { onMount } from "svelte";

	$: clickedPos = $boardClickedPos;
	$: draggable = $boardDraggable;
	$: grabbing = $boardGrabbing;
	$: scale = $boardScale;

	onMount(() => {
		const board: HTMLElement | null = document.getElementById("board");

		if (board) {
			board.addEventListener(
				"wheel",
				(event: WheelEvent) => {
					boardScale.update((prev) => {
						let newScale: number = prev + event.deltaY * -0.005;
						newScale = Math.min(Math.max(newScale, 1), 2);

						return newScale;
					});

					board.style.transform = `scale(${scale})`;
					board.style.marginTop = `${(scale - 1) * 50}vh`;
					board.style.marginLeft = `${(scale - 1) * 50}vw`;
				},
				{ passive: false }
			)
		}
	});

	const handleMouseDown = (event: MouseEvent) => {
		if (draggable) {
			boardGrabbing.set(true);
			boardClickedPos.set({ x: event.clientX, y: event.clientY });
		}
	};

	const handleMouseUp = () => {
		boardClickedPos.set({ x: -1, y: -1 });
		boardGrabbing.set(false);
	};

	const handleMouseMove = (event: MouseEvent) => {
		if (draggable && clickedPos.x >= 0 && clickedPos.y >= 0) {
			const deltaX: number = event.clientX - clickedPos.x;
			const deltaY: number = event.clientY - clickedPos.y;

			const boardWrapper: HTMLElement | null = document.getElementById("board-wrapper");
			if (boardWrapper) {
				boardWrapper.scrollLeft -= deltaX;
				boardWrapper.scrollTop -= deltaY;

				boardClickedPos.set({ x: event.clientX, y: event.clientY });
			}
		}
	};
</script>

<div id="board-wrapper">
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div
		class={`${draggable && grabbing ? "grabbing" : draggable ? "grab" : ""}`}
		id="board"
		on:mousedown={handleMouseDown}
		on:mousemove={handleMouseMove}
		on:mouseup={handleMouseUp}
	>
		<slot />
	</div>
</div>

<style lang="scss">
  #board-wrapper {
    height: 100vh;
    overflow: auto;
    position: fixed;
    width: 100vw;
  }

  #board {
    background-image: radial-gradient(circle, #b8b8b8bf 1px, rgba(0, 0, 0, 0) 1px);
    background-size: 30px 30px;
    height: 100%;
    position: relative;
    transform-origin: 0 0;
    width: 100%;

    &.grab {
      cursor: grab;
    }

    &.grabbing {
      cursor: grabbing;
    }
  }
</style>
