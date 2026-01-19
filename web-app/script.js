const BACKEND = "https://smartattendance-mvp.onrender.com";

/* ================= FACULTY ================= */
async function createSession() {
  const classId = document.getElementById("classSelect").value;
  const subjectCode = document.getElementById("subjectSelect").value;

  try {
    const res = await fetch(
      `${BACKEND}/session/create?class_id=${classId}&subject_code=${subjectCode}`,
      { method: "POST" }
    );

    const data = await res.json();

    document.getElementById("sessionId").innerText = data.session_id;

    // optional QR
    document.getElementById("qrFrame").src =
      `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${data.session_id}`;

  } catch (err) {
    alert("Failed to create session");
    console.error(err);
  }
}

/* ================= STUDENT ================= */
async function markAttendance() {
  const rollOrEmail = document.getElementById("rollInput").value.trim();
  const sessionId = document.getElementById("sessionInput").value.trim();

  try {
    const res = await fetch(
      `${BACKEND}/attendance/mark?session_id=${sessionId}&student_email=${rollOrEmail}`,
      { method: "POST" }
    );

    const data = await res.json();
    alert(data.message || "Attendance marked");

  } catch (err) {
    alert("Attendance failed");
    console.error(err);
  }
}

/* ================= ROUTING ================= */
function openStudentDashboard() {
  const rollOrEmail = document.getElementById("rollInput").value.trim();
  if (!rollOrEmail) {
    alert("Enter roll/email first");
    return;
  }
  window.location.href = `student-dashboard.html?id=${encodeURIComponent(rollOrEmail)}`;
}

/* ================= DASHBOARD PLACEHOLDER ================= */
document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const span = document.getElementById("studentId");
  if (span && id) {
    span.innerText = id;
  }
});
