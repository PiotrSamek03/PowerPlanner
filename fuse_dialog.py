import streamlit as st
from fuse import Fuse

@st.dialog("Dodaj nowy bezpiecznik")
def fuse_fill():
    st.write("Dodaj nowy bezpiecznik do listy:")
    nazwa_bezpiecznika = st.text_input("Nazwa bezpiecznika")
    prad_znamionowy = st.number_input(
        "Prąd znamionowy (A)", min_value=1, max_value=100, value=16
    )

    if st.button("Zapisz w bazie"):
        if nazwa_bezpiecznika:
            new_fuse = Fuse(nazwa_bezpiecznika, prad_znamionowy)
            st.session_state.fuses_list.append(new_fuse)
            st.success(
                f"Dodano bezpiecznik: {nazwa_bezpiecznika}"
                f" ({prad_znamionowy} A)"
            )
            st.rerun()
        else:
            st.error("Podaj nazwę bezpiecznika!")
