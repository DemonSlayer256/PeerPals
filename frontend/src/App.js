import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [view, setView] = useState('login'); // login, student, mentor
  const [role, setRole] = useState('student'); // 'student' or 'mentor'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [feedbacks, setFeedbacks] = useState([]);
  const [concern, setConcern] = useState('');
  const [anonymous, setAnonymous] = useState(false);
  const [mentorId, setMentorId] = useState(1); // example
  const [inbox, setInbox] = useState([]);

  const handleLogin = () => {
    // For simplicity, skipping actual auth
    if (role === 'student') {
      setView('student');
    } else {
      setView('mentor');
    }
  };

  const sendConcern = () => {
    // Send feedback via API
    axios.post('http://127.0.0.1:8000/api/feedbacks/', {
      sid: anonymous ? null : 1, // Replace with actual student id
      mid: mentorId,
      text: concern,
      rating: 5, // Placeholder
    }).then(res => {
      alert('Concern sent!');
    });
  };

  useEffect(() => {
    if (view === 'mentor') {
      // Fetch feedbacks for mentor
      axios.get('http://127.0.0.1:8000/api/feedbacks/')
        .then(res => {
          // Filter feedbacks for this mentor
          setInbox(res.data.filter(fb => fb.mid === mentorId));
        });
    }
  }, [view]);

  if (view === 'login') {
    return (
      <div>
        <h2>Login</h2>
        <select onChange={(e) => setRole(e.target.value)} value={role}>
          <option value="student">Student</option>
          <option value="mentor">Mentor</option>
        </select>
        <input
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          placeholder="Password"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
      </div>
    );
  }

  if (view === 'student') {
    return (
      <div>
        <h2>Student Dashboard</h2>
        <textarea
          placeholder="Your concern..."
          value={concern}
          onChange={(e) => setConcern(e.target.value)}
        />
        <label>
          <input
            type="checkbox"
            onChange={(e) => setAnonymous(e.target.checked)}
          />
          Send Anonymously
        </label>
        <button onClick={sendConcern}>Send Concern</button>
      </div>
    );
  }

  if (view === 'mentor') {
    return (
      <div>
        <h2>Mentor Inbox</h2>
        {inbox.map((fb) => (
          <div key={fb.fid}>
            <p>From: {fb.sid ? `${fb.sid.f_name} ${fb.sid.l_name}` : 'Anonymous'}</p>
            <p>Message: {fb.text}</p>
            <p>Rating: {fb.rating}</p>
          </div>
        ))}
      </div>
    );
  }

  return null;
}

export default App;