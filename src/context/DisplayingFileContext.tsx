import { createContext, createSignal, useContext } from "solid-js";

// Define the context type
interface DisplayingFileContextType {
  filename: () => string; // Signal accessor
  setFilename: (value: string) => void;
}

// Create the context with a default value (can be null initially)
const DisplayingFileContext = createContext<DisplayingFileContextType | undefined>(undefined);

// Provider component
function DisplayingFileContextProvider(props: { children: any }) {
  // Reactive signals
  const [filename, setFilename] = createSignal<string>("");

  // Pass the signal functions themselves (not the invoked values)
  const value: DisplayingFileContextType = {
    filename, // Pass the signal accessor
    setFilename,
  };

  return (
    <DisplayingFileContext.Provider value={value}>{props.children}</DisplayingFileContext.Provider>
  );
}

// Hook to access context easily
function useDisplayingFileContext() {
  const context = useContext(DisplayingFileContext);
  if (!context) {
    throw new Error(
      "useOverlayContext must be used within an OverlayContextProvider"
    );
  }
  return context;
}

export { DisplayingFileContextProvider, useDisplayingFileContext };
