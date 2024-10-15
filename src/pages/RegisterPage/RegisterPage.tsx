// RegisterPage.tsx
import { useNavigate } from "@solidjs/router";
import { createSignal } from "solid-js";
import styles from "./RegisterPage.module.css";

const RegisterPage = () => {
  const [password, setPassword] = createSignal<string>("");
  const [error, setError] = createSignal<string>("");
  const [loading, setLoading] = createSignal<boolean>(false);
  const [username, setUsername] = createSignal<string>("");
  const navigate = useNavigate();

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

    const formDetails = {
      username: username(),
      password: password(),
    };

    try {
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formDetails),
      });

      setLoading(false);

      if (response.ok) {
        // const data = await response.json();
        // localStorage.setItem("token", data.access_token);
        // setUsername(username()); // Set the username in context
        navigate("/login");
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
    setUsername("");
    setPassword("");
  };

  return (
    <div class={styles.loginContainer}>
      <div class={styles.loginBox}>
        {error() && <p style={{ color: "red" }}>{error()}</p>}
        <h2>Register</h2>
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
            Register
          </button>
          <button class={styles.cancelBtn} onClick={handleCancel}>
            Cancel
          </button>
        </div>
        {/* {loading() ? "Registering..." : "Register"} */}
        <div class={styles.login} >
            Already Registered? <a class={styles.loginLink} href="/login">Go to login</a>
          </div>
      </div>
    </div>
  );
};

export default RegisterPage;
