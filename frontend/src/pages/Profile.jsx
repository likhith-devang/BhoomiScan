import { Link } from "react-router-dom";
import Button from "../components/Button";
import Card from "../components/Card";
import PageShell from "../components/PageShell";
import { useAuth } from "../hooks/useAuth";
import { useSubscription } from "../hooks/useSubscription";
import { getUserInitials } from "../lib/userDisplay";

export default function Profile() {
  const { user } = useAuth();
  const { planName } = useSubscription();
  const username = user?.username || "User";

  return (
    <PageShell>
      <p className="text-xs uppercase tracking-[0.32em] text-gold">Account</p>
      <h1 className="mt-3 font-display text-5xl text-ivory">Profile</h1>
      <Card hover={false} className="mt-8 flex flex-col gap-6 sm:flex-row sm:items-center">
        <span className="grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-royal to-gold text-lg font-bold text-ivory">
          {getUserInitials(username)}
        </span>
        <div className="flex-1">
          <h2 className="font-display text-3xl text-ivory">{username}</h2>
          <p className="mt-1 text-sm text-mist">Plan: {planName}</p>
        </div>
        <Link to="/profile/settings">
          <Button variant="ghost">Profile Settings</Button>
        </Link>
      </Card>
    </PageShell>
  );
}
