import Logo from "./Logo.jsx";

export default function App() {
  return (
    <main className="menu">
      <Logo />
      <h1>KhanalChess</h1>
      <p className="tagline">A minimalistic chess game.</p>
      <a className="btn btn-play" href="#">PLAY</a>
      <nav className="links" aria-label="Account and info">
        <a className="btn" href="#">Sign up</a>
        <a className="btn" href="#">Login</a>
        <a className="btn" href="#">About Us</a>
      </nav>
    </main>
  );
}
