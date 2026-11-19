import streamlit as st
from modules.models.fuse import Fuse
from modules.services import fuse_service

@st.dialog("Dodaj nowy bezpiecznik")
def fuse_fill():
    st.write("Dodaj nowy bezpiecznik do listy:")
    nazwa_bezpiecznika = st.text_input("Nazwa bezpiecznika")
    prad_znamionowy = st.number_input(
        "Prąd znamionowy (A)", min_value=1, max_value=100, value=16
    )

    if st.button("Zapisz bezpiecznik"):
        if nazwa_bezpiecznika:
            user_id = st.session_state.get("user_id")
            if not user_id:
                st.error("Błąd: Brak zalogowanego użytkownika!")
                return
            
            try:
                saved_fuse = fuse_service.add_fuse_to_db(user_id, nazwa_bezpiecznika, prad_znamionowy)
                
                if saved_fuse:
                    st.session_state.fuses_list.append(saved_fuse)
                else:
                    new_fuse = Fuse(nazwa_bezpiecznika, prad_znamionowy)
                    st.session_state.fuses_list.append(new_fuse)
                
                st.session_state["fuses"] = st.session_state.fuses_list

                st.success(f"Dodano bezpiecznik: {nazwa_bezpiecznika} ({prad_znamionowy} A)")
                st.rerun()
                
            except Exception as e:
                st.error(f"Błąd zapisu bezpiecznika w bazie: {e}")
        else:
            st.error("Podaj nazwę bezpiecznika!")
