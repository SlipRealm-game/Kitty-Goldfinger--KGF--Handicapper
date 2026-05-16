✅ Perfect! You have successfully added the rpscrape folder.

Final Clean app.py (Copy & Paste This)
Pythonimport streamlit as st
import pandas as pd
import sys
import os

# === Add rpscrape support ===
if os.path.exists("rpscrape"):
    sys.path.append("rpscrape")

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping Logic | Honoring Kitty's Techniques")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0, pedigree_note=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.2)
    score += (board_hit_rate * 25)

    high_odds_hitter = (odds >= 12 and board_hit_rate >= 0.50)
    pedigree_bonus = any(x in pedigree_note.lower() for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown"])

    return round(score, 1), high_odds_hitter, pedigree_bonus

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Pick 5 Builder", "🏇 Race Card Predictions"])

with tab3:
    st.subheader("🏇 Race Card Predictions")

    if st.button("🔄 Test rpscrape Import"):
        try:
            import racecards
            st.success("✅ rpscrape successfully imported!")
        except Exception as e:
            st.error(f"rpscrape import failed: {e}")

    # Race Selection
    selected_race = st.selectbox("Select Race", [
        "Laurel Park - Race 7",
        "2026 Preakness",
        "Santa Anita - Race 6",
        "Mountaineer - Race 1"
    ])

    if st.button("🔄 Load Race Field"):
        # You can expand this later with real scraper
        st.info("Loading demo data... (rpscrape ready for future use)")

    # Manual Table (Main Working Area)
    st.subheader("Edit Race Field")
    default_data = pd.DataFrame({
        "PP": list(range(1, 11)),
        "Horse Name": [f"Horse {i}" for i in range(1, 11)],
        "Pedigree Note": [""] * 10,
        "Speed Figure": [85] * 10,
        "Stamina": [6] * 10,
        "Odds": [10.0] * 10,
        "Board Hit Rate": [0.6] * 10
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
            
            score, hitter, ped_bonus = kgf_score(name, speed, stamina, odds, board, ped)
            
            results.append({
                "PP": row["PP"],
                "Horse": name,
                "Score": score,
                "Odds": odds,
                "High Odds Hitter": "🔥" if hitter else "",
                "Pedigree": "👑" if ped_bonus else ""
            })

        results.sort(key=lambda x: x["Score"], reverse=True)
        st.dataframe(results, use_container_width=True)

st.caption("KGF Handicapper v1 — Built with Mom's Logic and Wisdom 🐱💰")
