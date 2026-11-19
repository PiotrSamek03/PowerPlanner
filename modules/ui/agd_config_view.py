import streamlit as st
from modules.constants.agd_colors import PALETA_AGD_SLOWNIK
from modules.logic.agd_sync import AgdSynchronizer
from modules.state.canvas_state import CanvasStateManager

def render_agd_config():
    if not st.session_state.agd_list:
        st.info("ℹNie zatwierdzono jeszcze żadnego sprzętu AGD. Narysuj elementy na mapie i kliknij przycisk zatwierdzenia powyżej.")
        return

    odwrocony_slownik = AgdSynchronizer.get_reversed_palette()
    color_names = list(PALETA_AGD_SLOWNIK.keys())

    if st.button("Zapisz wszystkie zmiany", type="primary", use_container_width=True):
        updates = []
        for idx, agd in enumerate(st.session_state.agd_list):
            wybrana_nazwa_koloru = st.session_state.get(f"select_color_{idx}", color_names[0])
            updates.append({
                "idx": idx,
                "text": st.session_state.get(f"name_{idx}", agd.get("text", "")),
                "color": PALETA_AGD_SLOWNIK.get(wybrana_nazwa_koloru, "#0077b6"),
                "moc": st.session_state.get(f"moc_{idx}", int(agd.get("moc", 0))),
                "fuse_name": st.session_state.get(f"fuse_{idx}", None),
            })

        updated_agd, updated_canvas = AgdSynchronizer.apply_updates(
            st.session_state.agd_list,
            st.session_state.canvas_data,
            updates
        )
        CanvasStateManager.save_agd_and_canvas_updates(updated_agd, updated_canvas)

        st.success("Pomyślnie zapisano zmiany dla wszystkich urządzeń!")
        st.rerun()

    st.markdown("")

    header_cols = st.columns([3, 3, 1.5, 2.5, 1])
    header_cols[0].markdown("**Nazwa urządzenia**")
    header_cols[1].markdown("**Kolor (z podglądem)**")
    header_cols[2].markdown("**Moc (W)**")
    header_cols[3].markdown("**Bezpiecznik**")
    header_cols[4].markdown("**Status**")

    fuses_options = [
        f.name if hasattr(f, "name") else (f.get("name", f"Bezpiecznik {i+1}") if isinstance(f, dict) else str(f))
        for i, f in enumerate(st.session_state.fuses_list)
    ]

    for idx, agd in enumerate(st.session_state.agd_list):
        obj_idx = agd.get("object_index", 0)
        row_cols = st.columns([3, 3, 1.5, 2.5, 1])

        with row_cols[0]:
            nowa_nazwa = st.text_input(
                "Nazwa",
                value=agd.get("text", f"Urządzenie #{idx+1}"),
                key=f"name_{idx}",
                label_visibility="collapsed"
            )

        with row_cols[1]:
            current_color = agd.get("color", "#0077b6")
            if st.session_state.canvas_data and "objects" in st.session_state.canvas_data:
                if obj_idx < len(st.session_state.canvas_data["objects"]):
                    current_color = st.session_state.canvas_data["objects"][obj_idx].get("stroke", current_color)

            aktualna_nazwa_koloru = odwrocony_slownik.get(current_color, color_names[0])
            wybrana_nowa_nazwa = st.selectbox(
                "Kolor",
                color_names,
                index=color_names.index(aktualna_nazwa_koloru) if aktualna_nazwa_koloru in PALETA_AGD_SLOWNIK else 0,
                key=f"select_color_{idx}",
                label_visibility="collapsed"
            )
            new_color = PALETA_AGD_SLOWNIK[wybrana_nowa_nazwa]

            st.markdown(
                f"""<div style="display: flex; align-items: center; gap: 6px; margin-top: -6px; margin-bottom: 5px;">
                    <div style="width: 14px; height: 14px; background-color: {new_color}; border-radius: 3px; border: 1px solid #fff;"></div>
                    <span style="font-size: 11px; color: #888; font-family: monospace;">{new_color}</span>
                </div>""",
                unsafe_allow_html=True
            )

        with row_cols[2]:
            moc_val = st.number_input(
                "Moc",
                min_value=0,
                max_value=15000,
                step=100,
                value=int(agd.get("moc", 0)),
                key=f"moc_{idx}",
                label_visibility="collapsed"
            )

        with row_cols[3]:
            if fuses_options:
                current_fuse = agd.get("fuse_name", fuses_options[0])
                wybrany_bezpiecznik = st.selectbox(
                    "Bezpiecznik",
                    fuses_options,
                    index=fuses_options.index(current_fuse) if current_fuse in fuses_options else 0,
                    key=f"fuse_{idx}",
                    label_visibility="collapsed"
                )
            else:
                st.caption("Brak bezpieczników")
                wybrany_bezpiecznik = None

        czy_zmienione = AgdSynchronizer.has_unsaved_changes(
            agd, nowa_nazwa, new_color, moc_val, wybrany_bezpiecznik
        )

        with row_cols[4]:
            if czy_zmienione:
                st.markdown("<div style='padding-top: 6px; font-size: 18px; text-align: center;' title='Niezapisane zmiany'>❌</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='padding-top: 6px; font-size: 18px; text-align: center;' title='Wszystko zapisane'></div>", unsafe_allow_html=True)