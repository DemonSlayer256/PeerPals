// Dashboard.jsx
import { useLocation } from 'react-router-dom';
import "../styles/DashboardStyles.css"
import Sidebar from './Sidebar';
import { useState } from 'react';
import DashMain from './DashMain';
import ProfileModal from './ProfileModal'; 
import ChangePasswordModal from './ChangePasswordModal';
import RegisterUserModal from './RegisterUserModal';

export default function Dashboard() {
    const location = useLocation();
    const data = location.state;
    console.log("user data",data)
    const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);
    const [isChangePassOpen, setIsChangePassOpen] = useState(false);
    const [registerType, setRegisterType] = useState(null);

    return(
        <div className="dash-container">
            <Sidebar 
                info={data} 
                onProfileClick={() => setIsProfileModalOpen(true)} 
                onChangePassClick={() => setIsChangePassOpen(true)}
            />
            
            <DashMain info={data} onRegisterClick={(type) => setRegisterType(type)}/>

            {registerType && (
                <RegisterUserModal 
                    type={registerType} 
                    onClose={() => setRegisterType(null)} 
                />
            )}

            {isProfileModalOpen && (
                <ProfileModal 
                    info={data} 
                    onClose={() => setIsProfileModalOpen(false)} 
                />
            )}

            {isChangePassOpen && (
            <ChangePasswordModal onClose={() => setIsChangePassOpen(false)} />
            )}
        </div>
    );
}