import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="KGF Handicapper", page_icon="🐱", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("🐱 Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping Logic | Kitty's Proven Techniques")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0, pedigree_note=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.0)
    score += (board_hit_rate * 20)
    ocelli = odds >= 12 and board_hit_rate >= 0.45
    if ocelli:
        score += 18
    if any(x in pedigree_note.lower() for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown"]):
        score += 12
    return round(score, 1), ocelli

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Pick 5 Builder", "🏇 Race Card Predictions"])

with tab1:
    st.subheader("Manual Horse Analysis")
    with st.form("kgf_form"):
        name = st.text_input("Horse Name", "Play It Cool")
        speed = st.number_input("Speed Figure", 0, 120, 85)
        stamina = st.slider("Stamina (1-10)", 1, 10, 6)
        odds = st.number_input("Odds", 1.0, 100.0, 20.0)
        board_rate = st.slider("Board Hit Rate", 0.0, 1.0, 0.6)
        pedigree = st.text_input("Pedigree / Triple Crown Note", "")
        
        if st.form_submit_button("Run KGF"):
            score, alert = kgf_score(name, speed, stamina, odds, board_rate, pedigree)
            st.success(f"**{name} Score: {score}**")
            if alert:
                st.warning("⚠️ Top-5 Liker / Ocelli Signal!")

with tab2:
    st.subheader("Pick 5 Builder")
    st.write("Select horses for 5 consecutive races")
    races = ["Race 1", "Race 2", "Race 3", "Race 4", "Race 5"]
    selections = {}
    for r in races:
        selections[r] = st.multiselect(f"{r} - Horses", ["#1 Favorite", "#2 Value", "#3 Longshot", "#4 Bomb"], default=["#1 Favorite"])
    
    if st.button("Calculate $0.50 Pick 5 Cost"):
        combos = 1
        for r in races:
            combos *= len(selections[r])
        cost = combos * 0.5
        st.success(f"Total combinations: {combos:,} | **$0.50 Pick 5 Cost: ${cost:,.2f}**")

with tab3:
    st.subheader("🏇 Race Card Predictions - Multi-Track Live Pull")
    
    tracks = ["Aqueduct", "Santa Anita", "Laurel Park", "Mountaineer", "Churchill Downs", 
              "Gulfstream Park", "Saratoga", "Belmont Park", "Keeneland", "Del Mar"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        track = st.selectbox("Track", tracks)
    with col2:
        date = st.date_input("Race Date", value="today")
    with col3:
        race_num = st.number_input("Race Number", 1, 14, 6)

    st.write(f"**{track} — Race {race_num} — {date}**")

    if st.button("🔄 Pull Live Race Data (Multi-Source)"):
        with st.spinner("Trying multiple sources..."):
            data = None
            # 1. NYRA / Aqueduct JSON attempt
            if track.lower() in ["aqueduct", "belmont", "saratoga"]:
                try:
                    url = f"https://www.nyra.com/{track.lower()}/racing/entries/?day={date}&limit=entries&race={race_num}"
                    r = requests.get(url, timeout=10)
                    if r.status_code == 200:
                        st.success("✅ NYRA JSON pulled!")
                        data = r.json() if r.text.strip().startswith('{') else None
                except:
                    pass

            # 2. Fallback HTML parsing (works on most tracks)
            if not data:
                try:
                    url = f"https://entries.horseracingnation.com/entries-results/{track.lower().replace(' ', '-')}/{date}"
                    r = requests.get(url, timeout=10)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    # Basic table extraction example
                    tables = soup.find_all('table')
                    if tables:
                        st.success("✅ HTML parsed from HorseRacingNation")
                        st.write("Found tables - basic parsing ready (expand later)")
                except:
                    st.warning("All sources failed - use manual entry")

            if data:
                st.json(data[:500])  # Show partial for debugging

    # === MANUAL TABLE (always available) ===
    st.subheader("Manual / Edited Field Entry")
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
            score, alert = kgf_score(name, speed, stamina, odds, board, ped)
            results.append({
                "PP": row["PP"], 
                "Horse": name, 
                "Pedigree": ped,
                "Score": score, 
                "Top5 Liker": "⚠️" if alert else ""
            })
        results.sort(key=lambda x: x["Score"], reverse=True)
        st.dataframe(results, use_container_width=True)

st.caption("KGF Handicapper v1 — Multi-Track Live Pull + Kitty's Wisdom 🐱💰")
