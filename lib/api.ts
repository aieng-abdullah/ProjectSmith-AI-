export interface ChatResponse {
  response: string;
}

export interface PlanResponse {
  plan: string;
  cost: string;
  edges: string;
  prd: string;
}

export interface Memory {
  id: string;
  content: string;
  created_at: string;
}

// Use relative paths to call Next.js API routes
// which proxy to the FastAPI backend

export async function sendMessage(
  userId: string,
  threadId: string,
  message: string
): Promise<ChatResponse> {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      thread_id: threadId,
      message,
    }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.error || `Chat request failed: ${res.statusText}`);
  }

  return res.json();
}

export async function generatePlan(
  userId: string,
  threadId: string,
  message: string
): Promise<PlanResponse> {
  const res = await fetch("/api/plan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      thread_id: threadId,
      message,
    }),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.error || `Plan request failed: ${res.statusText}`);
  }

  return res.json();
}

// Memory API - uses NEXT_PUBLIC_API_URL for client-side fetching
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function getMemories(userId: string): Promise<Memory[]> {
  const res = await fetch(`${API_BASE}/memory/${userId}`);

  if (!res.ok) {
    throw new Error(`Memory fetch failed: ${res.statusText}`);
  }

  const data = await res.json();
  return data.memories || [];
}

export async function saveMemory(
  userId: string,
  messages: { role: string; content: string }[]
): Promise<void> {
  const res = await fetch(`${API_BASE}/memory/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      messages,
    }),
  });

  if (!res.ok) {
    throw new Error(`Memory save failed: ${res.statusText}`);
  }
}
