export default function Logo({ compact = false, className = "" }) {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <img
        src="/logo.png?v=globe"
        alt="BhoomiScan"
        width={64}
        height={64}
        className="h-14 w-14 shrink-0 object-contain sm:h-16 sm:w-16"
      />
      {!compact && (
        <span className="leading-none">
          <span className="block font-display text-[1.35rem] tracking-wide">
            <span className="text-ivory">Bhoomi</span>
            <span className="text-gold">Scan</span>
          </span>
          <span className="mt-1 block text-[9px] font-semibold uppercase tracking-[0.32em] text-gold/70">
            Your AIvocate
          </span>
        </span>
      )}
    </div>
  );
}
