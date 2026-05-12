import streamlit as st
import pandas as pd

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("Kitty Goldfinger (KGF) Handicapper")
st.subheader("Real Handicapping Assistant")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0, pedigree_note=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.2)
    score += (board_hit_rate * 25)

    high_odds_hitter = (odds >= 12 and board_hit_rate >= 0.50)
    pedigree_bonus = any(x in pedigree_note.lower() for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown"])

    return round(score, 1), high_odds_hitter, pedigree_bonus

# Expanded Real Data Library
race_library = {
    "Laurel Park - Race 7 (Today)": pd.DataFrame([
        {"PP":1,"Horse Name":"Magical Mondays","Pedigree Note":"Strong turf","Speed Figure":105,"Stamina":8,"Odds":1.8,"Board Hit Rate":0.75},
        {"PP":2,"Horse Name":"Brighty","Pedigree Note":"Demarchelier","Speed Figure":96,"Stamina":7,"Odds":10.0,"Board Hit Rate":0.65},
        {"PP":3,"Horse Name":"Play It Cool","Pedigree Note":"Midshipman","Speed Figure":88,"Stamina":9,"Odds":20.0,"Board Hit Rate":0.55},
        {"PP":4,"Horse Name":"Kitty's Son","Pedigree Note":"Cupid","Speed Figure":85,"Stamina":7,"Odds":20.0,"Board Hit Rate":0.50},
        {"PP":6,"Horse Name":"Close The Gate","Pedigree Note":"Closer","Speed Figure":98,"Stamina":9,"Odds":3.5,"Board Hit Rate":0.70},
        {"PP":7,"Horse Name":"Dalinar","Pedigree Note":"High class","Speed Figure":102,"Stamina":8,"Odds":2.5,"Board Hit Rate":0.72},
    ]),
    "2026 Preakness (May 16)": pd.DataFrame([
        {"PP":1,"Horse Name":"Taj Mahal","Pedigree Note":"Local Maryland","Speed Figure":105,"Stamina":8,"Odds":5.0,"Board Hit Rate":0.80},
        {"PP":2,"Horse Name":"Ocelli","Pedigree Note":"Derby 3rd","Speed Figure":98,"Stamina":9,"Odds":12.0,"Board Hit Rate":0.70},
        {"PP":9,"Horse Name":"Iron Honor","Pedigree Note":"Chad Brown","Speed Figure":108,"Stamina":8,"Odds":9.0,"Board Hit Rate":0.70},
    ])
    # Add more races here as needed
}

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Pick 5 Builder", "🏇 Race Card Predictions"])

with tab1:
    st.subheader("Manual Horse Analysis")
    selected_race = st.selectbox("Select Race", list(race_library.keys()))
    horse_list = race_library[selected_race]["Horse Name"].tolist()
    selected_horse = st.selectbox("Select Horse", horse_list)
    
    horse_row = race_library[selected_race][race_library[selected_race]["Horse Name"] == selected_horse].iloc[0]
    
    speed = st.number_input("Speed Figure", value=int(horse_row["Speed Figure"]))
    stamina = st.slider("Stamina", 1, 10, int(horse_row["Stamina"]))
    odds = st.number_input("Odds", value=float(horse_row["Odds"]))
    board_rate = st.slider("Board Hit Rate", 0.0, 1.0, float(horse_row["Board Hit Rate"]))
    pedigree = st.text_input("Pedigree Note", horse_row["Pedigree Note"])
    
    if st.button("Analyze This Horse"):
        score, hitter, ped_bonus = kgf_score(selected_horse, speed, stamina, odds, board_rate, pedigree)
        st.success(f"**{selected_horse} Score: {score}**")
        if hitter:
            st.warning("🔥 High Odds Board Hitter — Great for boxes!")
        if ped_bonus:
            st.success("👑 Elite Pedigree!")

with tab3:
    st.subheader("Race Card Predictions")
    selected_race = st.selectbox("Load Race", list(race_library.keys()))
    
    if st.button("Load Race Field"):
        st.session_state.current_df = race_library[selected_race].copy()
        st.success(f"Loaded {selected_race}")

    if 'current_df' in st.session_state:
        edited_df = st.data_editor(st.session_state.current_df, num_rows="dynamic", use_container_width=True)
    else:
        edited_df = st.data_editor(pd.DataFrame({
            "PP": list(range(1, 9)),
            "Horse Name": [f"Horse {i}" for i in range(1, 9)],
            "Pedigree Note": [""] * 8,
            "Speed Figure": [85] * 8,
            "Stamina": [6] * 8,
            "Odds": [10.0] * 8,
            "Board Hit Rate": [0.6] * 8
        }), num_rows="dynamic", use_container_width=True)

    if st.button("🚀 Run KGF Predictions"):
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

st.caption("KGF Handicapper v1 — Built with Mom's Wisdom")
