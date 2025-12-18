import React, { useState } from 'react';
import sendPatchReq from '../utils/sendPatchReq';

export default function ChangePasswordModal({ onClose }) {
    const [passwords, setPasswords] = useState({
        old_password: "",
        new_password: "",
        password_confirm: ""
    });
    const [error, setError] = useState("");

    const handleSubmit = async () => {
        // 1. Basic Validation
        if (passwords.new_password !== passwords.password_confirm) {
            setError("New passwords do not match!");
            return;
        }

        const access = localStorage.getItem('accessToken');
        const data = {
            password: passwords.new_password,
            password_confirm: passwords.password_confirm
        };

        try {
            // 2. Send request to your Django URL
            await sendPatchReq( 'http://localhost:8000/api/change_password/',data, access);
            alert("Password changed successfully!");
            onClose();
        } catch (err) {
            setError("Failed to change password. Check your old password.");
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h3>Change Password</h3>
                    <button className="close-x" onClick={onClose}>&times;</button>
                </div>

                {error && <p style={{ color: 'red', fontSize: '0.8rem' }}>{error}</p>}

                <div className="profile-form">
                    <div className="form-group">
                        <label>Old Password</label>
                        <input 
                            type="password" 
                            value={passwords.old_password}
                            onChange={(e) => setPasswords({...passwords, old_password: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>New Password</label>
                        <input 
                            type="password" 
                            value={passwords.new_password}
                            onChange={(e) => setPasswords({...passwords, new_password: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>Confirm New Password</label>
                        <input 
                            type="password" 
                            value={passwords.password_confirm}
                            onChange={(e) => setPasswords({...passwords, password_confirm: e.target.value})}
                        />
                    </div>
                </div>

                <div className="modal-actions">
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                    <button 
                        className="submit-btn" 
                        onClick={handleSubmit}
                        disabled={!passwords.old_password || !passwords.new_password}
                    >
                        Update Password
                    </button>
                </div>
            </div>
        </div>
    );
}