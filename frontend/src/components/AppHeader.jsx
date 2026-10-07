import { useEffect, useRef, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Button from "./Button";
import Logo from "./Logo";
import ProfileDropdown from "./ProfileDropdown";
import ProfilePill from "./ProfilePill";

function AuthNavLink({ to, children, className = "" }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `rounded-full px-3 py-1.5 text-sm font-semibold transition ${
          isActive ? "bg-white/10 text-gold" : "text-mist hover:text-ivory"
        } ${className}`
      }
    >
      {children}
    </NavLink>
  );
}

export default function AppHeader({ transparent = false }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    if (!menuOpen) return undefined;

    function handlePointer(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuOpen(false);
      }
    }

    function handleKey(event) {
      if (event.key === "Escape") setMenuOpen(false);
    }

    document.addEventListener("mousedown", handlePointer);
    document.addEventListener("keydown", handleKey);
    return () => {
      document.removeEventListener("mousedown", handlePointer);
      document.removeEventListener("keydown", handleKey);
    };
  }, [menuOpen]);

  function signOut() {
    setMenuOpen(false);
    navigate("/");
    logout();
  }

  return (
    <header
      className={`sticky top-0 z-40 border-b border-white/5 ${
        transparent ? "bg-void/40 backdrop-blur-xl" : "bg-void/80 backdrop-blur-xl"
      }`}
    >
      <div className="mx-auto flex h-20 max-w-6xl items-center gap-4 px-4 sm:px-6">
        <Link to={user ? "/dashboard" : "/"} className="shrink-0" aria-label="BhoomiScan home">
          <span className="md:hidden">
            <Logo compact />
          </span>
          <span className="hidden md:block">
            <Logo />
          </span>
        </Link>

        <nav className="flex min-w-0 flex-1 items-center justify-end gap-2 sm:gap-3">
          {user ? (
            <>
              <AuthNavLink to="/dashboard" className="hidden md:inline-flex">
                Home
              </AuthNavLink>
              <AuthNavLink to="/ai">AI</AuthNavLink>
              <div className="relative ml-1" ref={menuRef}>
                <ProfilePill user={user} open={menuOpen} onToggle={() => setMenuOpen((open) => !open)} />
                {menuOpen ? <ProfileDropdown onClose={() => setMenuOpen(false)} onSignOut={signOut} /> : null}
              </div>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm font-semibold text-mist hover:text-ivory">
                Login
              </Link>
              <Link to="/signup">
                <Button variant="gold">Get Started</Button>
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
