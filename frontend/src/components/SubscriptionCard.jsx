import Button from "./Button";
import Card from "./Card";

export default function SubscriptionCard({
  plan,
  current = false,
  selected = false,
  onSelect,
}) {
  return (
    <Card
      hover={false}
      className={`flex h-full flex-col ${
        selected || plan.highlighted ? "border-gold/40 shadow-gold" : ""
      }`}
    >
      <p className="text-[10px] uppercase tracking-[0.24em] text-gold">{plan.name}</p>
      <h3 className="mt-2 font-display text-4xl text-ivory">{plan.price}</h3>
      <p className="mt-1 text-sm text-mist">{plan.period}</p>
      <p className="mt-4 text-sm leading-relaxed text-ivory/80">{plan.summary}</p>
      <ul className="mt-5 flex-1 space-y-2 text-sm text-mist">
        {plan.features.map((feature) => (
          <li key={feature} className="flex gap-2">
            <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-gold" aria-hidden="true" />
            <span>{feature}</span>
          </li>
        ))}
      </ul>
      <div className="mt-6">
        {current ? (
          <p className="text-sm font-semibold text-gold">Your current plan</p>
        ) : (
          <Button variant={plan.highlighted ? "gold" : "ghost"} className="w-full" onClick={() => onSelect?.(plan)}>
            {plan.cta}
          </Button>
        )}
      </div>
    </Card>
  );
}
