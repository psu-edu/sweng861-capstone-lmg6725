import { useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function AppointmentRecommendationsPage() {
  const [serviceCategory, setServiceCategory] = useState("");
  const [timePreference, setTimePreference] = useState("any");

  const [recommendations, setRecommendations] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  // Natural-language request entered for the scheduling assistant.
  const [assistantRequest, setAssistantRequest] = useState("");
  const [assistantLoading, setAssistantLoading] = useState(false);
  const [assistantMessage, setAssistantMessage] = useState("");
  const [usingDevelopmentFallback, setUsingDevelopmentFallback] = useState(false);

  const serviceCategories = [
    "General Visit",
    "Sports Injury",
    "Vaccination",
    "Wellness Visit"
  ];

  // Shared helper so both the manual preference form and the AI assistant
  // use the same real appointment recommendation endpoint.
  const loadRecommendations = async (service, time) => {
    const data = await apiRequest(
      "/appointments/recommend",
      {
        method: "POST",
        body: JSON.stringify({
          service_category: service,
          time_preference: time
        })
      }
    );

    const results = data.recommendations || [];
    setRecommendations(results);

    if (results.length === 0) {
      setMessage(
        data.message ||
        "No recommended appointments were found."
      );
    }
  };

  // Existing manual recommendation flow.
  const handleRecommend = async (e) => {
    e.preventDefault();

    setError("");
    setMessage("");
    setAssistantMessage("");
    setRecommendations([]);

    if (!serviceCategory) {
      setError("Please select a service category.");
      return;
    }

    try {
      setLoading(true);
      await loadRecommendations(serviceCategory, timePreference);
    } catch (err) {
      setError(
        err.message ||
        "Unable to get appointment recommendations."
      );
    } finally {
      setLoading(false);
    }
  };

  // Convert the AI response into the exact values expected by
  // /appointments/recommend.
  const parseAssistantClassification = (aiText) => {
    if (!aiText) {
      throw new Error("The scheduling assistant returned an empty response.");
    }

    const serviceMatch = aiText.match(
      /SERVICE_CATEGORY:\s*(.+)/i
    );

    const timeMatch = aiText.match(
      /TIME_PREFERENCE:\s*(morning|afternoon|any)/i
    );

    if (!serviceMatch || !timeMatch) {
      throw new Error(
        "The scheduling assistant response could not be understood."
      );
    }

    const parsedService = serviceMatch[1].trim();
    const parsedTime = timeMatch[1].trim().toLowerCase();

    // Never trust an AI/fallback value that is outside the categories
    // supported by this scheduling page.
    if (!serviceCategories.includes(parsedService)) {
      throw new Error(
        "The scheduling assistant returned an unsupported service category."
      );
    }

    return {
      service: parsedService,
      time: parsedTime
    };
  };

  // AI-assisted recommendation flow. /ask-ai tries Drift first and can
  // currently return the clearly marked development fallback while the
  // provided Drift service is unavailable.
  const handleAssistantRecommend = async () => {
    setError("");
    setMessage("");
    setAssistantMessage("");
    setUsingDevelopmentFallback(false);
    setRecommendations([]);

    if (!assistantRequest.trim()) {
      setError(
        "Please describe the type of appointment you are looking for."
      );
      return;
    }

    try {
      setAssistantLoading(true);

      const aiResponse = await apiRequest(
        "/ask-ai",
        {
          method: "POST",
          body: JSON.stringify({
            prompt: `
You are a scheduling assistant for a Campus Health Appointment System.

Your job is to classify a user's scheduling request.

Choose exactly one of these service categories:
- General Visit
- Sports Injury
- Vaccination
- Wellness Visit

Choose exactly one of these time preferences:
- morning
- afternoon
- any

Important rules:
- Do not diagnose medical conditions.
- Do not provide medical advice.
- Do not recommend medication or treatment.
- Only classify the request for appointment scheduling.
- If the user does not specify a time preference, use "any".
- Use only the service categories listed above.
- Use only the time preferences listed above.

Return only these two lines:
SERVICE_CATEGORY: <service category>
TIME_PREFERENCE: <time preference>

User request:
${assistantRequest}
`,
            // Send the patient's text separately so the
            // development fallback does not classify words
            // from the AI instructions above.
            user_request: assistantRequest
          })
        }
      );

      const aiText =
        aiResponse?.choices?.[0]?.message?.content;

      const classification =
        parseAssistantClassification(aiText);

      // Reflect what the assistant selected in the existing controls too.
      setServiceCategory(classification.service);
      setTimePreference(classification.time);

      if (aiResponse.development_fallback) {
        setUsingDevelopmentFallback(true);
      }

      setAssistantMessage(
        `Scheduling assistant selected ${classification.service} with ` +
        `${classification.time === "any" ? "no specific" : classification.time} ` +
        "time preference."
      );

      // The AI only classifies the request. Real provider availability and
      // appointment ranking still come from the existing backend endpoint.
      await loadRecommendations(
        classification.service,
        classification.time
      );
    } catch (err) {
      setError(
        err.message ||
        "Unable to use the scheduling assistant."
      );
    } finally {
      setAssistantLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "0 auto",
        padding: "20px"
      }}
    >
      <h1
        style={{
          textAlign: "center",
          fontSize: "2.5rem",
          lineHeight: "1.2",
          marginTop: "0",
          marginBottom: "20px"
        }}
      >
        Find a Recommended Appointment
      </h1>

      <p>
        Select the type of appointment you need and your
        preferred time of day.
      </p>

      {/* Option 1: manual preference selection */}
      <form onSubmit={handleRecommend}>
        <div style={{ marginBottom: "20px" }}>
          <label htmlFor="service_category">
            <strong>Service</strong>
          </label>

          <br />

          <select
            id="service_category"
            value={serviceCategory}
            onChange={(e) => setServiceCategory(e.target.value)}
            style={{
              padding: "8px",
              minWidth: "220px",
              marginTop: "5px"
            }}
          >
            <option value="">Select Service</option>

            {serviceCategories.map((service) => (
              <option key={service} value={service}>
                {service}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: "20px" }}>
          <label htmlFor="time_preference">
            <strong>Preferred Time</strong>
          </label>

          <br />

          <select
            id="time_preference"
            value={timePreference}
            onChange={(e) => setTimePreference(e.target.value)}
            style={{
              padding: "8px",
              minWidth: "220px",
              marginTop: "5px"
            }}
          >
            <option value="any">No Preference</option>
            <option value="morning">Morning</option>
            <option value="afternoon">Afternoon</option>
          </select>
        </div>

        <button type="submit" disabled={loading || assistantLoading}>
          {loading
            ? "Finding Appointments..."
            : "Get Recommendations"}
        </button>
      </form>

      {/* Option 2: natural-language scheduling assistant */}
      <div
        style={{
          marginTop: "30px",
          marginBottom: "30px",
          textAlign: "center"
        }}
      >
        <hr />
        <h2>Not Sure What to Select?</h2>

        <p>
          Describe the type of appointment you are looking for and the
          scheduling assistant can help identify an appointment category.
        </p>

        {/* AI Scheduling Assistant disclaimer */}
        <div
          style={{
            maxWidth: "*00px",
            margin: "15px auto 20px*auto",
            padding: "12px",
            border: "1px solid #b8cce4",
            borderRadius: "6px",
            backgroundColor: "#eef6ff",
            textAlign: "left",
            lineHeight: "1.5"
          }}
        >
          <strong>Scheduling Assistant Notice</strong>

          <p
            style={{
              marginTop: "8px",
              marginBottom:"0"
            }}
          >
            The Scheduling assistant is designed only to help identify
            appointment categories and scheduling preferences. It does not
            provide medical diagnoses treatment recommendations, or medical
            advice. If you already know which provider you would like to see,
            please use View Available Appointments instead.
          </p>
        </div>*

        <textarea
          value={assistantRequest}
          onChange={(e) => setAssistantRequest(e.target.value)}
          placeholder="Example: I hurt my knee playing soccer and would prefer a morning appointment."
          rows="4"
          style={{
            width: "100%",
            maxWidth: "500px",
            padding: "10px"
          }}
        />

        <br />
        <br />

        <button
          type="button"
          onClick={handleAssistantRecommend}
          disabled={assistantLoading || loading}
        >
          {assistantLoading
            ? "Asking Scheduling Assistant..."
            : "Ask Scheduling Assistant"}
        </button>

        {/* Make it clear when the external Drift service was not used. */}
        {usingDevelopmentFallback && (
          <p
            style={{
              marginTop: "15px",
              color: "#8a6300"
            }}
          >
            Development mode: the external AI service is unavailable,
            so a simulated scheduling classification was used.
          </p>
        )}

        {assistantMessage && (
          <p style={{ marginTop: "15px" }}>
            {assistantMessage}
          </p>
        )}
      </div>

      {/* Loading message */}
      {(loading || assistantLoading) && (
        <p>
          Finding the best available appointments...
        </p>
      )}

      {/* Error */}
      {error && (
        <div style={{ marginTop: "20px" }}>
          <p style={{ color: "red" }}>
            {error}
          </p>

          <p>
            You can still browse available appointments manually.
          </p>

          <Link to="/appointments/slots">
            <button type="button">
              View Available Appointments
            </button>
          </Link>
        </div>
      )}

      {/* No Recommendations */}
      {message && (
        <p style={{ marginTop: "20px" }}>
          {message}
        </p>
      )}

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h2>Recommended Appointments</h2>

          {recommendations.map((recommendation, index) => (
            <div
              key={`${recommendation.provider_id}-${recommendation.appointment_date}`}
              style={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "15px",
                marginBottom: "15px"
              }}
            >
              <h3>Recommendation {index + 1}</h3>

              <p>
                <strong>Provider:</strong>{" "}
                {recommendation.provider_name}
              </p>

              <p>
                <strong>Specialty:</strong>{" "}
                {recommendation.specialty}
              </p>

              <p>
                <strong>Service:</strong>{" "}
                {recommendation.service_category}
              </p>

              <p>
                <strong>Date & Time:</strong>{" "}
                {new Date(
                  recommendation.appointment_date
                ).toLocaleString()}
              </p>

              <p>
                <strong>Why this was recommended:</strong>{" "}
                {recommendation.reason}
              </p>

              <Link
                to="/appointments/book"
                state={{
                  provider_name: recommendation.provider_name,
                  appointment_date: recommendation.appointment_date
                }}
              >
                <button type="button">
                  Select This Appointment
                </button>
              </Link>
            </div>
          ))}
        </div>
      )}

      {/* Manual scheduling */}
      <div style={{ marginTop: "30px" }}>
        <hr />

        <h2>Prefer to Choose Yourself?</h2>

        <p>
          You can ignore the recommendations and browse
          available appointment slots manually.
        </p>

        <Link to="/appointments/slots">
          <button type="button">
            View Available Appointments
          </button>
        </Link>
      </div>
    </div>
  );
}

export default AppointmentRecommendationsPage;