const API_BASE = "https://smartattendance-mvp.onrender.com";
let rollToEmail = {};

// Load students.csv
fetch("students.csv")
  .then(response => response.text())
  .then(data => {
    const rows = data.split("\n").slice(1); // skip header
    rows.forEach(row => {
      const cols = row.split(",");
      if (cols.length >= 2) {
        const roll = cols[0].trim();
        const email = cols[1].trim();
        if (roll && email) {
          rollToEmail[roll] = email;
        }
      }
    });
  });

function markAttendance() {
  const rollNo = document.getElementById("rollNo").value.trim();
  const sessionId = document.getElementById("sessionId").value.trim();
  const result = document.getElementById("result");

  if (!rollNo || !sessionId) {
    result.innerText = "Please fill all fields ❌";
    return;
  }

  const email = rollToEmail[rollNo];

  if (!email) {
    result.innerText = "Roll number not found ❌";
    return;
  }

  fetch(`${API_BASE}/attendance/mark?session_id=${sessionId}&student_email=${email}`, {
    method: "POST"
  })
    .then(res => {
      if (!res.ok) throw new Error();
      return res.json();
    })
    .then(() => {
      result.innerText = "Attendance marked ✅";
    })
    .catch(() => {
      result.innerText = "Error marking attendance ❌";
    });
}
