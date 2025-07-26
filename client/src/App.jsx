import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Transactions from "./pages/Transactions";
import ProtectedRoute from "./components/common/ProtectedRoute";
import Login from "./pages/LoginPage";
import Dashboard from "./components/Dashboard";
import { Navigate } from "react-router-dom";
import Navbar from "./components/common/Navbar";
import ErrorPage from "./pages/ErrorPage";
import useAuthStore from "./store/authStore";
import LandingPage from "./pages/LandingPage";

function App() {
  const { initializeAuth, isAuthenticated } = useAuthStore();

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  return (
    <div 
      className="flex flex-col min-w-screen min-h-screen" 
      style={{ backgroundColor: 'var(--color-bg-primary)' }}
    >
      <Router>
        <Routes>
          <Route path="/" element={
            <>
              <Navbar />
              <LandingPage />
            </>
          } />
          <Route path="/transactions" element={
            <>
              <Navbar />
              <Transactions />
            </>
          } />
          <Route path="/login" element={<Login />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Navbar />
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<ErrorPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
