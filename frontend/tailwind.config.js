/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        void: "#05060c",
        ink: "#0b1020",
        navy: "#10182d",
        sapphire: "#3d7cff",
        royal: "#1f4fd8",
        gold: "#d4af37",
        champagne: "#f0d78c",
        ivory: "#f6f1e6",
        mist: "#9aa6c3",
      },
      fontFamily: {
        display: ['"Cormorant Garamond"', "Georgia", "serif"],
        sans: ['"Manrope"', "ui-sans-serif", "system-ui"],
      },
      boxShadow: {
        royal: "0 20px 60px rgba(8, 16, 40, 0.55)",
        glow: "0 0 40px rgba(61, 124, 255, 0.22)",
        gold: "0 0 32px rgba(212, 175, 55, 0.18)",
      },
      backgroundImage: {
        "royal-radial":
          "radial-gradient(1200px 600px at 10% -10%, rgba(61,124,255,0.18), transparent 55%), radial-gradient(900px 500px at 90% 0%, rgba(212,175,55,0.12), transparent 50%), radial-gradient(700px 400px at 50% 100%, rgba(31,79,216,0.16), transparent 55%)",
      },
    },
  },
  plugins: [],
};
