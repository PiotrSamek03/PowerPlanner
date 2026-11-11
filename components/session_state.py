import streamlit as st
from components.login import render_login_page

def init_session_state():
    """Inicjalizuje domyślne zmienne stanu sesji dla PowerPlannera."""
    defaults = {
        "fuses_list": [],
        "agd_list": [],
        "canvas_data": None,
        "prev_agd_count": 0,
        "temp_latest_obj_idx": 0,
        "pending_obj_index": None,
        "canvas_version": 0,
        "force_reload_canvas": False,
        "prev_total_objects": 0,
        "skip_save": False,
        "agd_color_counter": 0,

        "canvas_width_slider": 900,
        "canvas_height_slider": 600,
        "drawing_mode_selectbox": "rect",  # Domyślnie prostokąt do ścian
        "stroke_width_slider": 10,
        "element_typ_radio": "Ściana / Pokój (Czarny)"  # Domyślnie wybrane ściany
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def manage_session():
    """Zarządza logowaniem oraz inicjalizuje stan aplikacji."""
    # Najpierw inicjalizujemy zmienne stanu
    init_session_state()

    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"] is None:
        render_login_page()
        return None
    
    with st.sidebar:
        st.write(f"Zalogowany: **{st.session_state['user'].email}**")
        if st.button("Wyloguj się"):
            st.session_state["user"] = None
            st.rerun()
            
    return st.session_state["user"]