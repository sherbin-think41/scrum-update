sample_formats = {
    "individual": [
        "Name: Name of the individual",
        "Date: Date of the update",
        "Plan for Today: What the individual plans to work on today",
        "Yesterday: Tasks the individual completed yesterday",
        "Blockers: Any blockers faced by the individual",
        "Next Steps: Next steps planned by the individual",
        "Weekly Summary: Summary of the individual’s contributions for the week"
    ],
    "team": [
        # "Individuals Contributions: give the summary of what each individual is worked on",
        "Accomplishments: What the team achieved yesterday or recently",
        "Next Steps: Next steps for the team",
        "Weekly Summary: Summary of the team's progress and contributions for the week .make it around 500 words and give the response in keypoints"
    ]
}

def load_team_document(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found. Please check the file path."
    except Exception as e:
        return f"An error occurred: {e}"

file_path_team = "documents/team_document.md"
file_path_individual=""
team_docs = load_team_document(file_path_team)
individual_docs = load_team_document(file_path_individual)

scrum_Summary = {
    "name": "John Doe",
    "date": "2025-01-27",
    "plan_for_today": "Complete the API integration and test edge cases.",
    "yesterday": "Worked on the database schema and resolved deployment issues.",
    "blockers": "Awaiting access to production API keys.",
    "next_steps": "Deploy the API integration and validate with QA.",

}
scrum_Summary2 = {
    "name": "Jane Smith",
    "date": "2025-01-28",
    "plan_for_today": "Finalize the frontend design for the dashboard and address feedback from the review meeting.",
    "yesterday": "Completed unit tests for the notification service and fixed bugs in the authentication module.",
    "blockers": "Pending clarification on dashboard requirements from the product team.",
    "next_steps": "Integrate the finalized dashboard design with backend APIs and test user workflows.",

}
scrum_Summary3 = {
    "name": "Leo",
    "date": "2025-01-29",
    "plan_for_today": "planing to create a payment system for the dashboard.",
    "yesterday": "completed unit tests for the notification service and fixed bugs in the authentication module.",
    "blockers": "No blocks",
    "next_steps": "integrate testing with payment system and test user workflows.",

}

SCRUM_PROMPT = f"""
    You are a scrum summary update bot. You are given a {scrum_Summary3}. Based on the scrum summary, your responsibilities are as follows:
    1. Update two sets of documents:
       - Individual Documents ({individual_docs}): This should include daily updates of individual. 
         - A day-wise summary of what each individual is working on.
         - A weekly summary at the end, summarizing the work done by each individual throughout the week.

       - Team Documents ({team_docs}): This should include:
         - A detailed update on the team's progress use individual contributions to make the update.
         - Every task or project milestone and individual contributions should be noted, ensuring nothing is missed.
         - A detailed weekly summary of the work done by each team member, providing a clear overview of the tasks.
         - **Ensure that the team document includes the contributions of all individuals, including those added previously**. When updating the team document, do not remove any existing other contents ,this should be strictly avoided.

    2. Provide the following in your response:
       - The **number of lines** updated in each document.
       - Details of **what changes were made** to each document.

    3. Ensure all edits adhere to the specified format:
       - Use the provided {sample_formats} for content editing.
       - Submit the edited documents in **Markdown format**.

    4. Output the following in **JSON format**:
        - Provide the name of individual **name**.
        - Provide the **team document** and **individual documents** in Markdown format.
        - Include the **number of lines** updated and **changes made** for each document.

    Ensure response includes:
    - "team_document": The team document in Markdown format, preserving all previous individual contributions.
    - "individual_documents": A list of individual documents in Markdown format.
    - "changes": A detailed list of changes made in JSON format, with the number of lines and what was altered in each document.
"""

