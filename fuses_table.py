import streamlit as st

def render_fuses_table(fuses_list):
    if not fuses_list:
        st.warning("Nie dodano jeszcze żadnych bezpieczników.")
    else:
        dane = [
            {
                "Nazwa": f.name, 
                "Prąd znamionowy (A)": f.amps, 
                "Stan": f.state, 
                "Przypisane elementy": len(f.attached_elements)
            } 
            for f in fuses_list
        ]
        st.table(dane)