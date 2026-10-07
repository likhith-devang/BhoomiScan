export const PLANS = {
  FREE: "FREE",
  PRO: "PRO",
  PREMIUM: "PREMIUM",
};

export const PLAN_STORAGE_PREFIX = "bhoomiscan.plan.";

export const SUBSCRIPTION_PLANS = [
  {
    id: PLANS.FREE,
    name: "Free",
    price: "Free",
    period: "forever",
    summary: "Store papers and start a basic property check.",
    features: [
      "Basic property document storage",
      "Limited document analysis",
      "Basic risk overview",
    ],
    cta: "Current plan",
  },
  {
    id: PLANS.PRO,
    name: "Pro",
    price: "Get Subscription",
    period: "for AI checks",
    summary: "Ask the AI assistant about your property papers.",
    features: [
      "More document analyses",
      "Full AI property analysis",
      "Detailed risk findings",
      "AI assistant",
    ],
    cta: "Upgrade to Pro",
    highlighted: true,
  },
  {
    id: PLANS.PREMIUM,
    name: "Premium",
    price: "Get Subscription",
    period: "for full due diligence",
    summary: "Deeper checks, fuller reports, and faster help.",
    features: [
      "Advanced due diligence",
      "Unlimited / expanded document analysis",
      "Detailed reports",
      "Priority support",
    ],
    cta: "Upgrade to Premium",
  },
];

export const PAYMENT_METHODS = [
  { id: "apple_pay", label: "Apple Pay" },
  { id: "paypal", label: "PayPal" },
  { id: "card", label: "Credit / Debit Card" },
];

export function planStorageKey(userId) {
  return `${PLAN_STORAGE_PREFIX}${userId}`;
}

export function readStoredPlan(userId) {
  if (!userId) return PLANS.FREE;
  try {
    const value = localStorage.getItem(planStorageKey(userId));
    if (value === PLANS.PRO || value === PLANS.PREMIUM || value === PLANS.FREE) {
      return value;
    }
  } catch {
    /* ignore private-mode storage errors */
  }
  return PLANS.FREE;
}

export function planLabel(plan) {
  if (plan === PLANS.PRO) return "Pro";
  if (plan === PLANS.PREMIUM) return "Premium";
  return "Free";
}

export function canUseAiAssistant(plan) {
  return plan === PLANS.PRO || plan === PLANS.PREMIUM;
}
