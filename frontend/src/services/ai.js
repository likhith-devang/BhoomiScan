import api from "./api";

/**
 * Phase 2 AI client.
 * Connects to future endpoints for chat, OCR, translation,
 * document classification, and risk analysis without inventing answers.
 */
export const aiApi = {
  chat: ({ question, propertyCaseId }) =>
    api.post("/ai/chat", {
      question,
      property_case_id: propertyCaseId || null,
    }),
};

export async function askPropertyAssistant({ question, propertyCaseId }) {
  const response = await aiApi.chat({ question, propertyCaseId });
  const data = response.data || {};
  return data.answer || data.reply || data.message || "BhoomiScan AI did not return an answer.";
}
