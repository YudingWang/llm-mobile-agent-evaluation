# LLM Mobile Agent Evaluation

This project provides a lightweight framework for evaluating large language models (LLMs) as agents that interact with simulated Android-like user interfaces to complete mobile tasks. It benchmarks an LLM's ability to reason over UI observations and take correct action sequences to reach a defined goal.

## Features

- Action-based agent framework using structured prompts
- Supports zero-shot, reasoning-based, and few-shot prompting
- Evaluation pipeline for accuracy and success rate
- Streamlit-based log viewer for visual analysis
- Generates per-episode prediction logs in JSON

## Repository Structure

```
.
├── src/                          # Python logic and execution scripts
│   ├── agent.py                 # LLM interaction logic
│   ├── run_episode.py          # Run agent on one episode
│   ├── eval.py                 # Evaluate 3+ episodes
│   ├── eval_extended.py        # Run benchmark on 10 episodes
│   └── visualizer.py           # Streamlit visualization UI
├── prompts/                     # Prompt variants and templates
│   ├── prompt_template.txt
│   ├── prompt_with_reasoning.txt
│   └── few_shot_examples.txt
├── results/                     # Logs of predictions and comparisons
│   ├── episode_01.json
│   ├── eval_log.json
│   └── eval_10episodes.json
├── report.md                    # Performance analysis and recommendations
└── README.md                    # Project overview
```

## Getting Started

### 1. Install requirements

This project is compatible with Python 3.8+ and uses only standard libraries + Streamlit.

```bash
pip install streamlit
```

### 2. Run a single test case

```bash
python src/run_episode.py
```

### 3. Evaluate model performance

```bash
python src/eval.py             # Small test set
python src/eval_extended.py   # Full benchmark
```

### 4. Visualize predictions

```bash
streamlit run src/visualizer.py
```

Navigate to `http://localhost:8501`, then upload any `.json` file from `results/`.

## Prompt Strategies

- `prompt_template.txt`: Basic zero-shot instruction
- `prompt_with_reasoning.txt`: Adds action justification
- `few_shot_examples.txt`: Optional examples for in-context learning

## Output Format

Each episode is logged as a JSON file containing:

- Goal
- Observations per step
- Predicted and ground truth actions
- Correctness (boolean)
- Reasoning (if enabled)

These files can be visualized or used for metric reporting.

## Report

The file `report.md` summarizes:

- Step-level accuracy
- Episode success rate
- Failure cases
- Agent behavior patterns (hallucination, overgeneralization)
- Recommendations (UI validation, retries, memory)
