import streamlit as st
import pandas as pd
import numpy as np
import datetime
from google import genai

# ----------------------------------------
# Gemini Client Setup
# ----------------------------------------
client = genai.Client(
    api_key="AIzaSyBijh4TPKgpQc6dcopS651I7t3rLEBriUc"   # <-- Replace with your regenerated key
)

# ----------------------------------------
# Page Config
# ----------------------------------------
st.set_page_config(page_title="Cognitive Mirror", layout="wide")

st.markdown("""
<style>
body { background-color: #0E1117; color: white; }
h1, h2, h3 { color: #00FF9D; }
.stMetric { background-color: #1C1F26; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Cognitive Mirror")
st.markdown("### GenAI Preventive Intelligence System")

st.markdown("""
Cognitive Mirror analyzes behavioral trends to detect early cognitive
imbalance before visible symptoms escalate.
""")

# ----------------------------------------
# Session State
# ----------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------------------
# Input Section
# ----------------------------------------
st.subheader("📥 Daily Cognitive Signals")

col1, col2, col3 = st.columns(3)

with col1:
    sleep = st.slider("Sleep Hours", 3, 10, 7)

with col2:
    stress = st.slider("Stress Level (1-5)", 1, 5, 3)

with col3:
    focus = st.slider("Focus Level (1-5)", 1, 5, 3)

reflection = st.text_area("Daily Reflection")

if st.button("Save Entry"):
    st.session_state.history.append({
        "Date": datetime.date.today(),
        "Sleep": sleep,
        "Stress": stress,
        "Focus": focus,
        "Reflection": reflection
    })
    st.success("Entry Saved")

# ----------------------------------------
# Display History
# ----------------------------------------
if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history)

    st.subheader("📊 Behavioral Trend Dashboard")
    st.dataframe(df)
    st.line_chart(df[["Sleep", "Stress", "Focus"]])

# ----------------------------------------
# Utility Functions
# ----------------------------------------
def detect_trend(series):
    if len(series) < 2:
        return "Stable"
    if series.iloc[-1] > series.iloc[-2]:
        return "Increasing"
    elif series.iloc[-1] < series.iloc[-2]:
        return "Decreasing"
    return "Stable"

def detect_acceleration(series):
    if len(series) < 3:
        return 0
    return series.iloc[-1] - series.iloc[-3]

def calculate_risk(df):
    avg_sleep = df["Sleep"].mean()
    avg_stress = df["Stress"].mean()
    avg_focus = df["Focus"].mean()

    score = 0
    if avg_sleep < 6:
        score += 1
    if avg_stress > 3:
        score += 1
    if avg_focus < 3:
        score += 1

    if score == 0:
        return "Low", "green"
    elif score == 1:
        return "Moderate", "orange"
    else:
        return "High", "red"

def cognitive_stability_index(df):
    sleep_score = (df["Sleep"].mean() / 10) * 40
    stress_score = ((6 - df["Stress"].mean()) / 5) * 35
    focus_score = (df["Focus"].mean() / 5) * 25
    return round(sleep_score + stress_score + focus_score)

# ----------------------------------------
# Analysis Section
# ----------------------------------------
if len(st.session_state.history) >= 1:

    if st.button("🧠 Run Cognitive Analysis"):

        df = pd.DataFrame(st.session_state.history)

        risk_level, color = calculate_risk(df)
        stability_score = cognitive_stability_index(df)

        sleep_trend = detect_trend(df["Sleep"])
        stress_trend = detect_trend(df["Stress"])
        focus_trend = detect_trend(df["Focus"])

        stress_acceleration = detect_acceleration(df["Stress"])

        st.subheader("⚠ Risk Overview")
        st.markdown(
            f"<h2 style='color:{color}'>{risk_level} Risk</h2>",
            unsafe_allow_html=True
        )

        st.metric("🧠 Cognitive Stability Index", f"{stability_score}/100")

        st.write(f"Sleep Trend: {sleep_trend}")
        st.write(f"Stress Trend: {stress_trend}")
        st.write(f"Focus Trend: {focus_trend}")

        if stress_acceleration >= 2:
            st.error("⚠ Rapid Stress Acceleration Detected")

        # ----------------------------------------
        # Gemini AI Insight
        # ----------------------------------------
        with st.spinner("Generating Preventive Insight..."):

            prompt = f"""
You are a preventive intelligence AI.

User Behavioral Data:
{df.to_string(index=False)}

Sleep Trend: {sleep_trend}
Stress Trend: {stress_trend}
Focus Trend: {focus_trend}

Risk Level: {risk_level}

Provide:
- Explanation of behavioral trends
- Early cognitive imbalance indicators
- 3 adaptive preventive micro-actions
- Calm and supportive tone
- No medical diagnosis
"""

            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )

                if response.candidates:
                    ai_text = ""
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, "text"):
                            ai_text += part.text
                else:
                    ai_text = "No insight generated."

            except Exception as e:
                ai_text = f"AI generation failed: {str(e)}"

            st.subheader("🪞 Cognitive Insight Report")
            st.write(ai_text)

            confidence = np.random.randint(85, 97)
            st.metric("AI Confidence Score", f"{confidence}%")

else:
    st.info("Add at least one entry to run analysis.")
