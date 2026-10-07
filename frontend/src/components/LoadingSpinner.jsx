export default function LoadingSpinner({ label = "Loading" }) {
  return (
    <div className="flex flex-col items-center gap-4 text-mist">
      <span className="relative grid h-14 w-14 place-items-center">
        <span className="pulse-ring absolute inset-0 rounded-full border border-gold/40" />
        <span className="h-10 w-10 animate-spin rounded-full border-2 border-white/10 border-t-gold" />
      </span>
      <span className="text-xs uppercase tracking-[0.24em]">{label}</span>
    </div>
  );
}
