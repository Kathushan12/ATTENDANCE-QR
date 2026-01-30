import { ensureDevice, API } from "./api.js";

function getSessionIdFromPath() {
  // expecting /s/<id>
  const parts = window.location.pathname.split("/");
  const sIndex = parts.indexOf("s");
  if (sIndex >= 0 && parts[sIndex+1]) return parts[sIndex+1];
  return null;
}

function getToken() {
  const url = new URL(window.location.href);
  return url.searchParams.get("t");
}

await ensureDevice();

const sid = getSessionIdFromPath();
const token = getToken();

document.getElementById("info").innerText =
  `Session: ${sid || "?"} | QR Token: ${token ? "received" : "missing"}`;

document.getElementById("lookupBtn").onclick = async () => {
  const reg = document.getElementById("reg").value.trim();
  const res = await fetch(`${API}/api/student/lookup/${encodeURIComponent(reg)}`, {
    credentials: "include"
  });

  const details = document.getElementById("details");
  if (!res.ok) {
    details.innerText = "Not found or not on University Wi-Fi.";
    return;
  }
  const data = await res.json();
  details.innerHTML = `<b>Name:</b> ${data.name}<br/><b>Index:</b> ${data.index_no}`;
};

document.getElementById("markBtn").onclick = async () => {
  const reg = document.getElementById("reg").value.trim();
  const msg = document.getElementById("msg");

  if (!token) {
    msg.innerText = "Token missing. Scan QR again.";
    return;
  }

  const res = await fetch(`${API}/api/student/mark`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    credentials: "include",
    body: JSON.stringify({ reg_no: reg, token })
  });

  const text = await res.text();
  msg.innerText = res.ok ? `✅ ${text}` : `❌ ${text}`;
};
