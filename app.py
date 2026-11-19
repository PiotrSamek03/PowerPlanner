import streamlit as st

st.set_page_config(page_title="Kreator Rzutu Mieszkania", layout="wide")

from modules.state.session_manager import SessionManager
from modules.ui.login_view import render_login_page
from modules.ui.user_sidebar_view import render_user_sidebar
from modules.ui.sidebar_view import render_sidebar
from modules.ui.fuse_dialog_view import fuse_fill
from modules.ui.fuses_table_view import render_fuses_table
from modules.ui.canvas_view import render_floor_plan_canvas
from modules.ui.agd_config_view import render_agd_config
from modules.ui.calculations_view import render_calculations_section

user_id = SessionManager.ensure_session_initialized()

if not user_id:
    render_login_page()
else:
    render_user_sidebar()
    render_sidebar()

    st.title("PowerPlanner")
    st.markdown("Stwórz pomocniczy rzut mieszkania i sprawdź obciążenie obwodów elektrycznych w 4 prostych krokach.")

    st.markdown("1. Dodaj bezpieczniki do listy, aby móc przypisywać je do obwodów elektrycznych.")
    if len(st.session_state.fuses_list) == 0:
        st.warning("Nie dodano jeszcze żadnego bezpiecznika. Kliknij przycisk poniżej, aby dodać nowy bezpiecznik.")

    if st.button("Dodaj bezpiecznik", icon=":material/add:"):
        fuse_fill()

    st.subheader("Lista bezpieczników i obwodów")
    render_fuses_table(st.session_state.fuses_list)

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
        * **Naprawa migania / błędów:** W razie migającego elementu na mapie, wciśnij przycisk "Reset canvas & history" w menu nad białym płótnem – usunie to ostatnio narysowany element.
        """)

    render_floor_plan_canvas()

    st.markdown("---")
    st.subheader("Krok 3: Konfiguracja urządzeń i przypisanie do obwodów")
    render_agd_config()

    st.markdown("")
    render_calculations_section()