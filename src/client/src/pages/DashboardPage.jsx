import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function DashboardPage() {
  const [error, setError] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    // Verify current session still has authentication token
    apiRequest("/session-info")
      .then((data) => {
        if (!data.access_token) {
          setError(
            "Authentication token is missing. Please log in again."
          );
          return;
        }

        // Save the authenticated user's role so the
        // dashboard can show the correct tools.
        setRole(data.role || "");
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
      {role === "doctor" ? (
        <div>
          <h2>Doctor Tools</h2>

          <Link to="/doctor">
            <button type="button">
              Doctor Dashboard
            </button>
          </Link>
        </div>
      ) : (
        <div>
          <h2>Appointments</h2>

          {/* Patient appointment actions */}
          <div
            style={{
              display: "flex",
              gap: "15px",
              marginTop: "15px"
            }}
          >
            <Link to="/appointments">
              <button type="button">
                View My Appointments
              </button>
            </Link>

            <Link to="/appointments/recommend">
              <button type="button">
                Find Recommended Appointment
              </button>
            </Link>

            <Link to="/appointments/slots">
              <button type="button">
                View Available Slots
              </button>
            </Link>
          </div>
        </div>
      )}

      <hr style={{ marginTop: "25px" }} />

      <h2>Account</h2>

      <Link to="/profile">
        <button type="button">
          My Profile
        </button>
      </Link>

      {/* Backend clears the session before returning to login */}
      <button
        type="button"
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