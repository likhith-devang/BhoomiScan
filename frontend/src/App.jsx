import { AnimatePresence, motion } from "framer-motion";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import AI from "./pages/AI";
import Contact from "./pages/Contact";
import DocumentAnalysis from "./pages/DocumentAnalysis";
import DocumentUpload from "./pages/DocumentUpload";
import DueDiligence from "./pages/DueDiligence";
import FinalReportPage from "./pages/FinalReport";
import Home from "./pages/Home";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import ProfileSettings from "./pages/ProfileSettings";
import PropertyDomain from "./pages/PropertyDomain";
import PropertyType from "./pages/PropertyType";
import Signup from "./pages/Signup";
import Subscription from "./pages/Subscription";

function PageFrame({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
    >
      {children}
    </motion.div>
  );
}

export default function App() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route
          path="/"
          element={
            <PageFrame>
              <Landing />
            </PageFrame>
          }
        />
        <Route
          path="/login"
          element={
            <PageFrame>
              <Login />
            </PageFrame>
          }
        />
        <Route
          path="/signup"
          element={
            <PageFrame>
              <Signup />
            </PageFrame>
          }
        />
        <Route element={<ProtectedRoute />}>
          <Route
            path="/dashboard"
            element={
              <PageFrame>
                <Home />
              </PageFrame>
            }
          />
          <Route
            path="/ai"
            element={
              <PageFrame>
                <AI />
              </PageFrame>
            }
          />
          <Route
            path="/profile/settings"
            element={
              <PageFrame>
                <ProfileSettings />
              </PageFrame>
            }
          />
          <Route
            path="/profile"
            element={
              <PageFrame>
                <Profile />
              </PageFrame>
            }
          />
          <Route
            path="/contact"
            element={
              <PageFrame>
                <Contact />
              </PageFrame>
            }
          />
          <Route
            path="/subscription"
            element={
              <PageFrame>
                <Subscription />
              </PageFrame>
            }
          />
          <Route
            path="/property-domain"
            element={
              <PageFrame>
                <PropertyDomain />
              </PageFrame>
            }
          />
          <Route
            path="/property-type"
            element={
              <PageFrame>
                <PropertyType />
              </PageFrame>
            }
          />
          <Route
            path="/property-case/:id/upload"
            element={
              <PageFrame>
                <DocumentUpload />
              </PageFrame>
            }
          />
          <Route
            path="/property-case/:caseId/documents/:documentId/analysis"
            element={
              <PageFrame>
                <DocumentAnalysis />
              </PageFrame>
            }
          />
          <Route
            path="/property-case/:id/due-diligence"
            element={
              <PageFrame>
                <DueDiligence />
              </PageFrame>
            }
          />
          <Route
            path="/property-case/:id/reports/:reportId"
            element={
              <PageFrame>
                <FinalReportPage />
              </PageFrame>
            }
          />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  );
}
