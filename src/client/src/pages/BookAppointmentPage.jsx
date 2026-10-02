import { useState } from "react";
import { apiRequest } from "../services/api";

function BookAppointmentPage() {
  const [formData, setFormData] = useState({
    appointment_date: "",
    provider_name: "",
    reason: "",
    patient_notes: "",
    pcp_notification_requested: false,
    pcp_name: "",
    pcp_email: ""
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  // synch component state
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
        ...formData,
        [name]: type === "checkbox" ? checked : value
        });
    };


  // Validate and submit the appointment form to the booking endpoint
  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    // Required fields before request can be sent
    if (
      !formData.provider_name ||
      !formData.appointment_date ||
      !formData.reason
    ) {
      setError("Doctor, appointment date, and reason are required.");
      return;
    }

    try {
      setLoading(true);

      await apiRequest("/appointments/book", {
        method: "POST",
        body: JSON.stringify(formData)
      });

      setSuccess("Appointment booked successfully.");

      // Clear form after appointment is created successfully
      setFormData({
        appointment_date: "",
        provider_name: "",
        reason: "",
        patient_notes: "",
        pcp_notification_requested: false,
        pcp_name: "",
        pcp_email: ""
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Book Appointment</h1>

      {success && (
        <p style={{ color: "green" }}>
          {success}
        </p>
      )}

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      <form onSubmit={handleSubmit}>

        <label>Provider</label>
        <br />
        <select
          name="provider_name"
          value={formData.provider_name}
          onChange={handleChange}
        >
          <option value="">Select Provider</option>
          <option value="Dr. Alex">Dr. Alex</option>
          <option value="Dr. Lauren">Dr. Lauren</option>
          <option value="Dr. Harrison">Dr. Harrison</option>
          <option value="Nurse Sharon">Nurse Sharon</option>
          <option value="Nurse Brandon">Nurse Brandon</option>
          <option value="Nurse Braxton">Nurse Braxton</option>
          <option value="Campus Health Center">
            Campus Health Center
          </option>
        </select>

        <br />
        <br />

        <div>
          <label>Appointment Date</label>
          <br />
          {/* Prevent users from selecting a date in the past. */}
          <input
            type = "datetime-local"
            name = "appointment_date"
            value = {formData.appointment_date}
            onChange = {handleChange}
            min = {new Date().toISOString().slice(0,16)}
          />
        </div>

        <br />

        <div>
          <label>Provider Name</label>
          <br />
          <input
            type="text"
            name="provider_name"
            value={formData.provider_name}
            readOnly
          />
        </div>

        <br />

        <div>
          <label>Reason</label>
          <br />
          <input
            type="text"
            name="reason"
            value={formData.reason}
            onChange={handleChange}
          />
        </div>

        <br />

        <div>
          <label>Patient Notes</label>
          <br />
          <textarea
            name="patient_notes"
            value={formData.patient_notes}
            onChange={handleChange}
          />
        </div>

        <br />

        <div>
          <label>
            <input
              type="checkbox"
              name="pcp_notification_requested"
              checked={formData.pcp_notification_requested}
              onChange={handleChange}
            />
            Notify PCP
          </label>
        </div>

        <br />

        <div>
          <label>PCP Name</label>
          <br />
          <input
            type="text"
            name="pcp_name"
            value={formData.pcp_name}
            onChange={handleChange}
          />
        </div>

        <br />

        <div>
          <label>PCP Email</label>
          <br />
          <input
            type="email"
            name="pcp_email"
            value={formData.pcp_email}
            onChange={handleChange}
          />
        </div>

        <br />

        <button
          aria-label="Book Appointment"
          type="submit"
          disabled={loading}
        >
          {loading ? "Booking..." : "Book Appointment"}
        </button>
      </form>
    </div>
  );
}

export default BookAppointmentPage;