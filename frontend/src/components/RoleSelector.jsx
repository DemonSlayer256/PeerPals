export default function RoleSelector ( props ){ //Fixed parameter error
    return (
        <div className="role-selector">
        <button
            className={`role-button ${props.selected === 'student' ? 'active' : ''}`}
            onClick={() => props.onSelect('student')}
        >
            Student
        </button>
        <button
            className={`role-button ${props.selected === 'mentor' ? 'active' : ''}`}
            onClick={() => props.onSelect('mentor')}
        >
            Mentor
        </button>
        <button
            className={`role-button ${props.selected === 'admin' ? 'active' : ''}`}
            onClick={() => props.onSelect('admin')}
        >
            Admin
        </button>
        </div>
    )
}