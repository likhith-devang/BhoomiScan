import { useState } from "react";
import Button from "../components/Button";
import Card from "../components/Card";
import PageShell from "../components/PageShell";
import SubscriptionCard from "../components/SubscriptionCard";
import { PAYMENT_METHODS, PLANS, SUBSCRIPTION_PLANS } from "../constants/subscription";
import { useSubscription } from "../hooks/useSubscription";

export default function Subscription() {
  const { plan } = useSubscription();
  const [selectedPlan, setSelectedPlan] = useState(plan === PLANS.FREE ? PLANS.PRO : plan);
  const [paymentMethod, setPaymentMethod] = useState("apple_pay");
  const [notice, setNotice] = useState("");

  function continueToPayment() {
    setNotice("Payment integration coming soon.");
  }

  return (
    <PageShell wide>
      <p className="text-xs uppercase tracking-[0.32em] text-gold">Plans</p>
      <h1 className="mt-3 font-display text-5xl text-ivory">Subscription</h1>
      <p className="mt-4 max-w-2xl text-mist">
        Choose a plan that fits your property checks. Payment is not live yet, so nothing will be charged.
      </p>

      <section className="mt-10 grid gap-5 lg:grid-cols-3">
        {SUBSCRIPTION_PLANS.map((item) => (
          <SubscriptionCard
            key={item.id}
            plan={item}
            current={item.id === plan}
            selected={item.id === selectedPlan}
            onSelect={(next) => {
              setSelectedPlan(next.id);
              setNotice("");
            }}
          />
        ))}
      </section>

      <Card hover={false} className="mt-10">
        <h2 className="font-display text-3xl text-ivory">Choose payment method</h2>
        <p className="mt-2 text-sm text-mist">
          Pick how you would like to pay. This screen is ready for a real payment provider later.
        </p>
        <fieldset className="mt-6 space-y-3">
          <legend className="sr-only">Payment method</legend>
          {PAYMENT_METHODS.map((method) => (
            <label
              key={method.id}
              className={`flex cursor-pointer items-center gap-3 rounded-2xl border px-4 py-3 text-sm ${
                paymentMethod === method.id
                  ? "border-gold/50 bg-gold/10 text-ivory"
                  : "border-white/10 bg-white/5 text-mist"
              }`}
            >
              <input
                type="radio"
                name="payment-method"
                value={method.id}
                checked={paymentMethod === method.id}
                onChange={() => setPaymentMethod(method.id)}
                className="accent-gold"
              />
              {method.label}
            </label>
          ))}
        </fieldset>
        <div className="mt-6">
          <Button variant="gold" onClick={continueToPayment}>
            Continue to Payment
          </Button>
        </div>
        {notice ? (
          <p className="mt-4 text-sm font-semibold text-gold" role="status">
            {notice}
          </p>
        ) : null}
      </Card>
    </PageShell>
  );
}
