export default function Input({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
  autoComplete,
  error,
  name,
  required,
}) {
  return (
    <label className="block space-y-2">
      <span className="text-xs font-semibold uppercase tracking-[0.18em] text-mist">{label}</span>
      <input
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        autoComplete={autoComplete}
        required={required}
        className={`w-full rounded-2xl border bg-void/70 px-4 py-3 text-sm text-ivory outline-none transition placeholder:text-mist/50 focus:border-gold/60 focus:shadow-gold ${
          error ? "border-red-400/50" : "border-white/10"
        }`}
      />
      {error ? <span className="block text-xs text-red-300">{error}</span> : null}
    </label>
  );
}
