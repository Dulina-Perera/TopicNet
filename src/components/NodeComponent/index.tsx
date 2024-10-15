import { Accessor, Component, For, createEffect, createSignal } from "solid-js";
import styles from "./styles.module.css";
import NodeData from "../NodeDataPage/NodeData";
import { useOverlayContext } from "../../context/OverlayContext";

interface NodeProps {
    id: string;
    x: number;
    y: number;
    numberInputs: number;
    numberOutputs: number;
    selected: boolean;
    topic : string;
    content : string;
    onMouseDownNode: (id: string, event: any) => void;
    onMouseDownOutput: (outputPositionX: number, outputPositionY: number, nodeId: string, outputIndex: number) => void;
    onMouseEnterInput: (inputPositionX: number, inputPositionY: number, nodeId: string, outputIndex: number) => void;
    onMouseLeaveInput: (nodeId: string, inputIndex: number) => void;
}

const NodeComponent: Component<NodeProps> = (props: NodeProps) => {
    const { setIsOverlay, setTitle, setContent, isOverlay, title, content } = useOverlayContext()


    // Handlers
    function handleMouseDownOutput(ref: any, event: any, outputIndex: number) {
        // Disable drag node
        event.stopPropagation();

        const centerX =
            ref.getBoundingClientRect().left + Math.abs(ref.getBoundingClientRect().right - ref.getBoundingClientRect().left) / 2;
        const centerY =
            ref.getBoundingClientRect().top + Math.abs(ref.getBoundingClientRect().bottom - ref.getBoundingClientRect().top) / 2;

        props.onMouseDownOutput(centerX, centerY, props.id, outputIndex);
    }

    function handleMouseEnterInput(ref: any, inputIndex: number) {
        const centerX =
            ref.getBoundingClientRect().left + Math.abs(ref.getBoundingClientRect().right - ref.getBoundingClientRect().left) / 2;
        const centerY =
            ref.getBoundingClientRect().top + Math.abs(ref.getBoundingClientRect().bottom - ref.getBoundingClientRect().top) / 2;

        props.onMouseEnterInput(centerX, centerY, props.id, inputIndex);
    }

    function handleMouseLeaveInput(inputIndex: number) {
        props.onMouseLeaveInput(props.id, inputIndex);
    }

    const handleContentButtonClick = () => {
        console.log("Rendering overlay....")
        setTitle(props.topic);  // Set the title of the overlay
        setContent(props.content);  // Set the content of the overlay
        setIsOverlay(true);  // Show the overlay
        console.log("Overlay : ", isOverlay())
        console.log("Title : ", title())
        console.log("Content : ", content())
      };

    return (
        <div
            class={props.selected ? styles.nodeSelected : styles.node}
            style={{
                transform: `translate(${props.x}px, ${props.y}px)`,
            }}
            onMouseDown={(event: any) => {
                // Prevent click on board
                event.stopPropagation();

                props.onMouseDownNode(props.id, event);
            }}
        >
            <div class={styles.inputsWrapper}>
                <For each={[...Array(Number(props.numberInputs)).keys()]}>
                    {(_, index: Accessor<number>) => {
                        let inputRef: any = null;
                        return (
                            <div
                                ref={inputRef}
                                class={styles.input}
                                onMouseEnter={() => handleMouseEnterInput(inputRef, index())}
                                onMouseLeave={() => handleMouseLeaveInput(index())}
                            ></div>
                        );
                    }}
                </For>
            </div>
            
            <h6>{props.topic}</h6>
            
            {/* <p style={{ 
            "max-height": "200px", 
            "overflow-y": "auto", 
            "padding": "0px", 
            "border": "1px solid #ccc" 
            }}>
                {props.content}
            </p> */}
            <button class="content-btn" onClick={handleContentButtonClick}>Content</button>
            
            <div class={styles.outputsWrapper}>
                <For each={[...Array(Number(props.numberOutputs)).keys()]}>
                    {(_, index: Accessor<number>) => {
                        let outputRef: any = null;
                        return (
                            <div
                                ref={outputRef}
                                class={styles.output}
                                onMouseDown={(event: any) => handleMouseDownOutput(outputRef, event, index())}
                            ></div>
                        );
                    }}
                </For>
                
            </div>
            
        </div>
    );
};

export default NodeComponent;
