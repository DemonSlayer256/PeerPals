import React from 'react';
import '../styles/DashMain.css';
import DashImg from "../images/dash-img.jpg"
import Calender from './Calender';

// Mock Data structure kept for logical content mapping
const MOCK_SESSIONS = [
    { id: 1, title: "DSA Review", date: "12/12/2025", time: "8:00pm", mentor: "Bob" },
    { id: 2, title: "Intro to React Hooks Workshop", date: "13/12/2025", time: "10:00am", mentor: "Carla" },
    { id: 1, title: "DSA Review", date: "12/12/2025", time: "8:00pm", mentor: "Bob" },
    { id: 2, title: "Intro to React Hooks Workshop", date: "13/12/2025", time: "10:00am", mentor: "Carla" }
];

export default function DashMain(props) {
    const userName = "Alice"; 

    return(
        <div className="dash-main"> 
            
            {/* 1. Welcome Banner */}
            <div className="welcome-card">
                <div className="welcome-text">
                    <h2>Welcome Back, {userName}!</h2>
                    <p>
                        Manage all the things from a single dashboard. See latest info sessions, recent conversations, and update your recommendations.
                    </p>
                </div>
                <div className="welcome-illustration">
                    <img 
                        src={DashImg} 
                        alt="welcome image"
                    />
                </div>
            </div>
            
            <div className="content-grid">
                <div className="calender">
                    <h3 className="calendar-title">Session Calendar</h3>
                    <Calender/>
                </div>

                <div className="upcoming-sessions-container">
                    <h3 className="section-title">Upcoming Sessions</h3>

                    <div className="session-list">
                        {MOCK_SESSIONS.map(session => (
                            <div key={session.id} className="session-card">
                                <div className="session-header">
                                    <span className="session-time">{session.time}</span>
                                    <span className="session-date">{session.date}</span>
                                </div>
                                <h4>{session.title}</h4>
                                <p className="session-mentor">Mentor: {session.mentor}</p>
                                <button className="join-button">
                                    Join Session
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="book-session-container" id='book-session'>
                    <h3 className="section-title">Book a Session</h3>
                    <div className="book-session">
                        <div className="book-options">
                            <div className="book-anonymously">
                                Book Anonymously
                            </div>
                            <div className="book-standard">
                                Book Standard Session
                            </div>
                        </div>
                        <p className="book-info">
                            Need quick, confidential help? Try anonymous booking.
                        </p>
                    </div>
                </div>

            </div>
        </div>
    )
}