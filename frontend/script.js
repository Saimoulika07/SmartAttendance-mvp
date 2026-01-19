const BACKEND = "https://smartattendance-mvp.onrender.com";

/* ================= FACULTY ================= */

async function createSession() {
  const classId = document.getElementById("classSelect").value;
  const subject = document.getElementById("subjectSelect").value;

  try {
    const res = await fetch(
      `${BACKEND}/session/create?class_id=${encodeURIComponent(classId)}&subject_code=${encodeURIComponent(subject)}`,
      { method: "POST" }
    );

    if (!res.ok) {
      alert("Session creation failed");
      return;
    }

    const data = await res.json();
    document.getElementById("sessionId").innerText = data.session_id;

    document.getElementById("qrFrame").src =
      `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${data.session_id}`;

  } catch (e) {
    alert("Backend not reachable");
  }
}

async function loadFacultyAnalytics() {
  const classId = document.getElementById("classSelect").value;
  const subject = document.getElementById("subjectSelect").value;

  const res = await fetch(
    `${BACKEND}/analytics/faculty?class_id=${classId}&subject_code=${subject}`
  );
  const data = await res.json();

  document.getElementById("facultyStats").innerText =
    `Attendance: ${data.attendance_percentage}%`;

  const color = data.attendance_percentage < 75 ? "red" : "green";

  if (window.facultyChartObj) {
    window.facultyChartObj.destroy();
  }

  window.facultyChartObj = new Chart(
    document.getElementById("facultyChart"),
    {
      type: "bar",
      data: {
        labels: ["Present", "Absent"],
        datasets: [{
          data: [data.present, data.absent],
          backgroundColor: [color, "#ddd"]
        }]
      }
    }
  );
}

/* ================= STUDENT ================= */

async function markAttendance() {
  const email = document.getElementById("rollInput").value.trim();
  const sessionId = document.getElementById("sessionInput").value.trim();

  try {
    const res = await fetch(
      `${BACKEND}/attendance/mark?session_id=${encodeURIComponent(sessionId)}&student_email=${encodeURIComponent(email)}`,
      { method: "POST" }
    );

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail);
      return;
    }

    alert(data.message);

  } catch (e) {
    alert("Network error");
  }
}

/* ================= STUDENT DASHBOARD ================= */

async function loadStudentDashboard() {
  const params = new URLSearchParams(window.location.search);
  const email = params.get("id");

  const res = await fetch(
    `${BACKEND}/analytics/student?student_email=${encodeURIComponent(email)}`
  );
  const data = await res.json();

  document.getElementById("info").innerText =
    `Attendance: ${data.attendance_percentage}%`;

  const color = data.attendance_percentage < 75 ? "red" : "green";

  if (window.studentChartObj) {
    window.studentChartObj.destroy();
  }

  window.studentChartObj = new Chart(
    document.getElementById("studentChart"),
    {
      type: "doughnut",
      data: {
        labels: ["Present", "Absent"],
        datasets: [{
          data: [
            data.attended_sessions,
            data.total_sessions - data.attended_sessions
          ],
          backgroundColor: [color, "#ddd"]
        }]
      }
    }
  );
}

if (document.getElementById("studentChart")) {
  loadStudentDashboard();
}
