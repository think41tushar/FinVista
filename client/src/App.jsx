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
import MutualFundAnalysis from "./pages/MutualFundAnalysis";

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
          <div>
            <Navbar />
        <Routes>
          <Route path="/" element={
            <>
              <LandingPage />
            </>
          } />
          <Route path="/transactions" element={
            <>
              <Transactions />
            </>
          } />
          <Route path="/analysis" element={
            <ProtectedRoute>
              <MutualFundAnalysis />
            </ProtectedRoute>
          } />
          <Route path="/login" element={<Login />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<ErrorPage />} />
        </Routes>
          </div>
      </Router>
    </div>
  );
}

export default App;
