import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Transactions from "./pages/Transactions";
import ProtectedRoute from "./components/common/ProtectedRoute";
import Login from "./pages/LoginPage";
import Dashboard from "./components/Dashboard";
import { AuthProvider } from "./contexts/AuthContext";
import { Navigate } from "react-router-dom";
import Navbar from "./components/common/Navbar";
import ErrorPage from "./pages/ErrorPage";

function App() {
  return (
    <div className="flex flex-col min-w-screen min-h-screen bg-gray-50">
      <Router>
        <AuthProvider>
          <Navbar />
          <Routes>
            <Route path="/transactions" element={<Transactions />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<ErrorPage />} />
          </Routes>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
