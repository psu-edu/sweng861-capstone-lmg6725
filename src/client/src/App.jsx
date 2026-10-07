import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import DoctorRoute from "./components/DoctorRoute";
import DoctorDashboardPage from "./pages/DoctorDashboardPage";
import AppointmentsPage from "./pages/AppointmentsPage";
import AppointmentDetailPage from "./pages/AppointmentDetailPage";
import BookAppointmentPage from "./pages/BookAppointmentPage";
import ProfilePage from "./pages/ProfilePage";
import AppointmentSlotsPage from "./pages/AppointmentSlotsPage";
import AppointmentRecommendationsPage from "./pages/AppointmentRecommendationsPage";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/doctor" element={<DoctorRoute> <DoctorDashboardPage /></DoctorRoute>}/>
        <Route path="/doctor/appointments" element={<DoctorRoute> <AppointmentsPage /></DoctorRoute>}/>
        <Route path="/appointments" element={<AppointmentsPage />} />
        <Route path="/appointments/slots" element={<AppointmentSlotsPage />} />
        <Route path="/appointments/recommend" element={<AppointmentRecommendationsPage />} />
        <Route path="/appointments/:id" element={<AppointmentDetailPage />} />
        <Route path="/appointments/book" element={<BookAppointmentPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;