import streamlit as st
from modules.services.auth_service import AuthService
from modules.state.session_manager import SessionManager

def render_login_page():
    st.title("PowerPlanner – Logowanie")
    
    tab_login, tab_register = st.tabs(["Logowanie", "Rejestracja"])
    
    with tab_login:
        email = st.text_input("E-mail", key="login_email")
        password = st.text_input("Hasło", type="password", key="login_password")
        
        if st.button("Zaloguj się"):
            try:
                user_data = AuthService.login(email, password)
                SessionManager.login_user(user_data)
                st.success("Zalogowano pomyślnie!")
                st.rerun()
            except Exception as e:
                st.error(f"Błąd logowania: {e}")
                
    with tab_register:
        reg_email = st.text_input("E-mail", key="reg_email")
        reg_password = st.text_input("Hasło (min. 6 znaków)", type="password", key="reg_password")
        
        if st.button("Zarejestruj się"):
            try:
                AuthService.register(reg_email, reg_password)
                st.success("Rejestracja udana! Sprawdź skrzynkę e-mail, aby potwierdzić konto.")
            except Exception as e:
                st.error(f"Błąd rejestracji: {e}")