import { useLocation } from 'react-router-dom';

export default function Dashboard()
{
    const location = useLocation();
    const data = location.state;
    return(
        <>
            <p>Login success!! user-id: {data.user_id} username:{data.username}</p>
        </>
    )
}