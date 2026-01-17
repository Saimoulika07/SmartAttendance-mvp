const API_BASE = "https://smartattendance-mvp.onrender.com";

let qr;
let countdown;

function createSession() {
  const classId = document.getElementById("classId").value;
  const output = document.getElementById("output");
  const qrDiv = document.getElementById("qr");
  const timerDiv = document.getElementById("timer");

  if (!classId) {
    output.innerText = "Enter Class ID ❌";
    return;
  }

  fetch(`${API_BASE}/session/create?class_id=${classId}`, {
    method: "POST"
  })
    .then(res => res.json())
    .then(data => {
      const sessionId = data.session_id;

      output.innerHTML = `
        <strong>Session Created ✅</strong><br>
        <b>Session ID:</b> ${sessionId}<br>
        <small>QR valid for 5 minutes</small>
      `;

      // Clear old QR
      qrDiv.innerHTML = "";
      timerDiv.innerText = "";

      // Generate QR
      qr = new QRCode(qrDiv, {
        text: sessionId,
        width: 200,
        height: 200
      });

      // Start 5-min countdown
      let seconds = 300;
      clearInterval(countdown);

      countdown = setInterval(() => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        timerDiv.innerText = `Expires in ${mins}:${secs.toString().padStart(2, "0")}`;

        seconds--;
        if (seconds < 0) {
          clearInterval(countdown);
          timerDiv.innerText = "QR expired ❌";
        }
      }, 1000);
    })
    .catch(() => {
      output.innerText = "Error creating session ❌";
    });
}
