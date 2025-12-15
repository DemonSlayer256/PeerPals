import React from 'react';
import '../styles/Calender.css'
// Theme Constants (now empty/removed)

// This component uses pure JSX and depends entirely on external CSS for styling.
const Calendar = ({ sessions }) => {
    // Helper to check for events on a specific day (using mock data from MOCK_SESSIONS)
    const getSessionByDay = (day) => {
        // In a real app, this would require proper date comparison
        const dayMap = { 12: 1, 13: 2, 15: 3, 16: 4 }; // Map day of month to session ID
        // Check if the current day has an event based on the mock map
        return dayMap[day];
    };

    return (
        <div className="calendar-container">
            <div className="calendar-header">
                <button className="nav-button prev-button">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" /></svg>
                </button>
                <h4 className="month-label">December 2025</h4>
                <button className="nav-button next-button">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" /></svg>
                </button>
            </div>

            <div className="calendar-weekdays">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => <span key={day}>{day}</span>)}
            </div>

            <div className="calendar-days-grid">
                {[...Array(30).keys()].map(i => {
                    const day = i + 1;
                    const isToday = day === 14;
                    const hasEvent = getSessionByDay(day);
                    
                    // We map class names based on state to be picked up by CSS
                    let dayClass = 'calendar-day';
                    if (isToday) {
                        dayClass += ' is-today';
                    } else if (hasEvent) {
                        dayClass += ' has-event';
                    }

                    return (
                        <div 
                            key={i} 
                            className={dayClass}
                        >
                            {day}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Calendar;