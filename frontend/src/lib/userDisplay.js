export function getUserInitials(username = "") {
  const parts = String(username)
    .split(/[\s._-]+/)
    .map((part) => part.replace(/[^A-Za-z0-9]/g, ""))
    .filter(Boolean);

  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }

  const letters = String(username).replace(/[^A-Za-z0-9]/g, "");
  if (!letters) return "BS";
  return letters.slice(0, 2).toUpperCase();
}

export function formatDateTime(value) {
  if (!value) return "Not yet";
  return new Date(value).toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatDate(value) {
  if (!value) return "Not yet";
  return new Date(value).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
