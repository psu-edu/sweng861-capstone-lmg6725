import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

// Login page for the application. It redirects users to Okta for authentication.
function LoginPage() {
  // Store any login-related error message to display in the UI.
  const [error, setError] = useState("");

  // Check the URL for a login error returned by the backend or auth flow.
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);

    if (params.get("error")) {
      setError("Login failed. Please try again.");
    }
  }, []);

  // Redirect the user to the backend's Okta login route.
  const handleLogin = () => {
    window.location.href = `${import.meta.env.VITE_BACKEND_URL}/login`;
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Login</h1>

      {/* Show an error if the login attempt failed. */}
      {error && (
        <p style={{ color: "red", fontWeight: "bold" }}>
          {error}
        </p>
      )}

      <button onClick={handleLogin}>
        Login with Okta
      </button>
    </div>
  );
}

export default LoginPage;