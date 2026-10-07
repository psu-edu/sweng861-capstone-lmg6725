import { useState } from "react";
import { apiRequest } from "../services/api";
import { useLocation } from "react-router-dom";
import { useEffect} from "react";

function BookAppointmentPage() {
  const location = useLocation();
  // If coming from appointment slots page it will be passed in here
  const selectedSlot = location.state || {};
  const hasSelectedSlot = Boolean(selectedSlot.provider_name && selectedSlot.appointment_date);

  const cameFromSlotsPage = Boolean(selectedSlot.provider_name && selectedSlot.appointment_date);

  // Providers from database
  const [providers, setProviders] = useState([]);
  const [providersLoading, setProvidersLoading] = useState(true);
  const [providersError, setProvidersError] = useState("");

  // Booking form data
  const [formData, setFormData] = useState({
    appointment_date: selectedSlot.appointment_date || "",
    provider_name: selectedSlot.provider_name || "",
    reason: "",
    patient_notes: "",
    pcp_notification_requested: false,
    pcp_name: "",
    pcp_email: ""
  });

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  
  // Fetch providers from the database
  useEffect(() => {
    apiRequest("/providers")
      .then((data) => {setProviders(data.providers || []);})
      .catch((err) => {setProvidersError(err.message);})
      .finally(() => {setProvidersLoading(false);});
  }, []);

  // synchronize component state
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
        <div>
          <label htmlFor="provider_name">
            <strong>Provider</strong>
          </label>

          <br />

          <select
            id="provider_name"
            name="provider_name"
            value={formData.provider_name}
            onChange={handleChange}
            disabled={providersLoading || cameFromSlotsPage}
            required
          >
            <option value="">
              {providersLoading
                ? "Loading providers..."
                : "Select Provider"}
            </option>

            {providers.map((provider) => (
              <option
                key={provider.id}
                value={provider.name}
              >
                {provider.name}
                {provider.specialty
                  ? ` - ${provider.specialty}`
                  : ""}
              </option>
            ))}
          </select>

          {providersError && (
            <p style={{ color: "red" }}>
              Unable to load providers: {providersError}
            </p>
          )}
        </div>

        <br />

        <div>
          <label>Appointment Date</label>
          <br />
          {/* Prevent users from selecting a date in the past. */}
          <input
            type = "datetime-local"
            name = "appointment_date"
            value={
              formData.appointment_date
              ? formData.appointment_date.slice(0, 16)
              : ""
              }
            onChange = {handleChange}
            readOnly={cameFromSlotsPage}
            min = {new Date().toISOString().slice(0,16)}
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

        {/* PCP Notification */}
        <div
          style={{
            marginTop: "20px",
            marginBottom: "20px",
            padding: "15px",
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#f9f9f9"
          }}
        >
          <h3>Primary Care Provider Notification</h3>
          {/* Authorization information */}
          <div
            style={{
              backgroundColor: "#fff4d6",
              border: "1px solid #e0b84f",
              borderRadius: "6px",
              padding: "12px",
              marginBottom: "15px"
            }}
          >
            <strong>Important Authorization Information</strong>

            <p>
              Checking this option does not automatically send
              your appointment information to your Primary Care
              Provider.
            </p>

            <p>
              A physical authorization signature must be completed
              in the Campus Health office before information can be
              sent to your PCP.
            </p>

            <p>
              If you have already completed an authorization form
              for your current PCP, you do not need to sign another
              form.
            </p>

            <p>
              To change your PCP, select this option and enter the
              new PCP information below. A new authorization may be
              required before information is sent.
            </p>

            <p style={{ marginBottom: "0" }}>
              To stop sending information to your PCP, please call
              the Campus Health office or visit the office in person.
            </p>
          </div>
          
          {/* PCP request checkbox */}
          <label>
            <input
              type="checkbox"
              name="pcp_notification_requested"
              checked={
                formData.pcp_notification_requested
              }
              onChange={handleChange}
            />

            {" "}
            Request notification to my Primary Care Provider
          </label>
          
          {/* Show PCP information only when requested */}
          {formData.pcp_notification_requested && (
            <div
              style={{
                marginTop: "15px"
              }}
            >
              {/* PCP Name */}
              <div
                style={{
                  marginBottom: "15px"
                }}
              >
                <label htmlFor="pcp_name">
                  <strong>Primary Care Provider Name</strong>
                </label>

                <br />

                <input
                  id="pcp_name"
                  type="text"
                  name="pcp_name"
                  value={formData.pcp_name}
                  onChange={handleChange}
                  required={formData.pcp_notification_requested}
                  style={{
                    width: "100%",
                    padding: "8px",
                    marginTop: "5px"
                  }}
                />
              </div>
              {/* PCP Email */}
              <div>
                <label htmlFor="pcp_email">
                  <strong>Primary Care Provider Email</strong>
                </label>

                <br />

                <input
                  id="pcp_email"
                  type="email"
                  name="pcp_email"
                  value={formData.pcp_email}
                  onChange={handleChange}
                  required={formData.pcp_notification_requested}
                  style={{
                    width: "100%",
                    padding: "8px",
                    marginTop: "5px"
                  }}
                />
              </div>
            </div>
          )}
        </div>

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