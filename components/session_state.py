import streamlit as st
from components.login import render_login_page
from components.save import save_button
from components.db import load_user_fuses, load_user_project

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
        "element_typ_radio": "Ściana / Pokój (Czarny)",  # Domyślnie wybrane ściany
        
        "data_loaded": False  # Flaga zapobiegająca ciągłemu odpytywaniu bazy
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def load_user_data_from_cloud(user_id: str):
    """Pobiera zapisane dane (bezpieczniki, rzut, AGD) z Supabase, ustawia statusy i przelicza obwody."""
    if not st.session_state.get("data_loaded", False):
        
        # 1. Pobieramy bezpieczniki
        fuses = load_user_fuses(user_id)
        if fuses:
            st.session_state["fuses_list"] = fuses
            st.session_state["fuses"] = fuses
        else:
            # Jeśli w bazie nic nie ma, zostawiamy pustą listę lub domyślne
            st.session_state["fuses_list"] = []
            
        # 2. Pobieramy projekt (rzut i AGD)
        project = load_user_project(user_id)
        if project:
            if project.get("canvas_json"):
                st.session_state["canvas_data"] = project.get("canvas_json")
                
            if project.get("agd_list_json"):
                loaded_agd = project.get("agd_list_json")
                
                # Zabezpieczamy każdy element AGD, aby interfejs widział go jako ZAPISANY
                for item in loaded_agd:
                    if isinstance(item, dict):
                        item["saved"] = True
                        item["status"] = "Zapisany"  # Najczęstszy string w takich tabelach
                        item["synced"] = True
                        
                st.session_state["agd_list"] = loaded_agd

        # 3. Automatyczne przeliczenie obwodów / obciążeń po wczytaniu
        try:
            # Jeśli masz w projekcie funkcję przeliczającą obwody, wywołaj ją tutaj, np.:
            # from components.calculations import recalculate_circuits
            # recalculate_circuits()
            pass
        except Exception as e:
            print(f"Błąd podczas automatycznego przeliczania obwodów: {e}")

        # Oznaczamy, że dane dla tej sesji zostały wczytane
        st.session_state["data_loaded"] = True

def manage_session():
    """Zarządza logowaniem oraz inicjalizuje stan aplikacji."""
    # Najpierw inicjalizujemy zmienne stanu z domyślnymi wartościami
    init_session_state()

    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None

    if not st.session_state["user_id"]:
        render_login_page()
        return None
    
    # Skoro użytkownik jest zalogowany, automatycznie wczytujemy jego dane z bazy
    load_user_data_from_cloud(st.session_state["user_id"])
    
    with st.sidebar:
        # Pobieramy bezpiecznie e-mail z sesji
        user_email = st.session_state.get('user_email', 'Użytkownik')
        st.write(f"Zalogowany: **{user_email}**")
        
        if st.button("Wyloguj się"):
            # Czyszczymy klucze sesji odpowiedzialne za login i dane
            st.session_state["user_id"] = None
            st.session_state["user_email"] = None
            st.session_state["user"] = None
            st.session_state["data_loaded"] = False
            
            # Resetujemy też do pustych wartości / domyślnych po wylogowaniu
            st.session_state["canvas_data"] = None
            st.session_state["agd_list"] = []
            st.session_state["fuses_list"] = []
            
            st.rerun()
            
        save_button()
            
    return st.session_state["user_id"]