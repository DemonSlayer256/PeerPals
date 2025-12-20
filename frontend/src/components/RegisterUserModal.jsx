import React, { useState } from 'react';
import sendPostReq from '../utils/sendPostReq';

export default function RegisterUserModal({ type, onClose }) {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        password_confirm: "", // Required by your validate_password
        name: "",             // Mapped to first_name in your backend
        email: "",
        role: type,
        branch: "",
        sem: "",
        mid: "",              // Username of the mentor
        contact: ""           // For mentors
    });
    const handleSubmit = async () => {
        const access = localStorage.getItem('accessToken');
        
        // Ensure semester is sent as an integer as per your backend validation
        const finalData = {
            ...formData,
            sem: formData.sem ? parseInt(formData.sem) : null
        };

        try {
            await sendPostReq(finalData, 'http://localhost:8000/api/register/', access);
            alert(`${type.toUpperCase()} registered successfully!`);
            console.log(finalData.role)
            onClose();
        } catch (err) {
            console.error(err);
            alert("Registration failed. Please check your inputs.");
        }
    };
    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h3>Register New {type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                    <button className="close-x" onClick={onClose}>&times;</button>
                </div>

                <div className="profile-form">
                    <div className="form-row">
                        <div className="form-group">
                            <label>Full Name</label>
                            <input type="text" placeholder="Full Name" onChange={(e)=>setFormData({...formData, name: e.target.value})} />
                        </div>
                        <div className="form-group">
                            <label>Username</label>
                            <input 
                                type="text" 
                                placeholder="Username" 
                                onChange={(e) => {
                                    const val = e.target.value;
                                    setFormData(prev => {
                                        const updatedData = { ...prev, username: val };
                                        if (type === 'mentor') {
                                            updatedData.mid = val;
                                            updatedData.sem = 5;
                                        }
                                        return updatedData;
                                    });
                                }} 
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input type="email" placeholder="Email" onChange={(e)=>setFormData({...formData, email: e.target.value})} />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Password</label>
                            <input type="password" placeholder="••••" onChange={(e)=>setFormData({...formData, password: e.target.value})} />
                        </div>
                        <div className="form-group">
                            <label>Confirm Password</label>
                            <input type="password" placeholder="••••" onChange={(e)=>setFormData({...formData, password_confirm: e.target.value})} />
                        </div>
                    </div>

                    {/* --- Dynamic Fields based on Role --- */}
                    
                    {(type === 'student' || type === 'mentor') && (
                        <div className="form-group">
                            <label>Branch</label>
                            <input type="text" placeholder="e.g. CSE" onChange={(e)=>setFormData({...formData, branch: e.target.value})} />
                        </div>
                    )}

                    {type === 'student' && (
                        <div className="form-row">
                            <div className="form-group">
                                <label>Semester (1-8)</label>
                                <input type="number" placeholder="Sem" onChange={(e)=>setFormData({...formData, sem: e.target.value})} />
                            </div>
                            <div className="form-group">
                                <label>Assign Mentor (Username)</label>
                                <input type="text" placeholder="Mentor Username" onChange={(e)=>setFormData({...formData, mid: e.target.value})} />
                            </div>
                        </div>
                    )}
                        <div className="form-group">
                            <label>Contact Number</label>
                            <input type="text" placeholder="+123456789" onChange={(e)=>setFormData({...formData, contact: e.target.value})} />
                        </div>
                </div>

                <div className="modal-actions">
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                    <button className="submit-btn" onClick={handleSubmit}>Register User</button>
                </div>
            </div>
        </div>
    );
}