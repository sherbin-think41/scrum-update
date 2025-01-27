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
        "Date: Date of the update",
        "Plan for Today: What the team plans to achieve today",
        "Accomplishments: What the team achieved yesterday or recently",
        "Next Steps: Next steps for the team",
        "Weekly Summary: Summary of the team's progress and contributions for the week"
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
file_path_individual="documents/individual_document.md"
team_docs = load_team_document(file_path_team)
individual_docs = load_team_document(file_path_individual)

scrum_Summary = {
    "name": "John Doe",
    "date": "2025-01-27",
    "plan_for_today": "Complete the API integration and test edge cases.",
    "yesterday": "Worked on the database schema and resolved deployment issues.",
    "blockers": "Awaiting access to production API keys.",
    "next_steps": "Deploy the API integration and validate with QA.",
    "weekly_summary": "Resolved critical database issues, completed UI improvements, and started API integration."
}


scrum_Summary2 = {
    "name": "Jane Smith",
    "date": "2025-01-28",
    "plan_for_today": "Finalize the frontend design for the dashboard and address feedback from the review meeting.",
    "yesterday": "Completed unit tests for the notification service and fixed bugs in the authentication module.",
    "blockers": "Pending clarification on dashboard requirements from the product team.",
    "next_steps": "Integrate the finalized dashboard design with backend APIs and test user workflows.",
    "weekly_summary": "Improved test coverage for critical modules, fixed high-priority bugs, and made progress on dashboard development."
}


SCRUM_PROMPT = f"""
    You are a scrum summary update bot. You are given a {scrum_Summary2}. Based on the scrum summary, your responsibilities are as follows:
    
    1. Update two sets of documents:
       - Individual Documents ({individual_docs}): This should include daily updates for each individual Each update should have:
         - A day-wise summary of what each individual is working on.
         - A weekly summary at the end, summarizing the work done by each individual throughout the week.
    
       - Team Documents ({team_docs}): This should include:
         - A weekly summary of the work done by each team member.
         - A detailed update on the team's progress, blockers, and any overall feedback.
    
    2. Provide the following in your response:
       - The **number of lines** updated in each document.
       - Details of **what changes were made** to each document.
    
    3. Ensure all edits adhere to the specified format:
       - Use the provided {sample_formats} for content editing.
       - Submit the edited documents in **Markdown format**.
       - Store the documents in your system as text files.
    
    4. Output the following in **JSON format**:
       - Provide the **team document** and **individual documents** in Markdown format.
       - Include the **number of lines** updated and **changes made** for each document.
    
    Ensure response includes:
    - "team_document": The team document in Markdown format.
    - "individual_documents": A list of individual documents in Markdown format.
    - "changes": A detailed list of changes made in JSON format, with the number of lines and what was altered in each document.

"""

