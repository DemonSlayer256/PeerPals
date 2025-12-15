import profileIcon from "../images/profile-icon.jpg";
import logout from '../utils/logout';

export default function Sidebar(props){
    return(
        <div className="sidebar">
            <div className="profile-card">
                <div className="profile-icon">
                    <img src={profileIcon} alt="profile" className="profile-icon pic"/>
                </div>
                <h4 className="user-name">{props.info.first_name+" "+props.info.last_name}</h4>
                <p className="user-role">{props.info.role}</p>
            </div>

            <div className="dashboard">
                <i className="fa-regular fa-house"></i>
                <p>Dashboard</p>
            </div>
            <div className="dash-functions">
                <h2 className="dash-setting">Activities</h2>
                <ul>
                    <li>Sessions Calender</li>
                    <li>Upcoming Sessions</li>
                    {props.info.role==='mentor'?" ":<li>Book a Session</li>}
                </ul>
                <h2 className="dash-setting">Account settings</h2>
                <ul>
                    <li>Personal info</li>
                    <button onClick={logout}>Logout</button>
                </ul>
            </div>
        </div>
    )
}