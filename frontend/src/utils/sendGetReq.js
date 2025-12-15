// sendGetReq.js (MODIFIED with Refresh Logic)

import logout from "./logout"; 
const BASE_URL = 'http://localhost:8000';

async function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
        logout();
        throw new Error("No refresh token available. Forcing logout.");
    }

    try {
        const refreshResponse = await fetch(`${BASE_URL}/api/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken }),
        });

        const refreshData = await refreshResponse.json();

        if (refreshResponse.ok) {
            localStorage.setItem('accessToken', refreshData.access);
            console.log("Token refreshed successfully.");
            return refreshData.access;
        } else {
            console.error("Token refresh failed. Refresh token is likely expired.", refreshData);
            logout();
            throw new Error("Token refresh failed. Forcing logout.");
        }
    } catch (error) {
        console.error("Network error during token refresh:", error);
        logout();
        throw error;
    }
}


// The main utility function
async function sendGetReq(url, accessToken) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    };

    const requestOptions = {
        method: 'GET',
        headers: headers,
    };

    // Use a loop to handle the single retry attempt after refresh
    let response = await fetch(url, requestOptions);

    // --- 1. Check for Unauthorized (401) ---
    if (response.status === 401) {
        console.warn("Access token expired. Attempting refresh...");
        try {
            // Get the new access token (will log out if refresh fails)
            const newAccessToken = await refreshAccessToken(); 
            
            // --- 2. RETRY THE ORIGINAL REQUEST with the new token ---
            const retryHeaders = {
                ...headers,
                'Authorization': `Bearer ${newAccessToken}`
            };
            
            const retryOptions = {
                ...requestOptions,
                headers: retryHeaders
            };

            response = await fetch(url, retryOptions);
            
            // Check if the retry succeeded
            if (response.ok) {
                console.log("Original request succeeded after token refresh.");
            } else if (response.status === 401) {
                // If the server still returns 401 after refresh, something is critically wrong (e.g., race condition)
                console.error("Request failed even after token refresh. Logging out.");
                logout();
                throw new Error("Authentication failed permanently.");
            }
        } catch (error) {
            // If refreshAccessToken threw an error (meaning logout occurred)
            // Re-throw the error to stop the original calling function (e.g., getData)
            throw error; 
        }
    }

    // --- 3. Handle successful or non-401 responses ---
    if (!response.ok) {
        // Handle 403 Forbidden, 404 Not Found, 500 Server Error, etc.
        const errorDetails = await response.json().catch(() => ({})); 
        throw new Error(`Request failed with status ${response.status}. Details: ${JSON.stringify(errorDetails)}`);
    }

    // --- 4. Return Data ---
    const data = await response.json();
    return data;
}

export default sendGetReq;