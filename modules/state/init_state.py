import streamlit as st

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
        "drawing_mode_selectbox": "rect",
        "stroke_width_slider": 10,
        "element_typ_radio": "Ściana / Pokój (Czarny)",
        
        "data_loaded": False  # Flaga zapobiegająca ciągłemu odpytywaniu bazy
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value