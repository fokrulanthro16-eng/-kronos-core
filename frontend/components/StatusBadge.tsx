import { CheckCircle, XCircle, AlertTriangle, HelpCircle } from "lucide-react";

type Level = "SAFE" | "LOW" | "CLEAN" | "PASS" |
             "SUSPICIOUS" | "WARN" | "MEDIUM" | "UNKNOWN" | "DEPRECATED" |
             "DANGEROUS" | "TYPOSQUAT" | "PHANTOM" | "HIGH" | "CRITICAL" | "BLOCKED" | "FAIL" |
             string;

const map: Record<string, { bg: string; text: string; border: string; Icon: typeof CheckCircle }> = {
  SAFE:       { bg: "bg-green-950/60",  text: "text-green-400",  border: "border-green-800/50",  Icon: CheckCircle },
  LOW:        { bg: "bg-green-950/60",  text: "text-green-400",  border: "border-green-800/50",  Icon: CheckCircle },
  CLEAN:      { bg: "bg-green-950/60",  text: "text-green-400",  border: "border-green-800/50",  Icon: CheckCircle },
  PASS:       { bg: "bg-green-950/60",  text: "text-green-400",  border: "border-green-800/50",  Icon: CheckCircle },
  SUSPICIOUS: { bg: "bg-yellow-950/60", text: "text-yellow-400", border: "border-yellow-800/50", Icon: AlertTriangle },
  WARN:       { bg: "bg-yellow-950/60", text: "text-yellow-400", border: "border-yellow-800/50", Icon: AlertTriangle },
  MEDIUM:     { bg: "bg-yellow-950/60", text: "text-yellow-400", border: "border-yellow-800/50", Icon: AlertTriangle },
  UNKNOWN:    { bg: "bg-yellow-950/60", text: "text-yellow-400", border: "border-yellow-800/50", Icon: AlertTriangle },
  DEPRECATED: { bg: "bg-yellow-950/60", text: "text-yellow-400", border: "border-yellow-800/50", Icon: AlertTriangle },
  DANGEROUS:  { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
  TYPOSQUAT:  { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
  PHANTOM:    { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
  HIGH:       { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
  CRITICAL:   { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
  BLOCKED:    { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
  FAIL:       { bg: "bg-red-950/60",    text: "text-red-400",    border: "border-red-800/50",    Icon: XCircle },
};

const fallback = { bg: "bg-gray-900/60", text: "text-gray-400", border: "border-gray-700/50", Icon: HelpCircle };

export function StatusBadge({ level, label }: { level: Level; label?: string }) {
  const s = map[level?.toUpperCase()] ?? fallback;
  const { bg, text, border, Icon } = s;
  return (
    <span className={`badge border ${bg} ${text} ${border}`}>
      <Icon className="h-3 w-3" />
      {label ?? level}
    </span>
  );
}
