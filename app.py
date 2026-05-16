import streamlit as st
import pandas as pd
import requests
import sys
import os

# rpscrape support
if os.path.exists("rpscrape"):
    sys.path.append("rpscrape")

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

# Large Logo
st.image("logo.jpg", width=250)

st.title("Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping Logic | Honoring Kitty's Techniques")

RAPIDAPI_KEY = "39171a45bemsh0b148cc74b98d59p113376jsnba83cc13ac54"

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0, pedigree_note=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.2)
    score += (board_hit_rate * 25)

    high_odds_hitter = (odds >= 12 and board_hit_rate >= 0.50)
    pedigree_bonus = any(x in pedigree_note.lower() for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown"])

    return round(score, 1), high_odds_hitter, pedigree_bonus

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Pick 5 Builder", "🏇 Race Card Predictions"])

# ====================== TAB 1: MANUAL ENTRY ======================
with tab1:
    st.subheader("Manual Horse Analysis")
    name = st.text_input("Horse Name", "Play It Cool")
    speed = st.number_input("Speed Figure", 0, 120, 85)
    stamina = st.slider("Stamina (1-10)", 1, 10, 6)
    odds = st.number_input("Odds", 1.0, 100.0, 20.0)
    board_rate = st.slider("Board Hit Rate", 0.0, 1.0, 0.6)
    pedigree = st.text_input("Pedigree Note", "")
    
    if st.button("Analyze This Horse"):
        score, hitter, ped_bonus = kgf_score(name, speed, stamina, odds, board_rate, pedigree)
        st.success(f"**{name} Score: {score}**")
        if hitter:
            st.warning("🔥 High Odds Board Hitter — Strong for boxes!")
        if ped_bonus:
            st.success("👑 Elite Pedigree!")

# ====================== TAB 2: PICK 5 ======================
with tab2:
    st.subheader("Pick 5 Builder")
    st.write("Select track and build your Pick 5")
    track = st.selectbox("Pick 5 Track", ["Santa Anita", "Laurel Park", "Aqueduct", "Mountaineer", "Churchill Downs"])
    
    races = ["Race 1", "Race 2", "Race 3", "Race 4", "Race 5"]
    selections = {}
    for r in races:
        selections[r] = st.multiselect(f"{r} - Horse Type", 
            ["Strong Favorite", "High Odds Hitter", "Pedigree Play", "Value Play"], 
            default=["Strong Favorite"])
    
    if st.button("Generate Suggested Pick 5"):
        st.success("KGF Suggested Pick 5:")
        for r in races:
            st.write(f"**{r}**: {selections[r][0]}")

    if st.button("Calculate $0.50 Pick 5 Cost"):
        combos = 1
        for r in races:
            combos *= len(selections[r])
        cost = combos * 0.5
        st.success(f"Total combinations: {combos:,} | **Cost: ${cost:,.2f}**")

# ====================== TAB 3: RACE CARD ======================
with tab3:
    st.subheader("🏇 Race Card Predictions")
    
    tracks = ["Santa Anita", "Laurel Park", "Aqueduct", "Mountaineer", "Churchill Downs", 
              "Gulfstream Park", "Saratoga", "Belmont Park"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        track = st.selectbox("Track", tracks)
    with col2:
        date = st.date_input("Race Date", value="today")
    with col3:
        race_num = st.number_input("Race Number", 1, 14, 6)

    st.write(f"**{track} — Race {race_num} — {date}**")

    # Both Pull Buttons
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Pull with RapidAPI"):
            try:
                url = "https://horse-racing-usa.p.rapidapi.com/race"
                headers = {
                    "X-RapidAPI-Key": RAPIDAPI_KEY,
                    "X-RapidAPI-Host": "horse-racing-usa.p.rapidapi.com"
                }
                params = {"track": track.lower().replace(" ", "-"), "date": str(date), "race": race_num}
                response = requests.get(url, headers=headers, params=params, timeout=15)
                if response.status_code == 200:
                    st.success("✅ RapidAPI Data Pulled!")
                    st.json(response.json())
                else:
                    st.error(f"RapidAPI Error: {response.status_code}")
            except Exception as e:
                st.error(f"RapidAPI failed: {e}")

    with col_b:
        if st.button("🔄 Pull with rpscrape"):
            try:
                import racecards
                st.success("✅ rpscrape imported!")
            except Exception as e:
                st.error(f"rpscrape failed: {e}")

    # Manual Table
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

st.caption("KGF Handicapper v1 — Both Pull Methods 💰")
