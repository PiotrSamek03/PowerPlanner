import streamlit as st
from components.agd_colors import PALETA_AGD_SLOWNIK

def render_sidebar():
    with st.sidebar:
        st.header("📐 Skala i Rozmiar Obszaru")
        
        # Suwaki i ustawienia płótna
        st.slider("Szerokość obszaru (X)", min_value=500, max_value=1600, value=900, step=50, key="canvas_width_slider")
        st.slider("Wysokość obszaru (Y)", min_value=400, max_value=1200, value=600, step=50, key="canvas_height_slider")

        st.selectbox(
            "Tryb rysowania:",
            ("rect", "circle", "point", "freedraw", "line"),
            key="drawing_mode_selectbox"
        )
            
        st.slider("Grubość linii / rozmiar:", 2, 40, 10, key="stroke_width_slider")

        # Wybór typu rysowanego elementu
        element_typ = st.radio(
            "Co rysujesz?",
            [
                "Ściana / Pokój (Czarny)",
                "Gniazdko (Żółty)",
                "Sprzęt AGD / Światło (Własny kolor z palety)",
            ],
            key="element_typ_radio"
        )

        # Logika kolorów
        if element_typ == "Sprzęt AGD / Światło (Własny kolor z palety)":
            wybrana_nazwa = st.selectbox(
                "Wybierz kolor urządzenia:", 
                list(PALETA_AGD_SLOWNIK.keys()),
                key="wybrana_nazwa_agd_selectbox"
            )
            
            # Bezpieczne pobranie koloru ze słownika
            stroke_color = PALETA_AGD_SLOWNIK.get(wybrana_nazwa, "#0077b6")
            fill_color = stroke_color + "66"
            
            # Estetyczny podgląd koloru w sidebarze
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; background-color: #1e1e1e; padding: 8px 12px; border-radius: 6px; border: 1px solid #333; margin-top: -5px; margin-bottom: 10px;">
                    <div style="width: 28px; height: 28px; background-color: {stroke_color}; border-radius: 4px; border: 2px solid #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-size: 13px; font-weight: 600; color: #f0f0f0;">{wybrana_nazwa}</span>
                        <span style="font-size: 11px; color: #888; font-family: monospace;">{stroke_color}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        elif element_typ.startswith("Ściana"):
            stroke_color = "#000000"
            fill_color = "rgba(0, 0, 0, 0.1)"
        else:
            stroke_color = "#FFD700"
            fill_color = "rgba(255, 215, 0, 0.5)"

        # Zapis ostatecznych kolorów do sesji (z czego korzysta główny app.py)
        st.session_state.stroke_color_sidebar = stroke_color
        st.session_state.fill_color_sidebar = fill_color