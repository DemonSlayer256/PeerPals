import { useLocation } from 'react-router-dom';
import logout from '../utils/logout';
import profileIcon from '../images/profile-icon.jpg'
export default function AdminDash(){
    const location = useLocation();
    const data = location.state || {
        user_id: 'S12345',
        first_name: 'Alice',
        last_name:' Johnson',
        role: 'Admin',
        email: 'student@example.com' 
    };
    return (
        <>
            <div className="sidebar">
                        <div className="profile-card">
                            <div className="profile-icon">
                                <img src={profileIcon} alt="profile" className="profile-icon pic"/>
                            </div>
                            <h4 className="user-name">{data.first_name+" "+data.last_name}</h4>
                            <p className="user-role">{data.role}</p>
                        </div>
            
                        <div className="dashboard">
                            <i className="fa-regular fa-house"></i>
                            <p>Dashboard</p>
                        </div>
                        <div className="dash-functions">
                            <h2 className="dash-setting">Activities</h2>
                            <ul>
                                <li>Register a User</li>
                                <li>Assign a Mentor</li>
                                <li>Manage Sessions</li>
                            </ul>
                            <h2 className="dash-setting">Account settings</h2>
                            <ul>
                                <li >Personal info</li>
                                <li >Change Password</li>
                                <button onClick={logout}>Logout</button>
                            </ul>
                        </div>
            </div>
        </>
    )
}