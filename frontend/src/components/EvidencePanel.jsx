import { DOCUMENT_TYPE_LABELS } from "../constants/analysis";

export default function EvidencePanel({ evidence = [], onClose }) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-void/80 p-4" onClick={onClose}>
      <div
        role="dialog"
        aria-labelledby="evidence-title"
        className="royal-frame max-h-[80vh] w-full max-w-2xl overflow-y-auto p-6"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="relative z-10">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-gold">Source evidence</p>
              <h2 id="evidence-title" className="mt-2 font-display text-3xl text-ivory">
                View Evidence
              </h2>
            </div>
            <button type="button" onClick={onClose} className="text-sm text-mist hover:text-ivory" aria-label="Close evidence">
              Close
            </button>
          </div>
          {evidence.length === 0 ? (
            <p className="mt-6 text-sm text-mist">No source text is attached to this finding.</p>
          ) : (
            <div className="mt-6 space-y-4">
              {evidence.map((item) => (
                <article key={item.id || `${item.extracted_field}-${item.source_text}`} className="rounded-2xl border border-white/10 bg-void/50 p-4">
                  <p className="text-[10px] uppercase tracking-[0.18em] text-gold">
                    {DOCUMENT_TYPE_LABELS[item.document_type] || item.document_type || "Document"}
                    {item.page_number ? ` · Page ${item.page_number}` : ""}
                  </p>
                  {item.extracted_field ? (
                    <p className="mt-1 text-xs text-mist">{String(item.extracted_field).replaceAll("_", " ")}</p>
                  ) : null}
                  <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-ivory/90">{item.source_text}</p>
                </article>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
