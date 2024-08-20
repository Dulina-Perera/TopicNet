import styles from './styles.module.css';
import { Component, createSignal } from 'solid-js';

interface ButtonProps {
	show_delete: boolean;
	on_click_add: (input_cnt: number, output_cnt: number) => void;
	on_click_delete: () => void;
}

const ButtonComponent: Component<ButtonProps> = (props: ButtonProps) => {
	/* Signals */
	const [input_cnt, set_input_cnt] = createSignal<number>(0);
	const [is_open, set_is_open] = createSignal<boolean>(false);
	const [output_cnt, set_output_cnt] = createSignal<number>(0);

	const handle_change_input_cnt = (event: InputEvent) => {
		const target: HTMLInputElement = event.target as HTMLInputElement;
		set_input_cnt(parseInt(target.value));
	};

	const handle_change_output_cnt = (event: InputEvent) => {
		const target: HTMLInputElement = event.target as HTMLInputElement;
		set_output_cnt(parseInt(target.value));
	};

	const handle_on_click_add_node = (event: Event) => {
		event.stopPropagation();

		if (input_cnt() >= 0 && input_cnt() <= 4 && output_cnt() >= 0 && output_cnt() <= 4) {
			set_is_open(false);
			props.on_click_add(input_cnt(), output_cnt());
			set_input_cnt(0);
			set_output_cnt(0);
		}
	};

	const handle_on_click_dropdown = (event: Event) => {
		event.stopPropagation();
		set_is_open(true);
	}

	return (
		<div class={styles.wrapper}>
			<button class={props.show_delete ? styles.button_delete : styles.button_delete_hidden} onClick={props.on_click_delete}>
			<svg
				fill='currentColor'
				stroke-width='0'
				xmlns='http://www.w3.org/2000/svg'
				viewBox='0 0 448 512'
				height='1em'
				width='1em'
				style='overflow: visible; color: currentcolor;'
			>
				<path d='M135.2 17.7C140.6 6.8 151.7 0 163.8 0h120.4c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64s14.3-32 32-32h96l7.2-14.3zM32 128h384v320c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16v224c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z'></path>
			</svg>
			</button>
			<button class={styles.button_add} onClick={handle_on_click_dropdown}>
				<svg
					fill='currentColor'
					stroke-width='0'
					xmlns='http://www.w3.org/2000/svg'
					viewBox='0 0 16 16'
					height='1em'
					width='1em'
					style='overflow: visible; color: currentcolor;'
				>
					<path d='M14 7v1H8v6H7V8H1V7h6V1h1v6h6z'></path>
				</svg>
			</button>
			<div class={is_open() ? styles.dropdown : styles.dropdown_hidden}>
				<label class={styles.label}>Number of Inputs</label>
				<input class={styles.input} type='number' value={input_cnt()} onInput={handle_change_input_cnt}></input>
				<label class={styles.label}>Number of Outputs</label>
				<input class={styles.input} type='number' value={output_cnt()} onInput={handle_change_output_cnt}></input>
				<button class={styles.button_rect} onClick={handle_on_click_add_node}>
					Add Node
				</button>
			</div>
		</div>
	);
};

export default ButtonComponent;
