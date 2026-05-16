import streamlit as st
import pandas as pd

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

# Large logo across the top
st.image("logo.jpg", width=700)

st.title("Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping | Honoring Kitty's Techniques")

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

    if st.button("🔄 Load 2026 Preakness Field"):
        preakness_data = pd.DataFrame([
            {"PP":1, "Horse Name":"Taj Mahal", "Pedigree Note":"Local Maryland strong pedigree", "Speed Figure":105, "Stamina":8, "Odds":5.0, "Board Hit Rate":0.80},
            {"PP":2, "Horse Name":"Ocelli", "Pedigree Note":"Derby 3rd placer", "Speed Figure":98, "Stamina":9, "Odds":12.0, "Board Hit Rate":0.70},
            {"PP":3, "Horse Name":"Crupper", "Pedigree Note":"Longshot with upside", "Speed Figure":92, "Stamina":7, "Odds":30.0, "Board Hit Rate":0.55},
            {"PP":4, "Horse Name":"Robusta", "Pedigree Note":"Doug O'Neill", "Speed Figure":94, "Stamina":7, "Odds":25.0, "Board Hit Rate":0.60},
            {"PP":5, "Horse Name":"Talkin", "Pedigree Note":"Irad Ortiz Jr.", "Speed Figure":96, "Stamina":8, "Odds":20.0, "Board Hit Rate":0.65},
            {"PP":6, "Horse Name":"Chip Honcho", "Pedigree Note":"Asmussen", "Speed Figure":102, "Stamina":7, "Odds":12.0, "Board Hit Rate":0.75},
            {"PP":7, "Horse Name":"The Hell We Did", "Pedigree Note":"Todd Fincher", "Speed Figure":97, "Stamina":8, "Odds":15.0, "Board Hit Rate":0.58},
            {"PP":8, "Horse Name":"Bull by the Horns", "Pedigree Note":"Saffie Joseph", "Speed Figure":93, "Stamina":7, "Odds":30.0, "Board Hit Rate":0.50},
            {"PP":9, "Horse Name":"Iron Honor", "Pedigree Note":"Chad Brown", "Speed Figure":108, "Stamina":8, "Odds":9.0, "Board Hit Rate":0.70},
            {"PP":10, "Horse Name":"Napoleon Solo", "Pedigree Note":"Mid-pack type", "Speed Figure":99, "Stamina":8, "Odds":8.0, "Board Hit Rate":0.65},
        ])
        st.session_state.current_df = preakness_data
        st.success("✅ 2026 Preakness Field Loaded!")

    st.subheader("Edit Race Field")
    if 'current_df' in st.session_state:
        edited_df = st.data_editor(st.session_state.current_df, num_rows="dynamic", use_container_width=True)
    else:
        edited_df = st.data_editor(pd.DataFrame({
            "PP": list(range(1, 11)),
            "Horse Name": [f"Horse {i}" for i in range(1, 11)],
            "Pedigree Note": [""] * 10,
            "Speed Figure": [85] * 10,
            "Stamina": [6] * 10,
            "Odds": [10.0] * 10,
            "Board Hit Rate": [0.6] * 10
        }), num_rows="dynamic", use_container_width=True)

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

with tab2:
    st.subheader("Pick 5 Builder")
    st.write("Build your Pick 5")
    for i in range(1, 6):
        st.multiselect(f"Race {i} - Horses", ["Strong Favorite", "High Odds Hitter", "Pedigree Play"], default=["Strong Favorite"])

st.caption("KGF Handicapper v1 — Built Using Mom's Techiques 💰")
