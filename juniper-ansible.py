import requests
import json
import sys

# Define your Ollama API endpoint
OLLAMA_API_URL = 'http://localhost:11434/api/chat'

def generate_ansible_playbook(request):
    # Refined prompt to generate an Ansible playbook without unnecessary introductory lines
    prompt = (
        f"Generate an Ansible playbook in YAML format for the following task: "
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

    response = requests.post(
        OLLAMA_API_URL,
        headers={'Content-Type': 'application/json'},
        json=data,
        stream=True  # Stream the response to handle large data
    )

    full_response = ""

    for line in response.iter_lines():
        if line:
            try:
                json_line = json.loads(line.decode('utf-8'))
                if 'message' in json_line:
                    full_response += json_line['message']['content']
                if json_line.get('done', False):
                    break
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    lines = full_response.splitlines()
    cleaned_lines = [line for line in lines if not line.startswith('```')]
    return '\n'.join(cleaned_lines).strip() + '\n'

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py '<request>'")
        sys.exit(1)
    user_request = sys.argv[1]
    playbook_output = generate_ansible_playbook(user_request)

    if playbook_output:
        with open('playbook.yml', 'w') as playbook_file:
            playbook_file.write(playbook_output)
        print("Ansible playbook:\n")
        print(playbook_output.replace('```yml\n', '').replace('```', ''))
    else:
        print("Failed to generate Ansible playbook.")

if __name__ == "__main__":
    main()
