import requests
import json
import sys

# Define your Ollama API endpoint
OLLAMA_API_URL = 'http://localhost:11434/api/chat'

def generate_rh_ansible_playbook(request):
    # Refined prompt to generate an Ansible playbook for Red Hat Linux only, without unnecessary introductory lines
    # Prepare the JSON payload
    prompt = (
        f"Generate an Ansible playbook in YAML format for Red Hat Linux (not Ubuntu) for the following task: "
        f"{request}. Provide only the playbook in YAML format. Ensure there are no additional text, comments, or explanations."
    )
    data = {
            "model": "llama3.2-vision:latest",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Send the request to Ollama API
    response = requests.post(
        OLLAMA_API_URL,
        headers={'Content-Type': 'application/json'},
        json=data,
        stream=True  # Stream the response to handle large data
    )

    # Initialize variable to accumulate the response content
    full_response = ""

    # Read the response line by line
    for line in response.iter_lines():
        if line:
            try:
                # Parse each line as a JSON object
                json_line = json.loads(line.decode('utf-8'))
                if 'message' in json_line:
                    # Append the content of the 'message' field to full_response
                    full_response += json_line['message']['content']
                if json_line.get('done', False):
                    # End of the response stream
                    break
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    # Split response into lines, remove the "```yaml" line if it exists
    lines = full_response.splitlines()
    cleaned_lines = [line for line in lines if line.strip() != '```yaml']

    return '\n'.join(cleaned_lines).strip() + '\n'

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py '<request>'")
        sys.exit(1)

    # Read user request from command-line argument
    user_request = sys.argv[1]

    # Generate the Red Hat Ansible playbook
    playbook_output = generate_rh_ansible_playbook(user_request)

    if playbook_output:
        # Write the playbook to a file named rh-playbook.yml
        with open('rh-playbook.yml', 'w') as playbook_file:
            playbook_file.write(playbook_output)

        # Print the playbook to the terminal
        print("Red Hat Ansible playbook:\n")
        print(playbook_output)
    else:
        print("Failed to generate Red Hat Ansible playbook.")

if __name__ == "__main__":
    main()
