// HandleRequest.jsx (MODIFIED)

export default function HandleRequest(props) {
    // function setStatus() {
    //     // NOTE: This currently only updates the local props object, not the backend!
    //     props.sessions.status = 'approved';
    //     console.log("Session status updated locally:", props.sessions.status);
    // }
    
    // Safety check in case sessions is null while loading (though handled in DashMain)
    if (!props.sessions) {
        return (
            <div className="approve-requests-container">
                <h3 className="section-title">Approve Requests</h3>
                <div className="approve-requests-card">
                    <p>No new requests available.</p>
                </div>
            </div>
        );
    }

    // Deconstruct session data for clearer rendering
    const session = props.sessions;

    return (
        <div className="approve-requests-container">
            <h3 className="section-title">Approve Requests</h3>
            
            <div className="approve-requests-card">
                
                {/* Request Header/Title */}
                <h4>Session Request: {session.description || 'Untitled Session'}</h4>
                
                {/* Details */}
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
                    <p>{session.date || 'TBD'}</p>
                </div>

                <div className="request-detail-row">
                    <p className="detail-label">Type:</p>
                    {/* Add logic to check if session is anonymous */}
                    <p>{session.student === 'Anonymous' ? 'Anonymous' : 'Standard'}</p>
                </div>

                {/* Buttons */}
                <div className="request-actions">
                    <button  className="approve-button">
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