const API_BASE = "https://smartattendance-mvp.onrender.com";

let rollToEmail = {};

// Load students.csv and build roll → email map
fetch("students.csv")
  .then(res => res.text())
  .then(text => {
    const rows = text.split("\n").slice(1); // skip header
    rows.forEach(row => {
      if (!row.trim()) return;
      const cols = row.split(",");
      const roll = cols[0]?.trim();
      const email = cols[1]?.trim();
      if (roll && email) {
        rollToEmail[roll] = email;
      }
    });
  })
  .catch(err => {
    console.error("Failed to load students.csv", err);
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
      if (!res.ok) {
        return res.json().then(err => {
          throw new Error(err.detail || "Attendance already marked");
        });
      }
      return res.json();
    })
    .then(() => {
      result.innerText = "Attendance marked ✅";
    })
    .catch(err => {
      result.innerText = err.message;
    });
}
