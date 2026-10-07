const STATUS_STYLES = {
  DETECTED: "border-red-400/40 bg-red-950/35 text-red-100",
  NO_ISSUE_FOUND: "border-emerald-400/30 bg-emerald-950/35 text-emerald-100",
  NOT_VERIFIED: "border-white/15 bg-white/5 text-mist",
};

const STATUS_LABELS = {
  DETECTED: "Detected",
  NO_ISSUE_FOUND: "No issue found",
  NOT_VERIFIED: "Not verified",
};

export default function RiskCategoryCard({ finding, selected, onSelect }) {
  return (
    <button
      type="button"
      onClick={() => onSelect(finding)}
      aria-pressed={selected}
      className={`royal-frame w-full p-5 text-left transition ${selected ? "border-gold/60 shadow-gold" : ""}`}
    >
      <div className="relative z-10">
        <p className="text-[10px] uppercase tracking-[0.24em] text-gold">{finding.category_label}</p>
        <p className="mt-2 font-display text-2xl text-ivory">{finding.risk_level}</p>
        <span className={`mt-3 inline-flex rounded-full border px-3 py-1 text-[10px] uppercase tracking-[0.18em] ${STATUS_STYLES[finding.status] || STATUS_STYLES.NOT_VERIFIED}`}>
          {STATUS_LABELS[finding.status] || finding.status}
        </span>
        <p className="mt-3 text-sm leading-6 text-mist">{finding.summary}</p>
      </div>
    </button>
  );
}
