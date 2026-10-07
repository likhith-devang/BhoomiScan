import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import Atmosphere from "../components/Atmosphere";
import Button from "../components/Button";
import DemoAuthButton from "../components/DemoAuthButton";
import ErrorMessage from "../components/ErrorMessage";
import Input from "../components/Input";
import Logo from "../components/Logo";
import { errorMessage, useAuth } from "../hooks/useAuth";

export default function Login() {
  const { token, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (token) return <Navigate to="/dashboard" replace />;

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    if (!username.trim() || !password) {
      setError("Username and password are required.");
      return;
    }
    setSubmitting(true);
    try {
      await login(username.trim(), password);
      navigate(location.state?.from || "/dashboard", { replace: true });
    } catch (err) {
      setError(errorMessage(err, "Invalid username or password."));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen">
      <Atmosphere />
      <div className="mx-auto grid min-h-screen max-w-6xl items-center gap-10 px-6 py-12 lg:grid-cols-2">
        <div className="hidden lg:block">
          <Logo />
          <h1 className="mt-8 font-display text-6xl text-ivory">
            Welcome
            <br />
            back.
          </h1>
          <p className="mt-4 max-w-md text-mist">
            Log in to see your files or start a new property check.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="royal-frame p-8">
          <div className="relative z-10 space-y-5">
            <div className="lg:hidden">
              <Logo />
            </div>
            <h2 className="font-display text-4xl">Login</h2>
            <ErrorMessage>{error}</ErrorMessage>
            <Input
              label="Username"
              name="username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              autoComplete="username"
            />
            <Input
              label="Password"
              name="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              autoComplete="current-password"
            />
            <Button type="submit" variant="gold" className="w-full" disabled={submitting}>
              {submitting ? "Signing in…" : "Login"}
            </Button>
            <div className="flex items-center gap-3 text-[10px] uppercase tracking-[0.24em] text-mist">
              <span className="h-px flex-1 bg-white/10" />
              or
              <span className="h-px flex-1 bg-white/10" />
            </div>
            <DemoAuthButton icon="G">Continue with Google</DemoAuthButton>
            <DemoAuthButton icon="𝕏">Continue with X</DemoAuthButton>
            <DemoAuthButton icon="☎">Login with Phone Number</DemoAuthButton>
            <p className="text-center text-sm text-mist">
              New to BhoomiScan?{" "}
              <Link to="/signup" className="text-gold hover:underline">
                Create an account
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
