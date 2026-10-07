import { useState } from "react";

const ACCEPT = ".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg";

export default function UploadBox({ onFiles }) {
  const [dragging, setDragging] = useState(false);

  function handleFiles(fileList) {
    const files = Array.from(fileList || []);
    if (files.length) onFiles(files);
  }

  return (
    <label
      onDragOver={(event) => {
        event.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={(event) => {
        event.preventDefault();
        setDragging(false);
        handleFiles(event.dataTransfer.files);
      }}
      className={`royal-frame flex min-h-[240px] cursor-pointer flex-col items-center justify-center gap-4 border-dashed p-8 text-center transition ${
        dragging ? "border-gold/80 bg-gold/5" : "border-white/15"
      }`}
    >
      <input
        type="file"
        accept={ACCEPT}
        className="hidden"
        multiple
        onChange={(event) => {
          handleFiles(event.target.files);
          event.target.value = "";
        }}
      />
      <span className="grid h-16 w-16 place-items-center rounded-full border border-gold/30 bg-gold/10 text-gold">
        ↑
      </span>
      <div>
        <p className="font-display text-3xl text-ivory">Drop your files here</p>
        <p className="mt-2 text-sm text-mist">PDF, PNG, JPG or JPEG. Or click to choose files.</p>
      </div>
      <span className="rounded-full border border-white/15 px-4 py-2 text-xs uppercase tracking-[0.2em] text-champagne">
        Browse files
      </span>
    </label>
  );
}
