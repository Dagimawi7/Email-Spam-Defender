# dashboard.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# Enable CORS for frontend JS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend folder
frontend_folder = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_folder), name="frontend")


# Root route - serve the main index.html
@app.get("/")
def serve_index():
    index_path = os.path.join(frontend_folder, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend index.html not found"}


# Example endpoint to fetch emails
@app.get("/emails")
def get_emails():
    try:
        # In reality, you'd load from a database or your spam filter process
        emails = [
            {"id": 1, "subject": "Win a free iPhone!", "from": "scammer@example.com", "spam": True},
            {"id": 2, "subject": "Project update", "from": "boss@company.com", "spam": False},
        ]
        return emails
    except Exception as e:
        return {"error": str(e)}


# Endpoint to run spam detection process
@app.post("/process_emails")
def process_emails():
    try:
        # Here you'd run your spam-checking code
        # For now, just mock the process
        processed_emails = [
            {"id": 1, "subject": "Win a free iPhone!", "from": "scammer@example.com", "spam": True},
            {"id": 2, "subject": "Your bank account", "from": "fraud@bank.com", "spam": True},
            {"id": 3, "subject": "Meeting reminder", "from": "hr@company.com", "spam": False},
        ]
        return {"message": "Emails processed successfully", "emails": processed_emails}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("dashboard:app", host="127.0.0.1", port=8000, reload=True)
