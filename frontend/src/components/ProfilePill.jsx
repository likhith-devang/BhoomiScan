import { getUserInitials } from "../lib/userDisplay";
import { IconChevron } from "./icons";

export default function ProfilePill({ user, open, onToggle }) {
  const username = user?.username || "User";
  const initials = getUserInitials(username);

  return (
    <button
      type="button"
      onClick={onToggle}
      aria-haspopup="menu"
      aria-expanded={open}
      aria-label={`Open profile menu for ${username}`}
      className="flex max-w-[9.5rem] items-center gap-2 rounded-full border border-gold/25 bg-white/5 py-1 pl-1 pr-3 text-left shadow-gold transition hover:border-gold/50 hover:bg-white/10 sm:max-w-[16rem]"
    >
      <span
        aria-hidden="true"
        className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-gradient-to-br from-royal to-gold text-[11px] font-bold text-ivory"
      >
        {initials}
      </span>
      <span className="min-w-0 flex-1 truncate text-sm font-semibold text-ivory">{username}</span>
      <IconChevron className={`h-4 w-4 shrink-0 text-gold transition ${open ? "rotate-180" : ""}`} />
    </button>
  );
}
