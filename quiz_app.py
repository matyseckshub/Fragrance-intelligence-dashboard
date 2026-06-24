import os
import pandas as pd
import streamlit as st

# 1. PAGE SETUP
st.set_page_config(page_title="Fragrance Matchmaker", layout="centered")
st.title("Personalized Fragrance Matchmaker")
st.markdown("Answer a few questions to discover your ideal olfactory profile based on live market metrics.")
st.markdown("---")

# 2. DATA LOADING
csv_filename = "fragrance_intelligence_master.csv"

if not os.path.exists(csv_filename):
    st.error(f"Error: Could not find '{csv_filename}'. Please ensure the master CSV is in the same folder.")
    st.stop()

df = pd.read_csv(csv_filename)

# 3. INITIALIZE SESSION STATE (Tracks quiz progress)
if "step" not in st.session_state:
    st.session_state.step = 1
if "season" not in st.session_state:
    st.session_state.season = ""
if "preferred_note" not in st.session_state:
    st.session_state.preferred_note = ""
if "max_price" not in st.session_state:
    st.session_state.max_price = 150.0

def move_to_next_step():
    st.session_state.step += 1

def reset_quiz():
    st.session_state.step = 1
    st.rerun()


# STEP 1: SEASONAL IMPRESSIONS
if st.session_state.step == 1:
    st.subheader("Step 1: Seasonal Environment")
    st.markdown("Select the primary climate or environment where you intend to wear this fragrance.")

    season_choice = st.radio(
        "Which setting matches your intent?",
        ["Warm Weather / Daytime Freshness", "Cold Weather / Evening Luxury", "All-Season Signature / Professional Setting"]
    )

    if season_choice == "Warm Weather / Daytime Freshness":
        st.session_state.season = "Clean / Fresh"
    elif season_choice == "Cold Weather / Evening Luxury":
        st.session_state.season = "Woody / Spicy"
    else:
        st.session_state.season = "Floral"

    st.markdown("---")
    st.button("Next Question", on_click=move_to_next_step)


# STEP 2: SCENT ACCORD SELECTION
elif st.session_state.step == 2:
    st.subheader("Step 2: Olfactive Component Preferences")
    st.markdown("Which raw ingredient note do you find most appealing?")

    note_choice = st.selectbox(
        "Choose a key anchor note for your formula:",
        ["Bergamot", "Vanilla", "Jasmine", "Sandalwood", "Amber", "Patchouli", "Rose", "Lemon"]
    )

    st.session_state.preferred_note = note_choice

    st.markdown("---")
    st.button("Next Question", on_click=move_to_next_step)


# STEP 3: FINANCIAL PARAMETERS
elif st.session_state.step == 3:
    st.subheader("Step 3: Budget Optimization")
    st.markdown("Set your maximum spending limit for a full 100ml retail bottle configuration.")

    price_choice = st.slider(
        "Maximum Price Limit (USD):",
        min_value=30,
        max_value=400,
        value=150,
        step=10
    )

    st.session_state.max_price = price_choice

    st.markdown("---")
    st.button("Generate My Match", on_click=move_to_next_step)


# STEP 4: RECOMMENDATION ENGINE OUTPUT
elif st.session_state.step == 4:
    st.subheader("Your Algorithmic Match Results")
    st.markdown("Our data engine evaluated your inputs against the active marketplace ledger.")

    filtered_df = df[df["price_usd_100ml"] <= st.session_state.max_price]

    if st.session_state.season in filtered_df["style_category"].values:
        filtered_df = filtered_df[filtered_df["style_category"] == st.session_state.season]

    note_keyword = st.session_state.preferred_note.lower()

    def matches_note(row):
        top = str(row.get("top_notes", "")).lower()
        heart = str(row.get("heart_notes", "")).lower()
        base = str(row.get("base_notes", "")).lower()
        return note_keyword in top or note_keyword in heart or note_keyword in base

    ingredient_matches = filtered_df[filtered_df.apply(matches_note, axis=1)]

    if not ingredient_matches.empty:
        final_selection = ingredient_matches.sort_values(by="rating", ascending=False).iloc[0]
        match_found = True
    elif not filtered_df.empty:
        final_selection = filtered_df.sort_values(by="rating", ascending=False).iloc[0]
        match_found = True
    else:
        match_found = False

    if match_found:
        st.info(f"Based on your preference for {st.session_state.preferred_note} profiles within a budget of ${st.session_state.max_price}, your optimal selection is:")

        st.markdown(f"### **{final_selection['name']}** by {final_selection['brand']}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Market Style Profile", final_selection["style_category"])
        col2.metric("Retail Price Point", f"${final_selection['price_usd_100ml']:.2f}")
        col3.metric("Consumer Rating Score", f"{final_selection['rating']}/5")

        st.markdown("#### Formula Structural Composition:")
        st.write(f"**Top Notes:** {final_selection.get('top_notes', 'N/A')}")
        st.write(f"**Heart Notes:** {final_selection.get('heart_notes', 'N/A')}")
        st.write(f"**Base Notes:** {final_selection.get('base_notes', 'N/A')}")

    else:
        st.warning("No exact matches found matching those specific tight budget limits. Try broadening your criteria.")

    st.markdown("---")
    st.button("Retake the Quiz", on_click=reset_quiz)
