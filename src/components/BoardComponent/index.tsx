import { useNavigate } from "@solidjs/router";
import {
  Accessor,
  Component,
  For,
  Setter,
  createEffect,
  createResource,
  createSignal,
  onMount,
} from "solid-js";
import { useOverlayContext } from "../../context/OverlayContext";
import ButtonsComponent from "../ButtonsComponent";
import EdgeComponent from "../EdgeComponent";
import NodeComponent from "../NodeComponent";
import NodeData from "../NodeDataPage/NodeData";
import Sidebar from "../Sidebar/Sidebar";
import styles from "./styles.module.css";
import { useDisplayingFileContext } from "../../context/DisplayingFileContext";
import { useSidebarVisibleContext } from "../../context/SidebarVisibleContext";

function createNodeMap(
  nodes: [
    { node_id: string; parent_id: string; topic: string; content: string }
  ]
): Map<string, string[]> {
  const nodeMap = new Map();

  nodes.forEach((node) => {
    if (!nodeMap.has(node.node_id)) {
      nodeMap.set(node.node_id, []);
    }

    if (node.node_id !== "0") {
      if (!nodeMap.has(node.parent_id)) {
        nodeMap.set(node.parent_id, []);
      }

      nodeMap.get(node.parent_id).push(node.node_id);
    }
  });

  return nodeMap;
}
const fetchProducts = async () => {
  const res = await fetch("http://localhost:4000/nodes");
  return res.json();

  // try {

  //   const res = await fetch(`http://localhost:8000/generate`, {
  //     method: 'POST',
  //     body: localStorage.getItem("file_path"),
  //   });

  //   if (res.ok) {

  //     const data = await res.json();
  //     return data.nodes;

  //   } else {
  //     console.log('Failed to upload file.');
  //   }
  // } catch (error) {
  //   console.log('An error occurred. Please try again.');
  // }
};

interface Node {
  id: string;
  numberInputs: number;
  numberOutputs: number;
  topic: string;
  content: string;
  prevPosition: {
    get: Accessor<{ x: number; y: number }>;
    set: Setter<{ x: number; y: number }>;
  };
  currPosition: {
    get: Accessor<{ x: number; y: number }>;
    set: Setter<{ x: number; y: number }>;
  };
  inputEdgeIds: { get: Accessor<string[]>; set: Setter<string[]> };
  outputEdgeIds: { get: Accessor<string[]>; set: Setter<string[]> };
}

interface Edge {
  id: string;
  nodeStartId: string;
  nodeEndId: string;
  inputIndex: number;
  outputIndex: number;
  prevStartPosition: {
    get: Accessor<{ x: number; y: number }>;
    set: Setter<{ x: number; y: number }>;
  };
  currStartPosition: {
    get: Accessor<{ x: number; y: number }>;
    set: Setter<{ x: number; y: number }>;
  };
  prevEndPosition: {
    get: Accessor<{ x: number; y: number }>;
    set: Setter<{ x: number; y: number }>;
  };
  currEndPosition: {
    get: Accessor<{ x: number; y: number }>;
    set: Setter<{ x: number; y: number }>;
  };
}

const BoardComponent: Component = () => {
  const [products] = createResource(fetchProducts);
  const [hasRun, setHasRun] = createSignal(false);
  const navigate = useNavigate();
  // createEffect(() => {
  //   const verifyToken = async () => {
  //     const token = localStorage.getItem('token');
  //       console.log(token)
  //     try {
  //       const response = await fetch(`http://localhost:8000/verify-token/${token}`);

  //       if (!response.ok) {
  //         throw new Error('Token verification failed');
  //       }
  //     } catch (error) {
  //       localStorage.removeItem('token');
  //       navigate('/login');
  //     }
  //   };

  //   verifyToken();
  // }, [navigate]);

  // Signals
  const [grabbingBoard, setGrabbingBoard] = createSignal<boolean>(false);
  const [selectedNode, setSelectedNode] = createSignal<string | null>(null);
  const [selectedEdge, setSelectedEdge] = createSignal<string | null>(null);
  const [newEdge, setNewEdge] = createSignal<Edge | null>(null);
  const [insideInput, setInsideInput] = createSignal<{
    nodeId: string;
    inputIndex: number;
    positionX: number;
    positionY: number;
  } | null>(null);

  const [clickedPosition, setClickedPosition] = createSignal<{
    x: number;
    y: number;
  }>({ x: -1, y: -1 });

  const [nodes, setNodes] = createSignal<Node[]>([]);
  const [edges, setEdges] = createSignal<Edge[]>([]);
  const [scale, setScale] = createSignal<number>(1);

  const { isOverlay } = useOverlayContext();

  const { filename } = useDisplayingFileContext()

  const { isSidebarVisible } = useSidebarVisibleContext()

  onMount(() => {
    const boardElement = document.getElementById("board");

    if (boardElement) {
      // boardElement.addEventListener(
      //     "wheel",
      //     (event) => {
      //         // Update scale
      //         setScale(scale() + event.deltaY * -0.005);
      //         // Restrict scale
      //         setScale(Math.min(Math.max(1, scale()), 2));
      //         // Apply scale transform
      //         boardElement.style.transform = `scale(${scale()})`;
      //         boardElement.style.marginTop = `${(scale() - 1) * 50}vh`;
      //         boardElement.style.marginLeft = `${(scale() - 1) * 50}vw`;
      //     },
      //     { passive: false }
      // );
    }
  });

  // Handlers
  function handleOnMouseDownBoard(event: any) {
    // Deselect node
    setSelectedNode(null);

    // Deselect edge
    setSelectedEdge(null);

    // Start grabbing board
    setGrabbingBoard(true);
    setClickedPosition({ x: event.x, y: event.y });
  }

  function handleOnMouseUpBoard() {
    setClickedPosition({ x: -1, y: -1 });

    // Stop grabbing board
    setGrabbingBoard(false);

    // If a new edge is being set and is not inside input
    if (newEdge() !== null && insideInput() === null) {
      setNewEdge(null);
    }

    // If a new edge is being set and is inside input
    if (newEdge() !== null && insideInput() !== null) {
      const nodeStartId = newEdge()!.nodeStartId;
      const nodeEndId = insideInput()!.nodeId;

      const nodeStart = nodes().find((node) => node.id === nodeStartId);
      const nodeEnd = nodes().find((node) => node.id === nodeEndId);

      const boardWrapperElement = document.getElementById("boardWrapper");

      if (nodeStart && nodeEnd && boardWrapperElement) {
        const edgeId = `edge_${nodeStart.id}_${newEdge()?.outputIndex}_${
          nodeEnd.id
        }_${insideInput()?.inputIndex}`;

        if (
          nodeStart.outputEdgeIds.get().includes(edgeId) &&
          nodeEnd.inputEdgeIds.get().includes(edgeId)
        ) {
          setNewEdge(null);
          return;
        }

        nodeStart.outputEdgeIds.set([...nodeStart.outputEdgeIds.get(), edgeId]);
        nodeEnd.inputEdgeIds.set([...nodeEnd.inputEdgeIds.get(), edgeId]);

        // Update edge current positions
        newEdge()!.prevStartPosition.set((_) => {
          return {
            x:
              (newEdge()!.currStartPosition.get().x +
                boardWrapperElement.scrollLeft) /
              scale(),
            y:
              (newEdge()!.currStartPosition.get().y +
                boardWrapperElement.scrollTop) /
              scale(),
          };
        });

        newEdge()!.prevEndPosition.set((_) => {
          return {
            x:
              (insideInput()!.positionX + boardWrapperElement.scrollLeft) /
              scale(),
            y:
              (insideInput()!.positionY + boardWrapperElement.scrollTop) /
              scale(),
          };
        });

        newEdge()!.currEndPosition.set((_) => {
          return {
            x:
              (insideInput()!.positionX + boardWrapperElement.scrollLeft) /
              scale(),
            y:
              (insideInput()!.positionY + boardWrapperElement.scrollTop) /
              scale(),
          };
        });

        // Add new edge
        setEdges([
          ...edges(),
          {
            ...newEdge()!,
            id: edgeId,
            nodeEndId: nodeEnd.id,
            nodeEndInputIndex: insideInput()!.inputIndex,
          },
        ]);
        setNewEdge(null);
      }
    }
  }

  function handleOnMouseMove(event: any) {
    // User clicked somewhere
    if (clickedPosition().x >= 0 && clickedPosition().y >= 0) {
      // User clicked on node
      if (selectedNode() !== null) {
        const deltaX = event.x - clickedPosition().x;
        const deltaY = event.y - clickedPosition().y;

        const node = nodes().find((node) => node.id === selectedNode());
        if (node) {
          // Update node position
          node.currPosition.set((_) => {
            return {
              x: (node.prevPosition.get().x + deltaX) / scale(),
              y: (node.prevPosition.get().y + deltaY) / scale(),
            };
          });

          // Update input edges positions
          for (let i = 0; i < node.inputEdgeIds.get().length; i++) {
            const edgeId = node.inputEdgeIds.get()[i];
            const edge = edges().find((edge) => edge.id === edgeId);
            if (edge) {
              edge.currEndPosition.set((_) => {
                return {
                  x: (edge.prevEndPosition.get().x + deltaX) / scale(),
                  y: (edge.prevEndPosition.get().y + deltaY) / scale(),
                };
              });
            }
          }

          // Update output edges positions
          for (let i = 0; i < node.outputEdgeIds.get().length; i++) {
            const edgeId = node.outputEdgeIds.get()[i];
            const edge = edges().find((edge) => edge.id === edgeId);
            if (edge) {
              edge.currStartPosition.set((_) => {
                return {
                  x: (edge.prevStartPosition.get().x + deltaX) / scale(),
                  y: (edge.prevStartPosition.get().y + deltaY) / scale(),
                };
              });
            }
          }
        }
      }
      // User clicked on board, move board
      else {
        const deltaX = event.x - clickedPosition().x;
        const deltaY = event.y - clickedPosition().y;

        const boardWrapperElement = document.getElementById("boardWrapper");
        if (boardWrapperElement) {
          boardWrapperElement.scrollBy(-deltaX, -deltaY);
          setClickedPosition({ x: event.x, y: event.y });
        }
      }
    }

    // User is setting new edge
    if (newEdge() !== null) {
      const boardWrapperElement = document.getElementById("boardWrapper");
      if (boardWrapperElement) {
        newEdge()?.currEndPosition.set({
          x: (event.x + boardWrapperElement.scrollLeft) / scale(),
          y: (event.y + +boardWrapperElement.scrollTop) / scale(),
        });
      }
    }
  }

  function handleOnMouseDownNode(id: string, event: any) {
    // Deselect edge
    setSelectedEdge(null);

    // Select node
    setSelectedNode(id);

    // Update first click position
    setClickedPosition({ x: event.x, y: event.y });

    const node = nodes().find((node) => node.id === selectedNode());
    if (node) {
      // Update node position
      node.prevPosition.set((_) => {
        return {
          x: node.currPosition.get().x * scale(),
          y: node.currPosition.get().y * scale(),
        };
      });

      // Update input edges positions
      for (let i = 0; i < node.inputEdgeIds.get().length; i++) {
        const edgeId = node.inputEdgeIds.get()[i];
        const edge = edges().find((edge) => edge.id === edgeId);
        if (edge) {
          edge.prevEndPosition.set((_) => {
            return {
              x: edge.currEndPosition.get().x * scale(),
              y: edge.currEndPosition.get().y * scale(),
            };
          });
        }
      }

      // Update output edges positions
      for (let i = 0; i < node.outputEdgeIds.get().length; i++) {
        const edgeId = node.outputEdgeIds.get()[i];
        const edge = edges().find((edge) => edge.id === edgeId);
        if (edge) {
          edge.prevStartPosition.set((_) => {
            return {
              x: edge.currStartPosition.get().x * scale(),
              y: edge.currStartPosition.get().y * scale(),
            };
          });
        }
      }
    }
  }

  function handleOnClickAdd(
    id: string,
    numberInputs: number,
    numberOutputs: number,
    topic: string,
    content: string
  ) {
    // Create random positions
    const randomX = Math.random() * window.innerWidth;
    const randomY = Math.random() * window.innerHeight;

    // Create signal
    const [nodePrev, setNodePrev] = createSignal<{ x: number; y: number }>({
      x: randomX,
      y: randomY,
    });
    const [nodeCurr, setNodeCurr] = createSignal<{ x: number; y: number }>({
      x: randomX,
      y: randomY,
    });
    const [inputsEdgesIds, setInputsEdgesIds] = createSignal<string[]>([]);
    const [outputsEdgesIds, setOutputsEdgesIds] = createSignal<string[]>([]);

    // Update global nodes array
    setNodes([
      ...nodes(),
      {
        // id: `node_${Math.random().toString(36).substring(2, 8)}`,
        id: id,
        numberInputs: numberInputs,
        numberOutputs: numberOutputs,
        topic: topic,
        content: content,
        prevPosition: { get: nodePrev, set: setNodePrev },
        currPosition: { get: nodeCurr, set: setNodeCurr },
        inputEdgeIds: { get: inputsEdgesIds, set: setInputsEdgesIds },
        outputEdgeIds: { get: outputsEdgesIds, set: setOutputsEdgesIds },
      },
    ]);
  }

  function handleOnClickDelete() {
    // Find node in global nodes array
    const node = nodes().find((node) => node.id === selectedNode());

    // Check if node exists
    if (!node) {
      setSelectedNode(null);
      return;
    }

    // Delete node edges
    const inputs = node.inputEdgeIds.get();
    const outputs = node.outputEdgeIds.get();

    // Get all unique edges to delete
    const allEdges = [...inputs, ...outputs];
    const uniqueEdges = allEdges.filter((value, index, array) => {
      return array.indexOf(value) === index;
    });

    // Delete edges from correspondent nodes data
    for (let i = 0; i < uniqueEdges.length; i++) {
      const edge = edges().find((edge) => edge.id === uniqueEdges[i]);
      if (edge) {
        const nodeStart = nodes().find((node) => node.id === edge.nodeStartId);
        const nodeEnd = nodes().find((node) => node.id === edge.nodeEndId);

        nodeStart?.outputEdgeIds.set([
          ...nodeStart.outputEdgeIds
            .get()
            .filter((edgeId) => edgeId !== uniqueEdges[i]),
        ]);
        nodeEnd?.inputEdgeIds.set([
          ...nodeEnd.inputEdgeIds
            .get()
            .filter((edgeId) => edgeId !== uniqueEdges[i]),
        ]);

        // Delete edge from global data
        setEdges([...edges().filter((e) => edge.id !== e.id)]);
      }
    }

    // Delete node
    setNodes([...nodes().filter((node) => node.id !== selectedNode())]);
    setSelectedNode(null);
  }

  function handleOnMouseDownOutput(
    outputPositionX: number,
    outputPositionY: number,
    nodeId: string,
    outputIndex: number
  ) {
    // Deselect node
    setSelectedNode(null);

    const boardWrapperElement = document.getElementById("boardWrapper");

    if (boardWrapperElement) {
      // Create edge position signals with updated scale value
      const [prevEdgeStart, setPrevEdgeStart] = createSignal<{
        x: number;
        y: number;
      }>({
        x: (outputPositionX + boardWrapperElement.scrollLeft) / scale(),
        y: (outputPositionY + boardWrapperElement.scrollTop) / scale(),
      });
      const [currEdgeStart, setCurrEdgeStart] = createSignal<{
        x: number;
        y: number;
      }>({
        x: (outputPositionX + boardWrapperElement.scrollLeft) / scale(),
        y: (outputPositionY + boardWrapperElement.scrollTop) / scale(),
      });
      const [prevEdgeEnd, setPrevEdgeEnd] = createSignal<{
        x: number;
        y: number;
      }>({
        x: (outputPositionX + boardWrapperElement.scrollLeft) / scale(),
        y: (outputPositionY + boardWrapperElement.scrollTop) / scale(),
      });
      const [currEdgeEnd, setCurrEdgeEnd] = createSignal<{
        x: number;
        y: number;
      }>({
        x: (outputPositionX + boardWrapperElement.scrollLeft) / scale(),
        y: (outputPositionY + boardWrapperElement.scrollTop) / scale(),
      });

      setNewEdge({
        id: "",
        nodeStartId: nodeId,
        outputIndex: outputIndex,
        nodeEndId: "",
        inputIndex: -1,
        prevStartPosition: { get: prevEdgeStart, set: setPrevEdgeStart },
        currStartPosition: { get: currEdgeStart, set: setCurrEdgeStart },
        prevEndPosition: { get: prevEdgeEnd, set: setPrevEdgeEnd },
        currEndPosition: { get: currEdgeEnd, set: setCurrEdgeEnd },
      });
    }
  }

  function handleOnMouseEnterInput(
    inputPositionX: number,
    inputPositionY: number,
    nodeId: string,
    inputIndex: number
  ) {
    setInsideInput({
      nodeId,
      inputIndex,
      positionX: inputPositionX,
      positionY: inputPositionY,
    });
  }

  function handleOnMouseLeaveInput(nodeId: string, inputIndex: number) {
    if (
      insideInput() !== null &&
      insideInput()?.nodeId === nodeId &&
      insideInput()?.inputIndex === inputIndex
    )
      setInsideInput(null);
  }

  function handleOnMouseDownEdge(edgeId: string) {
    // Deselect node
    setSelectedNode(null);

    // Select edge
    setSelectedEdge(edgeId);
  }

  function handleOnDeleteEdge(edgeId: string) {
    const edge = edges().find((e) => e.id === edgeId);

    if (edge) {
      // Delete edge from start node
      const nodeStart = nodes().find((n) => n.id === edge.nodeStartId);
      if (nodeStart) {
        nodeStart.outputEdgeIds.set([
          ...nodeStart.outputEdgeIds
            .get()
            .filter((edgeId) => edgeId !== edge.id),
        ]);
      }

      // Delete edge from end node
      const nodeEnd = nodes().find((n) => n.id === edge.nodeEndId);
      if (nodeEnd) {
        nodeEnd.inputEdgeIds.set([
          ...nodeEnd.inputEdgeIds.get().filter((edgeId) => edgeId !== edge.id),
        ]);
      }

      // Delete edge from global edges array
      setEdges([...edges().filter((e) => e.id !== edge.id)]);
    }
  }

  //
  function addAutoedge(nodeId1: string, nodeId2: string) {
    // console.log(nodeId1)
    // console.log(nodeId2)

    // console.log(nodes())

    const newNode1 = nodes().find((node) => node.id === nodeId1);
    const newNode2 = nodes().find((node) => node.id === nodeId2); // Get the newly added node with one input

    // console.log(newNode1)
    // console.log(newNode2)

    if (newNode1 && newNode2) {
      const edgeId = `edge_${newNode1.id}_${newNode1.outputEdgeIds.get()[0]}_${
        newNode2.id
      }_${newNode2.inputEdgeIds.get()[0]}`;

      // Add edge to both nodes' edge lists
      newNode1.outputEdgeIds.set([...newNode1.outputEdgeIds.get(), edgeId]);
      newNode2.inputEdgeIds.set([...newNode2.inputEdgeIds.get(), edgeId]);

      // Create and add the edge

      const newEdge: Edge = {
        id: edgeId,
        nodeStartId: newNode1.id,
        nodeEndId: newNode2.id,
        outputIndex: 0,
        inputIndex: 0,
        prevStartPosition: {
          get: () => newNode1.currPosition.get(),
          set: () => (newPosition: { x: number; y: number }) =>
            newNode1.currPosition.set(newPosition),
        },
        currStartPosition: {
          get: () => newNode1.currPosition.get(),
          set: () => (newPosition: { x: number; y: number }) =>
            newNode1.currPosition.set(newPosition),
        },
        prevEndPosition: {
          get: () => newNode2.currPosition.get(),
          set: () => (newPosition: { x: number; y: number }) =>
            newNode2.currPosition.set(newPosition),
        },
        currEndPosition: {
          get: () => newNode2.currPosition.get(),
          set: () => (newPosition: { x: number; y: number }) =>
            newNode2.currPosition.set(newPosition),
        },
      };

      setEdges([...edges(), newEdge]);

      // Add new edge
      // setEdges([
      //     ...edges(),
      //     {
      //         ...newEdge()!,
      //         id: edgeId,
      //         nodeStartId: newNode1.id,
      //         nodeEndId: newNode2.id,
      //         inputIndex: 0,
      //         outputIndex: 0
      //     },
      // ]);
      // setNewEdge(null);
    }
  }


  createEffect(() => {
    // Ensure products() is available before proceeding
    if (products() && !hasRun()) {
      // Map over the products to handle each one
      products().map(
        (product: {
          node_id: string;
          topic: string;
          content: string;
          num_inputs: number;
          num_outputs: number;
        }) => {
          handleOnClickAdd(
            product.node_id,
            0,
            0,
            product.topic,
            product.content
          );
        }
      );

      // Create a node map from the products
      const hashMap: Map<string, string[]> = createNodeMap(products());
      console.log(hashMap);

      // Iterate over the hashMap and handle each key-value pair
      hashMap.forEach((values: string[], key: string) => {
        console.log(values); // Log the values array for each key

        values.forEach((value: string) => {
          console.log(`Key: ${key}, Value: ${value}`);
          addAutoedge(key, value);
        });
      });
      setHasRun(true);
    }
  });

  return (
    <div id="boardWrapper" class={styles.wrapper}>
      <Sidebar />
      {/* <button onclick={
                ()=>{
                    products()?.map((product: { node_id:string,topic: string; content: string; num_inputs: number, num_outputs:number})=>{
                        // console.log(product.node_id);
                        handleOnClickAdd(product.node_id ,0, 0, product.topic, product.content);
                    })

                    

                    const hashMap: Map<string, string[]> = createNodeMap(products());
                    console.log(hashMap);

                    hashMap.forEach((values: string[], key: string) => {
                        console.log(values);  // Log the values array for each key
                        
                        values.forEach((value: string) => {
                            console.log(`Key: ${key}, Value: ${value}`);
                            addAutoedge(key,value);
                        });
                    });


                }
            }>check</button> */}
      <ButtonsComponent
        showDelete={selectedNode() !== null}
        onClickAdd={handleOnClickAdd}
        onClickDelete={handleOnClickDelete}
        fileName= { filename() }
      />

      <div
        id="board"
        class={grabbingBoard() ? isSidebarVisible() ? styles.boardSidebarVisible : styles.boardDragging : isSidebarVisible() ? styles.board_with_sidebar : styles.board}
        onMouseDown={handleOnMouseDownBoard}
        onMouseUp={handleOnMouseUpBoard}
        onMouseMove={handleOnMouseMove}
      >
        <For each={nodes()}>
          {(node: Node) => (
            <NodeComponent
              id={node.id}
              x={node.currPosition.get().x}
              y={node.currPosition.get().y}
              numberInputs={node.numberInputs}
              numberOutputs={node.numberOutputs}
              selected={selectedNode() === node.id}
              topic={node.topic}
              content={node.content}
              onMouseDownNode={handleOnMouseDownNode}
              onMouseDownOutput={handleOnMouseDownOutput}
              onMouseEnterInput={handleOnMouseEnterInput}
              onMouseLeaveInput={handleOnMouseLeaveInput}
            />
          )}
        </For>

        {isOverlay() && <NodeData />}

        {newEdge() !== null && (
          <EdgeComponent
            selected={false}
            isNew={true}
            position={{
              x0: newEdge()!.currStartPosition.get().x,
              y0: newEdge()!.currStartPosition.get().y,
              x1: newEdge()!.currEndPosition.get().x,
              y1: newEdge()!.currEndPosition.get().y,
            }}
            onMouseDownEdge={() => {}}
            onClickDelete={() => {}}
          />
        )}
        <For each={edges()}>
          {(edge: Edge) => (
            <EdgeComponent
              selected={selectedEdge() === edge.id}
              isNew={false}
              position={{
                x0: edge.currStartPosition.get().x,
                y0: edge.currStartPosition.get().y,
                x1: edge.currEndPosition.get().x,
                y1: edge.currEndPosition.get().y,
              }}
              onMouseDownEdge={() => handleOnMouseDownEdge(edge.id)}
              onClickDelete={() => handleOnDeleteEdge(edge.id)}
            />
          )}
        </For>
      </div>
    </div>
  );
};

export default BoardComponent;
