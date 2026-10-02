import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function AppointmentDetailPage() {
  const { id } = useParams();

  const [appointment, setAppointment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [newDate, setNewDate] = useState("");
  const [showReschedule, setShowReschedule] = useState(false);

  // Confirm the cancellation, then update the appointment status locally.
  const handleCancel = async () => {
  const confirmed = window.confirm("Are you sure you want to cancel this appointment?");

  if (!confirmed) {
    return;
  }

  try {
    await apiRequest(`/appointments/${id}/cancel`, {
      method: "PUT"
    });

    setMessage("Appointment cancelled successfully.");

    setAppointment({
      ...appointment,
      status: "cancelled"
    });
  } catch (err) {
    setError(err.message);
  }
};

// Send selected date to API and refresh the appointment details
const handleReschedule = async () => {
  if (!newDate) {
    alert("Please select a new date.");
    return;
  }

  try {
    await apiRequest(
      `/appointments/${id}/reschedule`,
      {
        method: "PUT",
        body: JSON.stringify({
          appointment_date: newDate
        })
      }
    );

    setMessage("Appointment rescheduled successfully.");

    setAppointment({
      ...appointment,
      appointment_date: newDate,
      status: "scheduled"
    });

    setShowReschedule(false);
  } catch (err) {
    setError(err.message);
  }
};


  useEffect(() => {
    // Load the appointment whenever the route parameter changes
    apiRequest(`/appointments/${id}`)
      .then((data) => {
        setAppointment(data);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id]);

  // Show request is in progress
  if (loading) {
    return <p>Loading appointment...</p>;
  }

  // Show a friendly message for missing appointments and the API error otherwise.
  if (error) {
  if (error.includes("404")) {
    return (
      <p>
        This appointment does not exist or has been deleted.
      </p>
    );
  }

  return (
    <p style={{ color: "red" }}>
      {error}
    </p>
  );
}

  return (
    <div>
      <h1>Appointment Details</h1>
      {message && (
        <p style={{ color: "green" }}>
          {message}
          </p>
        )}
      <p><strong>Doctor:</strong> {appointment?.provider_name || "Not provided"}</p>
      <p><strong>Status:</strong> {appointment?.status || "Unknown"}</p>
      <p><strong>Date:</strong>{" "} {appointment?.appointment_date ? new Date(appointment.appointment_date).toLocaleString() : "Not scheduled"}</p>
      <p><strong>Reason:</strong> {appointment?.reason || "Not provided"}</p>
      <p><strong>Patient Notes:</strong> {appointment?.patient_notes || "Not provided"}</p>
      <p><strong>Doctor Notes:</strong> {appointment?.doctor_notes || "Not provided"}</p>
      <br />

      <button onClick={handleCancel}>
        Cancel Appointment
      </button>

      <button
      onClick={() => setShowReschedule(!showReschedule)}
      style={{ marginLeft: "10px" }}
      >
        Reschedule Appointment
      </button>

      {showReschedule && (
        <div style={{ marginTop: "20px" }}>
          <label>New Appointment Date</label>
          <br />
          
          <input
          type="datetime-local"
          value={newDate}
          onChange={(e) =>
            setNewDate(e.target.value)
          }
          />

          <br />
          <br />
          <button onClick={handleReschedule}>
            Save New Date
          </button>
        </div>
      )}
    </div>
  );
}

export default AppointmentDetailPage;