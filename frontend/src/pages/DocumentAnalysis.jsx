import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import AnalysisProgress from "../components/AnalysisProgress";
import Button from "../components/Button";
import ErrorMessage from "../components/ErrorMessage";
import EvidencePanel from "../components/EvidencePanel";
import ExtractedDetails from "../components/ExtractedDetails";
import LoadingSpinner from "../components/LoadingSpinner";
import PageShell from "../components/PageShell";
import RecommendationList from "../components/RecommendationList";
import RiskCategoryCard from "../components/RiskCategoryCard";
import { caseApi, errorMessage } from "../services/api";

function DetailRow({ label, value }) {
  if (value === null || value === undefined || value === "") return null;
  const display = typeof value === "boolean" ? (value ? "Present" : "Not present") : value;
  return (
    <div>
      <dt className="text-[10px] uppercase tracking-[0.18em] text-mist">{label}</dt>
      <dd className="mt-1 text-sm text-ivory">{display}</dd>
    </div>
  );
}

export default function DocumentAnalysis() {
  const { caseId, documentId } = useParams();
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState(null);
  const [showEvidence, setShowEvidence] = useState(false);
  const [showOriginal, setShowOriginal] = useState(false);
  const [showDocumentText, setShowDocumentText] = useState(false);

  async function load() {
    const response = await caseApi.documentAnalysis(caseId, documentId);
    setAnalysis(response.data);
    setSelected(response.data.findings?.[0] || null);
  }

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    load()
      .catch(async (err) => {
        if (err?.response?.status === 404) {
          try {
            await runAnalysis();
            return;
          } catch (inner) {
            if (!cancelled) setError(errorMessage(inner, "We could not analyse this document."));
            return;
          }
        }
        if (!cancelled) setError(errorMessage(err, "We could not load this analysis."));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [caseId, documentId]);

  async function runAnalysis() {
    setRunning(true);
    setError("");
    try {
      const response = await caseApi.analyze(caseId, documentId);
      setAnalysis(response.data);
      setSelected(response.data.findings?.[0] || null);
    } finally {
      setRunning(false);
      setLoading(false);
    }
  }

  const details = selected?.finding_data || {};

  return (
    <PageShell wide>
      <button type="button" onClick={() => navigate(`/property-case/${caseId}/upload`)} className="text-xs uppercase tracking-[0.2em] text-mist">
        ← Back to papers
      </button>
      <p className="mt-4 text-xs uppercase tracking-[0.32em] text-gold">Document analysis</p>
      <h1 className="mt-3 font-display text-5xl text-ivory">{analysis?.document_name || "BhoomiScan analysis"}</h1>
      {analysis?.document_status ? (
        <p className="mt-3 text-sm uppercase tracking-[0.18em] text-mist">{analysis.document_status}</p>
      ) : null}

      {error ? (
        <div className="mt-6">
          <ErrorMessage>{error}</ErrorMessage>
        </div>
      ) : null}

      {loading || running ? (
        <div className="mt-10 grid gap-8 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="royal-frame p-6">
            <div className="relative z-10">
              <LoadingSpinner label="Analyzing your document..." />
              <div className="mt-8">
                <AnalysisProgress processing />
              </div>
            </div>
          </div>
        </div>
      ) : null}

      {analysis && !running ? (
        <>
          <div className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
            <div className="royal-frame p-6">
              <div className="relative z-10">
                <h2 className="font-display text-3xl text-ivory">Progress</h2>
                <div className="mt-5">
                  <AnalysisProgress
                    steps={analysis.pipeline_steps}
                    failed={analysis.analysis_status === "FAILED"}
                  />
                </div>
                {analysis.processing_error ? (
                  <p className="mt-5 text-sm text-red-200">{analysis.processing_error}</p>
                ) : null}
                <div className="mt-6">
                  <Button variant="ghost" onClick={runAnalysis}>
                    Run analysis again
                  </Button>
                </div>
              </div>
            </div>
            <div className="royal-frame p-6">
              <div className="relative z-10">
                <p className="text-[10px] uppercase tracking-[0.2em] text-gold">Document type</p>
                <h2 className="mt-2 font-display text-3xl text-ivory">
                  {analysis.document_type_label || "Not identified"}
                </h2>
                <p className="mt-2 text-sm text-mist">{analysis.classification_note}</p>
                {analysis.classification_confidence != null ? (
                  <p className="mt-3 text-sm text-ivory">
                    Confidence: {Math.round(analysis.classification_confidence * 100)}%
                  </p>
                ) : null}
              </div>
            </div>
          </div>

          <ExtractedDetails data={analysis.extracted_data} />

          <section className="mt-12">
            <h2 className="font-display text-3xl text-ivory">Risk analysis</h2>
            <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {(analysis.findings || []).map((finding) => (
                <RiskCategoryCard
                  key={finding.id}
                  finding={finding}
                  selected={selected?.id === finding.id}
                  onSelect={setSelected}
                />
              ))}
            </div>
          </section>

          {selected ? (
            <section className="royal-frame mt-8 p-6">
              <div className="relative z-10">
                <p className="text-[10px] uppercase tracking-[0.2em] text-gold">{selected.category_label}</p>
                <h2 className="mt-2 font-display text-4xl text-ivory">{selected.status.replaceAll("_", " ")}</h2>
                <p className="mt-2 text-sm text-gold">Risk: {selected.risk_level}</p>
                <p className="mt-4 max-w-3xl text-sm leading-6 text-mist">{selected.summary}</p>
                <dl className="mt-6 grid gap-4 sm:grid-cols-2">
                  <DetailRow label="Case number" value={details.case_number} />
                  <DetailRow label="Court" value={details.court} />
                  <DetailRow label="Status" value={details.case_status} />
                  <DetailRow label="Stay order" value={details.stay_order} />
                  <DetailRow label="Transfer restriction" value={details.transfer_restricted} />
                  <DetailRow label="Seller" value={details.seller_name} />
                  <DetailRow label="Buyer" value={details.buyer_name} />
                  <DetailRow label="Survey number" value={details.survey_number} />
                  <DetailRow label="Khata number" value={details.khata_number} />
                  <DetailRow label="Area" value={details.area} />
                </dl>
                <div className="mt-6">
                  <Button variant="gold" onClick={() => setShowEvidence(true)}>
                    View source evidence
                  </Button>
                </div>
              </div>
            </section>
          ) : null}

          {(analysis.translated_text || analysis.original_text) && (
            <section className="mt-10">
              <div className="mb-3 flex flex-wrap items-center justify-between gap-4">
                <h2 className="font-display text-3xl text-ivory">Document text</h2>
                <div className="flex flex-wrap items-center gap-4">
                  {showDocumentText && analysis.original_text && analysis.translated_text ? (
                    <button type="button" className="text-sm text-gold" onClick={() => setShowOriginal((value) => !value)}>
                      {showOriginal ? "Show English" : "Show original text"}
                    </button>
                  ) : null}
                  <button
                    type="button"
                    role="switch"
                    aria-checked={showDocumentText}
                    aria-label="Show document text"
                    onClick={() => setShowDocumentText((value) => !value)}
                    className="inline-flex items-center gap-3 text-sm text-ivory"
                  >
                    <span className="text-xs uppercase tracking-[0.16em] text-mist">
                      {showDocumentText ? "Visible" : "Hidden"}
                    </span>
                    <span
                      className={`relative h-7 w-12 rounded-full transition ${
                        showDocumentText ? "bg-gold" : "border border-white/15 bg-white/10"
                      }`}
                    >
                      <span
                        className={`absolute top-0.5 left-0.5 h-6 w-6 rounded-full bg-ivory shadow transition ${
                          showDocumentText ? "translate-x-5" : "translate-x-0"
                        }`}
                      />
                    </span>
                  </button>
                </div>
              </div>
              {showDocumentText ? (
                <div className="royal-frame p-6">
                  <p className="relative z-10 whitespace-pre-wrap text-sm leading-7 text-ivory/85">
                    {showOriginal ? analysis.original_text : analysis.translated_text || analysis.original_text}
                  </p>
                </div>
              ) : (
                <p className="text-sm text-mist">Turn this on if you want to read the full extracted text.</p>
              )}
            </section>
          )}

          <RecommendationList items={analysis.recommendations} caseId={caseId} />
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to={`/property-case/${caseId}/upload`}>
              <Button variant="ghost">Upload another paper</Button>
            </Link>
            <Link to={`/property-case/${caseId}/due-diligence`}>
              <Button variant="gold">Get risk report</Button>
            </Link>
          </div>
        </>
      ) : null}

      {showEvidence ? <EvidencePanel evidence={selected?.evidence || []} onClose={() => setShowEvidence(false)} /> : null}
    </PageShell>
  );
}
