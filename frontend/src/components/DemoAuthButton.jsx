import { useState } from "react";
import { useToast } from "../hooks/useToast";

export default function DemoAuthButton({ icon, children }) {
  const { push } = useToast();
  const [hover, setHover] = useState(false);

  return (
    <button
      type="button"
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onFocus={() => setHover(true)}
      onBlur={() => setHover(false)}
      onClick={() => push("Demo only", "info")}
      className="relative flex w-full items-center justify-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-medium text-ivory transition hover:border-gold/40 hover:bg-white/10"
    >
      <span className="text-base">{icon}</span>
      {hover ? "Demo only" : children}
    </button>
  );
}
