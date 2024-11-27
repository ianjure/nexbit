import streamlit as st

# [STREAMLIT] PAGE CONFIGURATION
st.set_page_config(page_title="Nexbit", page_icon="🪙")

st.write("nexbit")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Bitcoin")
with col2:
    with st.popover("Change Crypto"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")
with col3:
    st.metric("Prediction", "70 °F", "1.2 °F")
