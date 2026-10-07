import { motion } from "framer-motion";

export default function Card({ children, className = "", hover = true, onClick }) {
  return (
    <motion.div
      onClick={onClick}
      whileHover={hover ? { y: -6, scale: 1.01 } : undefined}
      transition={{ type: "spring", stiffness: 260, damping: 20 }}
      className={`royal-frame p-6 ${onClick ? "cursor-pointer" : ""} ${className}`}
    >
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
}
