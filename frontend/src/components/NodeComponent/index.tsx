import styles from './styles.module.css';
import { Accessor, Component, For } from "solid-js";

interface NodeProps {
	id: string;
	x: number;
	y: number;
	input_cnt: number;
	output_cnt: number;
	selected: boolean;
	on_mouse_down_node: (id: string, event: MouseEvent) => void;
	on_mouse_down_output: (output_pos_x: number, output_pos_y: number, id: string, output_index: number) => void;
	on_mouse_enter_input: (output_pos_x: number, output_pos_y: number, id: string, input_index: number) => void;
	on_mouse_leave_input: (id: string, input_index: number) => void;
}

const NodeComponent: Component<NodeProps> = (props: NodeProps) => {
	const handle_mouse_down_output = (ref: any, event: MouseEvent, index: number) => {
		event.stopPropagation();

		const center_x = ref.getBoundingClientRect().left + Math.abs(ref.getBoundingClientRect().left - ref.getBoundingClientRect().right) / 2;
		const center_y = ref.getBoundingClientRect().top + Math.abs(ref.getBoundingClientRect().bottom - ref.getBoundingClientRect().top) / 2;

		props.on_mouse_down_output(center_x, center_y, props.id, index);
	}

	const handle_mouse_enter_input = (ref: any, index: number) => {
		const center_x = ref.getBoundingClientRect().left + Math.abs(ref.getBoundingClientRect().left - ref.getBoundingClientRect().right) / 2;
		const center_y = ref.getBoundingClientRect().top + Math.abs(ref.getBoundingClientRect().bottom - ref.getBoundingClientRect().top) / 2;

		props.on_mouse_enter_input(center_x, center_y, props.id, index);
	};

	const handle_mouse_leave_input = (index: number) => {
		props.on_mouse_leave_input(props.id, index);
	};

	return (
		<div
			class={props.selected ? styles.node_selected : styles.node}
			style={{
				transform: `translate(${props.x}px, ${props.y}px)`,
			}}
			onMouseDown={(event: MouseEvent) => {
				event.stopPropagation();
				props.on_mouse_down_node(props.id, event);
			}}
		>
			<div class={styles.input_wrapper}>
				<For each={[...Array(props.input_cnt).keys()]}>
					{(_, index: Accessor<number>) => {
						let input_ref: any = null;
						return (
							<div>
								ref={input_ref}
								class={styles.input}
								onMouseEnter={() => handle_mouse_enter_input(input_ref, index())}
								onMouseLeave={() => handle_mouse_leave_input(index())}
							</div>
						);
					}}
				</For>
			</div>
			<div class={styles.output_wrapper}>
				<For each={[...Array(props.output_cnt).keys()]}>
					{(_, index: Accessor<number>) => {
						let output_ref: any = null;
						return (
							<div>
								ref={output_ref}
								class={styles.output}
								onMouseDown={(event: MouseEvent) => handle_mouse_down_output(output_ref, event, index())}
							</div>
						);
					}}
				</For>
			</div>
		</div>
	);
};

export default NodeComponent;
