import streamlit as st
import requests

st.set_page_config(page_title="KGF Handicapper", layout="wide")

# === YOUR LOGO ===
st.image("logo.jpg", width=400)

st.title("Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping Logic | Honoring Kitty's Techniques")

# === RAPIDAPI KEY (put your key here) ===
RAPIDAPI_KEY = st.text_input("RapidAPI Key (for live race data)", type="password", value="")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0):
    score = 0        
    score += (speed * 0.4)
    score += (stamina * 2.0)
    score += (board_hit_rate * 25)
    ocelli = odds >= 15 and board_hit_rate >= 0.5
    if ocelli:
        score += 30
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
        
        if st.form_submit_button("Run KGF"):
            score, alert = kgf_score(name, speed, stamina, odds, board_rate)
            st.success(f"**{name} Score: {score}**")
            if alert:
                st.warning("⚠️ Ocelli Signal!")

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
    st.subheader("🏇 Race Card Predictions")
    st.write("Select track and race — then enter the field (or use RapidAPI for live data)")

    tracks = [
        "Laurel Park", "Pimlico", "Churchill Downs", "Keeneland", "Gulfstream Park",
        "Santa Anita", "Del Mar", "Aqueduct", "Belmont Park", "Saratoga", "Oaklawn Park",
        "Fair Grounds", "Tampa Bay Downs", "Monmouth Park", "Woodbine", "Ascot (UK)",
        "Dubai (UAE)", "Hong Kong", "Randwick (Australia)"
    ]

    col1, col2, col3 = st.columns(3)
    with col1:
        track = st.selectbox("Track", tracks)
    with col2:
        date = st.date_input("Race Date", value="today")
    with col3:
        race_num = st.number_input("Race Number", 1, 14, 7)

    st.write(f"**{track} — Race {race_num} — {date}**")

    # RapidAPI placeholder
    if RAPIDAPI_KEY and st.button("Load Live Race Data (RapidAPI)"):
        st.info("Fetching from RapidAPI... (add your actual API call here)")
        # Example:
        # response = requests.get("https://horse-racing.p.rapidapi.com/race_entries", 
        #     headers={"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": "horse-racing.p.rapidapi.com"},
        #     params={"track": track.lower(), "date": str(date)})
        # Then parse response.json()

    # Manual entry fallback
    num_horses = st.number_input("Horses in race", 4, 20, 10)
    horses = []
    for i in range(num_horses):
        with st.expander(f"Horse {i+1}"):
            name = st.text_input(f"Horse Name {i+1}", f"Horse {i+1}", key=f"name_{i}")
            speed = st.number_input(f"Speed Figure {i+1}", 0, 120, 85, key=f"speed_{i}")
            stamina = st.slider(f"Stamina {i+1}", 1, 10, 6, key=f"stamina_{i}")
            odds = st.number_input(f"Odds {i+1}", 1.0, 100.0, 10.0, key=f"odds_{i}")
            board_rate = st.slider(f"Board Hit Rate {i+1}", 0.0, 1.0, 0.6, key=f"board_{i}")
            horses.append({"name": name, "speed": speed, "stamina": stamina, "odds": odds, "board": board_rate})

    if st.button("🚀 Run KGF Predictions on Full Field"):
        results = []
        for h in horses:
            score, alert = kgf_score(h["name"], h["speed"], h["stamina"], h["odds"], h["board"])
            results.append({"Horse": h["name"], "KGF Score": score, "Ocelli": "⚠️" if alert else ""})

        results.sort(key=lambda x: x["KGF Score"], reverse=True)
        st.dataframe(results, use_container_width=True)
        
        st.success("**KGF Top 6 Predictions**")
        for i, r in enumerate(results[:6], 1):
            st.write(f"{i}. {r['Horse']} (Score: {r['KGF Score']}) {r['Ocelli']}")

st.caption("KGF Handicapper v1 — Built with Mom's Techniques + Mom's Wisdom 💰")
