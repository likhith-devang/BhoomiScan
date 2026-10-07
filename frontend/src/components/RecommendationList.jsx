import { Link } from "react-router-dom";
import Button from "./Button";

export default function RecommendationList({ items = [], caseId }) {
  if (!items.length) return null;
  return (
    <section className="mt-12">
      <h2 className="font-display text-3xl text-ivory">Recommended next documents</h2>
      <p className="mt-2 text-sm text-mist">Upload these papers to verify the risks that are still open.</p>
      <div className="mt-5 grid gap-4 md:grid-cols-2">
        {items.map((item) => (
          <article key={item.id || item.document_type} className="royal-frame p-5">
            <div className="relative z-10">
              <p className="text-[10px] uppercase tracking-[0.2em] text-gold">{item.category_label}</p>
              <h3 className="mt-2 font-display text-2xl text-ivory">{item.label}</h3>
              <p className="mt-2 text-sm text-mist">{item.reason}</p>
              <div className="mt-4">
                <Link to={`/property-case/${caseId}/upload`}>
                  <Button variant="ghost">Upload {item.label}</Button>
                </Link>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
