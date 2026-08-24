"""
RxTrack Agent - Google ADK version
Adapted from the original AWS Strands Agents SDK version,
built for the "All Things Agentic" hackathon.
"""

from google.adk.agents import Agent
from datetime import datetime, timedelta
import json
import os

DATA_FILE = "prescriptions.json"


def _load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def _save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_prescription(medication_name: str, dose: str, duration_days: int) -> str:
    """Add a new prescription and calculate when the treatment ends.

    Args:
        medication_name: Name of the medication.
        dose: Dosage instructions (e.g. "1 pill, twice a day").
        duration_days: How many days the treatment lasts.
    """
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=duration_days)

    data = _load_data()
    entry = {
        "medication_name": medication_name,
        "dose": dose,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "status": "active",
    }
    data.append(entry)
    _save_data(data)

    return f"Added {medication_name}. Treatment runs from {start_date} to {end_date}."


def list_active_treatments() -> str:
    """List all currently active treatments."""
    data = _load_data()
    active = [d for d in data if d["status"] == "active"]

    if not active:
        return "No active treatments found."

    lines = []
    for t in active:
        lines.append(f"- {t['medication_name']} ({t['dose']}), ends {t['end_date']}")
    return "\n".join(lines)


def check_reminders() -> str:
    """Check which treatments are ending soon (within 3 days) and need renewal."""
    data = _load_data()
    today = datetime.now().date()
    reminders = []

    for t in data:
        if t["status"] != "active":
            continue
        end_date = datetime.strptime(t["end_date"], "%Y-%m-%d").date()
        days_left = (end_date - today).days

        if days_left <= 3:
            reminders.append(
                f"⚠️ {t['medication_name']}: {days_left} day(s) left — "
                f"time to renew your prescription."
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