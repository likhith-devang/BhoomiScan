import { Link } from "react-router-dom";
import Button from "./Button";
import Card from "./Card";

export default function UpgradeCard({ title, description, to = "/subscription", cta = "Upgrade" }) {
  return (
    <Card hover={false} className="flex h-full flex-col">
      <p className="text-[10px] uppercase tracking-[0.24em] text-gold">Unlock</p>
      <h3 className="mt-2 font-display text-3xl text-ivory">{title}</h3>
      <p className="mt-3 flex-1 text-sm leading-relaxed text-mist">{description}</p>
      <div className="mt-6">
        <Link to={to}>
          <Button variant="gold">{cta}</Button>
        </Link>
      </div>
    </Card>
  );
}
