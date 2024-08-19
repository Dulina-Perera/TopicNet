import styles from './styles.module.css';
import { Component, createSignal, onMount } from 'solid-js';

const BoardComponent: Component = () => {
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

	};

	const handleOnMouseUpBoard = (event: MouseEvent) => {

	};

	const handleOnMouseMoveBoard = (event: MouseEvent) => {

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
