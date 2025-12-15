// App.jsx (MODIFIED)

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage'; // Assuming this holds your Login component
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute'; // <-- IMPORT THE NEW COMPONENT

function App() {
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        
        {/* Wrap protected routes */}
        <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard/>}/>
        </Route>
        
        {/* Optional: Add a catch-all route to redirect users to the landing/login page */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;