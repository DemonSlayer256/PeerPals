// ProfileModal.jsx
import React, { useState } from 'react';

export default function ProfileModal({ info, onClose }) {
    // Local state for the form inputs
    const [formData, setFormData] = useState({
        first_name: info.first_name,
        last_name: info.last_name,
        email: info.user_data.email,
        branch: info.user_data.branch,
        sem: info.user_data.sem,
        mentor:info.user_data.mentor_name
    });

    const handleSave = () => {
        console.log("Saving Profile Data:", formData);
        // This is where you'll call your API later
        onClose(); 
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h3>Personal Details</h3>
                    <button className="close-x" onClick={onClose}>&times;</button>
                </div>
                
                <div className="profile-form">
                    <div className="form-group">
                        <label>First Name</label>
                        <input 
                            type="text" 
                            value={formData.first_name} 
                            onChange={(e) => setFormData({...formData, first_name: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>Last Name</label>
                        <input 
                            type="text" 
                            value={formData.last_name} 
                            onChange={(e) => setFormData({...formData, last_name: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input type="email" value={formData.email} disabled /> 
                        <small>(Email cannot be changed)</small>
                    </div>
                    
                    {info.role === 'student' && (
                        <div className="form-row">
                            <div className="form-group">
                                <label>Branch</label>
                                <input type="text" value={formData.branch} readOnly />
                            </div>
                            <div className="form-group">
                                <label>Semester</label>
                                <input type="text" value={formData.sem} readOnly />
                            </div>
                            <div className="mentor form-group">
                                <label>Mentor</label>
                                <input type="text" value={formData.mentor} readOnly />
                            </div>
                        </div>
                    )}
                </div>

                <div className="modal-actions">
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                    <button className="submit-btn" onClick={handleSave}>Save Changes</button>
                </div>
            </div>
        </div>
    );
}