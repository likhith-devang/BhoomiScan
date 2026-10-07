import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Atmosphere from "../components/Atmosphere";
import Button from "../components/Button";
import DocumentCard from "../components/DocumentCard";
import ErrorMessage from "../components/ErrorMessage";
import FlowStepper from "../components/FlowStepper";
import LoadingSpinner from "../components/LoadingSpinner";
import Navbar from "../components/Navbar";
import RecommendationList from "../components/RecommendationList";
import UploadBox from "../components/UploadBox";
import { labelForDomain, labelForType } from "../constants/property";
import { useToast } from "../hooks/useToast";
import { caseApi, errorMessage } from "../services/api";

const ALLOWED = ["pdf", "png", "jpg", "jpeg"];
const MAX_BYTES = 10 * 1024 * 1024;

export default function DocumentUpload() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { push } = useToast();
  const [propertyCase, setPropertyCase] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [uploadingName, setUploadingName] = useState("");
  const [analyzingId, setAnalyzingId] = useState("");
  const [recalculating, setRecalculating] = useState(false);

  async function refresh() {
    const [caseResponse, docsResponse] = await Promise.all([caseApi.get(id), caseApi.documents(id)]);
    setPropertyCase(caseResponse.data);
    setDocuments(docsResponse.data);
    try {
      const recs = await caseApi.recommendations(id);
      setRecommendations(recs.data || []);
    } catch {
      setRecommendations([]);
    }
  }

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    refresh()
      .catch((err) => {
        if (!cancelled) {
          const status = err?.response?.status;
          if (status === 404) setError("We could not find this property file.");
          else if (status === 403) setError("You cannot open this property file.");
          else setError(errorMessage(err, "We could not open this property file."));
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  function enqueue(files) {
    const next = [];
    for (const file of files) {
      const ext = file.name.split(".").pop()?.toLowerCase();
      if (!ALLOWED.includes(ext)) {
        push("Please upload a PDF, PNG, JPG, or JPEG file.", "error");
        continue;
      }
      if (file.size > MAX_BYTES) {
        push("This file is too big. The limit is 10 MB.", "error");
        continue;
      }
      next.push({
        localId: crypto.randomUUID(),
        file,
        name: file.name,
        size: file.size,
      });
    }
    setQueue((current) => [...current, ...next]);
  }

  async function uploadOne(item) {
    setUploadingName(item.localId);
    setError("");
    try {
      await caseApi.upload(id, item.file);
      setQueue((current) => current.filter((entry) => entry.localId !== item.localId));
      await refresh();
      push("File saved.", "success");
    } catch (err) {
      setError(errorMessage(err, "We could not upload this file."));
    } finally {
      setUploadingName("");
    }
  }

  async function analyzeDocument(doc) {
    setAnalyzingId(doc.id);
    setError("");
    try {
      await caseApi.analyze(id, doc.id);
      push("Analysis is ready.", "success");
      await refresh();
      navigate(`/property-case/${id}/documents/${doc.id}/analysis`);
    } catch (err) {
      setError(errorMessage(err, "We could not analyse this document."));
      await refresh();
    } finally {
      setAnalyzingId("");
    }
  }

  async function removeDocument(doc) {
    try {
      await caseApi.deleteDocument(id, doc.id);
      push("Document removed.", "success");
      await refresh();
    } catch (err) {
      setError(errorMessage(err, "We could not delete this document."));
    }
  }

  async function recalculate() {
    setRecalculating(true);
    setError("");
    try {
      await caseApi.recalculate(id);
      push("Case analysis updated from all analyzed papers.", "success");
      navigate(`/property-case/${id}/due-diligence`);
    } catch (err) {
      setError(errorMessage(err, "Analyze at least one document first."));
    } finally {
      setRecalculating(false);
    }
  }

  const analyzedCount = documents.filter((item) => item.status === "ANALYZED").length;

  return (
    <div className="min-h-screen">
      <Atmosphere />
      <Navbar />
      <main className="mx-auto max-w-6xl px-6 py-12">
        <FlowStepper current={2} />
        <button type="button" onClick={() => navigate("/dashboard")} className="text-xs uppercase tracking-[0.2em] text-mist">
          ← Home
        </button>
        <h1 className="mt-4 font-display text-5xl text-ivory md:text-6xl">Document vault</h1>
        {propertyCase ? (
          <p className="mt-4 text-mist">
            {labelForDomain(propertyCase.domain)} · {labelForType(propertyCase.property_type)}
          </p>
        ) : null}
        <p className="mt-3 text-sm uppercase tracking-[0.18em] text-gold">Documents uploaded: {documents.length}</p>

        {loading ? (
          <div className="py-20">
            <LoadingSpinner label="Opening your file" />
          </div>
        ) : (
          <>
            <div className="mt-6">
              <ErrorMessage>{error}</ErrorMessage>
            </div>
            {!error ? (
              <div className="mt-8 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
                <div className="space-y-4">
                  <UploadBox onFiles={enqueue} />
                  {queue.map((item) => (
                    <DocumentCard
                      key={item.localId}
                      document={item}
                      pending
                      uploading={uploadingName === item.localId}
                      onRemove={() => setQueue((current) => current.filter((entry) => entry.localId !== item.localId))}
                      onUpload={() => uploadOne(item)}
                    />
                  ))}
                  {analyzedCount > 0 ? (
                    <div className="royal-frame p-6">
                      <div className="relative z-10">
                        <p className="text-xs uppercase tracking-[0.24em] text-gold">Next step</p>
                        <h2 className="mt-2 font-display text-3xl text-ivory">More documents can improve verification.</h2>
                        <p className="mt-2 text-sm text-mist">
                          Upload the papers below one by one. Missing evidence stays not verified until a supporting document is analyzed.
                        </p>
                      </div>
                    </div>
                  ) : null}
                  <RecommendationList items={recommendations} caseId={id} />
                </div>
                <div className="space-y-4">
                  <div className="royal-frame p-6">
                    <div className="relative z-10">
                      <p className="text-xs uppercase tracking-[0.24em] text-gold">Your papers</p>
                      <h2 className="mt-2 font-display text-3xl">Uploaded files</h2>
                      <p className="mt-2 text-sm text-mist">
                        Analyze each paper, then recalculate the full property file.
                      </p>
                      <div className="mt-6 flex flex-wrap gap-3">
                        <Button variant="gold" disabled={!analyzedCount || recalculating} onClick={recalculate}>
                          {recalculating ? "Recalculating…" : "Recalculate Analysis"}
                        </Button>
                        <Button variant="ghost" disabled={!analyzedCount} onClick={() => navigate(`/property-case/${id}/due-diligence`)}>
                          Get risk report
                        </Button>
                      </div>
                    </div>
                  </div>
                  {documents.length === 0 ? (
                    <p className="text-sm text-mist">No files uploaded yet.</p>
                  ) : (
                    documents.map((doc) => (
                      <DocumentCard
                        key={doc.id}
                        document={doc}
                        analyzing={analyzingId === doc.id}
                        onAnalyze={() => analyzeDocument(doc)}
                        onViewAnalysis={() => navigate(`/property-case/${id}/documents/${doc.id}/analysis`)}
                        onViewEvidence={() => navigate(`/property-case/${id}/documents/${doc.id}/analysis`)}
                        onDelete={() => removeDocument(doc)}
                      />
                    ))
                  )}
                </div>
              </div>
            ) : null}
          </>
        )}
      </main>
    </div>
  );
}
