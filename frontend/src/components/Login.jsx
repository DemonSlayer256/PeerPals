import React, { useState } from 'react';
import RoleSelector from '../components/RoleSelector';

function sendPostReq(postData)
{
    const requestOptions = {
    method: 'POST', // Specify the HTTP method as POST
    headers: {
        'Content-Type': 'application/json', // Indicate that the body contains JSON data
        'Access-Control-Allow-Origin': "*"
    },
    body: JSON.stringify(postData) // Convert the data object to a JSON string
    };

    const response = fetch('http://localhost:8000/api/login', requestOptions)
            .then(response => {
                if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json(); // Parse the JSON response
            })
            .then(data => {
                console.log('Success:', data); // Handle the successful response data
            })
            .catch(error => {
                console.error('Error:', error); // Handle any errors during the fetch operation
            });
    return response;
}

function signUp(e)
{   e.preventDefault();
    const formData = new FormData(e.target);
    const userName = formData.get("USN");
    const passWord = formData.get("password")
    // console.log(username,password)
    const postData = {
        username : userName,
        password : passWord
    }
    const response = sendPostReq(postData);
    console.log(response.status)
}


export default function Login() {

    const [selectedRole, setSelectedRole] = useState('student');

    return (
        <div className="login-card">
            <h3 className="login-title">Welcome Back!</h3>
            <RoleSelector selected={selectedRole} onSelect={setSelectedRole} />
            
            <form className="login-fields" action={signUp}>
                <input
                    type="text"
                    placeholder="USN"
                    className="input-field"
                    name="USN"
                />
                <input
                    type="password"
                    placeholder="Password"
                    className="input-field"
                    name='password'
                />
                <button className="primary-button">
                    Sign In as {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)}
                </button>
            </form>
            {/* <p className="forgot-link">Forgot Password?</p> */}
        </div>
    );
}