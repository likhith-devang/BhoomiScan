import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Atmosphere from "../components/Atmosphere";
import Button from "../components/Button";
import FlowStepper from "../components/FlowStepper";
import Navbar from "../components/Navbar";
import PropertyCard from "../components/PropertyCard";
import { DOMAIN_KEY, PROPERTY_DOMAINS } from "../constants/property";

export default function PropertyDomain() {
  const [selected, setSelected] = useState("RESIDENTIAL");
  const navigate = useNavigate();
  const current = PROPERTY_DOMAINS.find((item) => item.id === selected);

  function continueFlow() {
    if (!current?.available) {
      navigate("/subscription");
      return;
    }
    sessionStorage.setItem(DOMAIN_KEY, current.id);
    navigate("/property-type");
  }

  return (
    <div className="min-h-screen">
      <Atmosphere />
      <Navbar />
      <main className="mx-auto max-w-6xl px-6 py-12">
        <FlowStepper current={0} />
        <h1 className="font-display text-5xl text-ivory md:text-6xl">What kind of property is this?</h1>
        <p className="mt-4 max-w-2xl text-mist">
          Pick a property kind to begin. Agricultural, Commercial, and Industrial need a subscription.
        </p>
        <div className="mt-10 grid gap-5 md:grid-cols-2">
          {PROPERTY_DOMAINS.map((domain) => (
            <PropertyCard
              key={domain.id}
              domain={domain}
              selected={selected === domain.id}
              onSelect={(item) => setSelected(item.id)}
            />
          ))}
        </div>
        <div className="mt-10">
          <Button variant="gold" className="px-8 py-3" onClick={continueFlow}>
            {current?.available ? "Continue" : "Get Subscription"}
          </Button>
        </div>
      </main>
    </div>
  );
}
