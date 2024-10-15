// LoginPage.tsx
import { useNavigate } from "@solidjs/router";
import { createSignal } from "solid-js";
import { useUserContext } from "../../context/UserContext";
import styles from "./LoginPage.module.css";

const LoginPage = () => {
  const [password, setPassword] = createSignal<string>("");
  const [error, setError] = createSignal<string>("");
  const [loading, setLoading] = createSignal<boolean>(false);

  const navigate = useNavigate();
  const { username, setUsername } = useUserContext(); // Accessing username from UserContext

  localStorage.removeItem("token");
  localStorage.removeItem("file_path");

  const validateForm = () => {
    if (!username() || !password()) {
      setError("Username and password are required");
      return false;
    }
    setError("");
    return true;
  };

  const handleLogin = async (event: Event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setLoading(true);

    const formDetails = new URLSearchParams();
    formDetails.append("username", username());
    formDetails.append("password", password());

    try {
      const response = await fetch("http://localhost:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formDetails,
      });

      setLoading(false);

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        setUsername(username()); // Set the username in context
        navigate("/upload");
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Authentication failed!");
      }
    } catch (error) {
      setLoading(false);
      setError("An error occurred. Please try again later.");
    }
  };

  const handleCancel = () => {
    setUsername(""); // Clear the username
    setPassword(""); // Clear the password
    navigate("/"); // Redirect to the home page
  };

  return (
    <div class={styles.loginContainer}>
      <div class={styles.loginBox}>
        {error() && <p style={{ color: "red" }}>{error()}</p>}
        <h2>Login</h2>
        <div class={styles.inputGroup}>
          <label for="username">Username:</label>
          <input
            id="username"
            type="text"
            value={username()}
            onInput={(e) => setUsername(e.currentTarget.value)}
          />
        </div>

        <div class={styles.inputGroup}>
          <label for="password">Password:</label>
          <input
            id="password"
            type="password"
            value={password()}
            onInput={(e) => setPassword(e.currentTarget.value)}
          />
        </div>

        <div class={styles.buttonGroup}>
          <button
            class={styles.loginBtn}
            onClick={handleLogin}
            disabled={loading()}
          >
            Login
          </button>
          <button class={styles.cancelBtn} onClick={handleCancel}>
            Cancel
          </button>
        </div>
        {/* {loading() ? "Logging in..." : "Login"} */}
        <div class={styles.register}>
          Haven't Registered Yet?{" "}
          <a class={styles.registerLink} href="/register">
            Click to register
          </a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
