
import os
import json
from agent import generate_action

# Define 10 diverse episodes (simplified mock data)
episodes = [
    {
        "goal": "Uninstall the Slack app",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Apps\"]",
            "- App: Apps\n- UI Elements: [\"Slack\"]",
            "- App: Slack\n- UI Elements: [\"Uninstall\"]"
        ],
        "ground_truth": ["CLICK(\"Apps\")", "CLICK(\"Slack\")", "CLICK(\"Uninstall\")"]
    },
    {
        "goal": "Open Wi-Fi settings",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Network\"]",
            "- App: Network\n- UI Elements: [\"Wi-Fi\"]"
        ],
        "ground_truth": ["CLICK(\"Network\")", "CLICK(\"Wi-Fi\")"]
    },
    {
        "goal": "Enable Airplane Mode",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Connections\"]",
            "- App: Connections\n- UI Elements: [\"Airplane Mode\"]"
        ],
        "ground_truth": ["CLICK(\"Connections\")", "CLICK(\"Airplane Mode\")"]
    },
    {
        "goal": "Turn on Bluetooth",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Connections\"]",
            "- App: Connections\n- UI Elements: [\"Bluetooth\"]",
            "- App: Bluetooth\n- UI Elements: [\"On\"]"
        ],
        "ground_truth": ["CLICK(\"Connections\")", "CLICK(\"Bluetooth\")", "CLICK(\"On\")"]
    },
    {
        "goal": "Enable Dark Mode",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Display\"]",
            "- App: Display\n- UI Elements: [\"Dark Mode\"]"
        ],
        "ground_truth": ["CLICK(\"Display\")", "CLICK(\"Dark Mode\")"]
    },
    {
        "goal": "View Battery Usage",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Battery\"]",
            "- App: Battery\n- UI Elements: [\"Usage Details\"]"
        ],
        "ground_truth": ["CLICK(\"Battery\")", "CLICK(\"Usage Details\")"]
    },
    {
        "goal": "Change Wallpaper",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Display\"]",
            "- App: Display\n- UI Elements: [\"Wallpaper\"]"
        ],
        "ground_truth": ["CLICK(\"Display\")", "CLICK(\"Wallpaper\")"]
    },
    {
        "goal": "Check Storage",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Storage\"]"
        ],
        "ground_truth": ["CLICK(\"Storage\")"]
    },
    {
        "goal": "Enable Do Not Disturb",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Notifications\"]",
            "- App: Notifications\n- UI Elements: [\"Do Not Disturb\"]"
        ],
        "ground_truth": ["CLICK(\"Notifications\")", "CLICK(\"Do Not Disturb\")"]
    },
    {
        "goal": "Access Location Settings",
        "observations": [
            "- App: Settings\n- UI Elements: [\"Privacy\"]",
            "- App: Privacy\n- UI Elements: [\"Location\"]"
        ],
        "ground_truth": ["CLICK(\"Privacy\")", "CLICK(\"Location\")"]
    }
]

total_steps = 0
correct_steps = 0
successful_episodes = 0
all_logs = []
failures = []

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
            failures.append({
                "episode": ep_index,
                "goal": episode["goal"],
                "step": i+1,
                "observation": obs,
                "prediction": pred,
                "truth": truth,
                "reasoning": reasoning
            })
        print(f"Step {i+1} - Correct: {is_correct}")
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

# Save logs and failures
os.makedirs("results", exist_ok=True)
with open("results/eval_10episodes.json", "w") as f:
    json.dump(all_logs, f, indent=2)
with open("results/failures.json", "w") as f:
    json.dump(failures, f, indent=2)

# Summary
print(f"\nStep Accuracy: {correct_steps}/{total_steps} ({correct_steps / total_steps:.2%})")
print(f"Episode Success Rate: {successful_episodes}/{len(episodes)} ({successful_episodes / len(episodes):.2%})")
if failures:
    print(f"\nFailure Analysis ({len(failures)} issues):")
    for f in failures:
        print(f"- Episode {f['episode']} | Step {f['step']} | Mismatch: {f['predicted']} ≠ {f['truth']}")
        print(f"  Reasoning: {f['reasoning']}")
