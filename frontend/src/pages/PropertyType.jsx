import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Atmosphere from "../components/Atmosphere";
import ErrorMessage from "../components/ErrorMessage";
import FlowStepper from "../components/FlowStepper";
import Navbar from "../components/Navbar";
import PropertyTypeCard from "../components/PropertyTypeCard";
import { DOMAIN_KEY, RESIDENTIAL_PROPERTY_TYPES } from "../constants/property";
import { caseApi, errorMessage } from "../services/api";

export default function PropertyType() {
  const navigate = useNavigate();
  const [busyId, setBusyId] = useState("");
  const [error, setError] = useState("");

  async function selectType(item) {
    setError("");
    setBusyId(item.id);
    try {
      const domain = sessionStorage.getItem(DOMAIN_KEY) || "RESIDENTIAL";
      const response = await caseApi.create({ domain, property_type: item.id });
      navigate(`/property-case/${response.data.id}/upload`);
    } catch (err) {
      setError(errorMessage(err, "We could not start this check. Please try again."));
    } finally {
      setBusyId("");
    }
  }

  return (
    <div className="min-h-screen">
      <Atmosphere />
      <Navbar />
      <main className="mx-auto max-w-6xl px-6 py-12">
        <FlowStepper current={1} />
        <h1 className="font-display text-5xl text-ivory md:text-6xl">What kind of home is it?</h1>
        <p className="mt-4 max-w-2xl text-mist">
          Pick the option that best matches the property.
        </p>
        {error ? (
          <div className="mt-6">
            <ErrorMessage>{error}</ErrorMessage>
          </div>
        ) : null}
        <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {RESIDENTIAL_PROPERTY_TYPES.map((item) => (
            <PropertyTypeCard
              key={item.id}
              item={item}
              disabled={Boolean(busyId)}
              onSelect={selectType}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
