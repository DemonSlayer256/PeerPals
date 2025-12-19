import refreshAccessToken from "./refreshAccessToken";

export default async function sendPatchReq(url, updatedData, accessToken) {
    try {
        let response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(updatedData)
        });

        if (response.status === 401) {
            console.log("Access token expired. Attempting refresh...");
            try {
                const newAccessToken = await refreshAccessToken();
                response = await fetch(url, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${newAccessToken}`
                    },
                    body: JSON.stringify(updatedData)
                });
            } catch (refreshError) {
                throw new Error("Session expired. Please login again.");
            }
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error("Server Error Detail:", errorData);
            throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        console.log("Success:", data);
        return data;
    } catch (error) {
        console.error("Failed to update:", error);
        throw error; 
    }
};