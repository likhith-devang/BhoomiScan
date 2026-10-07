import Card from "../components/Card";
import PageShell from "../components/PageShell";
import { useAuth } from "../hooks/useAuth";
import { useSubscription } from "../hooks/useSubscription";
import { formatDate } from "../lib/userDisplay";

function Field({ label, value }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
      <dt className="text-[10px] uppercase tracking-[0.2em] text-mist">{label}</dt>
      <dd className="mt-1 text-sm font-semibold text-ivory">{value}</dd>
    </div>
  );
}

export default function ProfileSettings() {
  const { user } = useAuth();
  const { planName } = useSubscription();

  return (
    <PageShell>
      <p className="text-xs uppercase tracking-[0.32em] text-gold">Account</p>
      <h1 className="mt-3 font-display text-5xl text-ivory">Profile Settings</h1>
      <p className="mt-4 max-w-2xl text-mist">
        These details come from your signed-in BhoomiScan account. Editing is kept simple for now.
      </p>
      <Card hover={false} className="mt-8">
        <dl className="grid gap-4 sm:grid-cols-2">
          <Field label="Username" value={user?.username || "Not available"} />
          <Field label="Email" value="Not added yet" />
          <Field label="Account status" value="Active" />
          <Field label="Subscription status" value={planName} />
          <Field label="Member since" value={formatDate(user?.created_at)} />
        </dl>
      </Card>
    </PageShell>
  );
}
