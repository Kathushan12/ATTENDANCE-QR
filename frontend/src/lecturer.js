import QRCode from "qrcode";
const API = "http://localhost:8000";

let sessionId = null;
let interval = null;

document.getElementById("loginBtn").onclick = async () => {
  const pw = document.getElementById("pw").value;
  const res = await fetch(`${API}/api/auth/login`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({password: pw})
  });
  if (!res.ok) alert("Login failed");
  else alert("Login ok");
};

document.getElementById("startBtn").onclick = async () => {
  const module_code = document.getElementById("module").value.trim();
  const res = await fetch(`${API}/api/lecturer/session`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({module_code})
  });

  if (!res.ok) {
    alert("Module not found / error");
    return;
  }

  const data = await res.json();
  sessionId = data.session_id;
  document.getElementById("status").innerText = `Session started: ${sessionId}`;

  if (interval) clearInterval(interval);
  await refreshQR();
  interval = setInterval(refreshQR, 10000);
};

async function refreshQR() {
  if (!sessionId) return;

  const res = await fetch(`${API}/api/lecturer/session/${sessionId}/token`);
  const data = await res.json();

  document.getElementById("url").innerText = data.url;

  const canvas = document.getElementById("qr");
  await QRCode.toCanvas(canvas, data.url);
}
