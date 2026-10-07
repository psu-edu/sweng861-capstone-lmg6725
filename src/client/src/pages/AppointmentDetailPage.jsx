import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function AppointmentDetailPage() {
  const { id } = useParams();

  const [appointment, setAppointment] = useState(null);
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [newDate, setNewDate] = useState("");
  const [showReschedule, setShowReschedule] = useState(false);
  const [doctorNotes, setDoctorNotes] = useState("");

  useEffect(() => {
    // Load the signed-in role and appointment together so the page can
    // present patient controls or doctor visit-record controls appropriately.
    const loadPage = async () => {
      try {
        setLoading(true);
        setError("");

        const sessionData = await apiRequest("/session-info");
        setRole(sessionData.role || "");

        const data = await apiRequest(`/appointments/${id}`);
        setAppointment(data);
        setDoctorNotes(data.doctor_notes || "");
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadPage();
  }, [id]);

  // Patient-only action: cancel the current patient's appointment.
  const handleCancel = async () => {
    const confirmed = window.confirm(
      "Are you sure you want to cancel this appointment?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

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

  // Patient-only action: send a selected replacement date to the API.
  const handleReschedule = async () => {
    if (!newDate) {
      alert("Please select a new date.");
      return;
    }

    try {
      setError("");

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

  // Doctor-only action: save notes to the existing doctor-notes endpoint.
  const handleSaveDoctorNotes = async () => {
    try {
      setError("");
      setMessage("");

      await apiRequest(
        `/appointments/${id}/notes`,
        {
          method: "PUT",
          body: JSON.stringify({
            doctor_notes: doctorNotes
          })
        }
      );

      setAppointment({
        ...appointment,
        doctor_notes: doctorNotes
      });

      setMessage("Doctor notes saved successfully.");
    } catch (err) {
      setError(err.message);
    }
  };

  // Doctor-only action: mark the visit as completed.
const handleCompleteVisit = async () => {
  const confirmed = window.confirm(
    "Are you sure you want to mark this visit as completed?"
  );

  if (!confirmed) {
    return;
  }

  try {
    setError("");
    setMessage("");

    const data = await apiRequest(
      `/appointments/${id}/complete`,
      {
        method: "PUT"
      }
    );

    setAppointment({
      ...appointment,
      status: data.status || "completed"
    });

    setMessage(
      "Visit marked as completed successfully."
    );

  } catch (err) {
    setError(err.message);
  }
};

  if (loading) {
    return <p>Loading appointment...</p>;
  }

  if (error) {
    if (error.includes("404")) {
      return (
        <div>
          <p>
            This appointment does not exist or has been deleted.
          </p>

          <Link to={role === "doctor" ? "/doctor/appointments" : "/appointments"}>
            <button type="button">
              Back to Appointments
            </button>
          </Link>
        </div>
      );
    }

    return (
      <div>
        <p style={{ color: "red" }}>
          {error}
        </p>

        <Link to={role === "doctor" ? "/doctor/appointments" : "/appointments"}>
          <button type="button">
            Back to Appointments
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
      <h1>Appointment Details</h1>

      {message && (
        <p style={{ color: "green" }}>
          {message}
        </p>
      )}

      {/* Doctors need the patient identifier when reviewing all appointments. */}
      {role === "doctor" && (
        <p>
          <strong>Patient:</strong>{" "}
          {appointment?.patient_name || "Unknown Patient"}
        </p>
      )}

      <p>
        <strong>Provider:</strong>{" "}
        {appointment?.provider_name || "Not provided"}
      </p>

      <p>
        <strong>Status:</strong>{" "}
        {appointment?.status || "Unknown"}
      </p>

      <p>
        <strong>Date:</strong>{" "}
        {appointment?.appointment_date
          ? new Date(appointment.appointment_date).toLocaleString()
          : "Not scheduled"}
      </p>

      <p>
        <strong>Reason:</strong>{" "}
        {appointment?.reason || "Not provided"}
      </p>

      <div
        style={{
          marginTop: "20px",
          padding: "15px",
          border: "1px solid #ddd",
          borderRadius: "8px"
        }}
      >
        <h2>Visit Record</h2>

        <p>
          <strong>Patient Notes:</strong>{" "}
          {appointment?.patient_notes || "Not provided"}
        </p>

        {role === "doctor" ? (
          <div style={{ marginTop: "20px" }}>
            <label htmlFor="doctor_notes">
              <strong>Doctor Notes</strong>
            </label>
            <br />
            <textarea
              id="doctor_notes"
              value={doctorNotes}
              onChange={(e) => setDoctorNotes(e.target.value)}
              rows="6"
              style={{
                width: "100%",
                marginTop: "8px",
                padding: "10px"
              }}
              placeholder="Enter visit notes here."
            />
            <br />
            <br />
            <button
              type="button"
              onClick={handleSaveDoctorNotes}
            >
              Save Doctor Notes
            </button>

            {appointment?.status !== "completed" && (
              <>
              {" "}
              <button
                type="button"
                onClick={handleCompleteVisit}
              >
                Mark Visit Complete
              </button>
           </>
          )}
          </div>
        ) : (
          <p>
            <strong>Doctor Notes:</strong>{" "}
            {appointment?.doctor_notes || "Not provided"}
          </p>
        )}
      </div>

      {/* Cancel and reschedule remain patient-only controls. */}
      {role === "patient" && (
        <div style={{ marginTop: "20px" }}>
          <button
            type="button"
            onClick={handleCancel}
          >
            Cancel Appointment
          </button>

          <button
            type="button"
            onClick={() => setShowReschedule(!showReschedule)}
            style={{ marginLeft: "10px" }}
          >
            Reschedule Appointment
          </button>

          {showReschedule && (
            <div style={{ marginTop: "20px" }}>
              <label htmlFor="new_appointment_date">
                New Appointment Date
              </label>
              <br />
              <input
                id="new_appointment_date"
                type="datetime-local"
                value={newDate}
                onChange={(e) => setNewDate(e.target.value)}
              />
              <br />
              <br />
              <button
                type="button"
                onClick={handleReschedule}
              >
                Save New Date
              </button>
            </div>
          )}
        </div>
      )}

      <div style={{ marginTop: "25px" }}>
        <Link to={role === "doctor" ? "/doctor/appointments" : "/appointments"}>
          <button type="button">
            {role === "doctor"
              ? "Back to All Appointments"
              : "Back to My Appointments"}
          </button>
        </Link>
      </div>
    </div>
  );
}

export default AppointmentDetailPage;
