import { useState } from "react";
import Button from "./Button";
import { errorMessage } from "../services/api";

export default function AIChat({ onSend, disabled = false, placeholder = "Ask BhoomiScan AI..." }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    const text = question.trim();
    if (!text || disabled || busy) return;

    const userMessage = { id: crypto.randomUUID(), role: "user", text };
    setMessages((current) => [...current, userMessage]);
    setQuestion("");
    setBusy(true);

    try {
      const reply = await onSend(text);
      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", text: reply },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: errorMessage(error, "BhoomiScan AI is not connected yet. Your question was not analysed."),
        },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex min-h-[28rem] flex-col rounded-3xl border border-white/10 bg-navy/60 shadow-glow">
      <div className="border-b border-white/10 px-5 py-4 sm:px-6">
        <h2 className="font-display text-3xl text-ivory">BhoomiScan AI</h2>
        <p className="mt-1 text-sm text-mist">Your property analysis assistant</p>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto px-5 py-5 sm:px-6" aria-live="polite">
        {messages.length === 0 ? (
          <p className="text-sm text-mist">Ask a question about your uploaded papers and risk analysis.</p>
        ) : (
          messages.map((message) => (
            <div key={message.id} className={message.role === "user" ? "text-right" : "text-left"}>
              <p className="text-[10px] uppercase tracking-[0.2em] text-gold">
                {message.role === "user" ? "You" : "BhoomiScan AI"}
              </p>
              <p
                className={`mt-1 inline-block max-w-[90%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  message.role === "user"
                    ? "bg-royal/40 text-ivory"
                    : "border border-white/10 bg-white/5 text-ivory/90"
                }`}
              >
                {message.text}
              </p>
            </div>
          ))
        )}
        {busy ? <p className="text-sm text-mist">Checking with BhoomiScan AI…</p> : null}
      </div>

      <form onSubmit={submit} className="border-t border-white/10 p-4 sm:p-5">
        <label className="sr-only" htmlFor="ai-question">
          Ask BhoomiScan AI
        </label>
        <div className="flex gap-3">
          <input
            id="ai-question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder={placeholder}
            disabled={disabled || busy}
            className="min-w-0 flex-1 rounded-full border border-white/10 bg-void/70 px-4 py-3 text-sm text-ivory outline-none placeholder:text-mist/50 focus:border-gold/60"
          />
          <Button type="submit" variant="gold" disabled={disabled || busy || !question.trim()}>
            Send
          </Button>
        </div>
      </form>
    </div>
  );
}
