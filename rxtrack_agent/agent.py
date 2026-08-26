"""
RxTrack Agent - Google ADK version
Adapted from the original AWS Strands Agents SDK version,
built for the "All Things Agentic" hackathon.
Now backed by Google Cloud Firestore for persistent storage.
"""

from google.adk.agents import Agent
from google.cloud import firestore
from datetime import datetime, timedelta

db = firestore.Client()
COLLECTION = "prescriptions"


def add_prescription(medication_name: str, dose: str, duration_days: int) -> str:
    """Add a new prescription and calculate when treatment ends.

    Args:
        medication_name: Name of the medication.
        dose: Dosage instructions (e.g. "1 pill, twice a day").
        duration_days: How many days the treatment lasts.
    """
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=duration_days)

    entry = {
        "medication_name": medication_name,
        "dose": dose,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "status": "active",
    }
    db.collection(COLLECTION).add(entry)

    return f"Added {medication_name}. Treatment ends on {end_date}."


def list_active_treatments() -> str:
    """List all currently active treatments."""
    docs = db.collection(COLLECTION).where("status", "==", "active").stream()
    active = [d.to_dict() for d in docs]

    if not active:
        return "No active treatments found."

    lines = []
    for t in active:
        lines.append(f"- {t['medication_name']} ({t['dose']}), ends {t['end_date']}")
    return "\n".join(lines)


def check_reminders() -> str:
    """Check which treatments are ending soon (within 3 days)."""
    docs = db.collection(COLLECTION).where("status", "==", "active").stream()
    today = datetime.now().date()
    reminders = []

    for d in docs:
        t = d.to_dict()
        end_date = datetime.strptime(t["end_date"], "%Y-%m-%d").date()
        days_left = (end_date - today).days

        if days_left <= 3:
            reminders.append(
                f"⚠️ {t['medication_name']}: {days_left} days left — time to renew your prescription."
            )

    if not reminders:
        return "No urgent reminders right now."
    return "\n".join(reminders)


root_agent = Agent(
    model="gemini-3.6-flash",
    name="rxtrack_agent",
    description="Tracks patient prescriptions and treatment reminders.",
    instruction=(
        "You are RxTrack, a friendly assistant that helps patients track their "
        "prescriptions and never miss a treatment renewal. Be concise and warm."
    ),
    tools=[add_prescription, list_active_treatments, check_reminders],
)
