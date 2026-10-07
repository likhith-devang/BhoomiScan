export default function ActivityCard({ title, detail, time }) {
  return (
    <article className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3">
      <p className="text-sm font-semibold text-ivory">{title}</p>
      <p className="mt-1 text-sm text-mist">{detail}</p>
      <p className="mt-2 text-[11px] uppercase tracking-[0.16em] text-gold/80">{time}</p>
    </article>
  );
}
