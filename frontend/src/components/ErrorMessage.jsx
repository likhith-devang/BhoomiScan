export default function ErrorMessage({ children }) {
  if (!children) return null;
  return (
    <div className="rounded-2xl border border-red-400/30 bg-red-950/40 px-4 py-3 text-sm text-red-100">
      {children}
    </div>
  );
}
