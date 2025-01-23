import json
from datetime import datetime
import os

# Summary of the scrum meetings
scrum_meeting_summaries = [
    {
        "date": "[23/03/2025]",
        "duration": "[10 minutes]",
        "participant": ["Sherbin"],
        "updates": {
            "frontend": [
                "Completed the UI for menu browsing and search functionality.",
                "Finalized the design for the checkout screen."
            ],
            "backend": [
                "API for user authentication and payment processing is now operational.",
                "Resolved issues with order synchronization in the database."
            ],
            "qa": [
                "Completed testing of the menu display feature on mobile devices.",
                "Reported 3 critical bugs related to order tracking."
            ]
        },
        "blockers": {
            "frontend": "Delay in integrating the payment gateway due to API response inconsistencies.",
            "backend": "Difficulty in handling high-volume order simulations during stress testing.",
            "qa": "Limited test coverage for older Android versions causing feature incompatibilities."
        },
        "next_steps": {
            "frontend": [
                "Begin integration of the payment gateway once API fixes are applied.",
                "Collaborate with the backend team to improve order status updates in the UI."
            ],
            "backend": [
                "Optimize server response time to handle peak loads.",
                "Fix payment API inconsistencies and re-run tests."
            ],
            "qa": [
                "Expand test scenarios to include edge cases for mobile responsiveness.",
                "Verify fixes for the reported bugs in the next sprint."
            ]
        }
    },
    {
        "date": "[24/03/2025]",
        "duration": "[15 minutes]",
        "participant": ["Adarash"],
        "updates": {
            "frontend": [
                "Implemented responsive design for the user profile page.",
                "Updated the navigation bar to include a quick access menu."
            ],
            "backend": [
                "Enhanced API security for user data endpoints.",
                "Deployed a new caching mechanism to reduce database load."
            ],
            "qa": [
                "Verified the functionality of the user profile page across devices.",
                "Conducted exploratory testing on the payment flow."
            ]
        },
        "blockers": {
            "frontend": "Challenges in optimizing animations for older browsers.",
            "backend": "Unexpected errors during database migration.",
            "qa": "Insufficient test cases for cross-browser compatibility."
        },
        "next_steps": {
            "frontend": [
                "Resolve animation optimization issues and test on targeted browsers.",
                "Collaborate with the design team to finalize the dashboard UI."
            ],
            "backend": [
                "Address database migration issues and validate the data integrity.",
                "Improve logging mechanisms to facilitate debugging."
            ],
            "qa": [
                "Expand test scenarios to include cross-browser and cross-device testing.",
                "Follow up on reported issues with detailed bug reports."
            ]
        }
    },
    {
        "date": "[25/03/2025]",
        "duration": "[15 minutes]",
        "participant": ["Adarash"],
        "updates": {
            "frontend": [
                "Implemented responsive design for the user profile page.",
                "Updated the navigation bar to include a quick access menu."
            ],
            "backend": [
                "Enhanced API security for user data endpoints.",
                "Deployed a new caching mechanism to reduce database load."
            ],
            "qa": [
                "Verified the functionality of the user profile page across devices.",
                "Conducted exploratory testing on the payment flow."
            ]
        },
        "blockers": {
            "frontend": "Challenges in optimizing animations for older browsers.",
            "backend": "Unexpected errors during database migration.",
            "qa": "Insufficient test cases for cross-browser compatibility."
        },
        "next_steps": {
            "frontend": [
                "Resolve animation optimization issues and test on targeted browsers.",
                "Collaborate with the design team to finalize the dashboard UI."
            ],
            "backend": [
                "Address database migration issues and validate the data integrity.",
                "Improve logging mechanisms to facilitate debugging."
            ],
            "qa": [
                "Expand test scenarios to include cross-browser and cross-device testing.",
                "Follow up on reported issues with detailed bug reports."
            ]
        }
    }
]

# Define file paths for storing documents
BASE_DIR = "./scrum_docs"
INDIVIDUAL_DIR = os.path.join(BASE_DIR, "individual")
TEAM_FILE = os.path.join(BASE_DIR, "team.md")

# Create directories if they don't exist
os.makedirs(INDIVIDUAL_DIR, exist_ok=True)

# Function to write or append content to a file
def write_to_file(file_path, content):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)

# Function to check if content for a specific date exists in a file
def content_exists(file_path, date):
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r", encoding="utf-8") as file:
        return date in file.read()

# Function to generate today's date string
def get_date_string():
    return datetime.now().strftime("%Y-%m-%d")

# Function to process scrum transcripts and update documents
def process_scrum_transcripts(scrum_transcripts):
    for scrum_transcript in scrum_transcripts:
        date_string = scrum_transcript.get("date", "").strip("[]")
        team_summary = f"## Updates for {date_string}\n\n"

        # Update individual participant documents
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
            if not content_exists(individual_file, date_string):
                if not os.path.exists(individual_file):
                    write_to_file(individual_file, f"# {participant}'s Updates\n\n")
                write_to_file(individual_file, individual_summary)

        # Update team document
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

        # Write to team document if content doesn't exist
        if not content_exists(TEAM_FILE, date_string):
            if not os.path.exists(TEAM_FILE):
                write_to_file(TEAM_FILE, "# Team Updates\n\n")

            write_to_file(TEAM_FILE, team_summary)

process_scrum_transcripts(scrum_meeting_summaries)

print("Documents updated successfully!")
