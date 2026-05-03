import streamlit as st

st.set_page_config(page_title="KGF Handicapper", layout="wide")
st.title("Kitty Goldfinger (KGF) Handicapper")
st.image("https://i.imgur.com/8YnqM.jpg", width=300)  # or local path
st.subheader("Ocelli-Style Board-Hit Logic | Honoring Mom's Techniques")

def kgf_score(horse_name, speed, stamina, odds, board_hit_rate=0.0):
    score = 0
    score += (speed * 0.4)
    score += (stamina * 2.0)
    score += (board_hit_rate * 25)
    ocelli = odds >= 15 and board_hit_rate >= 0.5
    if ocelli:
        score += 30
    return round(score, 1), ocelli

tab1, tab2 = st.tabs(["Manual Entry", "Pick 5 Builder"])

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
    st.info("Pick 5 builder coming soon!")

st.caption("KGF Handicapper v1 — Built with Grok + Mom's Wisdom 🐱💰")
