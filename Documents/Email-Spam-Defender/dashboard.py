from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Spam filter dashboard backend running."}


DATA_FILE = "flagged_emails.json"

# Load flagged emails from file or start empty
def load_flagged_emails():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_flagged_emails(emails):
    with open(DATA_FILE, "w") as f:
        json.dump(emails, f, indent=2)

flagged_emails = load_flagged_emails()

class EmailFeedback(BaseModel):
    id: str
    subject: str = ""
    sender: str = ""
    body: str = ""
    is_spam: bool

@app.get("/flagged")
def get_flagged_emails():
    # Return only emails currently marked as spam
    return [email for email in flagged_emails if email.get("is_spam", True)]

@app.post("/feedback")
def post_feedback(feedback: EmailFeedback):
    global flagged_emails
    # Update existing email feedback or add new
    for i, email in enumerate(flagged_emails):
        if email["id"] == feedback.id:
            flagged_emails[i]["is_spam"] = feedback.is_spam
            flagged_emails[i]["subject"] = feedback.subject
            flagged_emails[i]["sender"] = feedback.sender
            flagged_emails[i]["body"] = feedback.body
            save_flagged_emails(flagged_emails)
            return {"message": "Feedback updated"}
    # New email
    flagged_emails.append(feedback.dict())
    save_flagged_emails(flagged_emails)
    return {"message": "Feedback saved"}
