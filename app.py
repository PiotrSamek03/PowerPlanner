import streamlit as st

st.set_page_config(page_title="Kreator Rzutu Mieszkania", layout="wide")

import components.fuses_table as fuses_table
from components.fuse_dialog import fuse_fill
from components.session_state import manage_session
from components.sidebar import render_sidebar
from components.agd_config import render_agd_config
from components.calculations import calculate_load_and_check_errors
from components.canvas import render_floor_plan_canvas

user = manage_session()

if user:
    st.title("⚡ PowerPlanner")
    st.markdown("stwórz pomocniczy rzut mieszkania i sprawdź obciążenie obwodów elektrycznych w 4 prostych krokach")

    st.markdown("1. Dodaj bezpieczniki do listy, aby móc przypisywać je do obwodów elektrycznych.")
    if len(st.session_state.fuses_list) == 0:
        st.warning("Nie dodano jeszcze żadnego bezpiecznika. Kliknij przycisk poniżej, aby dodać nowy bezpiecznik.")

    if st.button("Dodaj bezpiecznik", icon=":material/add:"):
        fuse_fill()

    st.subheader("📋 Lista bezpieczników i obwodów")
    fuses_table.render_fuses_table(st.session_state.fuses_list)


    render_sidebar()

    st.markdown("2. Narysuj obszar mieszkania i dodaj sprzęt AGD oraz gniazdka (pamiętaj o uwzględnieniu oświetlenia).")

    st.markdown(
        """
        <style>
        [data-testid="stExpander"] {
            background-color: #3b82f633 !important; 
            border: 2px solid #60a5fa !important;     
            border-radius: 8px !important;
        }
        [data-testid="stExpander"] summary span, 
        [data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p,
        [data-testid="stExpander"] ul li {
            color: #ffffff !important;
        }
        [data-testid="stExpander"] svg {
            fill: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.expander("📖 Instrukcja obsługi i rozwiązywanie problemów"):
        st.markdown("""
        * **Wybieranie kolorów:** Wybieraj kolory sprzętu AGD z bezpiecznej palety w menu bocznym.
        * **Przesuwanie obiektu:** Kliknij przycisk "Edit" w menu nad białym płótnem, a następnie kliknij na obiekt.
        * **Usuwanie obiektu:** Kliknij przycisk "Edit", zaznacz element i wybierz "Delete" w menu nad białym płótnem.
        * **Powrót do rysowania:** W celu dalszego rysowania po przesunięciu lub usunięciu obiektu, naciśnij ikonkę z piórem "Edit" jeszcze raz.
        * **Naprawa migania / błędów:** W razie migającego elementu na mapie, wciśnij przycisk "Reset canvas & history" w menu nad białym płutnem – usunie to ostatnio narysowany element.
        """)

    render_floor_plan_canvas()

    st.markdown("---")
    st.subheader("⚙️ Krok 3: Konfiguracja urządzeń i przypisanie do obwodów")

    render_agd_config()

    st.markdown("")

    calculate_load_and_check_errors()