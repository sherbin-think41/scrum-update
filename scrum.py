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

    # Check for existing individual contributions in the team document
    individual_contributions = ""
    individual_section_pattern = rf"{individual_name}:\n(.*?)(?=\n[A-Z]|$)"
    match = re.search(individual_section_pattern, existing_team_summary, re.DOTALL)
    if match:
        individual_contributions = match.group(1).strip()

    # Generate the response using OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a scrum summary update bot."},
            {"role": "user", "content": f"Project scrum information: {project_scrum}."},
            {
                "role": "user",
                "content": f"""
                Update the team document with the following:
                - Include all individual contributions to date for {individual_name}.
                - Individual contributions should include: 
                  - Existing contributions: {individual_contributions}.
                  - New contribution: {individual_scrum}.
                - Ensure the overall team summary integrates:
                  - Project overview: {project_scrum}.
                  - Existing team summary: {existing_team_summary}.
                  - Consolidated weekly progress.
                - Preserve the structure: 
                  - Individual contributions listed under respective names.
                  - A cohesive consolidated summary at the end.
                """
            }
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
    with open(team_filename, "w") as team_file:
        team_file.write(f"## Weekly Summary Update (as of {current_date})\n\n{consolidated_summary}\n\n---\n")

    print(f"Scrum summaries updated in {individual_filename} and {team_filename}")


if __name__ == "__main__":
    # Example data usage
    project_scrum = "Food Ordering App is moving forward with the integration of essential features like payment gateway and order tracking. The overall goal is to provide a seamless user experience for customers to order food online."

    individual_scrum_adarsh = "Adarsh has successfully implemented the search functionality, enabling users to search for restaurants and menu items efficiently. This feature has been reviewed and approved for deployment."

    individual_scrum_husian = "Husian has successfully implemented the payment gateway integration, allowing users to pay for orders using their credit card. This feature has been reviewed and approved for deployment."

    individual_scrum_sherbin_1 = "Sherbin has completed the login and registration feature, which allows users to securely sign up and log in to the app. The feature has been tested and is ready for deployment."
    individual_scrum_sherbin_2 = "Sherbin has successfully implemented the order tracking feature, enabling users to track their orders and view their order history. This feature has been reviewed and approved for deployment."

    update_scrum_summary(project_scrum, individual_scrum_adarsh, "adarsh")
    update_scrum_summary(project_scrum, individual_scrum_husian, "husian")
    update_scrum_summary(project_scrum, individual_scrum_sherbin_1, "sherbin")
    update_scrum_summary(project_scrum, individual_scrum_sherbin_2, "sherbin")
