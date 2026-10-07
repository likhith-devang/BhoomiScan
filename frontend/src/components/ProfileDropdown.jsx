import { Link } from "react-router-dom";
import { IconLogout, IconMail, IconSettings, IconSparkle, IconUser } from "./icons";

const items = [
  { to: "/profile", label: "Profile", icon: IconUser },
  { to: "/profile/settings", label: "Profile Settings", icon: IconSettings },
  { to: "/contact", label: "Contact Us", icon: IconMail },
  { to: "/subscription", label: "Subscription", icon: IconSparkle },
];

export default function ProfileDropdown({ onClose, onSignOut }) {
  return (
    <div
      role="menu"
      aria-label="Profile menu"
      className="absolute right-0 z-50 mt-2 w-56 overflow-hidden rounded-2xl border border-white/10 bg-navy/95 p-1.5 shadow-glow backdrop-blur-xl"
    >
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <Link
            key={item.to}
            to={item.to}
            role="menuitem"
            onClick={onClose}
            className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-ivory/90 transition hover:bg-white/10 hover:text-ivory"
          >
            <Icon className="h-4 w-4 text-gold" />
            {item.label}
          </Link>
        );
      })}
      <div className="my-1 border-t border-white/10" />
      <button
        type="button"
        role="menuitem"
        onClick={onSignOut}
        className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-red-200 transition hover:bg-red-950/40"
      >
        <IconLogout className="h-4 w-4" />
        Sign Out
      </button>
    </div>
  );
}
