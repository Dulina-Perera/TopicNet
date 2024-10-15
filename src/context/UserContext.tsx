import { createContext, createSignal, useContext } from "solid-js";

// Define the context type
interface UserContextType {
  username: () => string; // Signal accessor
  setUsername: (value: string) => void;
}

// Create the context with a default value (can be null initially)
const UserContext = createContext<UserContextType | undefined>(undefined);

// Provider component
function UserContextProvider(props: { children: any }) {
  // Reactive signals
  const [username, setUsername] = createSignal<string>("");

  // Pass the signal functions themselves (not the invoked values)
  const value: UserContextType = {
    username, // Pass the signal accessor
    setUsername,
  };

  return (
    <UserContext.Provider value={value}>{props.children}</UserContext.Provider>
  );
}

// Hook to access context easily
function useUserContext() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error(
      "useOverlayContext must be used within an OverlayContextProvider"
    );
  }
  return context;
}

export { UserContextProvider, useUserContext };
