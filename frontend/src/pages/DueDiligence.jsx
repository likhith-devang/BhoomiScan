import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ErrorMessage from "../components/ErrorMessage";
import LoadingSpinner from "../components/LoadingSpinner";
import PageShell from "../components/PageShell";
import { caseApi, errorMessage } from "../services/api";

const inflight = new Map();

async function prepareSignedReport(caseId) {
  if (inflight.has(caseId)) return inflight.get(caseId);
  const task = (async () => {
    await caseApi.recalculate(caseId);
    const created = await caseApi.finalize(caseId);
    return created.data;
  })();
  inflight.set(caseId, task);
  try {
    return await task;
  } finally {
    inflight.delete(caseId);
  }
}

export default function DueDiligence() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    prepareSignedReport(id)
      .then((report) => {
        if (!cancelled) navigate(`/property-case/${id}/reports/${report.id}`, { replace: true });
      })
      .catch((err) => {
        if (!cancelled) setError(errorMessage(err, "Analyze at least one document first."));
      });
    return () => {
      cancelled = true;
    };
  }, [id, navigate]);

  return (
    <PageShell wide>
      <button type="button" onClick={() => navigate(`/property-case/${id}/upload`)} className="text-xs uppercase tracking-[0.2em] text-mist">
        ← Document vault
      </button>
      {error ? (
        <div className="mt-8">
          <ErrorMessage>{error}</ErrorMessage>
        </div>
      ) : (
        <div className="py-16">
          <LoadingSpinner label="Preparing your risk report..." />
        </div>
      )}
    </PageShell>
  );
}
