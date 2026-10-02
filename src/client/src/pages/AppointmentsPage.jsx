import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function AppointmentsPage() {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch the current user's appointments when the page loads
    apiRequest("/appointments")
      .then((data) => {
        setAppointments(data.appointments || []);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // Show status message while request is pending
  if (loading) {
    return <p>Loading appointments...</p>;
  }

  // Show errors instead of incomplete appointment list
  if (error) {
    return (
      <p style={{ color: "red" }}>
        {error}
      </p>
    );
  }

  return (
    <div>
      <h1>My Appointments</h1>

      {/* Seprate empty result from a table with appointments. */}
      {appointments.length === 0 ? (
        <p>No appointments found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Provider</th>
              <th>Status</th>
              <th>View</th>
            </tr>
          </thead>

          <tbody>
            {appointments.map((appointment) => (
              <tr key={appointment.id}>
                <td>{appointment.id}</td>
                <td>{appointment.provider_name}</td>
                <td>{appointment.status}</td>

                <td>
                  <Link
                    to={`/appointments/${appointment.id}`}
                  >
                    View Details
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default AppointmentsPage;