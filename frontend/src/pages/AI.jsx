import { Link } from "react-router-dom";
import AIChat from "../components/AIChat";
import Button from "../components/Button";
import Card from "../components/Card";
import PageShell from "../components/PageShell";
import { useSubscription } from "../hooks/useSubscription";
import { askPropertyAssistant } from "../services/ai";

export default function AI() {
  const { canUseAI } = useSubscription();

  return (
    <PageShell>
      <p className="text-xs uppercase tracking-[0.32em] text-gold">BhoomiScan AI</p>
      <h1 className="mt-3 font-display text-5xl text-ivory md:text-6xl">BhoomiScan AI</h1>
      <p className="mt-4 max-w-2xl text-mist">
        Ask questions about your property documents and risk analysis.
      </p>

      {canUseAI ? (
        <div className="mt-8">
          <AIChat onSend={(question) => askPropertyAssistant({ question })} />
        </div>
      ) : (
        <Card hover={false} className="mt-8">
          <h2 className="font-display text-3xl text-ivory">Your AI property assistant</h2>
          <p className="mt-3 max-w-xl text-sm leading-relaxed text-mist">
            Your AI property assistant is available with a Pro subscription. We will not invent
            answers here. After you upgrade and Phase 2 is connected, this page becomes your live
            assistant for uploaded papers and risk findings.
          </p>
          <div className="mt-6">
            <Link to="/subscription">
              <Button variant="gold">Upgrade to Pro</Button>
            </Link>
          </div>
        </Card>
      )}
    </PageShell>
  );
}
