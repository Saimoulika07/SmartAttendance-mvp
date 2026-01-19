const BACKEND = "https://smartattendance-mvp.onrender.com";

/* ---------- STUDENT DASHBOARD ---------- */
async function loadStudentDashboard() {
  const params = new URLSearchParams(window.location.search);
  const email = params.get("id");

  const res = await fetch(`${BACKEND}/analytics/student?student_email=${email}`);
  const data = await res.json();

  document.getElementById("info").innerText =
    `Attendance: ${data.attendance_percentage}%`;

  const color = data.attendance_percentage < 75 ? "red" : "green";

  new Chart(document.getElementById("studentChart"), {
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
  });
}

if (document.getElementById("studentChart")) {
  loadStudentDashboard();
}


/* ---------- FACULTY ---------- */
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

  new Chart(document.getElementById("facultyChart"), {
    type: "bar",
    data: {
      labels: ["Present", "Absent"],
      datasets: [{
        data: [data.present, data.absent],
        backgroundColor: [color, "#ddd"]
      }]
    }
  });
}
