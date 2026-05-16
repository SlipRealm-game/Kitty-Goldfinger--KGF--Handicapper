import streamlit as st
import pandas as pd

st.set_page_config(page_title="KGF Handicapper", page_icon="logo2.jpg", layout="wide")

# Large logo across the top
st.image("logo.jpg", width=700)

st.title("Kitty Goldfinger (KGF) Handicapper")
st.subheader("Kitty Style Handicapping | Honoring Kitty's Techniques")

# Unified scoring logic matching pedigree and handicapping parameters
def kgf_score(speed, stamina, odds, board_hit_rate=0.0, pedigree_note="", trainer="", jockey=""):
    score = 0
    score += (speed * 0.45)
    score += (stamina * 2.2)
    score += (board_hit_rate * 25)

    # Identifies high odds horses that love hitting the board
    high_odds_hitter = (odds >= 12 and board_hit_rate >= 0.50)
    
    # Text-matching across pedigree, trainer, or jockey descriptions
    search_text = f"{pedigree_note} {trainer} {jockey}".lower()
    pedigree_bonus = any(x in search_text for x in ["secretariat", "justify", "pharoah", "chrome", "triple crown", "nyquist", "a.p. indy", "authentic"])

    return round(score, 1), high_odds_hitter, pedigree_bonus

# Exact details generated for all 14 horses
def get_preakness_data():
    return pd.DataFrame([
        {"PP": 1, "Horse Name": "Taj Mahal", "Trainer": "Brittany Russell", "Jockey": "Sheldon Russell", "Lifetime Winnings ($)": 210000, "Pedigree Note": "Sired by Nyquist (Uncle Mo/Storm Cat/Secretariat lines)", "Speed Figure": 105, "Stamina": 8, "Odds": 5.0, "Board Hit Rate": 0.80},
        {"PP": 2, "Horse Name": "Ocelli", "Trainer": "D. Whitworth Beckman", "Jockey": "Tyler Gaffalione", "Lifetime Winnings ($)": 609800, "Pedigree Note": "Derby 3rd place finisher. #1 ranked average stride length.", "Speed Figure": 98, "Stamina": 9, "Odds": 6.0, "Board Hit Rate": 0.70},
        {"PP": 3, "Horse Name": "Crupper", "Trainer": "Donnie Von Hemel", "Jockey": "Junior Alvarado", "Lifetime Winnings ($)": 145000, "Pedigree Note": "Sired by Alternation (A.P. Indy/Secretariat line for stamina)", "Speed Figure": 92, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.55},
        {"PP": 4, "Horse Name": "Robusta", "Trainer": "Doug O'Neill", "Jockey": "Rafael Bejarano", "Lifetime Winnings ($)": 115000, "Pedigree Note": "Calumet Farm homebred. Troubled trip in Derby, strong bounce-back candidate.", "Speed Figure": 94, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.60},
        {"PP": 5, "Horse Name": "Talkin", "Trainer": "Danny Gargan", "Jockey": "Irad Ortiz Jr.", "Lifetime Winnings ($)": 288625, "Pedigree Note": "3rd in Blue Grass. High-percentage connections and jockey upgrade.", "Speed Figure": 96, "Stamina": 8, "Odds": 20.0, "Board Hit Rate": 0.65},
        {"PP": 6, "Horse Name": "Chip Honcho", "Trainer": "Steve Asmussen", "Jockey": "Jose Ortiz", "Lifetime Winnings ($)": 240000, "Pedigree Note": "Gun Runner winner. 2nd-longest average stride length in field.", "Speed Figure": 102, "Stamina": 7, "Odds": 5.0, "Board Hit Rate": 0.75},
        {"PP": 7, "Horse Name": "The Hell We Did", "Trainer": "Todd Fincher", "Jockey": "Luis Saez", "Lifetime Winnings ($)": 134818, "Pedigree Note": "Sired by Authentic (Into Mischief line). Highly consistent tactician.", "Speed Figure": 97, "Stamina": 8, "Odds": 15.0, "Board Hit Rate": 0.58},
        {"PP": 8, "Horse Name": "Bull by the Horns", "Trainer": "Saffie Joseph Jr.", "Jockey": "Micah Husbands", "Lifetime Winnings ($)": 187115, "Pedigree Note": "Rushaway Stakes winner. Deep closer built for long Laurel stretch.", "Speed Figure": 93, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.50},
        {"PP": 9, "Horse Name": "Iron Honor", "Trainer": "Chad Brown", "Jockey": "Flavien Prat", "Lifetime Winnings ($)": 229250, "Pedigree Note": "Sired by Nyquist. CRITICAL CHANGE: Blinkers taken off to track pace.", "Speed Figure": 108, "Stamina": 8, "Odds": 4.5, "Board Hit Rate": 0.70},
        {"PP": 10, "Horse Name": "Napoleon Solo", "Trainer": "Chad Summers", "Jockey": "Paco Lopez", "Lifetime Winnings ($)": 319000, "Pedigree Note": "G1 Champagne Stakes winner. Massive early pace numbers from outside.", "Speed Figure": 99, "Stamina": 8, "Odds": 8.0, "Board Hit Rate": 0.65},
        {"PP": 11, "Horse Name": "Corona de Oro", "Trainer": "Dallas Stewart", "Jockey": "John Velazquez", "Lifetime Winnings ($)": 95000, "Pedigree Note": "3rd in Lexington. Trainer known for placing massive longshots in exotics.", "Speed Figure": 91, "Stamina": 7, "Odds": 30.0, "Board Hit Rate": 0.45},
        {"PP": 12, "Horse Name": "Incredibolt", "Trainer": "Riley Mott", "Jockey": "Jaime Torres", "Lifetime Winnings ($)": 340000, "Pedigree Note": "6th in Derby. Posted a triple-digit 100 speed rating in Virginia Derby.", "Speed Figure": 100, "Stamina": 8, "Odds": 5.0, "Board Hit Rate": 0.60},
        {"PP": 13, "Horse Name": "Great White", "Trainer": "John Ennis", "Jockey": "Alex Achard", "Lifetime Winnings ($)": 110000, "Pedigree Note": "High-stamina grind style. Fresh face skipping the Derby.", "Speed Figure": 93, "Stamina": 8, "Odds": 15.0, "Board Hit Rate": 0.50},
        {"PP": 14, "Horse Name": "Pretty Boy Miah", "Trainer": "Jeremiah Englehart", "Jockey": "Ricardo Santana Jr.", "Lifetime Winnings ($)": 125000, "Pedigree Note": "Blazing early speed but drawn in the tough far outside Post 14.", "Speed Figure": 97, "Stamina": 6, "Odds": 15.0, "Board Hit Rate": 0.55}
    ])

def get_empty_field():
    return pd.DataFrame({
        "PP": list(range(1, 15)),
        "Horse Name": [f"Horse {i}" for i in range(1, 15)],
        "Trainer": [""] * 14,
        "Jockey": [""] * 14,
        "Lifetime Winnings ($)": [0] * 14,
        "Pedigree Note": [""] * 14,
        "Speed Figure": [85] * 14,
        "Stamina": [6] * 14,
        "Odds": [10.0] * 14,
        "Board Hit Rate": [0.5] * 14
    })

# Core logic processing function reused by both entry styles
def process_predictions(df, source_label):
    results = []
    for _, row in df.iterrows():
        name = row["Horse Name"]
        speed = row["Speed Figure"]
        stamina = row["Stamina"]
        odds = row["Odds"]
        board = row["Board Hit Rate"]
        ped = row["Pedigree Note"]
        trn = row["Trainer"]
        jck = row["Jockey"]
        
        score, hitter, ped_bonus = kgf_score(speed, stamina, odds, board, ped, trn, jck)
        
        results.append({
            "PP": row["PP"],
            "Horse": name,
            "Trainer": trn,
            "Jockey": jck,
            "KGF Score": score,
            "Odds": odds,
            "High Odds Hitter": "🔥" if hitter else "",
            "Pedigree Play": "👑" if ped_bonus else "",
            "Notes / Analytics": ped
        })

    results.sort(key=lambda x: x["KGF Score"], reverse=True)
    st.subheader(f"🏆 Top Generated Contenders ({source_label})")
    st.dataframe(results, use_container_width=True)
    
    # Store processed names in session state to feed into the Pick 5 module dynamically
    st.session_state.active_horses = [r["Horse"] for r in results]

# Initialize global tracking structures
if 'current_df' not in st.session_state:
    st.session_state.current_df = get_empty_field()
if 'active_horses' not in st.session_state:
    st.session_state.active_horses = []

tab1, tab2, tab3 = st.tabs(["📝 Manual Entry", "🎯 Pick 5 Builder", "🏇 Race Card Predictions"])

# --- TAB 1: MANUAL ENTRY ---
with tab1:
    st.subheader("📝 Manual Grid Field Setup")
    st.write("Use this page to construct a field from scratch or alter entries if API access is offline.")
    
    # Clear / Reset Button specific to manual operations
    if st.button("🗑️ Reset Blank Manual Field"):
        st.session_state.current_df = get_empty_field()
        st.rerun()

    # Dynamic data editor mirroring the race card layout exactly
    edited_manual_df = st.data_editor(st.session_state.current_df, key="manual_editor", num_rows="dynamic", use_container_width=True)

    if st.button("⚙️ Run Predictions from Manual Entry"):
        st.session_state.current_df = edited_manual_df
        process_predictions(edited_manual_df, "Manual Entry Calculation")

# --- TAB 3: RACE CARD PREDICTIONS ---
with tab3:
    st.subheader("🏇 Race Card Automated Loading")

    if st.button("🔄 Load 2026 Preakness Field (14 Horses)"):
        preakness_data = get_preakness_data()
        st.session_state.current_df = preakness_data
        st.success("✅ Complete 14-Horse Preakness Field & Historical Handicapping Details Loaded!")
        st.rerun()

    st.subheader("Edit Race Field Parameters")
    edited_card_df = st.data_editor(st.session_state.current_df, key="card_editor", num_rows="dynamic", use_container_width=True)

    if st.button("🚀 Run KGF Predictions on Full Field"):
        st.session_state.current_df = edited_card_df
        process_predictions(edited_card_df, "Race Card Calculation")

# --- TAB 2: PICK 5 BUILDER ---
with tab2:
    st.subheader("🎯 Reactive Pick 5 Builder")
    
    # Track Selection context to trigger full validation logic
    track_selection = st.selectbox("Select Active Circuit / Track:", ["Laurel Park (Preakness 2026)", "Pimlico", "Churchill Downs", "Belmont at Saratoga", "Custom/Manual Circuit"])
    st.write(f"Building Ticket Matrix for: **{track_selection}**")
    
    # Pull selections directly from either active computation path
    available_pool = st.session_state.active_horses if st.session_state.active_horses else [f"Horse {i}" for i in range(1, 15)]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Select Contenders for Each Leg")
        leg1 = st.multiselect("Race 1 (Leg 1) Candidates", available_pool, default=available_pool[:2] if len(available_pool) > 1 else available_pool)
        leg2 = st.multiselect("Race 2 (Leg 2) Candidates", available_pool, default=available_pool[:1] if available_pool else [])
        leg3 = st.multiselect("Race 3 (Leg 3) Candidates", available_pool, default=available_pool[:1] if available_pool else [])
        leg4 = st.multiselect("Race 4 (Leg 4) Candidates", available_pool, default=available_pool[:1] if available_pool else [])
        leg5 = st.multiselect("Race 5 (Leg 5) Candidates", available_pool, default=available_pool[:1] if available_pool else [])

    with col2:
        st.markdown("### Ticket Cost Calculator")
        base_cost = st.selectbox("Base Wager Amount", [0.50, 1.00, 2.00, 5.00], index=0)
        
        # Calculate permutations mathematically
        total_combinations = len(leg1) * len(leg2) * len(leg3) * len(leg4) * len(leg5)
        ticket_cost = total_combinations * base_cost
        
        st.metric(label="Total Combinations", value=f"{total_combinations}")
        st.metric(label="Estimated Ticket Cost", value=f"${ticket_cost:,.2f}")
        
        if total_combinations == 0:
            st.warning("⚠️ Make sure to select at least one horse for every leg to calculate ticket geometry.")
        else:
            st.success("✨ Ticket Matrix Validated!")

st.markdown("---")
st.caption("KGF Handicapper v1 — Built Using Mom's Techniques 💰")

