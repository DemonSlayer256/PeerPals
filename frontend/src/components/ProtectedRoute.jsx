// src/utils/ProtectedRoute.jsx

import { Navigate, Outlet } from 'react-router-dom';

const ProtectedRoute = () => {
    // Check for the required token
    const accessToken = localStorage.getItem('accessToken'); 

    // If a token exists, the user can see the protected content.
    if (accessToken) {
        return <Outlet />; // Renders the nested <Route> component (Dashboard)
    }

    // If no token, redirect to the login page (which should be your LandingPage or a dedicated /login route)
    // Assuming your LandingPage handles the login form, we redirect to "/"
    return <Navigate to="/" replace />; 
};

export default ProtectedRoute;