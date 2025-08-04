from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

DATA_FILE = "flagged_emails.json"

# Load flagged emails from file or start empty
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        flagged_emails = json.load(f)
else:
    flagged_emails = []

class EmailFeedback(BaseModel):
    id: str
    subject: str
    sender: str
    body: str
    is_spam: bool

@app.get("/flagged")
def get_flagged_emails():
    return flagged_emails

@app.post("/feedback")
def post_feedback(feedback: EmailFeedback):
    # Save feedback (e.g. to remove from spam, or for retraining)
    for i, email in enumerate(flagged_emails):
        if email["id"] == feedback.id:
            flagged_emails[i]["is_spam"] = feedback.is_spam
            with open(DATA_FILE, "w") as f:
                json.dump(flagged_emails, f, indent=2)
            return {"message": "Feedback saved"}
    # If new email, add it
    flagged_emails.append(feedback.dict())
    with open(DATA_FILE, "w") as f:
        json.dump(flagged_emails, f, indent=2)
    return {"message": "Feedback saved"}
