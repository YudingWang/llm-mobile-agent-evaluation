
import os
import json
from agent import generate_action

# Define multiple test episodes
episodes = [
    {
        "goal": "Uninstall the Slack app",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Apps\", \"Search\", \"Battery\"]",
            "- App: Apps\n- UI Elements: [\"Slack\", \"Zoom\"]",
            "- App: Slack\n- UI Elements: [\"Uninstall\"]"
        ],
        "ground_truth": ["CLICK(\"Apps\")", "CLICK(\"Slack\")", "CLICK(\"Uninstall\")"]
    },
    {
        "goal": "Open Wi-Fi settings",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Network\", \"Wi-Fi\", \"Display\"]",
            "- App: Network\n- UI Elements: [\"Wi-Fi\"]"
        ],
        "ground_truth": ["CLICK(\"Network\")", "CLICK(\"Wi-Fi\")"]
    },
    {
        "goal": "Enable Airplane Mode",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Connections\", \"Display\"]",
            "- App: Connections\n- UI Elements: [\"Airplane Mode\"]"
        ],
        "ground_truth": ["CLICK(\"Connections\")", "CLICK(\"Airplane Mode\")"]
    }
]

total_steps = 0
correct_steps = 0
successful_episodes = 0
all_logs = []

for ep_index, episode in enumerate(episodes, start=1):
    log = {
        "goal": episode["goal"],
        "steps": []
    }
    success = True
    print(f"\nEpisode {ep_index}: {episode['goal']}")
    for i, obs in enumerate(episode["observations"]):
        pred, reasoning = generate_action(episode["goal"], obs)
        truth = episode["ground_truth"][i]
        is_correct = pred.strip() == truth.strip()
        total_steps += 1
        correct_steps += int(is_correct)
        if not is_correct:
            success = False
        print(f"\nStep {i+1}")
        print("Observation:", obs)
        print("Prediction:", pred)
        print("Ground Truth:", truth)
        print("Correct:", is_correct)

        log["steps"].append({
            "observation": obs,
            "predicted": pred,
            "truth": truth,
            "reasoning": reasoning,
            "correct": is_correct
        })
    if success:
        successful_episodes += 1
    all_logs.append(log)

# Write log file
os.makedirs("results", exist_ok=True)
with open("results/eval_log.json", "w") as f:
    json.dump(all_logs, f, indent=2)

# Summary
print(f"\nStep Accuracy: {correct_steps}/{total_steps} ({correct_steps / total_steps:.2%})")
print(f"Episode Success Rate: {successful_episodes}/{len(episodes)} ({successful_episodes / len(episodes):.2%})")
