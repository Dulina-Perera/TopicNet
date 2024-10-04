<script lang="ts">
	import { boardClickedPosition, grabbingBoard, boardScale } from "$lib/stores";
	import { onMount } from "svelte";

	$: clickedPosition = $boardClickedPosition;
	$: grabbing = $grabbingBoard;
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
		grabbingBoard.set(true);
		boardClickedPosition.set({ x: event.clientX, y: event.clientY });
	};

	const handleMouseUp = () => {
		boardClickedPosition.set({ x: -1, y: -1 });
		grabbingBoard.set(false);
	};

	const handleMouseMove = (event: MouseEvent) => {
		if (clickedPosition.x >= 0 && clickedPosition.y >= 0) {
			const deltaX: number = event.clientX - clickedPosition.x;
			const deltaY: number = event.clientY - clickedPosition.y;

			const boardWrapper: HTMLElement | null = document.getElementById("board-wrapper");
			if (boardWrapper) {
				boardWrapper.scrollLeft -= deltaX;
				boardWrapper.scrollTop -= deltaY;

				boardClickedPosition.set({ x: event.clientX, y: event.clientY });
			}
		}
	};
</script>

<div
	class="fixed h-screen left-0 overflow-scroll top-0 w-screen"
	id="board-wrapper"
>
	<!-- svelte-ignore a11y-no-static-element-interactions -->
	<div
		class={`
			${grabbing ? "cursor-grabbing" : "cursor-grab"}
			bg-[length:30px_30px] bg-[radial-gradient(circle,#b8b8b8bf_1px,rgba(0,0,0,0)_1px)] h-screen relative w-screen
		`}
		id="board"
		on:mousedown={handleMouseDown}
		on:mouseup={handleMouseUp}
		on:mousemove={handleMouseMove}
	></div>
</div>
