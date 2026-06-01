from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = (
    Path(__file__).resolve().parent / "example-data" / "workshop_scenarios.csv"
)


@st.cache_data
def load_scenarios() -> pd.DataFrame:
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    return pd.DataFrame(
        [
            {
                "title": "Fallback Prototype Scenario",
                "audience": "Workshop participant",
                "problem": "Turn an idea into a testable prototype",
                "example_input": "A broad idea needs one concrete user journey.",
                "evidence_1": "The user has a real idea.",
                "evidence_2": "The prototype needs safe example data.",
                "evidence_3": "Feedback should guide the next iteration.",
                "recommendation": "Start with one clickable journey before adding integrations.",
                "next_step": "Show the prototype to one tester and capture feedback.",
            }
        ]
    )


st.set_page_config(page_title="AI Lab Rapid Prototype", layout="wide")

scenarios = load_scenarios()

st.title("AI Lab Rapid Prototype")
st.caption("Phase 2 functional app scaffold")

left, right = st.columns([0.34, 0.66], gap="large")

with left:
    selected_title = st.selectbox("Scenario", scenarios["title"].tolist())
    selected = scenarios.loc[scenarios["title"] == selected_title].iloc[0]

    emphasis = st.radio(
        "Output emphasis",
        ["Practical next step", "Evidence first", "User feedback"],
    )

    user_context = st.text_area(
        "Extra context",
        value=str(selected["example_input"]),
        height=150,
    )

    generate = st.button("Generate prototype output", type="primary")

with right:
    st.subheader(selected["title"])
    st.write(f"Audience: {selected['audience']}")
    st.write(f"Problem: {selected['problem']}")

    evidence = [
        selected["evidence_1"],
        selected["evidence_2"],
        selected["evidence_3"],
    ]

    st.markdown("#### Visible context / evidence")
    for item in evidence:
        st.write(f"- {item}")

    if generate:
        st.markdown("#### Draft output")
        if emphasis == "Evidence first":
            st.write("Based on the evidence above:")
        elif emphasis == "User feedback":
            st.write("For a feedback-focused test:")
        else:
            st.write("Recommended next move:")

        st.info(selected["recommendation"])
        st.write(f"Next step: {selected['next_step']}")
        st.write(f"Included context: {user_context}")
    else:
        st.markdown("#### Draft output")
        st.write("Choose a scenario and generate a draft output.")

    st.markdown("#### Feedback placeholder")
    feedback = st.radio(
        "Was this useful for a first prototype test?",
        ["Not answered", "Yes", "Partly", "No"],
        horizontal=True,
    )
    notes = st.text_input("Feedback notes")

    if feedback != "Not answered" or notes:
        st.success("Feedback captured locally for the demo flow.")
