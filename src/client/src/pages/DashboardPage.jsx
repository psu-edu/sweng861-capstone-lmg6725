import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function DashboardPage() {
  const [error, setError] = useState("");

  useEffect(() => {
    // Verify current session still has authentication token
    apiRequest("/session-info")
      .then((data) => {
        if (!data.access_token) {
          // Ask the user to authenticate again if session is incomplete.
          setError(
            "Authentication token is missing. Please log in again."
          );
        }
      })
      .catch(() => {
        // failed session lookup treated as expired or invalid session
        setError(
          "Authentication token is missing. Please log in again."
        );
      });
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      {error && (
        <p
          style={{
            color: "red",
            fontWeight: "bold"
          }}
        >
          {error}
        </p>
      )}

      <h1>Campus Health Dashboard</h1>

      <p>
        Welcome to the Campus Health application.
      </p>

      <hr />

      <h2>Appointments</h2>

      {/* Provide the primary appointment actions from the dashboard. */}
      <div
        style={{
          display: "flex",
          gap: "15px",
          marginTop: "15px"
        }}
      >
        <Link to="/appointments">
          <button>
            View My Appointments
          </button>
        </Link>

        <Link to="/appointments/book">
          <button>
            Book Appointment
          </button>
        </Link>
      </div>

      <hr style={{ marginTop: "25px" }} />

      <h2>Account</h2>

      {/*backend clear session before returning to the login flow */}
      <button
        onClick={() => {
          window.location.href =
            "http://localhost:5000/logout";
        }}
      >
        Logout
      </button>
    </div>
  );
}

export default DashboardPage;