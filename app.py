import streamlit as st
import pandas as pd

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("🐱 Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping Logic | Honoring Kitty's Techniques")

def kgf_score_and_notes(horse_name, speed, stamina, odds, board_hit_rate=0.0, 
                       pedigree_note="", track_condition="dry"):
    score = 0
    notes = []

    score += (speed * 0.45)
    score += (stamina * 2.2)
    score += (board_hit_rate * 25)

    # === SMART HIGHLIGHTS FOR BOX BETS ===
    if board_hit_rate >= 0.65:
        notes.append("✅ Consistent Board Hitter (Strong for boxes)")
    if odds >= 12 and board_hit_rate >= 0.55:
        notes.append("🔥 High Odds + Board Threat (Great exotic value)")
    if speed >= 100:
        notes.append("⚡ High Speed Figure")
    if stamina >= 8:
        notes.append("🏃 Strong Stamina / Distance Fit")
    if any(x in pedigree_note.lower() for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown"]):
        notes.append("👑 Triple Crown / Elite Pedigree")
    if odds >= 20 and board_hit_rate >= 0.60:
        notes.append("💎 Mystery High Odds Contender (Hidden Gem)")
    if track_condition == "wet" and "mud" in pedigree_note.lower():
        notes.append("🌧 Wet Track Specialist")

    # Final Ocelli / Top-5 Liker
    top5_liker = odds >= 10 and board_hit_rate >= 0.50
    if top5_liker:
        notes.append("⭐ Top-5 Liker / Ocelli Signal")

    return round(score, 1), top5_liker, notes

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Pick 5 Builder", "🏇 Race Card Predictions"])

with tab3:
    st.subheader("🏇 Race Card Predictions")

    tracks = ["Santa Anita", "Laurel Park", "Aqueduct", "Mountaineer", "Churchill Downs", "Gulfstream Park"]
    col1, col2, col3 = st.columns(3)
    with col1:
        track = st.selectbox("Track", tracks)
    with col2:
        date = st.date_input("Race Date", value="today")
    with col3:
        race_num = st.number_input("Race Number", 1, 14, 6)

    st.write(f"**{track} — Race {race_num} — {date}**")

    # Manual Table with enhanced columns
    default_data = pd.DataFrame({
        "PP": list(range(1, 11)),
        "Horse Name": [f"Horse {i}" for i in range(1, 11)],
        "Pedigree Note": [""] * 10,
        "Speed Figure": [85] * 10,
        "Stamina": [6] * 10,
        "Odds": [10.0] * 10,
        "Board Hit Rate": [0.6] * 10,
        "Track Condition": ["dry"] * 10
    })

    edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

    if st.button("🚀 Run KGF Predictions on Full Field"):
        results = []
        for _, row in edited_df.iterrows():
            name = row["Horse Name"]
            speed = row["Speed Figure"]
            stamina = row["Stamina"]
            odds = row["Odds"]
            board = row["Board Hit Rate"]
            ped = row["Pedigree Note"]
            track_cond = row.get("Track Condition", "dry")

            score, top5, notes = kgf_score_and_notes(name, speed, stamina, odds, board, ped, track_cond)
            
            results.append({
                "PP": row["PP"],
                "Horse": name,
                "Score": score,
                "Odds": odds,
                "Top5 Liker": "⭐" if top5 else "",
                "Key Notes": " | ".join(notes[:3]) if notes else ""
            })

        results.sort(key=lambda x: x["Score"], reverse=True)
        st.dataframe(results, use_container_width=True)

        st.success("**KGF Contenders for Box Bets**")
        for i, r in enumerate(results[:6], 1):
            st.write(f"**{i}.** PP {r['PP']} - **{r['Horse']}** (Score: {r['Score']}) {r['Top5 Liker']}")
            if r['Key Notes']:
                st.caption(f"→ {r['Key Notes']}")

st.caption("KGF Handicapper v1 — Built with Grok + Mom's Wisdom 🐱💰")
