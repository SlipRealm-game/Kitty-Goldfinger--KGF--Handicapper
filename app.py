import streamlit as st
import pandas as pd

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("🐱 Kitty Goldfinger (KGF) Handicapper")
st.subheader("Real Handicapping Assistant - Honoring Kitty's Techniques")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0, pedigree_note=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.2)
    score += (board_hit_rate * 25)

    high_odds_hitter = odds >= 12 and board_hit_rate >= 0.50
    pedigree_bonus = any(x in pedigree_note.lower() for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown"])

    return round(score, 1), high_odds_hitter, pedigree_bonus

tab1, tab2, tab3 = st.tabs(["Manual Entry", "Pick 5 Builder", "🏇 Race Card Predictions"])

with tab3:
    st.subheader("Select Race")
    tracks = ["Santa Anita", "Laurel Park", "Aqueduct", "Mountaineer", "Churchill Downs", "Gulfstream Park"]
    col1, col2, col3 = st.columns(3)
    with col1:
        track = st.selectbox("Track", tracks)
    with col2:
        date = st.date_input("Race Date", value="today")
    with col3:
        race_num = st.number_input("Race Number", 1, 14, 6)

    if st.button("🔄 Load Race Horses"):
        # Demo data for different races (you can expand this)
        if track == "Laurel Park" and race_num == 7:
            df = pd.DataFrame([
                {"PP":1, "Horse Name":"Magical Mondays", "Trainer":"McGaughey", "Pedigree Note":"Strong turf", "Speed Figure":105, "Stamina":8, "Odds":1.8, "Board Hit Rate":0.75},
                {"PP":2, "Horse Name":"Brighty", "Trainer":"Motion", "Pedigree Note":"Demarchelier", "Speed Figure":96, "Stamina":7, "Odds":10.0, "Board Hit Rate":0.65},
                {"PP":3, "Horse Name":"Play It Cool", "Trainer":"Delgado", "Pedigree Note":"Midshipman", "Speed Figure":88, "Stamina":9, "Odds":20.0, "Board Hit Rate":0.55},
                {"PP":4, "Horse Name":"Kitty's Son", "Trainer":"Maker", "Pedigree Note":"Cupid", "Speed Figure":85, "Stamina":7, "Odds":20.0, "Board Hit Rate":0.50},
            ])
        else:
            df = pd.DataFrame([
                {"PP":1, "Horse Name":"Favorite Horse", "Trainer":"Baffert", "Pedigree Note":"Secretariat line", "Speed Figure":105, "Stamina":8, "Odds":3.5, "Board Hit Rate":0.80},
                {"PP":2, "Horse Name":"Value Play", "Trainer":"Asmussen", "Pedigree Note":"", "Speed Figure":98, "Stamina":7, "Odds":8.0, "Board Hit Rate":0.65},
            ])
        st.success(f"Loaded {track} Race {race_num}")
        st.session_state.current_df = df

    st.subheader("Race Field")
    if 'current_df' in st.session_state:
        edited_df = st.data_editor(st.session_state.current_df, num_rows="dynamic", use_container_width=True)
    else:
        edited_df = st.data_editor(pd.DataFrame({
            "PP": list(range(1, 9)),
            "Horse Name": [f"Horse {i}" for i in range(1, 9)],
            "Trainer": ["" for _ in range(8)],
            "Pedigree Note": ["" for _ in range(8)],
            "Speed Figure": [85] * 8,
            "Stamina": [6] * 8,
            "Odds": [10.0] * 8,
            "Board Hit Rate": [0.6] * 8
        }), num_rows="dynamic", use_container_width=True)

    if st.button("🚀 Run KGF Analysis"):
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
                "Trainer": row.get("Trainer", ""),
                "Score": score,
                "Odds": odds,
                "High Odds Hitter": "🔥" if hitter else "",
                "Pedigree": "👑" if ped_bonus else "",
                "Note": ped
            })

        results.sort(key=lambda x: x["Score"], reverse=True)
        st.dataframe(results, use_container_width=True)

st.caption("KGF Handicapper v1 — Testing Version")
