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

export default refreshAccessToken;