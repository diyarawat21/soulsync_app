import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Affirmations by mood
affirmations = {
    "Happy": [
        "Keep shining, your light is infectious!",
        "Your joy is a gift to the world.",
        "Your smile brightens someone’s day. 😊"
    ],
    "Anxious": [
        "Breathe. You are safe in this moment.",
        "It’s okay to pause. You’re doing your best.",
        "Let go. You are enough as you are."
    ],
    "Meh": [
        "Even slow days move you forward.",
        "Your presence matters more than your productivity.",
        "You are still growing, even when it’s quiet."
    ],
    "Sad": [
        "Your feelings are valid. This too shall pass.",
        "You’re not alone — be gentle with yourself.",
        "Tears are proof that you’re healing. 🌧️"
    ],
    "Inspired": [
        "Follow that spark — it’s your soul guiding you.",
        "You’re creating magic — one step at a time.",
        "Your vision is powerful — keep going. 🌟"
    ]
}

# Page setup
st.set_page_config(page_title="SoulSync | Daily Tracker", layout="centered")
st.title("🌸 SoulSync: Daily Emotion & Affirmation Tracker")
st.markdown("_Track how you feel, write it out, and receive a gentle healing affirmation._")

# Mood input
mood = st.selectbox("🌤️ How are you feeling today?", list(affirmations.keys()))
note = st.text_area("📝 Write a short note-to-self or journal entry:")

# Submit button
if st.button("💖 Submit"):
    if mood and note.strip():
        # Try to read last affirmation
        try:
            log = pd.read_csv("mood_log.csv", names=["Timestamp", "Mood", "Note", "Affirmation"])
            last_affirmation = log["Affirmation"].iloc[-1] if not log.empty else ""
        except:
            last_affirmation = ""

        # Avoid repeating the same affirmation
        choices = [a for a in affirmations[mood] if a != last_affirmation]
        affirmation = random.choice(choices) if choices else random.choice(affirmations[mood])

        # Show affirmation
        st.success(f"✨ Affirmation for you: *{affirmation}*")

        # Save entry to CSV
        entry = pd.DataFrame([[datetime.now(), mood, note, affirmation]],
                            columns=["Timestamp", "Mood", "Note", "Affirmation"])
        entry.to_csv("mood_log.csv", mode='a', header=False, index=False)

        st.toast("Saved to journal!", icon="📁")
    else:
        st.warning("Please select a mood and write something.")

# Show last 10 entries
with st.expander("📖 View Journal (Last 10 Entries)"):
    try:
        log = pd.read_csv("mood_log.csv", names=["Timestamp", "Mood", "Note", "Affirmation"])
        st.dataframe(log.tail(10))
    except FileNotFoundError:
        st.info("No journal entries yet.")
