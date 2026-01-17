const API_BASE = "https://smartattendance-mvp.onrender.com";

let qr;
let countdown;

function createSession() {
  const classId = document.getElementById("classId").value.trim();
  const subjectCode = document.getElementById("subjectCode").value.trim();
  const output = document.getElementById("output");
  const qrDiv = document.getElementById("qr");
  const timerDiv = document.getElementById("timer");

  if (!classId || !subjectCode) {
    output.innerText = "Enter Class ID and Subject Code ❌";
    return;
  }

  fetch(`${API_BASE}/session/create?class_id=${classId}&subject_code=${subjectCode}`, {
    method: "POST"
  })
    .then(res => res.json())
    .then(data => {
      const sessionId = data.session_id;

      output.innerHTML = `
        <strong>Session Created ✅</strong><br>
        <b>Session ID:</b> ${sessionId}<br>
        <b>Subject:</b> ${subjectCode}<br>
        <small>QR valid for 5 minutes</small>
      `;

      qrDiv.innerHTML = "";
      timerDiv.innerText = "";

      new QRCode(qrDiv, {
        text: sessionId,
        width: 200,
        height: 200
      });

      let seconds = 300;
      clearInterval(countdown);

      countdown = setInterval(() => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        timerDiv.innerText = `Expires in ${m}:${s.toString().padStart(2, "0")}`;
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
