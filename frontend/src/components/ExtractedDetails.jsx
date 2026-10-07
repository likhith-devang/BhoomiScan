function Row({ label, value }) {
  if (!value && value !== false) return null;
  const display = typeof value === "boolean" ? (value ? "Present" : "Not present") : value;
  return (
    <div>
      <dt className="text-[10px] uppercase tracking-[0.18em] text-mist">{label}</dt>
      <dd className="mt-1 text-sm text-ivory">{display}</dd>
    </div>
  );
}

export default function ExtractedDetails({ data }) {
  if (!data) return null;
  const property = data.property || {};
  const ownership = data.ownership || {};
  const transaction = data.transaction || {};
  const litigation = data.litigation || {};
  return (
    <section className="mt-10">
      <h2 className="font-display text-3xl text-ivory">Extracted property details</h2>
      <div className="royal-frame mt-5 p-6">
        <dl className="relative z-10 grid gap-4 sm:grid-cols-2 md:grid-cols-3">
          <Row label="Survey number" value={property.survey_number} />
          <Row label="Khata number" value={property.khata_number} />
          <Row label="Area" value={property.area} />
          <Row label="Village" value={property.village} />
          <Row label="Hobli" value={property.hobli} />
          <Row label="Taluk" value={property.taluk} />
          <Row label="District" value={property.district} />
          <Row label="Seller" value={ownership.seller_name} />
          <Row label="Buyer" value={ownership.buyer_name} />
          <Row label="Sale amount" value={transaction.sale_amount} />
          <Row label="Previous deed" value={transaction.previous_deed_number} />
          <Row label="Case number" value={litigation.case_number} />
          <Row label="Court" value={litigation.court} />
          <Row label="Stay order" value={litigation.stay_order} />
          <Row label="Transfer restriction" value={litigation.transfer_restricted} />
        </dl>
      </div>
    </section>
  );
}
