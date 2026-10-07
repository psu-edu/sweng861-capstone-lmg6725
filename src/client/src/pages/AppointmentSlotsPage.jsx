import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { apiRequest } from "../services/api";

function AppointmentSlotsPage() {
  const [slots, setSlots] = useState([]);
  const [selectedProvider, setSelectedProvider] = useState("");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Keep this provider list the same as BookAppointmentPage.jsx
  const [providers, setProviders] = useState([]);

  useEffect(() => {
    apiRequest("/appointments/slots")
      .then((data) => {
        setSlots(data.slots || []);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  useEffect(() => {
  apiRequest("/providers")
    .then((data) => {
      setProviders(data.providers || []);
    })
    .catch((err) => {
      setError(err.message);
    });
}, []);

  // Get slots for the selected provider
  const providerSlots = slots.filter(
    (slot) => slot.provider_name === selectedProvider
  );

  // Get the months that contain available appointments
  const months = [
    ...new Set(
      providerSlots.map((slot) => {
        const date = new Date(slot.appointment_date);

        return date.toLocaleDateString("en-US", {
          month: "long",
          year: "numeric"
        });
      })
    )
  ];

  // Filter by month if a month has been selected
  const filteredSlots = providerSlots.filter((slot) => {
    if (!selectedMonth) {
      return true;
    }

    const date = new Date(slot.appointment_date);

    const slotMonth = date.toLocaleDateString("en-US", {
      month: "long",
      year: "numeric"
    });

    return slotMonth === selectedMonth;
  });

  // Group appointments by calendar date
  const slotsByDate = filteredSlots.reduce((groups, slot) => {
    const date = new Date(slot.appointment_date);

    const dateKey = date.toLocaleDateString("en-US", {
      weekday: "long",
      month: "long",
      day: "numeric",
      year: "numeric"
    });

    if (!groups[dateKey]) {
      groups[dateKey] = [];
    }

    groups[dateKey].push(slot);

    return groups;
  }, {});

  const handleProviderChange = (e) => {
  setSelectedProvider(e.target.value);

  // Reset the month whenever the provider changes
  setSelectedMonth("");
};

if (loading) {
  return <p>Loading available appointments...</p>;
}

if (error) {
  return <p style={{ color: "red" }}>{error}</p>;
}

return (
  <div
    style={{
      maxWidth: "900px",
      margin: "0 auto",
      padding: "20px"
    }}
  >
    <h1>Available Appointment Slots</h1>

    {/* Scheduling information */}
    <div
      style={{
        backgroundColor: "#eef6ff",
        padding: "15px",
        marginBottom: "25px",
        borderRadius: "8px"
      }}
    >
      <strong>Scheduling Information</strong>

      <p style={{ marginBottom: "0" }}>
        Appointments may be booked up to 3 months in advance.
        Appointments are available Monday through Friday only.
      </p>
    </div>

    {/* Provider and month filters */}
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        gap: "20px",
        flexWrap: "wrap",
        marginBottom: "30px"
      }}
    >
      <div>
        <label htmlFor="provider">
          <strong>Provider</strong>
        </label>

        <br />

        <select
          id="provider"
          value={selectedProvider}
          onChange={handleProviderChange}
          style={{
            padding: "8px",
            minWidth: "200px"
          }}
        >
          <option value="">Select Provider</option>

          {providers.map((provider) => (
            <option
              key={provider.id}
              value={provider.name}
            >
              {provider.name}
            </option>
          ))}
        </select>
      </div>

      {selectedProvider && (
        <div>
          <label htmlFor="month">
            <strong>Month</strong>
          </label>

          <br />

          <select
            id="month"
            value={selectedMonth}
            onChange={(e) => setSelectedMonth(e.target.value)}
            style={{
              padding: "8px",
              minWidth: "180px"
            }}
          >
            <option value="">All Available Months</option>

            {months.map((month) => (
              <option
                key={month}
                value={month}
              >
                {month}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>

    {!selectedProvider && (
      <p>
        Select a provider to view available appointment
        dates and times.
      </p>
    )}

    {selectedProvider && (
      <>
        <h2>
          Available Times for {selectedProvider}
        </h2>

        {Object.keys(slotsByDate).length === 0 ? (
          <p>
            No appointment slots are currently available
            for this provider.
          </p>
        ) : (
          Object.entries(slotsByDate).map(
            ([date, dateSlots]) => (
              <div
                key={date}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  padding: "15px",
                  marginBottom: "15px"
                }}
              >
                <h3 style={{ marginTop: "0" }}>
                  {date}
                </h3>

                <div
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "10px"
                  }}
                >
                  {dateSlots.map((slot) => (
                    <Link
                      key={slot.appointment_date}
                      to="/appointments/book"
                      state={{
                        provider_name: slot.provider_name,
                        appointment_date:
                          slot.appointment_date
                      }}
                    >
                      <button
                        type="button"
                        style={{
                          padding: "8px 14px",
                          cursor: "pointer"
                        }}
                      >
                        {new Date(
                          slot.appointment_date
                        ).toLocaleTimeString(
                          "en-US",
                          {
                            hour: "numeric",
                            minute: "2-digit"
                          }
                        )}
                      </button>
                    </Link>
                  ))}
                </div>
              </div>
            )
          )
        )}
      </>
    )}
  </div>
);
}

export default AppointmentSlotsPage;