const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function sendMessage(message, sessionId = null) {
  // Backend ChatRequest schema expects { message, session_id }
  const body = { message };
  if (sessionId) body.session_id = sessionId;

  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Chat error ${res.status}: ${text}`);
  }
  return res.json();
}

export async function fetchSessions() {
  const res = await fetch(`${BASE_URL}/sessions`);
  if (!res.ok) throw new Error(`Sessions error: ${res.status}`);
  return res.json();
}

export async function fetchHistory(sessionId) {
  const res = await fetch(`${BASE_URL}/history/${sessionId}`);
  if (!res.ok) throw new Error(`History error: ${res.status}`);
  return res.json();
}