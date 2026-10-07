const STEPS = ["Property kind", "Home type", "Document vault", "Risk report"];

export default function FlowStepper({ current = 0 }) {
  return (
    <ol className="mb-10 flex flex-wrap items-center gap-3 text-xs uppercase tracking-[0.2em] text-mist">
      {STEPS.map((step, index) => {
        const active = index === current;
        const done = index < current;
        return (
          <li key={step} className="flex items-center gap-3">
            <span
              className={`grid h-7 w-7 place-items-center rounded-full border text-[10px] ${
                active
                  ? "border-gold bg-gold text-void"
                  : done
                    ? "border-sapphire/50 bg-sapphire/20 text-ivory"
                    : "border-white/15"
              }`}
            >
              {index + 1}
            </span>
            <span className={active ? "text-gold" : ""}>{step}</span>
            {index < STEPS.length - 1 ? <span className="hidden h-px w-10 bg-white/10 sm:block" /> : null}
          </li>
        );
      })}
    </ol>
  );
}
