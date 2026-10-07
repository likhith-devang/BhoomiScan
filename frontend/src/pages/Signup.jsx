import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import Atmosphere from "../components/Atmosphere";
import Button from "../components/Button";
import ErrorMessage from "../components/ErrorMessage";
import Input from "../components/Input";
import Logo from "../components/Logo";
import { errorMessage, useAuth } from "../hooks/useAuth";

export default function Signup() {
  const { token, signup } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (token) return <Navigate to="/dashboard" replace />;

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    if (!username.trim()) {
      setError("Username is required.");
      return;
    }
    if (!password) {
      setError("Password is required.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    setSubmitting(true);
    try {
      await signup({
        username: username.trim(),
        password,
        confirm_password: confirmPassword,
      });
      navigate("/login", { replace: true, state: { registered: username.trim() } });
    } catch (err) {
      setError(errorMessage(err, "We could not create your account. Please try again."));
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
          <h1 className="mt-8 font-display text-6xl text-ivory">Create your account.</h1>
          <p className="mt-4 max-w-md text-mist">
            Sign up to save your property papers and start a check.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="royal-frame p-8">
          <div className="relative z-10 space-y-5">
            <div className="lg:hidden">
              <Logo />
            </div>
            <h2 className="font-display text-4xl">Create account</h2>
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
              autoComplete="new-password"
            />
            <Input
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              autoComplete="new-password"
              error={confirmPassword && password !== confirmPassword ? "Passwords do not match." : ""}
            />
            <Button type="submit" variant="gold" className="w-full" disabled={submitting}>
              {submitting ? "Creating account…" : "Sign up"}
            </Button>
            <p className="text-center text-sm text-mist">
              Already registered?{" "}
              <Link to="/login" className="text-gold hover:underline">
                Login
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
