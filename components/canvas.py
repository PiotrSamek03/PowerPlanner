import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from components.agd_colors import PALETA_AGD_SLOWNIK

def render_floor_plan_canvas():
    blank_image = Image.new("RGB", (st.session_state.canvas_width_slider, st.session_state.canvas_height_slider), color="white")
    canvas_inicjalny = st.session_state.canvas_data if st.session_state.get("force_reload_canvas", False) else None
    st.session_state.force_reload_canvas = False
    
    canvas_result = st_canvas(
        fill_color=st.session_state.fill_color_sidebar,
        stroke_width=st.session_state.stroke_width_slider,
        stroke_color= st.session_state.stroke_color_sidebar,
        background_image=blank_image,
        initial_drawing=st.session_state.canvas_data,
        update_streamlit=True,
        drawing_mode=st.session_state.drawing_mode_selectbox,
        point_display_radius=st.session_state.stroke_width_slider if st.session_state.drawing_mode_selectbox == 'point' else 0,
        width=st.session_state.canvas_width_slider,
        height=st.session_state.canvas_height_slider,
        key=f"stabilna_mapa_canvas_{st.session_state.canvas_version}",
    )
    
    if canvas_result.json_data is not None:
        nowe_obiekty = canvas_result.json_data.get("objects", [])
        stary_stan = st.session_state.get("canvas_data")
        stara_lista_obj = stary_stan.get("objects", []) if stary_stan and "objects" in stary_stan else []
            
        # Zabezpieczenie przed gubieniem/miganiem obiektów przy szybkim rysowaniu:
        # Akceptujemy nowy stan, jeśli liczba obiektów jest większa/równa lub stara lista była pusta.
        # Chroni to przed sytuacją, gdy szybki ruch wyśle tymczasowo niepełny JSON.
        if len(nowe_obiekty) >= len(stara_lista_obj) or len(stara_lista_obj) == 0:
            st.session_state.canvas_data = canvas_result.json_data

    if st.button("💾 Zatwierdź rzut i przejdź do konfiguracji urządzeń", type="primary"):
        if st.session_state.get("canvas_data") and "objects" in st.session_state["canvas_data"]:
            objects = st.session_state["canvas_data"]["objects"]
            
            agd_objects = []
            for i, obj in enumerate(objects):
                kolor_obiektu = obj.get("stroke", "")
                if kolor_obiektu in PALETA_AGD_SLOWNIK.values():
                    agd_objects.append((i, obj))
            
            if len(agd_objects) == 0:
                st.warning("⚠️ Nie narysowano żadnego sprzętu AGD z wybranej palety na mapie!")
            else:
                new_agd_list = []
                for idx, (obj_idx, obj) in enumerate(agd_objects):
                    kolor = obj.get("stroke", "#0077b6")
                    new_agd_list.append({
                        "object_index": obj_idx,
                        "text": f"Urządzenie AGD #{idx + 1}",
                        "moc": 0,
                        "fuse_id": None,
                        "color": kolor
                    })
                
                st.session_state.agd_list = new_agd_list
                st.success(f"✅ Zatwierdzono! Wykryto {len(agd_objects)} urządzeń do konfiguracji poniżej.")
                st.rerun()
        else:
            st.warning("⚠️ Płótno jest puste.")    