
import streamlit as st
import json

st.set_page_config(page_title="QualGent Agent Visualization", layout="wide")

st.title("LLM Agent Episode Visualizer")

st.sidebar.header("Load Episode Log")
uploaded_file = st.sidebar.file_uploader("Upload a log file", type=["json", "txt"])

if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")
    episodes = []
    try:
        episodes = json.loads(raw_text)
    except Exception:
        st.error("Could not parse JSON. Make sure the format is correct.")

    if episodes:
        for i, ep in enumerate(episodes):
            st.markdown(f"### Episode {i+1}: {ep.get('goal', 'Unknown Goal')}")
            for step_id, step in enumerate(ep.get("steps", [])):
                with st.expander(f"Step {step_id+1}: Observation → Action"):
                    st.markdown(f"**Observation:** {step.get('observation')}")
                    st.markdown(f"**Predicted Action:** `{step.get('predicted')}`")
                    st.markdown(f"**Ground Truth:** `{step.get('truth')}`")
                    st.markdown(f"**Correct:** {'YES' if step.get('predicted') == step.get('truth') else 'NO'}")
                    if "reasoning" in step:
                        st.markdown(f"**Model Reasoning:** {step['reasoning']}")
