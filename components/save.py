import streamlit as st

from components.db import save_user_project

def save_button():
    """Wywołuje funkcję zapisu projektu po kliknięciu przycisku."""
    if st.button("💾 Zapisz projekt"):
        user_id = st.session_state.get("user_id")
        canvas_data = st.session_state.get("canvas_data")
        agd_list = st.session_state.get("agd_list", [])
        if user_id and canvas_data is not None:
            save_user_project(user_id, canvas_data, agd_list)
            st.success("Projekt został zapisany pomyślnie!")
        else:
            st.error("Nie można zapisać projektu. Upewnij się, że jesteś zalogowany i masz narysowany rzut.")