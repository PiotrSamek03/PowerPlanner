import streamlit as st

def render_fuses_table(fuses_list):
    """Renderuje tabelę bezpieczników, obsługując zarówno obiekty, jak i słowniki z bazy."""
    if not fuses_list:
        st.info("Brak zdefiniowanych bezpieczników.")
        return

    st.subheader("⚡ Lista bezpieczników")
    
    # Przygotowujemy dane do wyświetlenia (np. DataFrame lub pętla)
    data = []
    for f in fuses_list:
        # Bezpieczne pobieranie danych niezależnie od tego, czy f to dict, czy obiekt klasy
        if isinstance(f, dict):
            name = f.get("name", "Brak nazwy")
            current_amp = f.get("current_amp", f.get("prad", 16))
        else:
            name = getattr(f, "name", getattr(f, "nazwa", "Brak nazwy"))
            current_amp = getattr(f, "current_amp", getattr(f, "prad", 16))
            
        data.append({"Nazwa": name, "Prąd (A)": current_amp})

    # Wyświetlamy tabelę w Streamlit
    st.table(data)