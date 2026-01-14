const BACKEND_URL = "https://smartattendance-mvp.onrender.com";

function markAttendance() {
  const email = document.getElementById("email").value;
  const session = document.getElementById("session").value;

  fetch(`${BACKEND_URL}/attendance/mark?session_id=${session}&student_email=${email}`, {
    method: "POST"
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerText = data.message || "Attendance marked!";
  })
  .catch(err => {
    document.getElementById("result").innerText = "Error marking attendance";
  });
}
