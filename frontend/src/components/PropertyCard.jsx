import { GET_SUBSCRIPTION_MESSAGE } from "../constants/property";
import { motion } from "framer-motion";

export default function PropertyCard({ domain, selected, onSelect }) {
  return (
    <motion.button
      type="button"
      onClick={() => onSelect(domain)}
      whileHover={{ y: -8 }}
      whileTap={{ scale: 0.98 }}
      className={`royal-frame w-full p-6 text-left transition ${
        selected ? "border-gold/70 shadow-gold" : ""
      }`}
    >
      <div className="relative z-10 space-y-4">
        <div className="flex items-start justify-between gap-3">
          <h3 className="font-display text-3xl text-ivory">{domain.title}</h3>
          {domain.available ? (
            <span className="rounded-full border border-gold/40 bg-gold/10 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-gold">
              Available
            </span>
          ) : (
            <span className="rounded-full border border-gold/40 bg-gold/10 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-gold">
              Upgrade
            </span>
          )}
        </div>
        <p className="text-sm leading-6 text-mist">{domain.description}</p>
        {!domain.available && selected ? (
          <p className="rounded-xl border border-gold/20 bg-gold/5 px-3 py-2 text-xs text-champagne">
            {GET_SUBSCRIPTION_MESSAGE}
          </p>
        ) : null}
      </div>
    </motion.button>
  );
}
