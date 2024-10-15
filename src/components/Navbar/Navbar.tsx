import { createEffect, createSignal } from "solid-js";
import { useUserContext } from "../../context/UserContext";
import "./navbar.css";

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = createSignal(true); // Example signal for logged-in state
  const { username, setUsername } = useUserContext(); // username context

  // Check whether a user is logged in
  createEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem("token");
      console.log(token);

      if (!token) {
        setIsLoggedIn(false); // No token means not logged in
      }

      try {
        const response = await fetch(
          `http://localhost:8000/verify-token/${token}`
        );

        if (response.ok) {
          setIsLoggedIn(true); // Token is valid, user is logged in
        } else {
          throw new Error("Token verification failed");
        }
      } catch (error) {
        localStorage.removeItem("token"); // Remove token if verification fails
        setIsLoggedIn(false); // Not logged in
      }
    };

    verifyToken();
  });

  // You can now use `isLogged()` to check if the user is logged in elsewhere in your component.

  const handleLogout = () => {
    // Logic to handle logout
    setIsLoggedIn(false);
    setUsername("");
    // Perform any other necessary actions like clearing tokens
  };

  return (
    <nav>
      <div class="left">
        <a href="/" class="logo">
          <span>TopicNet</span>
        </a>
        <a href="/upload">Upload</a>
        <a href="/#about-section">About</a>
      </div>

      <div class="right">
        {isLoggedIn() ? (
          <div class="user-info">
            <div class="userCircle">{username()?.charAt(0).toUpperCase()}</div>
            <span class="username">{username()}</span>
            <a onClick={handleLogout} class="logout-link">
              Logout
            </a>
          </div>
        ) : (
          <>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
