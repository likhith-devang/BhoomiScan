import { motion } from "framer-motion";

export default function PropertyTypeCard({ item, onSelect, disabled }) {
  return (
    <motion.button
      type="button"
      disabled={disabled}
      onClick={() => onSelect(item)}
      whileHover={disabled ? undefined : { y: -8, scale: 1.02 }}
      className="royal-frame w-full p-6 text-left disabled:cursor-wait disabled:opacity-70"
    >
      <div className="relative z-10 space-y-3">
        <div className="h-px w-12 bg-gradient-to-r from-gold to-transparent" />
        <h3 className="font-display text-2xl text-ivory">{item.title}</h3>
        <p className="text-sm leading-6 text-mist">{item.description}</p>
        <span className="inline-block text-xs uppercase tracking-[0.2em] text-sapphire">Choose this →</span>
      </div>
    </motion.button>
  );
}
