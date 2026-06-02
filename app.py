from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parent / "example-data" / "rider_sessions.csv"

CONFIDENCE_COLOURS = {"HIGH": "green", "MEDIUM": "orange", "LOW": "red"}


@st.cache_data
def load_sessions() -> pd.DataFrame:
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        df["session_date"] = pd.to_datetime(df["session_date"])
        return df
    return pd.DataFrame(
        [
            {
                "rider_name": "Demo rider",
                "session_date": "2026-05-08",
                "subject_type": "rider",
                "test_types": "pct,flexchair",
                "pct_v_sit_cm": 42,
                "pct_wall_sit_asym_pct": 6.0,
                "flexchair_total_score": 68,
                "flexchair_unbalanced_pct": 15,
                "mental_activation_score": None,
                "mental_stress_score": None,
                "confidence_level": "MEDIUM",
                "recommendation": "Example recommendation — replace with real data.",
            }
        ]
    )


st.set_page_config(page_title="EquInnoLab — Prestatiesport Portal", layout="wide")

sessions = load_sessions()

st.title("Prestatiesport Portal")
st.caption("EquInnoLab · Phase 2 functional app scaffold — Report Generator")

left, right = st.columns([0.32, 0.68], gap="large")

with left:
    riders = sorted(sessions["rider_name"].unique().tolist())
    selected_rider = st.selectbox("Rider", riders)

    rider_sessions = sessions[sessions["rider_name"] == selected_rider].sort_values(
        "session_date", ascending=False
    )

    session_labels = rider_sessions["session_date"].dt.strftime("%d %b %Y") + " · " + rider_sessions["subject_type"]
    selected_label = st.selectbox("Analysis session", session_labels.tolist())

    selected_idx = session_labels.tolist().index(selected_label)
    row = rider_sessions.iloc[selected_idx]

    emphasis = st.radio(
        "Report emphasis",
        ["Practical next step", "Evidence first", "Welfare & flags"],
    )

    extra_context = st.text_area(
        "Extra context",
        value="Focus on readiness for the upcoming competition block.",
        height=100,
    )

    generate = st.button("Generate draft report", type="primary")

with right:
    st.subheader(row["rider_name"])

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Session date", row["session_date"].strftime("%d %b %Y"))
    col_b.metric("Subject type", str(row["subject_type"]).capitalize())
    col_c.metric(
        "Confidence",
        str(row["confidence_level"]) if pd.notna(row["confidence_level"]) else "—",
    )

    st.markdown("#### Test types included")
    test_types = [t.strip() for t in str(row["test_types"]).split(",")]
    st.write("  ·  ".join(f"`{t}`" for t in test_types))

    st.markdown("#### Visible evidence")

    evidence_items = []

    if pd.notna(row.get("pct_v_sit_cm")):
        evidence_items.append(
            f"**Physical Capacity (pct)** — V-sit: {row['pct_v_sit_cm']} cm · Wall-sit asymmetry: {row['pct_wall_sit_asym_pct']}%"
        )
    if pd.notna(row.get("flexchair_total_score")):
        evidence_items.append(
            f"**Flexchair balance** — Total score: {row['flexchair_total_score']} / 100 · Unbalanced: {row['flexchair_unbalanced_pct']}%"
        )
    if pd.notna(row.get("mental_activation_score")):
        evidence_items.append(
            f"**Mental Readiness (OMSAT-3)** — Activation: {row['mental_activation_score']} · Stress reaction: {row['mental_stress_score']}"
        )
    if not evidence_items:
        evidence_items = ["No structured metrics available for this session in the example data."]

    for item in evidence_items:
        st.markdown(f"- {item}")

    if generate:
        st.markdown("#### Draft report output")

        conf = str(row["confidence_level"]) if pd.notna(row["confidence_level"]) else "MEDIUM"
        colour = CONFIDENCE_COLOURS.get(conf, "grey")
        st.markdown(f"Confidence: :{colour}[**{conf}**]")

        if conf == "LOW":
            st.warning(
                "LOW confidence — not enough data for trend claims. "
                "Review this section before publishing.",
                icon="⚠️",
            )

        if emphasis == "Welfare & flags" and "lactate" in str(row["test_types"]):
            st.error(
                "**Welfare flag (P-01):** Lactate value in this session exceeded "
                "4.0 mmol/L. Review horse recovery data before presenting "
                "performance insights.",
                icon="🚨",
            )

        if emphasis == "Evidence first":
            st.markdown("**Based on the evidence above:**")
        elif emphasis == "Welfare & flags":
            st.markdown("**Welfare and data quality flags first:**")
        else:
            st.markdown("**Recommended next step:**")

        rec = str(row["recommendation"]) if pd.notna(row["recommendation"]) else "No recommendation available."
        st.info(rec)

        if extra_context.strip():
            st.caption(f"Extra context included: {extra_context.strip()}")

        st.markdown("---")
        st.markdown(
            "**Review gate (P-02):** In the full portal, a sport scientist must "
            "approve and publish this report before the coach can see it."
        )
    else:
        st.markdown("#### Draft report output")
        st.write("Select a session and generate a draft report.")

    st.markdown("#### Feedback")
    feedback = st.radio(
        "Was this report output useful for a first review?",
        ["Not answered", "Yes", "Partly", "No"],
        horizontal=True,
    )
    notes = st.text_input("Feedback notes")

    if feedback != "Not answered" or notes:
        st.success("Feedback captured locally for the demo flow.")
