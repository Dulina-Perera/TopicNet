import { createContext, createSignal, useContext } from "solid-js";

// Define the context type
interface SidebarVisibleContextType {
  isSidebarVisible: () => boolean; // Signal accessor
  setIsSidebarVisible: (value: boolean) => void;
}

// Create the context with a default value (can be null initially)
const SidebarVisibleContext = createContext<SidebarVisibleContextType | undefined>(undefined);

// Provider component
function SidebarVisibleContextProvider(props: { children: any }) {
  // Reactive signals
  const [isSidebarVisible, setIsSidebarVisible] = createSignal<boolean>(false);

  // Pass the signal functions themselves (not the invoked values)
  const value: SidebarVisibleContextType = {
    isSidebarVisible, // Pass the signal accessor
    setIsSidebarVisible,
  };

  return (
    <SidebarVisibleContext.Provider value={value}>{props.children}</SidebarVisibleContext.Provider>
  );
}

// Hook to access context easily
function useSidebarVisibleContext() {
  const context = useContext(SidebarVisibleContext);
  if (!context) {
    throw new Error(
      "useSidebarVisibleContext must be used within an SidebarVisibleContextProvider"
    );
  }
  return context;
}

export { SidebarVisibleContextProvider, useSidebarVisibleContext };
