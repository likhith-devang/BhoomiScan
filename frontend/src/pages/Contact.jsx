import { useState } from "react";
import Button from "../components/Button";
import Card from "../components/Card";
import Input from "../components/Input";
import PageShell from "../components/PageShell";
import { IconMail } from "../components/icons";
import { useAuth } from "../hooks/useAuth";

export default function Contact() {
  const { user } = useAuth();
  const [name, setName] = useState(user?.username || "");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
    setSent(true);
  }

  return (
    <PageShell>
      <p className="text-xs uppercase tracking-[0.32em] text-gold">Support</p>
      <h1 className="mt-3 font-display text-5xl text-ivory">Contact Us</h1>
      <p className="mt-4 max-w-2xl text-lg text-mist">Need help with your property analysis?</p>

      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {[
          { title: "Email support", copy: "Ask about a property file or account." },
          { title: "General enquiry", copy: "Questions about plans and how BhoomiScan works." },
          { title: "Technical support", copy: "Help with login, uploads, or the AI assistant." },
        ].map((item) => (
          <Card key={item.title} hover={false}>
            <IconMail className="h-5 w-5 text-gold" />
            <h2 className="mt-3 font-display text-2xl text-ivory">{item.title}</h2>
            <p className="mt-2 text-sm text-mist">{item.copy}</p>
          </Card>
        ))}
      </div>

      <Card hover={false} className="mt-8">
        {sent ? (
          <p className="text-sm font-semibold text-gold">Thanks! Our team will get back to you.</p>
        ) : (
          <form className="space-y-5" onSubmit={handleSubmit}>
            <Input
              label="Name"
              required
              value={name}
              onChange={(event) => setName(event.target.value)}
            />
            <Input
              label="Email"
              type="email"
              required
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@email.com"
            />
            <label className="block space-y-2">
              <span className="text-xs font-semibold uppercase tracking-[0.18em] text-mist">Message</span>
              <textarea
                required
                rows={5}
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                className="w-full rounded-2xl border border-white/10 bg-void/70 px-4 py-3 text-sm text-ivory outline-none placeholder:text-mist/50 focus:border-gold/60"
                placeholder="How can we help?"
              />
            </label>
            <Button type="submit" variant="gold">
              Send Message
            </Button>
          </form>
        )}
      </Card>
    </PageShell>
  );
}
