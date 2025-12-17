import '../styles/DashMain.css';
import DashImg from "../images/dash-img.jpg"
import Calender from './Calender';
import sendGetReq from '../utils/sendGetReq';
import HandleRequest from './Handlerequest';
import sendPostReq from '../utils/sendPostReq';
import { useState,useEffect } from 'react';

// Mock Data structure kept for logical content mapping
// const MOCK_SESSIONS = [
//     { id: 1, title: "DSA Review", date: "12/12/2025", time: "8:00pm", mentor: "Bob" },
//     { id: 2, title: "Intro to React Hooks Workshop", date: "13/12/2025", time: "10:00am", mentor: "Carla" },
//     { id: 3, title: "DSA Review", date: "12/12/2025", time: "8:00pm", mentor: "Bob" }
// ];

async function getData()
{
    const access=localStorage.getItem('accessToken');
    const userRole = localStorage.getItem('userRole')
    console.log("tokens from local storage",access);
    if(access){
        // const userinfo = await sendGetReq('http://localhost:8000/api/students/',access);
        const sessions = await sendGetReq('http://localhost:8000/api/sessions/',access)
        console.log("session obj",sessions)
        return sessions;
    }

}

 function requestSession(requestType)
    {
        const access=localStorage.getItem('accessToken');
        const session = sendPostReq(requestType,'http://localhost:8000/api/sessions/',access);
        console.log("requested session!")
    }

export default function DashMain(props) {
    const [sessionsData, setSessionsData] = useState(null); 
    // isLoading tracks if the data is being fetched (initially true).
    const [isLoading, setIsLoading] = useState(true); 

    // 3. Use useEffect for the Side Effect (Data Fetching)
    useEffect(() => {
        const fetchData = async () => {
            try {
                // Wait for the data fetch
                const fetchedData = await getData();
                
                // Store the result in state, which triggers a re-render
                setSessionsData(fetchedData); 
            } catch (err) {
                console.error("Error fetching sessions data:", err);
                // Handle error state if needed
            } finally {
                // Set loading to false once the operation is complete (success or failure)
                setIsLoading(false); 
            }
        };

         fetchData(); // Execute the inner async function
        console.log("retrieved sessions in effects",sessionsData);
    },[]); // 4. Dependency Array: [] means this runs only once on mount.
    console.log("retrieved sessions",sessionsData);

    const removeApprovedSession = (id) => {
        setSessionsData(prevSessions => prevSessions.filter(item => item.id !== id));
    };

    return(
        <div className="dash-main"> 
            <div className="welcome-card">
                <div className="welcome-text">
                    <h2>Welcome Back, {props.info.first_name}!</h2>
                    <p>
                        Manage all the things from a single dashboard. See latest info sessions, recent conversations, and update your recommendations.
                    </p>
                </div>
                <div className="welcome-illustration">
                    <img 
                        src={DashImg} 
                        alt="welcome"
                    />
                </div>
            </div>
            
            <div className="content-grid">
                <div className="dash-main-left">
                    <div className="calender">
                        <h3 className="calendar-title">Session Calendar</h3>
                        <Calender/>
                    </div>

                    {!sessionsData?"":props.info.role==='mentor'?
                        // Inside DashMain.jsx, where you render the scroll container
                    <div className="approve-requests-section">
                        <h3 className="section-title">Approve Requests</h3>
                        
                        <div className="requests-scroll-container">
                            {/* Filter the data first to see what's actually left to show */}
                            {sessionsData && sessionsData.filter(s => s.status !== 'accept').length > 0 ? (
                                sessionsData
                                    .filter(s => s.status !== 'accept')
                                    .map((session) => (
                                        <HandleRequest 
                                            key={session.id} 
                                            sessions={session} 
                                            onApprovalSuccess={removeApprovedSession} 
                                        />
                                    ))
                            ) : (
                                /* This message shows only when the filtered list is empty */
                                <div className="approve-requests-card empty-state">
                                    <p>No new requests available.</p>
                                </div>
                            )}
                        </div>
                    </div>:<div className="book-session-container" id='book-session'>
                        <h3 className="section-title">Book a Session</h3>
                        <div className="book-session">
                            <div className="book-options">
                                <div className="book-anonymously" onClick={()=>{requestSession({anon:true})}}>
                                    Book Anonymously
                                </div>
                                <div className="book-standard" onClick={()=>{requestSession({anon:false})}}>
                                    Book Standard Session
                                </div>
                            </div>
                            <p className="book-info">
                                Need quick, confidential help? Try anonymous booking.
                            </p>
                        </div>
                    </div>}
                </div>

                <div className="upcoming-sessions-container">
                    <h3 className="section-title">Upcoming Sessions</h3>

                    {(sessionsData === null || sessionsData.length === 0) ? (
                    <p>No sessions available</p>
                    ) : (
                    <div className="session-list">
                        {sessionsData.filter(s => s.status === 'accept').map((session) => (
                        <div key={session.id} className="session-card">
                            <div className="session-header">
                            <span className="session-time">{session.description}</span>
                            <span className="session-date">{session.date}</span>
                            </div>
                            <h4>{session.description}</h4>
                            <p className="session-mentor">Mentor: {session.mentor_name}</p>
                            <button className="join-button">
                            Join Session
                            </button>
                        </div>
                    ))}
                </div>
)}
                </div>

            </div>
        </div>
    )
}