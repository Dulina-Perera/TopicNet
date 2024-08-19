import styles from './styles.module.css';
import { Component, createSignal, onMount } from 'solid-js';

const BoardComponent: Component = () => {
	const [clicked_position, set_clicked_position] = createSignal<{ x: number, y: number }>({ x: -1, y: -1 });
	const [grabbing_board, set_grabbing_board] = createSignal<boolean>(false);
	const [scale, set_scale] = createSignal<number>(1);

	onMount(() => {
		const board_element = document.getElementById('board');

		if (board_element) {
			board_element.addEventListener('wheel', (event: WheelEvent) => {
				// Set the scale of the board.
				set_scale(scale() + event.deltaY * -0.005);

				// Restrict the scale of the board.
				set_scale(Math.min(Math.max(1, scale()), 2));

				// Apply the scale to the board.
				board_element.style.transform = `scale(${scale()})`;
				board_element.style.marginTop = `${(scale() - 1) * 50}vh`
				board_element.style.marginLeft = `${(scale() - 1) * 50}vw`
			});
		}
	});

	const handleOnMouseDownBoard = (event: MouseEvent) => {
		// Start grabbing the board.
		set_grabbing_board(true);
		set_clicked_position({ x: event.x, y: event.y });
	};

	const handleOnMouseUpBoard = (event: MouseEvent) => {
		set_clicked_position({ x: -1, y: -1 });

		// Stop grabbing the board.
		set_grabbing_board(false);
	};

	const handleOnMouseMoveBoard = (event: MouseEvent) => {
		// User clicked on the board.
		if (clicked_position().x >= 0 && clicked_position().y >= 0) {
			const delta_x = event.x - clicked_position().x;
			const delta_y = event.y - clicked_position().y;

			const board_wrapper_element = document.getElementById('board_wrapper');
			if (board_wrapper_element) {
				board_wrapper_element.scrollBy(-delta_x, -delta_y);
				set_clicked_position({ x: event.x, y: event.y });
			}
		}
	};

	return (
		<div class={styles.wrapper} id="board_wrapper">
			<div
				class={grabbing_board() ? styles.board_dragging : styles.board }
				id="board"
				onMouseDown={handleOnMouseDownBoard}
				onMouseUp={handleOnMouseUpBoard}
				onMouseMove={handleOnMouseMoveBoard}
			></div>
		</div>
	);
};

export default BoardComponent;
