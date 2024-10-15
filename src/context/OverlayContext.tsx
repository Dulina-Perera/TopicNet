import { createContext, useContext } from "solid-js";
import { createSignal } from "solid-js";

// Define the context type
interface OverlayContextType {
  isOverlay: () => boolean; // Make it a function (signal accessor)
  setIsOverlay: (value: boolean) => void;
  title: () => string | null; // Signal accessor
  setTitle: (value: string | null) => void;
  content: () => string | null; // Signal accessor
  setContent: (value: string | null) => void;
}

// Create the context with a default value (can be null initially)
const OverlayContext = createContext<OverlayContextType | undefined>(undefined);

// Provider component
function OverlayContextProvider(props: { children: any }) {
  // Reactive signals
  const [isOverlay, setIsOverlay] = createSignal<boolean>(false);
  const [title, setTitle] = createSignal<string | null>(null);
  const [content, setContent] = createSignal<string | null>(null);

  // Pass the signal functions themselves (not the invoked values)
  const value: OverlayContextType = {
    isOverlay, // Pass the signal accessor (not isOverlay())
    setIsOverlay,
    title,     // Pass the signal accessor (not title())
    setTitle,
    content,   // Pass the signal accessor (not content())
    setContent,
  };

  return (
    <OverlayContext.Provider value={value}>
      {props.children}
    </OverlayContext.Provider>
  );
}

// Hook to access context easily
function useOverlayContext() {
  const context = useContext(OverlayContext);
  if (!context) {
    throw new Error("useOverlayContext must be used within an OverlayContextProvider");
  }
  return context;
}

export { OverlayContextProvider, useOverlayContext };
