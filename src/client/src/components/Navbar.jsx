import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function Navbar() {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => {
    // Get information about the currently logged-in user.
    apiRequest("/session-info")
      .then((data) => {
        if (data.logged_in) {
          setEmail(data.email || "");
          setRole(data.role || "");
        }
      })
      .catch(() => {
        // If no valid session exists, leave the account
        // information blank rather than breaking the navbar.
      });
  }, []);

  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
      <h2>Campus Health Portal</h2>

      <Link to="/dashboard">Dashboard</Link>
      {" | "}
      <Link to="/login">Login</Link>

      <div style={{ marginTop: "10px" }}>
        Logged in as {email} | {role} portal
      </div>
    </nav>
  );
}

export default Navbar;