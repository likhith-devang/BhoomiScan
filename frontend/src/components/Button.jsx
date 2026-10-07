import { motion } from "framer-motion";

const variants = {
  primary:
    "bg-gradient-to-r from-royal to-sapphire text-white shadow-glow hover:brightness-110",
  gold: "bg-gold text-void hover:bg-champagne shadow-gold",
  ghost:
    "border border-white/15 bg-white/5 text-ivory hover:border-gold/50 hover:bg-white/10",
  danger: "border border-red-400/30 bg-red-950/40 text-red-100 hover:bg-red-900/50",
};

export default function Button({
  children,
  variant = "primary",
  className = "",
  type = "button",
  disabled,
  onClick,
  ...rest
}) {
  return (
    <motion.button
      type={type}
      disabled={disabled}
      whileHover={disabled ? undefined : { y: -1 }}
      whileTap={disabled ? undefined : { scale: 0.98 }}
      onClick={onClick}
      className={`inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold tracking-wide transition disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
      {...rest}
    >
      {children}
    </motion.button>
  );
}
