import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Transactions from './pages/Transactions';

function App() {
  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--color-bg-primary)' }}>
      <Router>
        <Routes>
          <Route path="/transactions" element={<Transactions />} />
          <Route path="/" element={<Transactions />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
