import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RoleSelector from '../components/RoleSelector';
import sendPostReq from '../utils/sendPostReq';

export default function Login() {
    const navigate = useNavigate();
    const [selectedRole, setSelectedRole] = useState('student');
    async function signUp(formData) {
        const userName = formData.get("username");
        const passWord = formData.get("password");

        const postData = {
            username : userName,
            password : passWord,
            requested_role : selectedRole
        };

        try {
            let responseData = await sendPostReq(postData,'http://localhost:8000/api/login/');
            const resData = JSON.stringify(responseData);
            localStorage.setItem('accessToken', responseData.access); 
            localStorage.setItem('refreshToken', responseData.refresh); 
            localStorage.setItem('userRole', responseData.role);
            localStorage.setItem('resposeData',resData);

            // responseData.role = selectedRole;//hardcoded for testing
            let dashboardPath = '/dashboard'; 
            
            // if (role === 'student') {
            //     dashboardPath = '/student-dashboard';
            // } else if (role === 'mentor') {
            //     dashboardPath = '/mentor-dashboard';
            // } else if (role === 'admin') {
            //     dashboardPath = '/admin-dashboard';
            // }

            navigate(dashboardPath, { replace: true, state: responseData }); 

        } catch (error) {
            // Handle login failure (e.g., show an error message to the user)
            console.error("Login failed:", error);
            alert("Login failed. Please check your credentials.");
        }
    }


    return (
        <div className="login-card">
            <h3 className="login-title">Welcome Back!</h3>
            <RoleSelector selected={selectedRole} onSelect={setSelectedRole} />
            
            <form className="login-fields" action={signUp}>
                <input
                    type="text"
                    placeholder="USN"
                    className="input-field"
                    name="username"
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
        </div>
    );
}