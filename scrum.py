import openai
import os
from dotenv import load_dotenv
from datetime import datetime
import re

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



def generate_scrum_summary(project_scrum, individual_scrum, individual_name):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a scrum summary update bot."},
            {"role": "user", "content": f"You are given the project scrum information: {project_scrum}. Analyze the document properly."},
            {"role": "user", "content": f"Scrum summary of individual: {individual_scrum}"},
            {"role": "user", "content": """
                Please provide the scrum summaries in the following strict format:

                Weekly Summary:
                - Start with the overall project progress.
                - Include notable achievements this week.
                - Outline the next steps for the project.

                Daily Summary for Individual:
                - Start with the tasks completed by the individual.
                - Include the review status of tasks.
                - Mention any challenges faced.
                - Outline next steps for the individual.

                Please ensure the format is consistent with the labels "Weekly Summary:" and "Daily Summary:" for easy extraction.
            """
             }
        ]
    )
    content = response['choices'][0]['message']['content']
    print(content)

    content = content.strip()

    # Regex pattern to capture Weekly Summary and Daily Summary
    weekly_pattern = re.compile(r"Weekly Summary[:\-]?\s*(.*?)(?=Daily Summary|$)", re.S)
    daily_pattern = re.compile(r"Daily Summary[^\n]*[:\-]?\s*(.*)", re.S)

    # Extract Weekly Summary
    weekly_match = weekly_pattern.search(content)
    if weekly_match:
        weekly_summary = weekly_match.group(1).strip()
    else:
        print("Error: Weekly Summary not found in response.")
        return

    # Extract Daily Summary
    daily_match = daily_pattern.search(content)
    if daily_match:
        daily_summary = daily_match.group(1).strip()
    else:
        print("Error: Daily Summary not found in response.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create a folder named 'scrum_summaries' if it doesn't exist
    folder_name = "scrum_summaries"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save individual markdown file with the name of the individual
    individual_filename = os.path.join(folder_name, f"{individual_name}.md")
    with open(individual_filename, "w") as individual_file:
        individual_file.write(f"# {individual_name}'s Daily Scrum Summary\n\n{daily_summary}")

    # Create the team document (this will contain the weekly summary)
    team_filename = os.path.join(folder_name, "team_scrum.md")
    # with open(team_filename, "a") as team_file:  # Open with 'a' to append summaries
    #     team_file.write(f"# Team Scrum Progress by - {individual_filename}\n\n{weekly_summary}\n\n---\n")

    print(f"Scrum summaries saved as {individual_filename} and {team_filename}")

def update_scrum_summary(project_scrum, individual_scrum, individual_name):
    folder_name = "scrum_summaries"
    individual_filename = os.path.join(folder_name, f"{individual_name}.md")
    team_filename = os.path.join(folder_name, "team_scrum.md")

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
                - Individual contributions: {individual_filename}.
                - Existing team weekly summary (if any): {existing_team_summary}.
                - A consolidated weekly summary of all contributions and project progress.
                Ensure the format is structured and easy to read.
            """}
        ]
    )

    # Extract the generated content
    content = response['choices'][0]['message']['content']

    # Ensure the folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Update the individual's markdown file
    if os.path.exists(individual_filename):
        with open(individual_filename, "a") as individual_file:
            individual_file.write(f"\n# Update for {datetime.now().strftime('%Y-%m-%d')}\n\n{individual_scrum}\n")
    else:
        with open(individual_filename, "w") as individual_file:
            individual_file.write(f"# {individual_name}'s Daily Scrum Summary\n\n{individual_scrum}\n")

    # Update the team markdown file
    if os.path.exists(team_filename):
        with open(team_filename, "a") as team_file:
            team_file.write(f"## Weekly Summary Update (as of {datetime.now().strftime('%Y-%m-%d')})\n\n{content}\n\n---\n")
    else:
        with open(team_filename, "w") as team_file:
            team_file.write(f"## Weekly Summary Update (as of {datetime.now().strftime('%Y-%m-%d')})\n\n{content}\n\n---\n")

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

