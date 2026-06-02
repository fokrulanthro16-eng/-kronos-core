/**
 * Deterministic, locale-independent timestamp formatter.
 *
 * Always uses UTC so the output is identical on the server (Node.js) and in
 * any browser locale — preventing hydration mismatches when API-returned ISO
 * strings are rendered inside state-gated JSX.
 *
 * Output example: "2026-06-02 · 08:14 UTC"
 */
export function formatTimestamp(iso: string): string {
  const d = new Date(iso);
  const date = d.toISOString().slice(0, 10);           // "2026-06-02"
  const time = d.toISOString().slice(11, 16);           // "08:14"
  return `${date} · ${time} UTC`;
}

/**
 * Deterministic date-only formatter (no time component).
 * Output example: "2 June 2026"
 */
export function formatDate(iso: string): string {
  const d = new Date(iso);
  const months = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December",
  ];
  return `${d.getUTCDate()} ${months[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
}
