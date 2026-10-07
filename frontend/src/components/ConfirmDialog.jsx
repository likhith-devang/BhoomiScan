import Button from "./Button";

export default function ConfirmDialog({
  title,
  body,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  onConfirm,
  onCancel,
}) {
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-void/80 p-4" onClick={onCancel}>
      <div className="royal-frame w-full max-w-lg p-6" onClick={(event) => event.stopPropagation()} role="dialog">
        <div className="relative z-10">
          <p className="text-xs uppercase tracking-[0.24em] text-gold">Please confirm</p>
          <h2 className="mt-2 font-display text-3xl text-ivory">{title}</h2>
          <p className="mt-4 text-sm leading-6 text-mist">{body}</p>
          <div className="mt-6 flex flex-wrap justify-end gap-3">
            <Button variant="ghost" onClick={onCancel}>
              {cancelLabel}
            </Button>
            <Button variant="gold" onClick={onConfirm}>
              {confirmLabel}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
