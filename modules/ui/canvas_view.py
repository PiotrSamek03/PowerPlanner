import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from modules.logic.canvas_parser import CanvasParser
from modules.state.canvas_state import CanvasStateManager
from modules.logic.drawing_styles import DrawingStyleResolver


def _attach_agd_labels(canvas_data: dict, agd_list: list) -> dict:
    base_objects = [
        obj for obj in canvas_data.get("objects", [])
        if not obj.get("is_agd_label")
    ]
    labels = [
        DrawingStyleResolver.create_agd_index_object(
            item["agd_number"],
            item["center"][0],
            item["center"][1],
        )
        for item in agd_list
        if item.get("center")
    ]
    return {**canvas_data, "objects": base_objects + labels}


def render_floor_plan_canvas():
    blank_image = Image.new(
        "RGB",
        (st.session_state.canvas_width_slider, st.session_state.canvas_height_slider),
        color="white",
    )
    st.session_state.force_reload_canvas = False

    canvas_result = st_canvas(
        fill_color=st.session_state.fill_color_sidebar,
        stroke_width=st.session_state.stroke_width_slider,
        stroke_color=st.session_state.stroke_color_sidebar,
        background_image=blank_image,
        initial_drawing=st.session_state.canvas_data,
        update_streamlit=True,
        drawing_mode=st.session_state.drawing_mode_selectbox,
        point_display_radius=st.session_state.stroke_width_slider if st.session_state.drawing_mode_selectbox == "point" else 0,
        width=st.session_state.canvas_width_slider,
        height=st.session_state.canvas_height_slider,
        key=f"stabilna_mapa_canvas_{st.session_state.canvas_version}",
    )

    if canvas_result.json_data is not None:
        CanvasStateManager.update_canvas_data(canvas_result.json_data)

    if st.button("Zatwierdź rzut i przejdź do konfiguracji urządzeń", type="primary"):
        canvas_data = st.session_state.get("canvas_data")
        if not canvas_data or "objects" not in canvas_data:
            st.warning("⚠️ Płótno jest puste.")
            return

        new_agd_list = CanvasParser.parse_canvas_data(canvas_data)

        if not new_agd_list:
            st.warning("⚠️ Nie narysowano żadnego sprzętu AGD z wybranej palety na mapie!")
        else:
            updated_canvas_data = _attach_agd_labels(canvas_data, new_agd_list)
            CanvasStateManager.update_canvas_data(updated_canvas_data)
            CanvasStateManager.set_agd_list(new_agd_list)
            st.session_state.canvas_version += 1
            st.success(f"Zatwierdzono! Wykryto {len(new_agd_list)} urządzeń do konfiguracji poniżej.")
            st.rerun()