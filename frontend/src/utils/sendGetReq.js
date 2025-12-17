import logout from "./logout"; 
import refreshAccessToken from './refreshAccessToken';

async function sendGetReq(url, accessToken) {
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
    };

    const requestOptions = {
        method: 'GET',
        headers: headers,
    };
    let response = await fetch(url, requestOptions);
    if (response.status === 401) {
        console.warn("Access token expired. Attempting refresh...");
        try {
            const newAccessToken = await refreshAccessToken();
            const retryHeaders = {
                ...headers,
                'Authorization': `Bearer ${newAccessToken}`
            };
            
            const retryOptions = {
                ...requestOptions,
                headers: retryHeaders
            };

            response = await fetch(url, retryOptions);
            if (response.ok) {
                console.log("Original request succeeded after token refresh.");
            } else if (response.status === 401) {
                console.error("Request failed even after token refresh. Logging out.");
                logout();
                throw new Error("Authentication failed permanently.");
            }
        } catch (error) {
            throw error; 
        }
    }

    if (!response.ok) {
        const errorDetails = await response.json().catch(() => ({})); 
        throw new Error(`Request failed with status ${response.status}. Details: ${JSON.stringify(errorDetails)}`);
    }

    const data = await response.json();
    return data;
}

export default sendGetReq;