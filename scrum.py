import openai
import os
from dotenv import load_dotenv
from datetime import datetime
import re

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def update_scrum_summary(project_scrum, individual_scrum, individual_name):
    folder_name = "scrum_summaries"
    individual_filename = os.path.join(folder_name, f"{individual_name}.md")
    team_filename = os.path.join(folder_name, "team_scrum.md")
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Read existing team file content, if it exists
    existing_team_summary = ""
    if os.path.exists(team_filename):
        with open(team_filename, "r") as team_file:
            existing_team_summary = team_file.read()

    # Generate the response using OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a scrum summary update bot."},
            {"role": "user", "content": f"Project scrum information: {project_scrum}. Individual contribution: {individual_scrum}."},
            {"role": "user", "content": f"""
                Update the team document to include:
                - Individual contributions: {individual_scrum}.
                - Existing team weekly summary (if any): {existing_team_summary}.
                - A consolidated weekly summary of all contributions and project progress.
                Ensure the format is structured and easy to read.
            """}
        ]
    )

    # Extract the generated content
    consolidated_summary = response['choices'][0]['message']['content']

    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Update the individual document
    if os.path.exists(individual_filename):
        with open(individual_filename, "a") as individual_file:
            individual_file.write(f"\n# Update for {current_date}\n\n{individual_scrum}\n")
    else:
        with open(individual_filename, "w") as individual_file:
            individual_file.write(f"# {individual_name}'s Scrum Updates\n\n")
            individual_file.write(f"# Update for {current_date}\n\n{individual_scrum}\n")

    # Add a weekly summary to the individual file if it's the end of the week
    if datetime.now().weekday() == 6:  # Sunday is the last day of the week
        with open(individual_filename, "a") as individual_file:
            individual_file.write(f"\n# Weekly Summary (Ending {current_date})\n\n{consolidated_summary}\n")

    # Update the team document
    if os.path.exists(team_filename):
        with open(team_filename, "r") as team_file:
            team_content = team_file.read()

        # Check for an existing summary for the current week and replace or append
        date_pattern = rf"## Weekly Summary Update \(as of {current_date}\).*?---"
        if re.search(date_pattern, team_content, flags=re.S):
            # Replace the existing summary
            updated_content = re.sub(
                date_pattern,
                f"## Weekly Summary Update (as of {current_date})\n\n{consolidated_summary}\n\n---",
                team_content,
                flags=re.S
            )
        else:
            # Append the new summary
            updated_content = (
                team_content
                + f"\n## Weekly Summary Update (as of {current_date})\n\n{consolidated_summary}\n\n---\n"
            )

        with open(team_filename, "w") as team_file:
            team_file.write(updated_content)
    else:
        # Create a new team file if it doesn't exist
        with open(team_filename, "w") as team_file:
            team_file.write(f"## Weekly Summary Update (as of {current_date})\n\n{consolidated_summary}\n\n---\n")

    print(f"Scrum summaries updated in {individual_filename} and {team_filename}")



if __name__ == "__main__":
    # Example data usage
    project_scrum = "Food Ordering App is moving forward with the integration of essential features like payment gateway and order tracking. The overall goal is to provide a seamless user experience for customers to order food online."
    individual_scrum = "Sherbin has completed the login and registration feature, which allows users to securely sign up and log in to the app. The feature has been tested and is ready for deployment."

    individual_scrum_adarsh = "Adarsh has successfully implemented the search functionality, enabling users to search for restaurants and menu items efficiently. This feature has been reviewed and approved for deployment."

    individual_scrum_husian ="""Husian has successfully implemented the payment gateway integration, allowing users to pay for orders using their credit card. This feature has been reviewed and approved for deployment."""

    update_scrum_summary(project_scrum, individual_scrum_adarsh, "adarsh")

    update_scrum_summary(project_scrum, individual_scrum, "sherbin")

    update_scrum_summary(project_scrum, individual_scrum_husian, "husian")

