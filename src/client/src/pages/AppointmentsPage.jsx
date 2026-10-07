import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function AppointmentsPage() {
  const [appointments, setAppointments] = useState([]);
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    // Fetch the current user's role first, then load the correct list.
    const loadAppointments = async () => {
      try {
        setLoading(true);
        setError("");

        const sessionData = await apiRequest("/session-info");
        const userRole = sessionData.role;
        setRole(userRole);

        let endpoint;

        if (userRole === "doctor") {
          // Doctors can view all appointments.
          endpoint = "/appointments";
        } else if (userRole === "patient") {
          // Patients can only view their appointments.
          endpoint = "/appointments/mine";
        } else {
          throw new Error("Unable to determine user role.");
        }

        const data = await apiRequest(endpoint);
        setAppointments(data.appointments || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadAppointments();
  }, []);

  // Doctors can filter the appointment list by visit status.
  // Patients continue seeing their normal appointment list.
  const filteredAppointments =
    role === "doctor" && statusFilter !== "all"
      ? appointments.filter(
          (appointment) =>
            appointment.status === statusFilter
        )
      : appointments;

  if (loading) {
    return <p>Loading appointments...</p>;
  }

  if (error) {
    return (
      <p style={{ color: "red" }}>
        {error}
      </p>
    );
  }

  return (
    <div>
      {/* Doctor-only appointment status filter */}
      {role === "doctor" && (
        <div
          style={{
            marginBottom: "20px"
          }}
        >
          <label htmlFor="status_filter">
            <strong>Filter by Status</strong>
          </label>

          <br />

          <select
            id="status_filter"
            value={statusFilter}
            onChange={(e) =>
              setStatusFilter(e.target.value)
            }
            style={{
              padding: "8px",
              marginTop: "5px",
              minWidth: "180px"
            }}
          >
            <option value="all">
              All Appointments
            </option>

            <option value="scheduled">
              Scheduled
            </option>

            <option value="completed">
              Completed
            </option>

            <option value="cancelled">
              Cancelled
            </option>
          </select>
        </div>
      )}

      <h1>
        {role === "doctor"
          ? "All Appointments"
          : "My Appointments"}
      </h1>

      {filteredAppointments.length === 0 ? (
        <p>No appointments found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>

              {/* Patient identifier is relevant on the doctor-only list. */}
              {role === "doctor" && (
                <th>Patient</th>
              )}

              <th>Provider</th>
              <th>Date</th>
              <th>Status</th>
              <th>View</th>
            </tr>
          </thead>

          <tbody>
            {filteredAppointments.map((appointment) => (
              <tr key={appointment.id}>
                <td>{appointment.id}</td>

                {role === "doctor" && (
                  <td>
                    {appointment.patient_name || "Unknown Patient"}
                  </td>
                )}

                <td>
                  {appointment.provider_name}
                </td>

                <td>
                  {appointment.appointment_date
                    ? new Date(
                        appointment.appointment_date
                      ).toLocaleString()
                    : "Not scheduled"}
                </td>

                <td>
                  {appointment.status}
                </td>

                <td>
                  <Link
                    to={`/appointments/${appointment.id}`}
                  >
                    {role === "doctor"
                      ? "Open Visit Record"
                      : "View Details"}
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {role === "doctor" && (
        <div style={{ marginTop: "25px" }}>
          <Link to="/doctor">
            <button type="button">
              Back to Doctor Dashboard
            </button>
          </Link>
        </div>
      )}
    </div>
  );
}

export default AppointmentsPage;
