export const API = "http://localhost:8000";

export async function ensureDevice() {
  const res = await fetch(`${API}/api/student/device`, { credentials: "include" });
  return res.json();
}
