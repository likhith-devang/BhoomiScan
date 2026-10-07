import Button from "./Button";
import { formatBytes, formatDate } from "../constants/property";
import { DOCUMENT_TYPE_LABELS } from "../constants/analysis";

export default function DocumentCard({
  document,
  pending,
  onRemove,
  onUpload,
  uploading,
  analyzing,
  onAnalyze,
  onViewAnalysis,
  onViewEvidence,
  onDelete,
}) {
  const name = document.original_filename || document.name;
  const size = document.file_size ?? document.size;
  const uploaded = Boolean(document.id);
  const status = document.status || (uploaded ? "UPLOADED" : null);
  const typeLabel = DOCUMENT_TYPE_LABELS[document.document_type] || document.document_type;

  return (
    <div className="royal-frame flex flex-wrap items-center justify-between gap-4 p-4">
      <div className="relative z-10 min-w-0">
        <p className="truncate font-medium text-ivory">{name}</p>
        <p className="mt-1 text-xs uppercase tracking-[0.16em] text-mist">
          {formatBytes(size)}
          {typeLabel ? ` · ${typeLabel}` : ""}
          {status ? ` · ${status}` : uploaded ? " · Saved" : " · Ready to save"}
          {document.created_at ? ` · ${formatDate(document.created_at)}` : ""}
        </p>
      </div>
      <div className="relative z-10 flex flex-wrap gap-2">
        {pending ? (
          <>
            <Button variant="ghost" onClick={onRemove}>
              Remove
            </Button>
            <Button onClick={onUpload} disabled={uploading}>
              {uploading ? "Uploading…" : "Upload"}
            </Button>
          </>
        ) : (
          <>
            {status === "ANALYZED" ? (
              <>
                <Button variant="ghost" onClick={onViewAnalysis}>
                  View Analysis
                </Button>
                {onViewEvidence ? (
                  <Button variant="ghost" onClick={onViewEvidence}>
                    View Evidence
                  </Button>
                ) : null}
              </>
            ) : null}
            <Button onClick={onAnalyze} disabled={analyzing}>
              {analyzing ? "Analyzing…" : "Analyze"}
            </Button>
            {onDelete ? (
              <Button variant="danger" onClick={onDelete}>
                Delete
              </Button>
            ) : null}
          </>
        )}
      </div>
    </div>
  );
}
