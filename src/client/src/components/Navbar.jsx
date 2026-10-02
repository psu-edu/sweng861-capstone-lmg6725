import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
      <h2>Campus Health Portal</h2>

      <Link to="/dashboard">Dashboard</Link>
      {" | "}
      <Link to="/login">Login</Link>

      <div style={{ marginTop: "10px" }}>
        Logged in as user@example.com
      </div>
    </nav>
  );
}

export default Navbar;