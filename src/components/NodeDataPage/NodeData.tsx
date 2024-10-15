import styles from "./styles.module.css"
import cross from "../../assets/Cross.png"
import { useOverlayContext } from "../../context/OverlayContext";

interface NodeDataProps {
  title: string;
  content: string;
  onClose: () => void; // Function to close the overlay
}

const NodeData = () => {
  const { isOverlay, title, content, setIsOverlay } = useOverlayContext();

  console.log("Is overlay visible?", isOverlay())

  if (!isOverlay()) return null;  // Do not render the overlay if it is not active

  function onClose() {
    setIsOverlay(false)
    console.log(isOverlay())
  }

  return (
    <div class={styles.NodeDataPage}>
        <div class={styles.DataDisplayBox}>
            <div class={styles.closeIcon}><img class={styles.closeIcon} src={cross} onClick={onClose}/></div>
            <div class={styles.contentBox}>
                <div class={styles.Title}>{title()}</div>
                <div class={styles.content}>
                    {content()}
                </div>
            </div>
        </div>
    </div>
  )
}

export default NodeData