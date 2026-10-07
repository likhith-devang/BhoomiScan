import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "../components/Button";
import ErrorMessage from "../components/ErrorMessage";
import FlowStepper from "../components/FlowStepper";
import LoadingSpinner from "../components/LoadingSpinner";
import PageShell from "../components/PageShell";
import { caseApi, errorMessage } from "../services/api";

export default function FinalReportPage() {
  const { id, reportId } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [integrity, setIntegrity] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    const [reportResponse, verifyResponse] = await Promise.all([
      caseApi.report(id, reportId),
      caseApi.verifyReport(id, reportId),
    ]);
    setReport(reportResponse.data);
    setIntegrity(verifyResponse.data);
  }

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    load()
      .catch((err) => {
        if (!cancelled) setError(errorMessage(err, "We could not open this report."));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id, reportId]);

  async function downloadPdf() {
    try {
      const response = await caseApi.reportPdf(id, reportId);
      const url = window.URL.createObjectURL(response.data);
      const link = document.createElement("a");
      link.href = url;
      link.download = `BhoomiScan_Risk_Report_v${report?.version || 1}.pdf`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(errorMessage(err, "We could not download the PDF."));
    }
  }

  const content = report?.report_content || {};
  const reasons =
    content.score_reasons?.length
      ? content.score_reasons
      : (content.detected_issues || []).map((item) => ({
          reason: item.summary,
          points: null,
        }));
  const valid = integrity?.status === "VALID";

  return (
    <PageShell wide>
      <FlowStepper current={3} />
      <button type="button" onClick={() => navigate(`/property-case/${id}/upload`)} className="text-xs uppercase tracking-[0.2em] text-mist">
        ← Document vault
      </button>
      <p className="mt-4 text-xs uppercase tracking-[0.32em] text-gold">BhoomiScan · Your AIvocate.</p>
      <h1 className="mt-3 font-display text-5xl text-ivory">Risk report</h1>
      <p className="mt-3 max-w-3xl text-sm text-mist">Based on the documents provided. This is not a legal guarantee.</p>

      {error ? (
        <div className="mt-6">
          <ErrorMessage>{error}</ErrorMessage>
        </div>
      ) : null}

      {loading ? (
        <div className="py-16">
          <LoadingSpinner label="Opening the signed report..." />
        </div>
      ) : null}

      {report && !loading ? (
        <>
          <section className="royal-frame mt-10 p-8 md:p-10">
            <div className="relative z-10">
              <p className="text-[10px] uppercase tracking-[0.22em] text-gold">Risk score</p>
              <p className="mt-3 font-display text-7xl text-ivory md:text-8xl">{report.risk_score}</p>
              <p className="mt-2 text-sm uppercase tracking-[0.18em] text-mist">out of 100 · {report.risk_level}</p>

              <p className="mt-10 text-[10px] uppercase tracking-[0.22em] text-gold">Because</p>
              {reasons.length ? (
                <ul className="mt-4 space-y-3">
                  {reasons.map((item) => (
                    <li key={`${item.reason}-${item.category || ""}`} className="text-xl text-ivory md:text-2xl">
                      {item.reason}
                      {item.points ? <span className="ml-3 text-sm text-mist">+{item.points}</span> : null}
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="mt-4 text-xl text-ivory">No DETECTED issues in the provided documents.</p>
              )}
            </div>
          </section>

          <section className="royal-frame mt-6 p-6">
            <div className="relative z-10">
              <p className="text-[10px] uppercase tracking-[0.2em] text-gold">Report integrity</p>
              <h2 className="mt-2 font-display text-3xl text-ivory">{integrity?.status || "Unknown"}</h2>
              <p className={`mt-3 text-sm ${valid ? "text-emerald-200" : "text-red-200"}`}>
                {valid
                  ? "This stored report matches its SHA-256 hash and ledger record."
                  : "This stored report no longer matches its original hash."}
              </p>
              <p className="mt-3 break-all text-xs text-mist">Report hash {report.report_hash}</p>
              <p className="mt-2 text-xs text-mist">
                Record #{String(report.version).padStart(6, "0")} · {report.ledger?.hashed_at}
              </p>
              <div className="mt-6 flex flex-wrap gap-3">
                <Button variant="ghost" onClick={load}>
                  Verify Integrity
                </Button>
                <Button variant="gold" onClick={downloadPdf}>
                  Download PDF
                </Button>
              </div>
            </div>
          </section>
        </>
      ) : null}
    </PageShell>
  );
}
