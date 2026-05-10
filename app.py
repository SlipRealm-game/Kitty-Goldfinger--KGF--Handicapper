import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="KGF Handicapper", page_icon="🐱", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("🐱 Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping Logic | Honoring Kitty's Techniques")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0, pedigree_note=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.0)
    score += (board_hit_rate * 20)
    
    # Ocelli / Top-5 Liker Signal (high odds + likes the board)
    ocelli = odds >= 12 and board_hit_rate >= 0.45
    if ocelli:
        score += 18   # Moderate boost for sneaky top-5 horses
    
    # Bonus for strong pedigree / Triple Crown lineage
    if any(x in pedigree_note.lower() for x in ["secretariat", "triple crown", "justify", "american pharoah", "chrome"]):
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
        board_rate = st.slider("Board Hit Rate (Top 5 %)", 0.0, 1.0, 0.6)
        pedigree = st.text_input("Pedigree Note / Triple Crown Lineage", "")
        
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
    st.subheader("🏇 Race Card Predictions + RapidAPI")
    st.write("Select track/race — Pull data or edit full field (including pedigree)")

    tracks = ["Santa Anita", "Laurel Park", "Belmont Park", "Mountaineer", "Churchill Downs", "Gulfstream Park", "Aqueduct", "Saratoga", "Keeneland", "Del Mar", "Pimlico"]

    col1, col2, col3 = st.columns(3)
    with col1:
        track = st.selectbox("Track", tracks)
    with col2:
        date = st.date_input("Race Date", value="today")
    with col3:
        race_num = st.number_input("Race Number", 1, 14, 6)

    st.write(f"**{track} — Race {race_num} — {date}**")

    rapid_key = st.text_input("Your RapidAPI Key (Horse Racing USA)", type="password", key="rapid_key")

    if st.button("🔄 Pull Race Data from RapidAPI"):
        if not rapid_key:
            st.error("Enter your RapidAPI Key")
        else:
            try:
                url = "https://horse-racing-usa.p.rapidapi.com/race"
                headers = {"X-RapidAPI-Key": rapid_key, "X-RapidAPI-Host": "horse-racing-usa.p.rapidapi.com"}
                params = {"track": track.lower().replace(" ", "-"), "date": str(date), "race": int(race_num)}
                response = requests.get(url, headers=headers, params=params, timeout=15)
                if response.status_code == 200:
                    st.success("✅ Data pulled!")
                    st.json(response.json())
                else:
                    st.error(f"Error {response.status_code}")
            except Exception as e:
                st.error(f"Failed: {e}")

    # === FULL FIELD TABLE WITH PEDIGREE ===
    st.subheader("Edit Full Race Field")
    default_data = pd.DataFrame({
        "PP": list(range(1, 11)),
        "Horse Name": [f"Horse {i}" for i in range(1, 11)],
        "Pedigree / Triple Crown Note": [""] * 10,
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
            board_rate = row["Board Hit Rate"]
            pedigree = row["Pedigree / Triple Crown Note"]
            score, alert = kgf_score(name, speed, stamina, odds, board_rate, pedigree)
            results.append({
                "PP": row["PP"],
                "Horse": name,
                "Pedigree": pedigree,
                "KGF Score": score,
                "Top-5 Liker": "⚠️" if alert else ""
            })

        results.sort(key=lambda x: x["KGF Score"], reverse=True)
        st.dataframe(results, use_container_width=True)
        
        st.success("**KGF Top 6 Predictions** (Speed + Stamina + Board History + Pedigree + Top-5 Likers)")
        for i, r in enumerate(results[:6], 1):
            st.write(f"{i}. PP {r['PP']} - **{r['Horse']}** (Score: {r['KGF Score']}) {r['Top-5 Liker']} | Pedigree: {r['Pedigree']}")

st.caption("KGF Handicapper v1 — Built with Grok + Mom's Wisdom 🐱💰")
