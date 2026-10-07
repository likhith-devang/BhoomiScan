export const GET_SUBSCRIPTION_MESSAGE = "Get Subscription to use this.";

export const PROPERTY_DOMAINS = [
  {
    id: "RESIDENTIAL",
    title: "Homes",
    description: "Houses, flats, villas, and land meant for living. You can use this now.",
    available: true,
  },
  {
    id: "AGRICULTURAL",
    title: "Agricultural",
    description: "Farm land and other agricultural property.",
    available: false,
  },
  {
    id: "COMMERCIAL",
    title: "Commercial",
    description: "Shops, offices, and other business property.",
    available: false,
  },
  {
    id: "INDUSTRIAL",
    title: "Industrial",
    description: "Factories, warehouses, and industrial sites.",
    available: false,
  },
];

export const RESIDENTIAL_PROPERTY_TYPES = [
  {
    id: "VACANT_LAND",
    title: "Empty land",
    description: "Land with no house on it yet.",
  },
  {
    id: "INDEPENDENT_HOUSE",
    title: "Independent house",
    description: "A house that stands on its own, not inside a building.",
  },
  {
    id: "APARTMENT_FLAT",
    title: "Apartment / Flat",
    description: "A home inside a building with other homes.",
  },
  {
    id: "VILLA",
    title: "Villa",
    description: "A large house, often inside a gated community.",
  },
  {
    id: "RESIDENTIAL_PLOT",
    title: "House plot",
    description: "A marked piece of land meant for building a house.",
  },
];

export const RISK_PILLARS = [
  { title: "Who owns it", copy: "Does the seller really own this property?" },
  { title: "Court cases", copy: "Is anyone fighting over this property in court?" },
  { title: "Bank loans", copy: "Is there a loan or debt on this property?" },
  { title: "Permissions", copy: "Did the building get the needed government permissions?" },
  { title: "Land records", copy: "Do tax papers and land records match?" },
];

export const DOMAIN_KEY = "bhoomiscan.selectedDomain";
export const TOKEN_KEY = "bhoomiscan.token";

export function labelForType(id) {
  return RESIDENTIAL_PROPERTY_TYPES.find((item) => item.id === id)?.title || id;
}

export function labelForDomain(id) {
  return PROPERTY_DOMAINS.find((item) => item.id === id)?.title || id;
}

export function formatBytes(bytes) {
  if (!bytes && bytes !== 0) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

export function formatDate(value) {
  if (!value) return "—";
  return new Date(value).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}
