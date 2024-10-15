import { createSignal, For } from "solid-js";
import { useDisplayingFileContext } from "../../context/DisplayingFileContext";
import { useSidebarVisibleContext } from "../../context/SidebarVisibleContext";
import { useUserContext } from "../../context/UserContext";
import "./sidebar.css"; // Import your CSS styles

interface SidebarProps {
  files: string[]; // List of file names
  onDelete: (index: number) => void; // Function to handle file deletion
}

const Sidebar = () => {
  const [selectedIndex, setSelectedIndex] = createSignal<number>(0);
  const [files, setFiles] = createSignal<string[]>([
    "file1.pdf",
    "file2.docx",
    "file3.txt",
  ]);

  const { filename, setFilename } = useDisplayingFileContext();
  const { isSidebarVisible, setIsSidebarVisible } = useSidebarVisibleContext();
  const { username, setUsername } = useUserContext();

  setUsername("Tithra");

  setFilename(files()[0]);

  const handleDelete = (index: number) => {
    setFiles(files().filter((_, i) => i !== index));
    setFilename(files()[0]);
  };

  const handleFileClick = (index: number) => {
    setSelectedIndex(index);
    setFilename(files()[index]);
  };

  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible()); // Toggle the visibility of the sidebar
  };

  return (
    <div class={`sidebar ${isSidebarVisible() ? "visible" : ""}`}>
      <div class="top">
        <button
          title="Hide Sidebar"
          class="toggle-sidebar-btn"
          onClick={toggleSidebar}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="30px"
            height="30px"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="feather feather-sidebar"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
        </button>
        {username() && <span class="user-name">{username()}</span>}
      </div>

      <ul>
        <For each={files()}>
          {(file, index) => (
            <li
              class={selectedIndex() === index() ? "highlighted" : ""}
              onClick={() => handleFileClick(index())}
            >
              {file}
              <button class="delete-btn" onClick={() => handleDelete(index())}>
                🗑
              </button>
            </li>
          )}
        </For>
      </ul>
    </div>
  );
};

export default Sidebar;
