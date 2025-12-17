import sendPatchReq from '../utils/sendPatchReq';
import { useState } from 'react';

export default function HandleRequest(props) {

    const [selectedDate, setSelectedDate] = useState("");
    const session = props.sessions;
    console.log("sessions in handleRequest",session)
    async function setDate() {
        if (!selectedDate) {
            alert("Please select a date first!");
            return;
        }

        const pathData = {
            id:session.id,
            status: 'accept',
            date: selectedDate 
        };

        console.log("Sending data:", pathData);
        const access=localStorage.getItem('accessToken');
       try {
            // Wait for the server to confirm
            await sendPatchReq(`http://localhost:8000/api/sessions/${pathData.id}/`, pathData, access);
            
            // Call the parent function to remove the card from the UI
            props.onApprovalSuccess(session.id); 
            
        } catch (error) {
            console.error("Update failed:", error);
            alert("Could not approve session. Please try again.");
        }
    }
    
    if (!props.sessions || props.sessions.length === 0) {
        return (
            <div className="approve-requests-container">
                <h3 className="section-title">Approve Requests</h3>
                <div className="approve-requests-card">
                    <p>No new requests available.</p>
                </div>
            </div>
        );
    }
    return (
        <div className="approve-requests-container">
            <div className="approve-requests-card">
                <h4>Session Request: {session.id || 'Untitled Session'}</h4>
                <div className="request-detail-row">
                    <p className="detail-label">Student Name:</p>
                    <p>{session.student || 'N/A'}</p>
                </div>
                
                <div className="request-detail-row">
                    <p className="detail-label">Student USN:</p>
                    <p>{session.usn || 'N/A'}</p>
                </div>
                
                <div className="request-detail-row">
                    <p className="detail-label">Requested Date:</p>
                    <div className="setDate">
                        <input type="date" id='date'value={selectedDate} 
                            onChange={(e) => setSelectedDate(e.target.value)}/>
                    </div>
                </div>

                <div className="request-detail-row">
                    <p className="detail-label">Type:</p>
                    <p>{session.student === 'Anonymous' ? 'Anonymous' : 'Standard'}</p>
                </div>
                <div className="request-actions">
                    <button  className="approve-button" onClick={setDate}>
                        Approve and Set date
                    </button>
                    {/* <button className="decline-button">
                        Decline
                    </button> */}
                </div>
            </div>
        </div>
    );
}