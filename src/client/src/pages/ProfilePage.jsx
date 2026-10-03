import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function ProfilePage() {
  const [profile, setProfile] = useState({
    name: "",
    email: "",
    phone_number: ""
  });

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    apiRequest("/users/me")
      .then((data) => {
        setProfile({
          name: data.name || "",
          email: data.email || "",
          phone_number: data.phone_number || ""
        });
      })
      .catch((err) => {
        setError(err.message);
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    setMessage("");
    setError("");

    try {
      await apiRequest("/users/me", {
        method: "PUT",
        body: JSON.stringify({
          phone_number: profile.phone_number
        })
      });

      setMessage("Profile updated successfully.");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>My Profile</h1>

      {message && (
        <p style={{ color: "green" }}>
          {message}
        </p>
      )}

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      <form onSubmit={handleSubmit}>
        <div>
          <label>Name</label>
          <br />
          <input
            type="text"
            value={profile.name}
            readOnly
          />
        </div>

        <br />

        <div>
          <label>Email</label>
          <br />
          <input
            type="email"
            value={profile.email}
            readOnly
          />
        </div>

        <br />

        <div>
          <label>Phone Number</label>
          <br />
          <input
            type="tel"
            value={profile.phone_number}
            onChange={(e) =>
              setProfile({
                ...profile,
                phone_number: e.target.value
              })
            }
            placeholder="+12145551234"
          />
        </div>

        <br />

        <button type="submit">
          Save Changes
        </button>
      </form>
    </div>
  );
}

export default ProfilePage;