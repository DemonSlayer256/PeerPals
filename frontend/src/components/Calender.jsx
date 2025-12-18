import React from 'react';
import '../styles/Calender.css';

const Calendar = ({ sessions }) => {
    // Helper to find a session matching a specific day in December 2025
    const getSessionForDay = (day) => {
        if (!sessions || !Array.isArray(sessions)) return null;

        return sessions.find(session => {
            if (!session.date) return false;

            // Create a date object from the session date string (e.g., "2025-12-12")
            const sessionDate = new Date(session.date);
            
            // Check if it matches the day and is in December 2025
            // Note: getMonth() is 0-indexed (11 = December)
            return (
                sessionDate.getDate() === day &&
                sessionDate.getMonth() === 11 && 
                sessionDate.getFullYear() === 2025
            );
        });
    };

    return (
        <div className="calendar-container">
            <div className="calendar-header">
                <button className="nav-button prev-button">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                </button>
                <h4 className="month-label">December 2025</h4>
                <button className="nav-button next-button">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                    </svg>
                </button>
            </div>

            <div className="calendar-weekdays">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => <span key={day}>{day}</span>)}
            </div>

            <div className="calendar-days-grid">
                {[...Array(31).keys()].map(i => {
                    const day = i + 1;
                    const isToday = day === 14; // Assuming today is Dec 14 for visual highlight
                    const sessionOnThisDay = getSessionForDay(day);
                    
                    let dayClass = 'calendar-day';
                    if (isToday) dayClass += ' is-today';
                    if (sessionOnThisDay) dayClass += ' has-event';

                    return (
                        <div 
                            key={i} 
                            className={dayClass}
                            // Show a small tooltip with the session description on hover
                            title={sessionOnThisDay ? `Session: ${sessionOnThisDay.description}` : ''}
                        >
                            {day}
                            {/* Visual indicator for an event */}
                            {sessionOnThisDay && <div className="event-dot"></div>}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Calendar;