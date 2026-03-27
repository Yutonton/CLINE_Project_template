import type {
  AnswerItem,
  DiagnosticConfig,
  DiagnosticResult,
  DiagnosticSummary,
} from "../types/diagnostic";

const BASE = `${import.meta.env.VITE_API_BASE_URL ?? ""}/api/v1`;

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error ${res.status}: ${path}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  getDiagnostics: () => request<DiagnosticSummary[]>("/diagnostics"),

  getDiagnosticConfig: (id: string) =>
    request<DiagnosticConfig>(`/diagnostics/${id}/config`),

  postResult: (id: string, answers: AnswerItem[]) =>
    request<DiagnosticResult>(`/diagnostics/${id}/result`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),
};
