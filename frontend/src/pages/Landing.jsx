import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import Atmosphere from "../components/Atmosphere";
import Button from "../components/Button";
import Card from "../components/Card";
import Logo from "../components/Logo";
import Navbar from "../components/Navbar";
import { RISK_PILLARS } from "../constants/property";
import { useAuth } from "../hooks/useAuth";

const fade = {
  hidden: { opacity: 0, y: 24 },
  show: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: 0.08 * i, duration: 0.6, ease: [0.22, 1, 0.36, 1] },
  }),
};

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen">
      <Atmosphere />
      <Navbar transparent />
      <main className="mx-auto max-w-6xl px-6 pb-24 pt-10">
        <section className="grid items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]">
          <div>
            <motion.p
              variants={fade}
              initial="hidden"
              animate="show"
              className="text-xs uppercase tracking-[0.42em] text-gold"
            >
              Check your property papers first
            </motion.p>
            <motion.h1
              custom={1}
              variants={fade}
              initial="hidden"
              animate="show"
              className="mt-4 font-display text-6xl leading-[0.95] text-ivory md:text-8xl"
            >
              Your <span className="shimmer-text italic">AIvocate.</span>
            </motion.h1>
            <motion.p
              custom={2}
              variants={fade}
              initial="hidden"
              animate="show"
              className="mt-6 max-w-xl text-lg text-mist"
            >
              We help you check property papers before you buy.
            </motion.p>
            <motion.p
              custom={3}
              variants={fade}
              initial="hidden"
              animate="show"
              className="mt-4 max-w-xl text-base leading-7 text-ivory/80"
            >
              Upload your papers. BhoomiScan looks for problems with who owns the property,
              court cases, bank loans, building permissions, and land records.
            </motion.p>
            <motion.div custom={4} variants={fade} initial="hidden" animate="show" className="mt-8 flex flex-wrap gap-3">
              {user ? (
                <>
                  <Link to="/property-domain">
                    <Button variant="gold" className="px-7 py-3">
                      Start Property Analysis
                    </Button>
                  </Link>
                  <Link to="/dashboard">
                    <Button variant="ghost" className="px-7 py-3">
                      Home
                    </Button>
                  </Link>
                </>
              ) : (
                <>
                  <Link to="/signup">
                    <Button variant="gold" className="px-7 py-3">
                      Get Started
                    </Button>
                  </Link>
                  <Link to="/login">
                    <Button variant="ghost" className="px-7 py-3">
                      Login
                    </Button>
                  </Link>
                </>
              )}
            </motion.div>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="royal-frame p-8"
          >
            <div className="relative z-10">
              <Logo />
              <div className="gold-line my-6" />
              <p className="font-display text-3xl text-ivory">Five checks. One place.</p>
              <p className="mt-3 text-sm leading-6 text-mist">
                Keep all your property papers together. Later, BhoomiScan will read them and
                tell you what to watch out for.
              </p>
              <dl className="mt-8 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <dt className="text-mist">Now</dt>
                  <dd className="text-ivory">Save your papers safely</dd>
                </div>
                <div>
                  <dt className="text-mist">Next</dt>
                  <dd className="text-ivory">AI will read them</dd>
                </div>
              </dl>
            </div>
          </motion.div>
        </section>

        <section className="mt-24">
          <h2 className="font-display text-4xl text-ivory">What BhoomiScan checks</h2>
          <p className="mt-3 max-w-2xl text-mist">
            We look at five common problems before you buy a home.
          </p>
          <div className="mt-8 grid gap-5 md:grid-cols-2 lg:grid-cols-5">
            {RISK_PILLARS.map((pillar, index) => (
              <Card key={pillar.title} className="min-h-[180px]">
                <p className="text-[10px] uppercase tracking-[0.28em] text-gold">0{index + 1}</p>
                <h3 className="mt-3 font-display text-2xl">{pillar.title}</h3>
                <p className="mt-2 text-sm text-mist">{pillar.copy}</p>
              </Card>
            ))}
          </div>
        </section>

        <section className="mt-24 grid gap-6 md:grid-cols-3">
          {[
            { step: "01", title: "Start a file", copy: "Tell us what kind of home it is." },
            { step: "02", title: "Add your papers", copy: "Upload sale deeds, receipts, and other papers." },
            { step: "03", title: "Get a check", copy: "For now we only save your files. AI reading comes next." },
          ].map((item) => (
            <Card key={item.step}>
              <p className="text-gold">{item.step}</p>
              <h3 className="mt-2 font-display text-3xl">{item.title}</h3>
              <p className="mt-3 text-sm text-mist">{item.copy}</p>
            </Card>
          ))}
        </section>
      </main>
      <footer className="border-t border-white/5 py-8 text-center text-xs uppercase tracking-[0.24em] text-mist">
        BhoomiScan · Your AIvocate
      </footer>
    </div>
  );
}
