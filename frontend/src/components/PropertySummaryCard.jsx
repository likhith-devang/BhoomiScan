import { Link } from "react-router-dom";
import Button from "./Button";
import Card from "./Card";
import { labelForDomain, labelForType } from "../constants/property";
import { formatDateTime } from "../lib/userDisplay";

function analysisStatus(item) {
  if (item.document_count > 0) return "Papers saved";
  return "Waiting for papers";
}

export default function PropertySummaryCard({ item }) {
  return (
    <Card hover={false} className="flex h-full flex-col">
      <p className="text-[10px] uppercase tracking-[0.24em] text-gold">{labelForDomain(item.domain)}</p>
      <h3 className="mt-2 font-display text-3xl text-ivory">{labelForType(item.property_type)}</h3>
      <p className="mt-1 text-sm text-mist">Location not added yet</p>
      <dl className="mt-5 grid grid-cols-2 gap-3 text-sm">
        <div>
          <dt className="text-mist">Documents uploaded</dt>
          <dd className="text-ivory">{item.document_count}</dd>
        </div>
        <div>
          <dt className="text-mist">Analysis status</dt>
          <dd className="text-ivory">{analysisStatus(item)}</dd>
        </div>
        <div className="col-span-2">
          <dt className="text-mist">Last updated</dt>
          <dd className="text-ivory">{formatDateTime(item.updated_at || item.created_at)}</dd>
        </div>
      </dl>
      <div className="mt-6">
        <Link to={`/property-case/${item.id}/upload`}>
          <Button variant="ghost">Open Property</Button>
        </Link>
      </div>
    </Card>
  );
}
