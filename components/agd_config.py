import streamlit as st
from components.agd_colors import PALETA_AGD_SLOWNIK
from streamlit_drawable_canvas import st_canvas

def render_agd_config():
    if len(st.session_state.agd_list) > 0:
        odwrocony_slownik = {v: k for k, v in PALETA_AGD_SLOWNIK.items()}
        
        if st.button("💾 Zapisz wszystkie zmiany", type="primary", use_container_width=True):
            for idx, agd in enumerate(st.session_state.agd_list):
                obj_idx = agd.get("object_index", 0)
                
                nowa_nazwa = st.session_state.get(f"name_{idx}", agd.get("text", ""))
                wybrana_nazwa_koloru = st.session_state.get(f"select_color_{idx}", list(PALETA_AGD_SLOWNIK.keys())[0])
                new_color = PALETA_AGD_SLOWNIK.get(wybrana_nazwa_koloru, "#0077b6")
                moc_val = st.session_state.get(f"moc_{idx}", int(agd.get("moc", 0)))
                wybrany_bezpiecznik = st.session_state.get(f"fuse_{idx}", None)
                
                st.session_state.agd_list[idx]["text"] = nowa_nazwa
                st.session_state.agd_list[idx]["moc"] = moc_val
                st.session_state.agd_list[idx]["color"] = new_color
                if wybrany_bezpiecznik:
                    st.session_state.agd_list[idx]["fuse_name"] = wybrany_bezpiecznik
                
                if st.session_state.canvas_data and "objects" in st.session_state.canvas_data:
                    if obj_idx < len(st.session_state.canvas_data["objects"]):
                        st.session_state.canvas_data["objects"][obj_idx]["stroke"] = new_color
                        st.session_state.canvas_data["objects"][obj_idx]["fill"] = new_color + "66"
            
            st.session_state.canvas_version += 1
            st.success("✅ Pomyślnie zapisano zmiany dla wszystkich urządzeń!")
            st.rerun()

        st.markdown("")

        header_cols = st.columns([3, 3, 1.5, 2.5, 1])
        header_cols[0].markdown("**Nazwa urządzenia**")
        header_cols[1].markdown("**Kolor (z podglądem)**")
        header_cols[2].markdown("**Moc (W)**")
        header_cols[3].markdown("**Bezpiecznik**")
        header_cols[4].markdown("**Status**")

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
                
                aktualna_nazwa_koloru = odwrocony_slownik.get(current_color, list(PALETA_AGD_SLOWNIK.keys())[0])
                wybrana_nowa_nazwa = st.selectbox(
                    "Kolor", 
                    list(PALETA_AGD_SLOWNIK.keys()), 
                    index=list(PALETA_AGD_SLOWNIK.keys()).index(aktualna_nazwa_koloru) if aktualna_nazwa_koloru in PALETA_AGD_SLOWNIK else 0,
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
                fuses_options = []
                for i, f in enumerate(st.session_state.fuses_list):
                    if hasattr(f, "name"):
                        fuses_options.append(f.name)
                    elif isinstance(f, dict):
                        fuses_options.append(f.get("name", f"Bezpiecznik {i+1}"))
                    else:
                        fuses_options.append(str(f))
                
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

            saved_name = agd.get("text")
            saved_color = agd.get("color")
            saved_moc = agd.get("moc", 0)
            saved_fuse = agd.get("fuse_name")

            czy_zmienione = (
                nowa_nazwa != saved_name or
                new_color != saved_color or
                int(moc_val) != int(saved_moc) or
                wybrany_bezpiecznik != saved_fuse
            )

            with row_cols[4]:
                if czy_zmienione:
                    st.markdown("<div style='padding-top: 6px; font-size: 18px; text-align: center;' title='Niezapisane zmiany'>❌</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='padding-top: 6px; font-size: 18px; text-align: center;' title='Wszystko zapisane'>✅</div>", unsafe_allow_html=True)
    else:
        st.info("ℹ️ Nie zatwierdzono jeszcze żadnego sprzętu AGD. Narysuj elementy na mapie i kliknij przycisk zatwierdzenia powyżej.")