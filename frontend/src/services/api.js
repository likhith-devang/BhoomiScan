import axios from "axios";
import { TOKEN_KEY } from "../constants/property";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export function errorMessage(error, fallback = "Something went wrong. Please try again.") {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string" && detail.trim()) return detail;
  if (Array.isArray(detail) && detail[0]?.msg) return detail[0].msg;
  if (error?.message === "Network Error") return "Cannot reach BhoomiScan. Please check that the server is running.";
  return fallback;
}

export const authApi = {
  signup: (payload) => api.post("/auth/signup", payload),
  login: (payload) => api.post("/auth/login", payload),
  me: () => api.get("/auth/me"),
};

export const adminApi = {
  users: () => api.get("/admin/users"),
  assignRole: (userId, role) => api.patch(`/admin/users/${userId}/role`, { role }),
  auditLogs: (limit = 100) => api.get("/admin/audit-logs", { params: { limit } }),
};

export const caseApi = {
  create: (payload) => api.post("/property-cases", payload),
  list: () => api.get("/property-cases"),
  get: (id) => api.get(`/property-cases/${id}`),
  upload: (id, file) => {
    const data = new FormData();
    data.append("file", file);
    return api.post(`/property-cases/${id}/documents`, data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
  documents: (id) => api.get(`/property-cases/${id}/documents`),
  analyze: (caseId, documentId) =>
    api.post(`/property-cases/${caseId}/documents/${documentId}/analyze`, null, { timeout: 180000 }),
  documentAnalysis: (caseId, documentId) =>
    api.get(`/property-cases/${caseId}/documents/${documentId}/analysis`),
  caseAnalysis: (caseId) => api.get(`/property-cases/${caseId}/analysis`),
  recommendations: (caseId) => api.get(`/property-cases/${caseId}/recommendations`),
  evidence: (caseId, findingId) => api.get(`/property-cases/${caseId}/evidence/${findingId}`),
  deleteDocument: (caseId, documentId) => api.delete(`/property-cases/${caseId}/documents/${documentId}`),
  recalculate: (caseId) => api.post(`/property-cases/${caseId}/recalculate`),
  dueDiligence: (caseId) => api.get(`/property-cases/${caseId}/due-diligence`),
  comparisons: (caseId) => api.get(`/property-cases/${caseId}/comparisons`),
  finalize: (caseId) => api.post(`/property-cases/${caseId}/finalize`),
  reports: (caseId) => api.get(`/property-cases/${caseId}/reports`),
  report: (caseId, reportId) => api.get(`/property-cases/${caseId}/reports/${reportId}`),
  verifyReport: (caseId, reportId) => api.get(`/property-cases/${caseId}/reports/${reportId}/verify`),
  reportPdf: (caseId, reportId) =>
    api.get(`/property-cases/${caseId}/reports/${reportId}/pdf`, { responseType: "blob" }),
};

export default api;
