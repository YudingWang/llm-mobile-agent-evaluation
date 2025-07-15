
# LLM Agent Evaluation Report: Android World Benchmark

## Prompting and Evaluation Approach

To evaluate how well large language models (LLMs) can function as agents in mobile-like environments, I implemented a minimal agent loop using the `android_world` benchmark. I designed two prompt variants:

- Prompt A: Standard zero-shot format that directly asks for the next action in CLICK("...") syntax.
- Prompt B: A format that includes both the action and a brief one-sentence reasoning explaining the decision.

I also prepared a few-shot examples prompt for future extension or ablation testing. These variants allowed me to evaluate LLM behavior under different prompting strategies.

The evaluation loop compares model-generated actions against ground-truth labels using exact string match, and logs both correct/incorrect actions. Evaluation metrics include step-level accuracy and full-episode success rate. Logs were saved per episode and used for further analysis and visualization.

## Summary of Performance Metrics

I ran evaluations on two sets of episodes:

1. Initial 3-episode test:
   - Step Accuracy: 5/6 (83.33%)
   - Episode Success Rate: 2/3 (66.67%)
   - One episode failed due to an incorrect first-step action.
   - This set was used to validate the pipeline and debug action formatting and logic.

2. Full benchmark set (10 episodes):
   - Step Accuracy: 20/20 (100%)
   - Episode Success Rate: 10/10 (100%)
   - No observed failures in the full set.

## Failure Analysis (From Initial 3-Episode Test)

In the second episode ("Open Wi-Fi Settings"), the model predicted CLICK("Wi-Fi") directly from the first screen. The correct action was CLICK("Network").

Observation: "UI Elements": ["Network", "Wi-Fi", "Display"]
Prediction: CLICK("Wi-Fi")
Ground Truth: CLICK("Network")

This failure illustrates a critical point: LLMs may skip intermediate steps if the UI options appear similar to the goal label. It reinforces the need for strict grounding in current observations.

## Highlighted LLM Behaviors

Hallucinated Actions  
In the failed episode above, the model clicked a UI element that was technically present—but not actionable from the current context. Without additional UI state memory, the LLM assumed direct access.

Goal Misinterpretation  
There was no evidence of complete goal misunderstanding. All missteps were related to over-eager UI traversal rather than confusion about task objectives.

UI Reasoning Limitations  
While the model provided fluent and logically sound explanations, it lacked precision in validating whether its action candidates were currently valid. Reasoning quality is not a substitute for observation-grounded action validation.

## Illustrative Example Episodes

Episode: Enable Airplane Mode (Successful)
- Step 1: CLICK("Connections")
- Step 2: CLICK("Airplane Mode")
- Reasoning: "Airplane Mode is typically found under the Connections section."
- Outcome: Success

Episode: Uninstall Slack (Successful)
- Three correct steps: CLICK("Apps"), CLICK("Slack"), CLICK("Uninstall")
- The model followed standard UI logic accurately.

Episode: Open Wi-Fi Settings (Failure in initial test)
- Incorrect first step (CLICK("Wi-Fi")), bypassed required navigation through Network.

## Recommendations for Improving Agent Behavior

1. UI Element Validation is Critical  
   Before accepting a model’s output, it is essential to validate that the predicted action targets an element present in the current observation. This alone could have prevented the one failed episode.

2. Incorporate Memory or State History  
   Adding memory of previous actions could help the model avoid skipping steps or making duplicate decisions.

3. Allow for Retry Logic  
   If a predicted action refers to a non-existent UI element, implement a fallback that re-prompts the model or allows correction based on available context.

4. More Specific Prompt Conditioning  
   Conditioning the model to strictly act only on visible elements ("choose only from the UI elements shown") can help reduce over-assumptions.

5. Future Enhancements  
   Structured output (e.g., OpenAI function-calling format), visualization of UI progression, and model comparison (e.g., GPT-4, Claude) would provide deeper insight into agent reliability.

