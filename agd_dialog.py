import streamlit as st

def handle_dialog_dismiss():
    # Jeśli zamknięto okienko przez "X" lub poza nim, usuwamy obiekt
    idx_to_remove = st.session_state.pending_obj_index
    if idx_to_remove is not None and st.session_state.canvas_data and "objects" in st.session_state.canvas_data:
        if idx_to_remove < len(st.session_state.canvas_data["objects"]):
            st.session_state.canvas_data["objects"].pop(idx_to_remove)
    
    st.session_state.pending_obj_index = None
    st.session_state.canvas_version += 1  # Wymusza fizyczne wyczyszczenie elementu w przeglądarce
    
    # Synchronizujemy licznik obiektów
    if st.session_state.canvas_data:
        objs = st.session_state.canvas_data.get("objects", [])
        agd_indices = [i for i, obj in enumerate(objs) if obj.get("stroke") == "#0000FF"]
        st.session_state.prev_agd_count = len(agd_indices)

# Definicja okna dialogowego do dodawania AGD z on_dismiss
@st.dialog("Dodaj nowe AGD", on_dismiss=handle_dialog_dismiss)
def AGD_fill():
    st.write("Wprowadź parametry dla nowo narysowanego urządzenia AGD:")
    agd_name = st.text_input("Nazwa AGD", key="input_agd_name")
    moc = st.number_input("Moc znamionowa (W)", min_value=1, max_value=10000, value=2200, key="input_agd_moc")
    
    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("Zapisz w bazie"):
            if agd_name.strip():
                st.session_state.agd_list.append({
                    "text": agd_name.strip(), 
                    "moc": moc,
                    "object_index": st.session_state.pending_obj_index
                })
                st.session_state.pending_obj_index = None
                
                if st.session_state.canvas_data:
                    objs = st.session_state.canvas_data.get("objects", [])
                    agd_indices = [i for i, obj in enumerate(objs) if obj.get("stroke") == "#0000FF"]
                    st.session_state.prev_agd_count = len(agd_indices)
                    
                st.success(f"Dodano AGD: {agd_name} ({moc} W)")
                st.rerun()
            else:
                st.error("Podaj nazwę AGD!")
                
    with col_cancel:
        if st.button("Anuluj"):
            handle_dialog_dismiss()
            st.rerun()
