
import os
import re
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def load_prompt_template():
    with open("prompts/prompt_with_reasoning.txt") as f:
        return f.read()

def generate_action(goal, observation):
    prompt_template = load_prompt_template()
    prompt = prompt_template.format(goal=goal, observation=observation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message["content"].strip()

    # Extract Action and Reasoning using regex
    action_match = re.search(r'Action:\s*(CLICK\(.*?\))', content)
    reason_match = re.search(r'Reasoning:\s*(.*)', content)

    action = action_match.group(1).strip() if action_match else "UNKNOWN"
    reasoning = reason_match.group(1).strip() if reason_match else "N/A"
    return action, reasoning
