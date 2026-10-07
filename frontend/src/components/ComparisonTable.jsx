const RESULT_STYLES = {
  MATCH: "border-emerald-400/30 bg-emerald-950/30 text-emerald-100",
  MISMATCH: "border-red-400/40 bg-red-950/35 text-red-100",
  NOT_AVAILABLE: "border-white/15 bg-white/5 text-mist",
};

export default function ComparisonTable({ rows = [], empty = "No comparison results yet." }) {
  if (!rows.length) {
    return <p className="text-sm text-mist">{empty}</p>;
  }
  return (
    <div className="space-y-4">
      {rows.map((row) => (
        <article key={row.id || `${row.field}-${row.document_a_id}-${row.document_b_id}-${row.result}`} className="royal-frame p-5">
          <div className="relative z-10">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="text-[10px] uppercase tracking-[0.2em] text-gold">{row.field_label || row.field}</p>
              <span className={`rounded-full border px-3 py-1 text-[10px] uppercase tracking-[0.18em] ${RESULT_STYLES[row.result] || RESULT_STYLES.NOT_AVAILABLE}`}>
                {row.result.replaceAll("_", " ")}
              </span>
            </div>
            {row.result === "MISMATCH" ? (
              <dl className="mt-4 grid gap-3 sm:grid-cols-2">
                <div>
                  <dt className="text-[10px] uppercase tracking-[0.16em] text-mist">Document 1</dt>
                  <dd className="mt-1 text-sm text-ivory">{row.document_a_name || "First document"}</dd>
                  <dd className="mt-1 text-sm text-gold">{row.value_a}</dd>
                </div>
                <div>
                  <dt className="text-[10px] uppercase tracking-[0.16em] text-mist">Document 2</dt>
                  <dd className="mt-1 text-sm text-ivory">{row.document_b_name || "Second document"}</dd>
                  <dd className="mt-1 text-sm text-gold">{row.value_b}</dd>
                </div>
              </dl>
            ) : (
              <p className="mt-3 text-sm text-ivory/90">{row.value_a || "Not enough documents contain this field."}</p>
            )}
            {row.severity ? <p className="mt-3 text-xs uppercase tracking-[0.16em] text-gold">Severity: {row.severity}</p> : null}
            <p className="mt-3 text-sm leading-6 text-mist">{row.explanation}</p>
          </div>
        </article>
      ))}
    </div>
  );
}
