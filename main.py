import openai
import json
import re
from dotenv import load_dotenv
import os
import difflib
from template import SCRUM_PROMPT, load_team_document
from deepdiff import DeepDiff

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
            ],
            temperature=0.2
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
        if scrum_update is None:
            print("Failed to extract or parse JSON.")
            return

        # Save team document
        team_document_path = os.path.join(folder_path, "team_document.md")
        if os.path.exists(team_document_path):
            with open(team_document_path, 'r') as file:
                content = file.read()

        with open(team_document_path, "w") as file:
            output_path = "changes.json"
            compare_texts_and_save(content, scrum_update["team_document"], output_path)
            file.write(scrum_update["team_document"])
        print(f"Team document saved as '{team_document_path}'")

        # Save individual documents
        individual_name = scrum_update["name"]
        individual_document_path = os.path.join(folder_path, f"{individual_name}.md")
        with open(individual_document_path, "a") as file:
            file.write("\n\n\n".join(scrum_update["individual_documents"]))

    except Exception as e:
        print(f"Error saving documents: {e}")


def compare_texts_and_save(text1, text2, output_path):
    # Split the texts into lines
    text1_lines = text1.splitlines()
    text2_lines = text2.splitlines()

    # Compare the two texts
    diff = list(difflib.unified_diff(text1_lines, text2_lines, lineterm=''))

    # Extract changes
    changes = []
    for line in diff:
        if line.startswith('+ ') or line.startswith('- '):
            changes.append(line)

    # Count number of changed lines
    num_changes = len(changes)

    # Prepare the result as a dictionary
    result = {
        "changes": changes,
        "num_lines_changed": num_changes
    }

    # Save the result to a JSON file
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)

    return result

# main function
def main():

    scrum_update_json = get_scrum_update()
    # Save the documents locally
    save_documents(scrum_update_json)


if __name__ == "__main__":
    main()