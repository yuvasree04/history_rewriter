import streamlit as st
from history_backend import generate_histories

# Streamlit frontend
st.title("AI-Powered History Rewriter")
st.write("Personalize your alternate history by selecting your age group and a historical role, then enter a 'What-If' scenario!")
st.write("If the original history doesn't show, check the Command Prompt for the 'Raw API Response' to debug.")

# Layout personalization options in columns
col1, col2 = st.columns(2)
with col1:
    age_group = st.selectbox("Select Age Group:", ["Child", "Teen", "Adult"])
with col2:
    historical_role = st.selectbox("Select Historical Role:", ["Explorer", "Ruler", "Scientist", "Philosopher", "Warrior"])

scenario = st.text_input("Your Scenario (e.g., What if India hadn’t gained independence till now?):", "")
if st.button("Rewrite History"):
    if not scenario.strip():
        st.error("Please enter a valid scenario.")
    else:
        with st.spinner("Generating histories..."):
            original_history, alternate_history = generate_histories(scenario, age_group, historical_role)
            # Display Original History title and content
            # Add some spacing between sections
            st.markdown("<br>", unsafe_allow_html=True)
            # Display Alternate History title and content
            if "Unable to extract" in alternate_history or "Error" in alternate_history:
                st.error(alternate_history)
            else:
                st.write(alternate_history)