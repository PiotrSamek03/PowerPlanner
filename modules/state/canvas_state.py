import streamlit as st

class CanvasStateManager:
    @staticmethod
    def update_canvas_data(new_json_data: dict):
        if new_json_data is None:
            return
            
        nowe_obiekty = new_json_data.get("objects", [])
        stary_stan = st.session_state.get("canvas_data")
        stara_lista_obj = stary_stan.get("objects", []) if stary_stan and "objects" in stary_stan else []

        # Zabezpieczenie przed gubieniem obiektów przy szybkim rysowaniu
        if len(nowe_obiekty) >= len(stara_lista_obj) or len(stara_lista_obj) == 0:
            st.session_state.canvas_data = new_json_data

    @staticmethod
    def set_agd_list(agd_list: list):
        st.session_state.agd_list = agd_list

    @staticmethod
    def save_agd_and_canvas_updates(updated_agd_list: list, updated_canvas_data: dict):
        st.session_state.agd_list = updated_agd_list
        st.session_state.canvas_data = updated_canvas_data
        st.session_state.canvas_version += 1