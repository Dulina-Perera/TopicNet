import styles from './styles.module.css';
import { Component, createSignal } from 'solid-js';

const BoardComponent: Component = () => {
	const [grabbing_board, set_grabbing_board] = createSignal<boolean>(false);

	return (
		<div class={styles.wrapper} id="board_wrapper">
			<div class={grabbing_board() ? styles.board_dragging : styles.board } id="board"></div>
		</div>
	);
};

export default BoardComponent;
