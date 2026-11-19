import streamlit as st
from modules.state.session_manager import SessionManager
from modules.ui.save_view import save_button

def render_user_sidebar():
    with st.sidebar:
        user_email = st.session_state.get("user_email", "Użytkownik")
        st.write(f"Zalogowany: **{user_email}**")

        if st.button("Wyloguj się"):
            SessionManager.logout_user()
            st.rerun()

        save_button()