const API_BASE = "https://smartattendance-mvp.onrender.com";

function createSession() {
  const classId = document.getElementById("classId").value;
  const output = document.getElementById("output");

  if (!classId) {
    output.innerHTML = "Please enter a Class ID ❌";
    return;
  }

  output.innerHTML = "Creating session... ⏳";

  fetch(`${API_BASE}/session/create?class_id=${classId}`, {
    method: "POST"
  })
    .then(res => res.json())
    .then(data => {
      if (data.session_id) {
        output.innerHTML = `
          <strong>Session Created ✅</strong><br><br>
          <b>Session ID:</b><br>
          <code>${data.session_id}</code><br><br>
          <span>Share this Session ID with students.</span>
        `;
      } else {
        output.innerHTML = "Unexpected response ❌";
      }
    })
    .catch(err => {
      console.error(err);
      output.innerHTML = "Error creating session ❌";
    });
}
