const BACKEND = "https://smartattendance-mvp.onrender.com";

/* ========= COMMON ========= */

function rollToEmail(value) {
  if (!value) return "";
  if (value.includes("@")) return value.trim();
  return `${value.trim()}@aits-tpt.edu.in`;
}

/* ========= FACULTY ========= */

let facultyChartInstance = null;

async function createSession() {
  const classId = document.getElementById("classSelect").value;
  const subject = document.getElementById("subjectSelect").value;

  const res = await fetch(
    `${BACKEND}/session/create?class_id=${classId}&subject_code=${subject}`,
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

  loadFacultyAnalytics(); // auto refresh
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

  if (facultyChartInstance) facultyChartInstance.destroy();

  facultyChartInstance = new Chart(
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

/* ========= STUDENT DASHBOARD ========= */

let studentChartInstance = null;

async function loadStudentDashboard() {
  const params = new URLSearchParams(window.location.search);
  const roll = params.get("id");

  if (!roll) {
    document.getElementById("info").innerText = "No roll number provided";
    return;
  }

  document.getElementById("rollLabel").innerText = roll;
  const email = rollToEmail(roll);

  const res = await fetch(
    `${BACKEND}/analytics/student?student_email=${email}`
  );
  const data = await res.json();

  document.getElementById("info").innerText =
    `Attendance: ${data.attendance_percentage}%`;

  const color = data.attendance_percentage < 75 ? "red" : "green";

  if (studentChartInstance) studentChartInstance.destroy();

  studentChartInstance = new Chart(
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

/* Auto-load student dashboard */
if (document.getElementById("studentChart")) {
  loadStudentDashboard();
}
