// sendPostReq.js (The Fix)

// Add an optional parameter for the token
async function sendPostReq(postData, url, accessToken = null) {
    
    // Start with base headers
    const headers = {
        'Content-Type': 'application/json',
    };

    // **CRITICAL FIX: Attach the Authorization header if a token is provided**
    if (accessToken) {
        // Use the Bearer scheme expected by Django REST Framework (Simple JWT)
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const requestOptions = {
        method: 'POST',
        headers: headers, // Use the updated headers object
        body: JSON.stringify(postData)
    };

    try {
        const response = await fetch(url, requestOptions);
        
        // Handle 401 specifically for debugging
        if (response.status === 401) {
            const errorData = await response.json(); 
            throw new Error(`Login failed with status 401. Details: ${JSON.stringify(errorData)}`);
        }

        if (!response.ok) {
             const errorData = await response.json(); 
             throw new Error(`Request failed with status ${response.status}. Details: ${JSON.stringify(errorData)}`);
        }
        
        const data = await response.json();
        console.log('Success:', data);
        return data;

    } catch (error) {
        console.error('Error during fetch:', error);
        throw error;
    }
}

export default sendPostReq;