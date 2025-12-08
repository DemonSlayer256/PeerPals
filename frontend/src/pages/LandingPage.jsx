// LandingPage.jsx
import Login from "../components/Login";

export default function LandingPage() {
    return (
        <>
            <header className="navbar">
                <h1 className="logo">Peer Pals</h1>
                <nav className="nav-links">
                    <a href="#home">Home</a>
                    <a href="#about">About</a>
                    <a href="#contact" className="contact-link">
                        Contact Us
                    </a>
                </nav>
            </header>

            <main className="hero-section">
                <div className="hero-content">
                    <h2 className="tagline">
                        Mentoring Made Easy: Connect, Track, and Learn Instantly.
                    </h2>
                    <p className="sub-tagline">
                        Your pathway to academic success through peer mentorship.
                    </p>
                </div>

                <Login />
            </main>
        </>
    );
}