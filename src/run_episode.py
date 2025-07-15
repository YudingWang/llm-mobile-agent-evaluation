
# pip install openai streamlit langchain pydantic fuzzywuzzy

import os
import json
from agent import generate_action

episode = {
    "goal": "Uninstall the Slack app",
    "observations": [
        "- App: Settings\n- UI Elements: [\"Apps\", \"Search\", \"Battery\"]",
        "- App: Apps\n- UI Elements: [\"Slack\", \"Zoom\"]",
        "- App: Slack\n- UI Elements: [\"Uninstall\"]"
    ],
    "ground_truth": ["CLICK(\"Apps\")", "CLICK(\"Slack\")", "CLICK(\"Uninstall\")"]
}

log = {
    "goal": episode["goal"],
    "steps": []
}

print("Goal:", episode["goal"])
for i, obs in enumerate(episode["observations"]):
    print(f"\nStep {i+1} Observation:")
    print(obs)
    action, reasoning = generate_action(episode["goal"], obs)
    print("Predicted Action:", action)
    print("Reasoning:", reasoning)

    step = {
        "observation": obs,
        "predicted": action,
        "truth": episode["ground_truth"][i],
        "reasoning": reasoning
    }
    log["steps"].append(step)

os.makedirs("results", exist_ok=True)
with open("results/episode_01.json", "w") as f:
    json.dump([log], f, indent=2)
print("\nSaved log with reasoning to results/episode_01.json")
