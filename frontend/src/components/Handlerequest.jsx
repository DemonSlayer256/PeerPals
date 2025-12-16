export default function HandleRequest(props)
{
    console.log("received request from",props.sessions)
    return (
        <>
            <h4>Approve Requests</h4>
            <div className="approve-sessions">
                <h4 className="req-title"></h4>
                <button>Approve</button>
                <button>Decline</button>
            </div>
        </>
    );
}