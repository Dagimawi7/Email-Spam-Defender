const API_BASE = "http://localhost:8000"; // FastAPI backend URL

async function fetchFlaggedEmails() {
  const response = await fetch(`${API_BASE}/flagged`);
  const emails = await response.json();
  return emails;
}

async function sendFeedback(emailId, isSpam) {
  const response = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: emailId,
      subject: "",
      sender: "",
      body: "",
      is_spam: isSpam,
    }),
  });
  return response.json();
}

function createEmailItem(email) {
  const div = document.createElement("div");
  div.className = "email-item";

  const subject = document.createElement("h2");
  subject.textContent = email.subject;

  const sender = document.createElement("p");
  sender.innerHTML = `<strong>From:</strong> ${email.sender}`;

  const body = document.createElement("p");
  body.textContent = email.body;

  const btnNotSpam = document.createElement("button");
  btnNotSpam.textContent = "Mark as Not Spam";
  btnNotSpam.onclick = async () => {
    await sendFeedback(email.id, false);
    alert(`Marked "${email.subject}" as Not Spam.`);
    loadEmails();
  };

  div.appendChild(subject);
  div.appendChild(sender);
  div.appendChild(body);
  div.appendChild(btnNotSpam);

  return div;
}

async function loadEmails() {
  const emailList = document.getElementById("email-list");
  emailList.innerHTML = "Loading...";

  try {
    const emails = await fetchFlaggedEmails();

    if (emails.length === 0) {
      emailList.textContent = "No flagged emails.";
      return;
    }

    emailList.innerHTML = "";
    emails.forEach((email) => {
      emailList.appendChild(createEmailItem(email));
    });
  } catch (error) {
    emailList.textContent = "Error loading emails.";
    console.error(error);
  }
}

window.onload = loadEmails;
