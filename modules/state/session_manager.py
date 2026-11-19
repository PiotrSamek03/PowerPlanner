import streamlit as st
from modules.state.init_state import init_session_state
from modules.state.user_data_state import load_user_data_from_cloud

class SessionManager:
    @staticmethod
    def login_user(user_data: dict):
        st.session_state["user_id"] = user_data["user_id"]
        st.session_state["user_email"] = user_data["user_email"]
        st.session_state["data_loaded"] = False

    @staticmethod
    def logout_user():
        """Czyści dane użytkownika i stan projektu przy wylogowaniu."""
        st.session_state["user_id"] = None
        st.session_state["user_email"] = None
        st.session_state["user"] = None
        st.session_state["data_loaded"] = False

        st.session_state["canvas_data"] = None
        st.session_state["agd_list"] = []
        st.session_state["fuses_list"] = []
        st.session_state["fuses"] = []

    @staticmethod
    def ensure_session_initialized() -> str | None:
        """Inicjalizuje stan domyślny i ładuje dane z chmury, jeśli użytkownik jest zalogowany."""
        init_session_state()

        if "user_id" not in st.session_state:
            st.session_state["user_id"] = None

        user_id = st.session_state["user_id"]
        if user_id:
            load_user_data_from_cloud(user_id)

        return user_id

    @staticmethod
    def get_user_id():
        return st.session_state.get("user_id")

    @staticmethod
    def add_fuse_to_state(fuse):
        if "fuses_list" not in st.session_state:
            st.session_state.fuses_list = []
        st.session_state.fuses_list.append(fuse)
        st.session_state["fuses"] = st.session_state.fuses_list

        