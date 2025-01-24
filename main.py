import json
import os
from datetime import datetime

# Define file paths for storing documents
BASE_DIR = "./scrum_docs"
INDIVIDUAL_DIR = os.path.join(BASE_DIR, "individual")
TEAM_FILE = os.path.join(BASE_DIR, "team.md")
SCRUM_SUMMARY_FILE = "scrum_meeting_summaries.json"  # JSON file to load scrum summaries

# Create directories if they don't exist
os.makedirs(INDIVIDUAL_DIR, exist_ok=True)

# Function to write or append content to a file
def write_to_file(file_path, content):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)

# Function to check if content for a specific date and participant exists in a file
def content_exists_for_date_and_name(file_path, date, participants):
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return any(f"## Updates for {date} by {participant}" in content for participant in participants)

# Function to generate today's date string
def get_date_string():
    return datetime.now().strftime("%Y-%m-%d")

# Function to load the scrum summaries from a JSON file
def load_scrum_summaries():
    with open(SCRUM_SUMMARY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to update individual participant documents
def update_individual_participant_documents(scrum_transcript, date_string):
    for participant in scrum_transcript.get("participant", []):
        individual_file = os.path.join(INDIVIDUAL_DIR, f"{participant}.md")
        individual_summary = f"# Updates for {participant}\n\n## Date: {date_string}\n\n"

        # Add updates
        for category, updates in scrum_transcript.get("updates", {}).items():
            individual_summary += f"### {category.capitalize()}\n"
            for update in updates:
                individual_summary += f"- {update}\n"
            individual_summary += "\n"

        # Add blockers
        individual_summary += "### Blockers\n"
        for category, blocker in scrum_transcript.get("blockers", {}).items():
            individual_summary += f"- **{category.capitalize()}**: {blocker}\n"
        individual_summary += "\n"

        # Add next steps
        individual_summary += "### Next Steps\n"
        for category, steps in scrum_transcript.get("next_steps", {}).items():
            individual_summary += f"- **{category.capitalize()}**:\n"
            for step in steps:
                individual_summary += f"  - {step}\n"
        individual_summary += "\n"

        # Write to individual document if content doesn't exist
        if not content_exists_for_date_and_name(individual_file, date_string, [participant]):
            if not os.path.exists(individual_file):
                write_to_file(individual_file, f"# {participant}'s Updates\n\n")
            write_to_file(individual_file, individual_summary)

# Function to update team document
def update_team_document(scrum_transcript, date_string):
    team_summary = f"## Updates for {date_string} by {scrum_transcript.get('participant')}\n\n"

    if not content_exists_for_date_and_name(TEAM_FILE, date_string, scrum_transcript.get("participant", [])):
        # Add updates
        for category, updates in scrum_transcript.get("updates", {}).items():
            category_summary = f"### {category.capitalize()}\n"
            for update in updates:
                category_summary += f"- {update}\n"
            category_summary += "\n"
            team_summary += category_summary

        # Add blockers
        blockers_summary = "### Blockers\n"
        for category, blocker in scrum_transcript.get("blockers", {}).items():
            blockers_summary += f"- **{category.capitalize()}**: {blocker}\n"
        blockers_summary += "\n"
        team_summary += blockers_summary

        # Add next steps
        next_steps_summary = "### Next Steps\n"
        for category, steps in scrum_transcript.get("next_steps", {}).items():
            next_steps_summary += f"- **{category.capitalize()}**:\n"
            for step in steps:
                next_steps_summary += f"  - {step}\n"
        next_steps_summary += "\n"
        team_summary += next_steps_summary

        if not os.path.exists(TEAM_FILE):
            write_to_file(TEAM_FILE, "# Team Updates\n\n")

        write_to_file(TEAM_FILE, team_summary)

# Main function to process scrum transcripts
def process_scrum_transcripts(scrum_transcripts):
    for scrum_transcript in scrum_transcripts:
        date_string = scrum_transcript.get("date", "").strip("[]")

        # Update individual participant documents
        update_individual_participant_documents(scrum_transcript, date_string)

        # Update team document
        update_team_document(scrum_transcript, date_string)

# Load scrum summaries from file
scrum_meeting_summaries = load_scrum_summaries()

process_scrum_transcripts(scrum_meeting_summaries)

print("Documents updated successfully!")
