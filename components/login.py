import streamlit as st
from components.db import supabase

def render_login_page():
    st.title("⚡ PowerPlanner – Logowanie")
    
    tab_login, tab_register = st.tabs(["Logowanie", "Rejestracja"])
    
    with tab_login:
        email = st.text_input("E-mail", key="login_email")
        password = st.text_input("Hasło", type="password", key="login_password")
        
        if st.button("Zaloguj się"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state["user_id"] = res.user.id
                st.session_state["user_email"] = res.user.email
                st.success("Zalogowano pomyślnie!")
                st.rerun()
            except Exception as e:
                st.error(f"Błąd logowania: {e}")
                
    with tab_register:
        reg_email = st.text_input("E-mail", key="reg_email")
        reg_password = st.text_input("Hasło (min. 6 znaków)", type="password", key="reg_password")
        
        if st.button("Zarejestruj się"):
            try:
                res = supabase.auth.sign_up({"email": reg_email, "password": reg_password, "options": {"emailRedirectTo": "http://localhost:8502"}})
                st.success("Rejestracja udana! Sprawdź skrzynkę e-mail, aby potwierdzić konto.")
            except Exception as e:
                st.error(f"Błąd rejestracji: {e}")