import { useEffect, useState } from "react";
import {
  Navigate
} from "react-router-dom";

import { apiRequest } from "../services/api";

function DoctorRoute({ children }) {
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest("/session-info")
      .then((data) => {
        setRole(data.role || "");
      })
      .catch(() => {
        setRole("");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <p>
        Verifying doctor access...
      </p>
    );
  }

  if (role !== "doctor") {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    );
  }

  return children;
}

export default DoctorRoute;