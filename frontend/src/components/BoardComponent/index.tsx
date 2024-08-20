import ButtonComponent from '../ButtonComponent';
import styles from './styles.module.css';
import { Component, createSignal, onMount } from 'solid-js';

const BoardComponent: Component = () => {
	/* Signals */
	const [clicked_position, set_clicked_position] = createSignal<{ x: number, y: number }>({ x: -1, y: -1 });
	const [grabbing_board, set_grabbing_board] = createSignal<boolean>(false);
	const [scale, set_scale] = createSignal<number>(1);
	const [selected_node, set_selected_node] = createSignal<string | null>(null);

	onMount(() => {
		const board_element: HTMLElement | null = document.getElementById('board');

		if (board_element) {
			board_element.addEventListener(
				'wheel',
				(event: WheelEvent) => {
					set_scale(scale() + event.deltaY * -0.005); // Set the scale of the board.
					set_scale(Math.min(Math.max(1, scale()), 2)); // Restrict the scale of the board.

					// Apply the scale to the board.
					board_element.style.transform = `scale(${scale()})`;
					board_element.style.marginTop = `${(scale() - 1) * 50}vh`;
					board_element.style.marginLeft = `${(scale() - 1) * 50}vw`;
				},
				{ passive: false }
			);
		}
	});

	const handle_on_mouse_down_board = (event: MouseEvent) => {
		set_grabbing_board(true);
		set_clicked_position({ x: event.x, y: event.y });
	};

	const handle_on_mouse_up_board = (event: MouseEvent) => {
		set_clicked_position({ x: -1, y: -1 });
		set_grabbing_board(false);
	};

	const handle_on_mouse_move_board = (event: MouseEvent) => {
		if (clicked_position().x >= 0 && clicked_position().y >= 0) {
			const delta_x: number = event.x - clicked_position().x;
			const delta_y: number = event.y - clicked_position().y;

			const board_wrapper_element: HTMLElement | null = document.getElementById('board_wrapper');
			if (board_wrapper_element) {
				board_wrapper_element.scrollBy(-delta_x, -delta_y);
				set_clicked_position({ x: event.x, y: event.y });
			}
		}
	};

	const handle_on_click_add = (number_inputs: number, number_outputs: number) => {

	};

	const handle_on_click_delete = () => {

	};

	return (
		<div class={styles.wrapper} id='board_wrapper'>
			<ButtonComponent show_delete={selected_node() !== null} on_click_add={handle_on_click_add} on_click_delete={handle_on_click_delete}></ButtonComponent>
			<div
				class={grabbing_board() ? styles.board_dragging : styles.board}
				id='board'
				onMouseDown={handle_on_mouse_down_board}
				onMouseUp={handle_on_mouse_up_board}
				onMouseMove={handle_on_mouse_move_board}
			></div>
		</div>
	);
};

export default BoardComponent;
