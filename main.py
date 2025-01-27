import openai
import json
import re
from dotenv import load_dotenv
import os
from template import SCRUM_PROMPT

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# function to generate scrum updates
def get_scrum_update():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use a suitable model
            messages=[
                {"role": "system", "content": "You are a scrum summary update bot."},
                {"role": "user", "content":  f" {SCRUM_PROMPT}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error analyzing reviews: {e}"


def extract_json_from_text(text):
    # Regular expression pattern to match the JSON-like content
    try:
        # Search for the JSON structure in the response
        json_match = re.search(r'```json\n(.*?)```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)  # Extract JSON part
            return json.loads(json_str)  # Parse the JSON
        else:
            raise ValueError("No JSON found in the response.")
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return None

# Save the docs locally
def save_documents(scrum_update_json, folder_path="documents"):
    try:
        # Ensure the folder exists
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Extract valid JSON from the raw text
        scrum_update = extract_json_from_text(scrum_update_json)
        print("Scrum Update:", scrum_update)
        if scrum_update is None:
            print("Failed to extract or parse JSON.")
            return

        # Save team document
        team_document_path = os.path.join(folder_path, "team_document.md")
        with open(team_document_path, "w") as file:
            file.write(scrum_update["team_document"])
        print(f"Team document saved as '{team_document_path}'")

        # Save individual documents
        individual_name = scrum_update["name"]
        individual_document_path = os.path.join(folder_path, f"{individual_name}.md")

        with open(individual_document_path, "w") as file:
            file.write("\n\n\n".join(scrum_update["individual_documents"]))

        # Optionally, save the changes log
        changes_path = os.path.join(folder_path, "changes.json")
        with open(changes_path, "w") as file:
            json.dump(scrum_update["changes"], file, indent=4)
        print(f"Changes saved as '{changes_path}'")

    except Exception as e:
        print(f"Error saving documents: {e}")

# main function
def main():
    scrum_update_json = get_scrum_update()


    # Save the documents locally
    save_documents(scrum_update_json)


if __name__ == "__main__":
    main()
