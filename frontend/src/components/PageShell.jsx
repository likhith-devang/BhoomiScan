import Atmosphere from "./Atmosphere";
import Navbar from "./Navbar";

export default function PageShell({ children, wide = false }) {
  return (
    <div className="min-h-screen">
      <Atmosphere />
      <Navbar />
      <main className={`relative mx-auto px-5 py-10 sm:px-6 sm:py-12 ${wide ? "max-w-6xl" : "max-w-5xl"}`}>
        {children}
      </main>
    </div>
  );
}
