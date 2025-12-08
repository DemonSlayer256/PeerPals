import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RoleSelector from '../components/RoleSelector';
import sendPostReq from '../utils/sendPostReq';

export default function Login() {
    // 2. Initialize the hook
    const navigate = useNavigate();
    const [selectedRole, setSelectedRole] = useState('student');
    
    // 3. Make signUp an async function
    async function signUp(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const userName = formData.get("username");
        const passWord = formData.get("password");

        const postData = {
            username : userName,
            password : passWord
        };

        try {
            // 4. Await the response data
            const responseData = await sendPostReq(postData);

            // 5. Store data (like tokens) if necessary
            localStorage.setItem('accessToken', responseData.access); 
            localStorage.setItem('refreshToken', responseData.refresh); 
            localStorage.setItem('userRole', responseData.role);

            // 6. Redirect based on role
            // You can use a switch statement to route to specific dashboards
            const role = responseData.role;
            let dashboardPath = '/dashboard'; 
            
            if (role === 'student') {
                dashboardPath = '/student-dashboard';
            } else if (role === 'mentor') {
                dashboardPath = '/mentor-dashboard';
            } else if (role === 'admin') {
                dashboardPath = '/admin-dashboard';
            }

            navigate(dashboardPath, { replace: true, state: responseData }); // <-- This performs the redirect!

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
            
            <form className="login-fields" onSubmit={signUp}>
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