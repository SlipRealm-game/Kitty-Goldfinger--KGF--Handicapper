import streamlit as st
import pandas as pd

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=400)

st.title("Kitty Goldfinger (KGF) Handicapper")
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
    # Your manual entry code remains the same
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
    # Your Pick 5 code remains the same
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

    if st.button("🔄 Load 2026 Preakness Field (May 16)"):
        preakness_data = pd.DataFrame([
            {"PP": 1, "Horse Name": "Taj Mahal", "Pedigree Note": "Local Maryland horse, strong pedigree", "Speed Figure": 105, "Stamina": 8, "Odds": 5.0, "Board Hit Rate": 0.80},
            {"PP": 2, "Horse Name": "Ocelli", "Pedigree Note": "Derby 3rd, board hitter", "Speed Figure": 98, "Stamina": 9, "Odds": 6.0, "Board Hit Rate": 0.65},
            {"PP": 3, "Horse Name": "Crupper", "Pedigree Note": "Longshot with upside", "Speed Figure": 92, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.50},
            {"PP": 4, "Horse Name": "Robusta", "Pedigree Note": "Doug O'Neill trainee", "Speed Figure": 94, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.55},
            {"PP": 5, "Horse Name": "Talkin", "Pedigree Note": "Irad Ortiz Jr. mount", "Speed Figure": 96, "Stamina": 8, "Odds": 20.0, "Board Hit Rate": 0.60},
            {"PP": 6, "Horse Name": "Chip Honcho", "Pedigree Note": "Asmussen, consistent", "Speed Figure": 102, "Stamina": 7, "Odds": 5.0, "Board Hit Rate": 0.75},
            {"PP": 7, "Horse Name": "The Hell We Did", "Pedigree Note": "Todd Fincher", "Speed Figure": 97, "Stamina": 8, "Odds": 15.0, "Board Hit Rate": 0.58},
            {"PP": 8, "Horse Name": "Bull by the Horns", "Pedigree Note": "Saffie Joseph", "Speed Figure": 93, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.50},
            {"PP": 9, "Horse Name": "Iron Honor", "Pedigree Note": "Chad Brown", "Speed Figure": 108, "Stamina": 8, "Odds": 9.0, "Board Hit Rate": 0.70},
            {"PP": 10, "Horse Name": "Napoleon Solo", "Pedigree Note": "Mid-pack type", "Speed Figure": 99, "Stamina": 8, "Odds": 8.0, "Board Hit Rate": 0.65},
        ])
        st.success("✅ 2026 Preakness Field Loaded!")
        st.dataframe(preakness_data, use_container_width=True)
        st.session_state.edited_df = preakness_data  # Optional: save to session for editing

    st.subheader("Edit Race Field")
    if 'edited_df' in st.session_state:
        edited_df = st.data_editor(st.session_state.edited_df, num_rows="dynamic", use_container_width=True)
    else:
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

st.caption("KGF Handicapper v1 — Built with + Mom's Wisdom")
