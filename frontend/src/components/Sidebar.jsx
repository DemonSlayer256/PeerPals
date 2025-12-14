import profileIcon from "../images/profile-icon.jpg" 

export default function Sidebar(props){
    return(
        <div className="sidebar">
            <div className="profile-card">
                <div className="profile-icon">
                    <img src={profileIcon} alt="profile picture" className="profile-icon pic"/>
                </div>
                <h4 className="user-name">{props.info.username}</h4>
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
                    <li>Book a Session</li>
                </ul>
                <h2 className="dash-setting">Account settings</h2>
                <ul>
                    <li>Personal info</li>
                    <button>Logout</button>
                </ul>
            </div>
        </div>
    )
}