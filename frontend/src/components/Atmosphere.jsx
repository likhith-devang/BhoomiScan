export default function Atmosphere() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-void bg-royal-radial">
      <div className="orb left-[-8%] top-[10%] h-72 w-72 bg-royal/40" />
      <div className="orb right-[-6%] top-[20%] h-80 w-80 bg-gold/20" style={{ animationDelay: "1.8s" }} />
      <div className="orb bottom-[-10%] left-[30%] h-96 w-96 bg-sapphire/20" style={{ animationDelay: "3s" }} />
      <div className="noise" />
    </div>
  );
}
