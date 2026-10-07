import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";

function DoctorDashboardPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const checkDoctorAccess = async () => {
      try {
        const session = await apiRequest("/session-info");

        if (!session.logged_in) {
          navigate("/login");
          return;
        }

        // Patients cannot use the doctor portal.
        if (session.role !== "doctor") {
          setError(
            "You do not have permission to access the Doctor Dashboard."
          );
          return;
        }
      } catch (err) {
        setError(
          err.message ||
          "Unable to verify doctor access."
        );
      } finally {
        setLoading(false);
      }
    };

    checkDoctorAccess();
  }, [navigate]);

  if (loading) {
    return <p>Loading Doctor Dashboard...</p>;
  }

  if (error) {
    return (
      <div>
        <p style={{ color: "red" }}>
          {error}
        </p>

        <Link to="/dashboard">
          <button type="button">
            Back to Dashboard
          </button>
        </Link>
      </div>
    );
  }

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "0 auto",
        padding: "20px"
      }}
    >
      <h1>Doctor Dashboard</h1>

      <p>
        Manage patient appointments and visit records.
      </p>

      <div
        style={{
          marginTop: "25px",
          padding: "20px",
          border: "1px solid #ddd",
          borderRadius: "8px"
        }}
      >
        <h2>Appointments and Visit Records</h2>

        <p>
          Review scheduled appointments, patient notes,
          and doctor visit notes.
        </p>

        <Link to="/doctor/appointments">
          <button type="button">
            View All Appointments
          </button>
        </Link>
      </div>

      <div style={{ marginTop: "25px" }}>
        <Link to="/dashboard">
          <button type="button">
            Back to Main Dashboard
          </button>
        </Link>
      </div>
    </div>
  );
}

export default DoctorDashboardPage;
