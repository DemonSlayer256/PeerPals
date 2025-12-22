import '../styles/DashMain.css';
import DashImg from "../images/dash-img.jpg"
import Calender from './Calender';
import sendGetReq from '../utils/sendGetReq';
import HandleRequest from './Handlerequest';
import sendPostReq from '../utils/sendPostReq';
import { useState, useEffect } from 'react';

// --- Helper Functions ---
async function getData() {
    const access = localStorage.getItem('accessToken');
    if (access) {
        const sessions = await sendGetReq('http://localhost:8000/api/sessions/', access);
        return sessions;
    }
}

export default function DashMain(props) {
    // 1. ALL HOOKS AT THE TOP (The "Rules of Hooks" Fix)
    const [sessionsData, setSessionsData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [bookingConfig, setBookingConfig] = useState({ anon: false });
    const [sessionDescription, setSessionDescription] = useState("");

    // 2. Fetch Data on Load
    useEffect(() => {
        const fetchData = async () => {
            try {
                const fetchedData = await getData();
                setSessionsData(fetchedData);
            } catch (err) {
                console.error("Error fetching sessions:", err);
            } finally {
                setIsLoading(false);
            }
        };
        fetchData();
    }, []);

    // 3. Logic Handlers
    const openBookingForm = (isAnon) => {
        setBookingConfig({ anon: isAnon });
        setIsModalOpen(true);
    };

    const handleFinalSubmit = async () => {
        const access = localStorage.getItem('accessToken');
        const postData = {
            anon: bookingConfig.anon,
            description: sessionDescription
        };
        
        try{
            await sendPostReq(postData, 'http://localhost:8000/api/sessions/', access);
            setIsModalOpen(false);
            setSessionDescription("");
            alert("Session requested successfully!");
        }
        catch(err)
        {
            return (<div>{err}</div>)
        }
    };

    const removeApprovedSession = (id) => {
        setSessionsData(prev => prev.filter(item => item.id !== id));
    };

    // 4. Early Return for Loading
    if (isLoading) {
        return <div className="dash-main">Loading Dashboard Data...</div>;
    }

    if(props.info.role === 'admin')
    {
        const openRegisterStudent = () => {
            props.onRegisterClick("student"); 
        };

        const openRegisterMentor = () => {
            props.onRegisterClick("mentor");
        };
        return(
            <div className="dash-main">
                <div className="welcome-card">
                    <div className="welcome-text">
                        <h2>Welcome Back, {props.info.first_name || "User"}!</h2>
                        <p>Manage users and their data here.</p>
                    </div>
                    <div className="welcome-illustration">
                        <img src={DashImg} alt="welcome" />
                    </div>
                </div>

                <div className="dash-admin">
                   <div className='dash-admin-left'>
                        <div className="admin-session-container">
                                <h3 className="section-title">Register a User</h3>
                                <div className="admin-session">
                                    <div className="admin-options">
                                        <div className="book-anonymously" onClick={() => openRegisterStudent()}>
                                            New Student
                                        </div>
                                        <div className="book-standard" onClick={() => openRegisterMentor()}>
                                            New Mentor
                                        </div>
                                    </div>
                                    <p>Register a new user</p>
                                </div>
                        </div>

                        <div className="admin-session-container">
                                <h3 className="section-title">Assign a Mentor</h3>
                                <div className="admin-session">
                                    <div className="admin-mentor">
                                        <div className="book-anonymously assign-mentor" onClick={() => openRegisterStudent()}>
                                            Assign mentor
                                        </div>
                                        <p>Assign or change the mentor of a student</p>
                                    </div>
                                </div>
                        </div>
                    </div>
                    <div className="upcoming-sessions-container">
                        <h3 className="section-title">Booked Sessions</h3>
                        <div className="session-list">
                            {sessionsData?.filter(s => s.status === 'accept').map(session => (
                                <div key={session.id} className="session-card">
                                    <h4>{session.description}</h4>
                                    <p className="session-mentor">Session Type : {session.student !== 'Anonymous'?'Standard':'Anonymous'}</p>
                                    <p className="session-mentor">Name : {session.student !== 'Anonymous'?session.student:'Anonymous'}</p>
                                    <p className="session-mentor">Date : {session.date}</p>
                                    <p className="session-mentor">Description : {session.description? session.description:"General Advice"}</p>
                                    <p className="session-mentor">Mentor: {session.mentor_name}</p>
                                    <button className="join-button">Join Session</button>
                                </div>
                            )) || <p>No upcoming sessions.</p>}
                        </div>
                    </div>
                </div>
            </div>
            
        )
    }
    return (
        <div className="dash-main">
            {/* --- Welcome Banner --- */}
            <div className="welcome-card">
                <div className="welcome-text">
                    <h2>Welcome Back, {props.info.first_name || "User"}!</h2>
                    <p>Manage your sessions and track your progress from here.</p>
                </div>
                <div className="welcome-illustration">
                    <img src={DashImg} alt="welcome" />
                </div>
            </div>

            <div className="content-grid">
                {/* --- Left Column: Calendar & Actions --- */}
                <div className="dash-main-left">
                    <div className="calender">
                        <h3 className="calendar-title">Session Calendar</h3>
                        <Calender sessions={sessionsData}/>
                    </div>

                    {props.info.role === 'mentor' ? (
                        <div className="approve-requests-section">
                            <h3 className="section-title">Approve Requests</h3>
                            <div className="requests-scroll-container">
                                {sessionsData?.filter(s => s.status !== 'accept').length > 0 ? (
                                    sessionsData.filter(s => s.status !== 'accept').map(session => (
                                        <HandleRequest 
                                            key={session.id} 
                                            sessions={session} 
                                            onApprovalSuccess={removeApprovedSession} 
                                        />
                                    ))
                                ) : <p>No new requests.</p>}
                            </div>
                        </div>
                    ) : (
                        <div className="book-session-container">
                            <h3 className="section-title">Book a Session</h3>
                            <div className="book-session">
                                <div className="book-options">
                                    <div>
                                        <div className="book-anonymously" onClick={() => openBookingForm(true)}>Book Anonymously</div>
                                        <div className="book-standard" onClick={() => openBookingForm(false)}>Book Standard</div>
                                    </div>
                                    <p>Want a quick advice secretly? Try Anonymous booking!</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* --- Right Column: Upcoming Sessions --- */}
                <div className="upcoming-sessions-container">
                    <h3 className="section-title">Upcoming Sessions</h3>
                    <div className="session-list">
                        {sessionsData?.filter(s => s.status === 'accept').map(session => (
                            <div key={session.id} className="session-card">
                                <h4>{session.description}</h4>
                                <p className="session-mentor">Session Type : {session.student !== 'Anonymous'?'Standard':'Anonymous'}</p>
                                <p className="session-mentor">Name : {session.student !== 'Anonymous'?session.student:'Anonymous'}</p>
                                <p className="session-mentor">Date : {session.date}</p>
                                <p className="session-mentor">Description : {session.description? session.description:"General Advice"}</p>
                                <p className="session-mentor">Mentor: {session.mentor_name}</p>
                                <button className="join-button">Join Session</button>
                            </div>
                        )) || <p>No upcoming sessions.</p>}
                    </div>
                </div>
            </div>

            {/* --- THE MODAL (Appears on top of everything) --- */}
            {isModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>{bookingConfig.anon ? "Anonymous" : "Standard"} Booking</h3>
                        <p>What would you like to discuss in this session?</p>
                        <textarea 
                            className="modal-textarea"
                            value={sessionDescription}
                            onChange={(e) => setSessionDescription(e.target.value)}
                            placeholder="Type a short description..."
                        />
                        <div className="modal-actions">
                            <button className="cancel-btn" onClick={() => setIsModalOpen(false)}>Cancel</button>
                            <button className="submit-btn" onClick={handleFinalSubmit} disabled={!sessionDescription.trim()}>
                                Submit Request
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}