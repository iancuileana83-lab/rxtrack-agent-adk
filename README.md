# RxTrack Agent (ADK Edition)

RxTrack Agent helps patients track their prescriptions, active treatments, and renewal reminders through a simple conversational interface. This version is built with **Google's Agent Development Kit (ADK)**, powered by **Gemini**, and stores data persistently in **Google Cloud Firestore**.

## The Problem

Patients managing multiple or chronic prescriptions often lose track of dosages, treatment end dates, and renewal deadlines — leading to missed doses or interrupted treatment. RxTrack Agent acts as a lightweight AI assistant that logs prescriptions in natural language and helps patients stay on top of their treatment schedule.

## Who It's For

Patients managing multiple medications or long-term/chronic treatments, and anyone who wants a simple conversational way to track prescriptions without a complex app.

## Tech Stack

- **Google ADK** (Agent Development Kit) — agent framework
- **Gemini** (via Google GenAI SDK) — language model
- **Google Cloud Firestore** — persistent data storage
- **Python 3.12**

## Architecture

The agent exposes three tools:
- `add_prescription` — logs a new prescription (medication, dose, schedule, duration) to Firestore
- `list_active_treatments` — retrieves all currently active prescriptions
- `check_reminders` — checks which treatments are ending soon and need renewal

All prescription data is stored in the `prescriptions` collection in Firestore, making it persistent across sessions and viewable directly in the Firestore Console.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/iancuileana83-lab/rxtrack-agent-adk.git
cd rxtrack-agent-adk
```

### 2. Install dependencies

```bash
pip install google-cloud-firestore google-adk --break-system-packages
```

### 3. Authenticate with Google Cloud

This project uses Application Default Credentials to connect to Firestore:

```bash
gcloud auth application-default login --scopes="openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/cloud-platform"
```

Follow the printed link, sign in, and paste the authentication code back into the terminal when prompted.

### 4. Set up Firestore

Make sure your Google Cloud project has Firestore enabled (Native mode). The agent will automatically create the `prescriptions` collection on first use — no manual setup needed.

### 5. Set your Gemini API key

Get a key from [Google AI Studio](https://aistudio.google.com/apikey), then set it as an environment variable:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### 6. Run the agent

```bash
adk run rxtrack_agent
```

You can now chat with the agent directly in the terminal. Example:

```
Add a prescription for Amoxicillin, 500mg, twice daily, for 7 days
```

The agent will confirm the prescription and calculate the end date automatically. You can verify the data was saved by checking the `prescriptions` collection in the [Firestore Console](https://console.cloud.google.com/firestore).

## Example Commands

- "Add a prescription for Ibuprofen, 200mg, three times daily, for 5 days"
- "What are my active treatments?"
- "Do I have any prescriptions ending soon?"

## Project Status

Built for the All Things Agentic Hackathon. This is a working prototype demonstrating agentic prescription tracking with persistent Google Cloud storage.
