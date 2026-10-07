import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import PageShell from "../components/PageShell";
import UpgradeCard from "../components/UpgradeCard";
import { useAuth } from "../hooks/useAuth";

export default function Home() {
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <PageShell wide>
      <section className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.32em] text-gold">Your property workspace</p>
          <h1 className="mt-3 font-display text-5xl text-ivory md:text-6xl">
            Welcome back, {user?.username}
          </h1>
          <p className="mt-4 max-w-2xl text-mist">
            Start a new property check, or upgrade for AI help and fuller reports.
          </p>
        </div>
        <Button variant="gold" className="px-8 py-3 text-base" onClick={() => navigate("/property-domain")}>
          Start Property Analysis
        </Button>
      </section>

      <section className="mt-16">
        <h2 className="font-display text-3xl text-ivory">Unlock More with BhoomiScan</h2>
        <p className="mt-2 text-sm text-mist">Upgrade when you need AI help, deeper checks, and fuller reports.</p>
        <div className="mt-6 grid gap-5 md:grid-cols-3">
          <UpgradeCard
            title="AI Property Assistant"
            description="Ask questions about your property analysis."
            cta="Upgrade"
          />
          <UpgradeCard
            title="Advanced Due Diligence"
            description="Get deeper property verification."
            cta="Upgrade"
          />
          <UpgradeCard
            title="Detailed Reports"
            description="Generate comprehensive property reports."
            cta="Upgrade"
          />
        </div>
      </section>
    </PageShell>
  );
}
