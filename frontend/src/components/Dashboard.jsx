import { useLocation } from 'react-router-dom';
import "../styles/DashboardStyles.css"
import Sidebar from './Sidebar';
import { useState } from 'react';
import DashMain from './DashMain';

export default function Dashboard() {
    const location = useLocation();
    const data = location.state || {
        user_id: 'S12345',
        username: 'Alice Jhonson',
        role: 'Student',
        email: 'student@example.com' 
    };
    return(
        <div className="dash-container">
            <Sidebar info={data} />
            <DashMain info={data}/>
        </div>
    );
}