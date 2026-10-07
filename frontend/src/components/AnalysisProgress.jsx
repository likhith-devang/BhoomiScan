export default function AnalysisProgress({ steps = [], processing = false, failed = false }) {
  const items = steps.length
    ? steps
    : [
        { id: "uploaded", label: "Document uploaded", done: true },
        { id: "reading", label: "Reading document", done: false },
        { id: "extracting", label: "Extracting information", done: false },
        { id: "checking", label: "Checking risks", done: false },
        { id: "complete", label: "Analysis complete", done: false },
      ];

  return (
    <ol className="space-y-3">
      {items.map((step, index) => (
        <li key={step.id} className="flex items-center gap-3 text-sm">
          <span
            className={`grid h-6 w-6 place-items-center rounded-full border text-[11px] ${
              step.done
                ? "border-emerald-400/40 bg-emerald-950/50 text-emerald-200"
                : failed
                  ? "border-red-400/40 text-red-200"
                  : "border-white/15 text-mist"
            }`}
          >
            {step.done ? "✓" : index + 1}
          </span>
          <span className={step.done ? "text-ivory" : "text-mist"}>{step.label}</span>
        </li>
      ))}
      {processing ? <li className="text-sm text-gold">Analyzing your document...</li> : null}
    </ol>
  );
}
