import { useMemo } from "react";
import { useAuth } from "./useAuth";
import { canUseAiAssistant, planLabel, PLANS, readStoredPlan } from "../constants/subscription";

export function useSubscription() {
  const { user } = useAuth();

  return useMemo(() => {
    const plan = readStoredPlan(user?.id);
    return {
      plan,
      planName: planLabel(plan),
      isFree: plan === PLANS.FREE,
      isPro: plan === PLANS.PRO,
      isPremium: plan === PLANS.PREMIUM,
      canUseAI: canUseAiAssistant(plan),
    };
  }, [user?.id]);
}
