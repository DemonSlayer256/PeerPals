import React from 'react';
import '../styles/Calender.css';

const Calendar = ({ sessions }) => {
    const today = new Date();
    
    // 1. Keep these as numbers for easier comparison later
    const currentDay = today.getDate();
    const currentMonth = today.getMonth(); 
    const currentYear = today.getFullYear();

    // 2. Get the formatted month name
    const monthName = today.toLocaleString('default', { month: 'long' });

    // 3. DYNAMICALLY calculate how many days are in THIS specific month
    // Setting day '0' of the NEXT month gives us the last day of the CURRENT month
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    const getSessionForDay = (day) => {
        if (!sessions || !Array.isArray(sessions)) return null;

        return sessions.find(session => {
            if (!session.date) return false;
            const sessionDate = new Date(session.date);
            
            // Compare as numbers for strict accuracy
            return (
                sessionDate.getDate() === day &&
                sessionDate.getMonth() === currentMonth && 
                sessionDate.getFullYear() === currentYear
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
                <h4 className="month-label">{`${monthName} ${currentYear}`}</h4>
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
                {/* 4. Map through the EXACT number of days in the month */}
                {[...Array(daysInMonth).keys()].map(i => {
                    const day = i + 1;
                    const isToday = day === currentDay; // Direct number comparison
                    const sessionOnThisDay = getSessionForDay(day);
                    
                    let dayClass = 'calendar-day';
                    if (isToday) dayClass += ' is-today';
                    if (sessionOnThisDay) dayClass += ' has-event';

                    return (
                        <div 
                            key={day} 
                            className={dayClass}
                            title={sessionOnThisDay ? `Session: ${sessionOnThisDay.description}` : ''}
                        >
                            {day}
                            {sessionOnThisDay && <div className="event-dot"></div>}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Calendar;