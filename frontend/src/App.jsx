import Logo from "./Logo.jsx";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export default function App() {
  return (
    <main className="menu">
      <Logo />
      <h1>KhanalChess</h1>
      <p className="tagline">A minimalistic chess game.</p>
      <a className="btn btn-play" href="#">PLAY</a>
      <nav className="links" aria-label="Account and info">
        <a className="btn" href={`${API_URL}/auth/google/login`}>
          Continue with Google
        </a>
        <a className="btn" href="#">About Us</a>
      </nav>
    </main>
  );
}
