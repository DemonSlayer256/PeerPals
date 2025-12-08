// Login.jsx

async function sendPostReq(postData) {
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(postData)
    };

    try {
        const response = await fetch('http://localhost:8000/api/login/', requestOptions);
        if (!response.ok) {
            const errorData = await response.json(); 
            // Throwing an error here ensures the catch block in signUp() handles it.
            throw new Error(`Login failed with status ${response.status}. Details: ${JSON.stringify(errorData)}`);
        }
        const data = await response.json();
        console.log('Success:', data);
        return data;

    } catch (error) {
        // Log the error and re-throw it so signUp's catch block can handle it.
        console.error('Error during fetch:', error);
        throw error;
    }
}

export default sendPostReq;