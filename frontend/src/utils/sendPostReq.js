async function sendPostReq(postData, url, accessToken) {
    const headers = {
        'Content-Type': 'application/json',
    };
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const requestOptions = {
        method: 'POST',
        headers: headers, 
        body: JSON.stringify(postData)
    };

    try {
        const response = await fetch(url, requestOptions);
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