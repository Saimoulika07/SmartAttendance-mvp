const BACKEND_URL = "https://smartattendance-mvp.onrender.com";

function markAttendance() {
  const sessionId = document.getElementById("sessionId").value;
  const email = document.getElementById("email").value;

  fetch(`${BACKEND_URL}/attendance/mark?session_id=${sessionId}&student_email=${email}`, {
    method: "POST"
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerText = "Attendance marked ✅";
  })
  .catch(err => {
    document.getElementById("result").innerText = "Error ❌";
  });
}
