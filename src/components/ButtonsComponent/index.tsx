import { Component, createSignal, onCleanup } from "solid-js";
// import html2pdf from "html2pdf.js"; // You'll need to install this library for PDF export
import styles from "./styles.module.css";
import { useSidebarVisibleContext } from "../../context/SidebarVisibleContext";

interface ButtonsProps {
  showDelete: boolean;
  onClickAdd: (id: string, numberInputs: number, numberOutputs: number, topic: string, content: string) => void;
  onClickDelete: () => void;
  fileName: string; // Pass the file name as a prop
}

const ButtonsComponent: Component<ButtonsProps> = (props: ButtonsProps) => {
  // Signals
  const [isOpen, setIsOpen] = createSignal<boolean>(false);
  const [numberInputs, setNumberInputs] = createSignal<number>(0);
  const [numberOutputs, setNumberOutputs] = createSignal<number>(0);
  const [topic, setTopic] = createSignal<string>("");
  const [content, setContent] = createSignal<string>("");

  const { isSidebarVisible, setIsSidebarVisible } = useSidebarVisibleContext()

  // Handlers
  const handleOnClickAdd = (event: any) => {
    event.stopPropagation();
    setIsOpen(true);
  };

  const handleOnClickAddNode = (event: any) => {
    event.stopPropagation();

    // Validate number of inputs and outputs
    if (numberInputs() < 0 || numberOutputs() < 0) return;

    setIsOpen(false);
    props.onClickAdd("1", numberInputs(), numberOutputs(), topic(), content());
    setNumberInputs(0);
    setNumberOutputs(0);
  };

//   const handleDownloadPDF = () => {
//     const element = document.body;
//     const opt = {
//       margin: 1,
//       filename: "mind_map.pdf",
//       image: { type: "jpeg", quality: 0.98 },
//       html2canvas: { scale: 2 },
//       jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
//     };
//     html2pdf().from(element).set(opt).save();
//   };

  const handleChangeNumberInputs = (event: any) => setNumberInputs(event.target.value);
  const handleChangeNumberOutputs = (event: any) => setNumberOutputs(event.target.value);
  const handleChangeTopic = (event: any) => setTopic(event.target.value);
  const handleChangeContent = (event: any) => setContent(event.target.value);

  const handleClickOutsideDropwdown = () => {
    setIsOpen(false);
    setNumberInputs(0);
    setNumberOutputs(0);
  };



  return (
    <div class={styles.wrapper}>
      {/* Button to toggle sidebar visibility */}
      {!isSidebarVisible() && <button class={styles.toggleSidebarButton} onClick={() => setIsSidebarVisible(true)}>
        <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-sidebar"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line></svg>
      </button>}

      {/* Back Button */}
      <button class={styles.backButton} onClick={() => window.history.back()}>
        <svg
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 512 512"
          height="1.5em"
          width="1.5em"
        >
          <path d="M177.3 256l118.6-118.6c6.2-6.2 6.2-16.4 0-22.6s-16.4-6.2-22.6 0l-144 144c-6.2 6.2-6.2 16.4 0 22.6l144 144c6.2 6.2 16.4 6.2 22.6 0s6.2-16.4 0-22.6L177.3 256z"></path>
        </svg>
      </button>

      {/* File Name Display */}
      <div class={styles.fileNameDisplay}>
        <span>{props.fileName}</span>
      </div>

      {/* Add and Delete Buttons */}
      <button class={styles.buttonAdd} onClick={handleOnClickAdd}>
        <svg
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 448 512"
          height="1.5em"
          width="1.5em"
        >
          <path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32v144H48c-17.7 0-32 14.3-32 32s14.3 32 32 32h144v144c0 17.7 14.3 32 32 32s32-14.3 32-32V288h144c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"></path>
        </svg>
      </button>

      <button class={props.showDelete ? styles.buttonDelete : styles.buttonDeleteHidden} onClick={props.onClickDelete}>
        <svg
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 448 512"
          height="1.5em"
          width="1.5em"
        >
          <path d="M170.5 51.6L151.5 80h145l-19-28.4c-1.5-2.2-4-3.6-6.7-3.6H177.1c-2.7 0-5.2 1.3-6.7 3.6zM170.5 51.6zm147-26.6l36.7 55H424c13.3 0 24 10.7 24 24s-10.7 24-24 24h-8v304c0 44.2-35.8 80-80 80H112c-44.2 0-80-35.8-80-80V128h-8c-13.3 0-24-10.7-24-24s10.7-24 24-24h69.8l36.7-55.1c9.6-15.4 27.1-24.9 46.6-24.9h93.7c18.7 0 36.2 9.4 46.6 24.9z"></path>
        </svg>
      </button>

      {/* Download Button */}
      {/* <button class={styles.buttonDownload} onClick={handleDownloadPDF}>
        <svg
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 512 512"
          height="1.5em"
          width="1.5em"
        >
          <path d="M480 320h-64v128c0 17.67-14.33 32-32 32H128c-17.67 0-32-14.33-32-32V320H32c-6.42 0-12.28-3.81-14.97-9.71-2.69-5.9-1.92-12.85 1.97-18.03l224-320c5.83-8.31 18.17-10.47 26.48-4.64 8.32 5.83 10.47 18.17 4.64 26.48L82.27 288H176v80h160v-80h93.73L468.5 304c6.91 9.86 4.9 23.25-4.97 30.16-3.82 2.67-8.21 4.03-12.53 4.03z"></path>
        </svg>
      </button> */}

      {/* Dropdown Form */}
      <div class={isOpen() ? styles.dropdown : styles.dropdownHidden}>
        <label class={styles.label}>Number of inputs</label>
        <input class={styles.input} type="number" value={numberInputs()} onInput={handleChangeNumberInputs}></input>
        <label class={styles.label}>Number of outputs</label>
        <input class={styles.input} type="number" value={numberOutputs()} onInput={handleChangeNumberOutputs}></input>
        <label class={styles.label}>Topic</label>
        <input class={styles.input} type="text" value={topic()} onInput={handleChangeTopic}></input>
        <label class={styles.label}>Content</label>
        <input class={styles.input} type="text" value={content()} onInput={handleChangeContent}></input>
        <button class={styles.buttonRect} onClick={handleOnClickAddNode}>
          Add node
        </button>
      </div>
    </div>
  );
};

export default ButtonsComponent;
