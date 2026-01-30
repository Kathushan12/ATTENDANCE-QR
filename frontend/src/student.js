import { ensureDevice, API } from "./api.js";

function getSessionIdFromPath() {
  // expecting /s/<id>
  const parts = window.location.pathname.split("/").filter(Boolean);
  const sIndex = parts.indexOf("s");
  if (sIndex >= 0 && parts[sIndex + 1]) return parts[sIndex + 1];
  return null;
}

function getToken() {
  const url = new URL(window.location.href);
  return url.searchParams.get("t");
}

function getSessionIdFromQuery() {
  const url = new URL(window.location.href);
  return url.searchParams.get("sid");
}

function setText(el, text) {
  el.textContent = text;
}

function setMsg(el, ok, text) {
  el.textContent = (ok ? "✅ " : "❌ ") + text;
}

await ensureDevice();

const sid = getSessionIdFromPath() || getSessionIdFromQuery();
const token = getToken();

const info = document.getElementById("info");
const details = document.getElementById("details");
const msg = document.getElementById("msg");
const regInput = document.getElementById("reg");

setText(
  info,
  `Session: ${sid || "?"} | QR Token: ${token ? "received" : "missing"}`
);

// Lookup student
document.getElementById("lookupBtn").onclick = async () => {
  const reg = regInput.value.trim();
  if (!reg) {
    setMsg(msg, false, "Please enter your registration number.");
    return;
  }

  // Clear old messages before doing a new action
  setText(msg, "");
  setText(details, "Loading...");

  try {
    const res = await fetch(
      `${API}/api/student/lookup/${encodeURIComponent(reg)}`,
      { credentials: "include" }
    );

    if (!res.ok) {
      // Better error message
      const text = await res.text();
      setText(details, "");
      setMsg(msg, false, text || "Not found or not on University Wi-Fi.");
      return;
    }

    const data = await res.json();
    details.innerHTML = `<b>Name:</b> ${data.name}<br/><b>Index:</b> ${data.index_no}`;
    setMsg(msg, true, "Details loaded. Now click “Mark Attendance”.");
  } catch (e) {
    setText(details, "");
    setMsg(msg, false, "Network error. Please try again.");
  }
};

// Mark attendance
document.getElementById("markBtn").onclick = async () => {
  const reg = regInput.value.trim();
  if (!reg) {
    setMsg(msg, false, "Please enter your registration number.");
    return;
  }

  if (!token) {
    setMsg(msg, false, "Token missing. Scan QR again.");
    return;
  }

  // Clear old messages before marking
  setText(msg, "Submitting attendance...");
  // keep details as-is

  try {
    const res = await fetch(`${API}/api/student/mark`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ reg_no: reg, token }),
    });

    const text = await res.text();

    if (res.ok) {
      setMsg(msg, true, "OK - Attendance marked");
    } else {
      // show backend message (expired token / already marked / wifi blocked etc.)
      setMsg(msg, false, text || "Failed to mark attendance.");
    }
  } catch (e) {
    setMsg(msg, false, "Network error. Please try again.");
  }
};
