from agd import Agd
from agd_dialog import AGD_fill
from fuse import Fuse
import fuses_table
from PIL import Image
import reflex as rx
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from fuse_dialog import fuse_fill
from agd_colors import PALETA_AGD_SLOWNIK

st.set_page_config(page_title="Kreator Rzutu Mieszkania", layout="wide")

st.title("🛠️ Projektant Rzutu i Obwodów Elektrycznych")
st.markdown("stwórz pomocniczy rzut mieszkania i sprawdź obciążenie obwodów elektrycznych w 4 prostych krokach")

if "fuses_list" not in st.session_state:
    st.session_state.fuses_list = []
if "agd_list" not in st.session_state:
    st.session_state.agd_list = []
if "canvas_data" not in st.session_state:
    st.session_state.canvas_data = None
if "prev_agd_count" not in st.session_state:
    st.session_state.prev_agd_count = 0
if "temp_latest_obj_idx" not in st.session_state:
    st.session_state.temp_latest_obj_idx = 0
if "pending_obj_index" not in st.session_state:
    st.session_state.pending_obj_index = None
if "canvas_version" not in st.session_state:
    st.session_state.canvas_version = 0
if "force_reload_canvas" not in st.session_state:
    st.session_state.force_reload_canvas = False
if "prev_total_objects" not in st.session_state:
    st.session_state.prev_total_objects = 0
if "skip_save" not in st.session_state:
    st.session_state.skip_save = False
if "agd_color_counter" not in st.session_state:
    st.session_state.agd_color_counter = 0


if st.session_state.pending_obj_index is not None:
    AGD_fill()

st.markdown("1. Dodaj bezpieczniki do listy, aby móc przypisywać je do obwodów elektrycznych.")
if len(st.session_state.fuses_list) == 0:
    st.warning("Nie dodano jeszcze żadnego bezpiecznika. Kliknij przycisk poniżej, aby dodać nowy bezpiecznik.")

if st.button("Dodaj bezpiecznik", icon=":material/add:"):
    fuse_fill()

st.subheader("📋 Lista bezpieczników i obwodów")
fuses_table.render_fuses_table(st.session_state.fuses_list)


with st.sidebar:
    st.header("📐 Skala i Rozmiar Obszaru")
    canvas_width = st.slider("Szerokość obszaru (X)", min_value=500, max_value=1600, value=900, step=50)
    canvas_height = st.slider("Wysokość obszaru (Y)", min_value=400, max_value=1200, value=600, step=50)

    drawing_mode = st.selectbox(
        "Tryb rysowania:",
        ("rect", "circle", "point", "freedraw", "line")
    )
    
    stroke_width = st.slider("Grubość linii / rozmiar:", 2, 40, 10)

    element_typ = st.radio(
        "Co rysujesz?",
        [
            "Ściana / Pokój (Czarny)",
            "Gniazdko (Żółty)",
            "Sprzęt AGD / Światło (Własny kolor z palety)",
        ]
    )

    if element_typ == "Sprzęt AGD / Światło (Własny kolor z palety)":
        wybrana_nazwa = st.selectbox(
            "Wybierz kolor urządzenia:", 
            list(PALETA_AGD_SLOWNIK.keys())
        )
        stroke_color = PALETA_AGD_SLOWNIK[wybrana_nazwa]
    
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
    
        fill_color = stroke_color + "66"
    elif element_typ.startswith("Ściana"):
        stroke_color = "#000000"
        fill_color = "rgba(0, 0, 0, 0.1)"
    else:
        stroke_color = "#FFD700"
        fill_color = "rgba(255, 215, 0, 0.5)"

blank_image = Image.new("RGB", (canvas_width, canvas_height), color="white")

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

canvas_inicjalny = st.session_state.canvas_data if st.session_state.get("force_reload_canvas", False) else None
st.session_state.force_reload_canvas = False

canvas_result = st_canvas(
    fill_color=fill_color,
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_image=blank_image,
    initial_drawing=st.session_state.canvas_data,
    update_streamlit=True,
    drawing_mode=drawing_mode,
    point_display_radius=stroke_width if drawing_mode == 'point' else 0,
    width=canvas_width,
    height=canvas_height,
    key=f"stabilna_mapa_canvas_{st.session_state.canvas_version}",
)

if canvas_result.json_data is not None:
    nowe_obiekty = canvas_result.json_data.get("objects", [])
    stary_stan = st.session_state.get("canvas_data")
    stara_lista_obj = stary_stan.get("objects", []) if stary_stan and "objects" in stary_stan else []
    
    # Zabezpieczenie przed gubieniem/miganiem obiektów przy szybkim rysowaniu:
    # Akceptujemy nowy stan, jeśli liczba obiektów jest większa/równa lub stara lista była pusta.
    # Chroni to przed sytuacją, gdy szybki ruch wyśle tymczasowo niepełny JSON.
    if len(nowe_obiekty) >= len(stara_lista_obj) or len(stara_lista_obj) == 0:
        st.session_state.canvas_data = canvas_result.json_data


if st.button("💾 Zatwierdź rzut i przejdź do konfiguracji urządzeń", type="primary"):
    if st.session_state.get("canvas_data") and "objects" in st.session_state["canvas_data"]:
        objects = st.session_state["canvas_data"]["objects"]
        
        agd_objects = []
        for i, obj in enumerate(objects):
            kolor_obiektu = obj.get("stroke", "")
            if kolor_obiektu in PALETA_AGD_SLOWNIK.values():
                agd_objects.append((i, obj))
        
        if len(agd_objects) == 0:
            st.warning("⚠️ Nie narysowano żadnego sprzętu AGD z wybranej palety na mapie!")
        else:
            new_agd_list = []
            for idx, (obj_idx, obj) in enumerate(agd_objects):
                kolor = obj.get("stroke", "#0077b6")
                new_agd_list.append({
                    "object_index": obj_idx,
                    "text": f"Urządzenie AGD #{idx + 1}",
                    "moc": 0,
                    "fuse_id": None,
                    "color": kolor
                })
            
            st.session_state.agd_list = new_agd_list
            st.success(f"✅ Zatwierdzono! Wykryto {len(agd_objects)} urządzeń do konfiguracji poniżej.")
            st.rerun()
    else:
        st.warning("⚠️ Płótno jest puste.")

st.markdown("---")
st.subheader("⚙️ Krok 3: Konfiguracja urządzeń i przypisanie do obwodów")

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

st.markdown("")
if st.button("🧮 Oblicz obciążenie obwodów i sprawdź błędy", type="primary", use_container_width=True):
    if not st.session_state.agd_list:
        st.warning("⚠️ Brak urządzeń do obliczeń. Najpierw zatwierdź rzut z mapy.")
    else:
        obciazenie_bezpiecznikow = {}
        for f in st.session_state.fuses_list:
            f_name = f.name if hasattr(f, "name") else f.get("name", "Bezpiecznik")
            limit_watow = getattr(f, "max_power", 3680) 
            obciazenie_bezpiecznikow[f_name] = {"aktualna_moc": 0, "limit": limit_watow, "urzadzenia": []}

        bledy = []
        nieprzypisane = 0
        calkowita_moc_urzadzen = 0
        calkowity_limit_bezpiecznikow = sum(d["limit"] for d in obciazenie_bezpiecznikow.values())

        for agd in st.session_state.agd_list:
            nazwa = agd.get("text", "Urządzenie")
            moc = int(agd.get("moc", 0))
            bezpiecznik = agd.get("fuse_name")

            calkowita_moc_urzadzen += moc

            if moc <= 0:
                bledy.append(f"⚠️ Urządzenie **'{nazwa}'** ma ustawioną moc 0 W.")

            if not bezpiecznik:
                nieprzypisane += 1
                bledy.append(f"❌ Urządzenie **'{nazwa}'** nie jest przypisane do żadnego bezpiecznika!")
            elif bezpiecznik in obciazenie_bezpiecznikow:
                obciazenie_bezpiecznikow[bezpiecznik]["aktualna_moc"] += moc
                obciazenie_bezpiecznikow[bezpiecznik]["urzadzenia"].append({"nazwa": nazwa, "moc": moc})
            else:
                bledy.append(f"❌ Urządzenie **'{nazwa}'** wskazuje na nieistniejący bezpiecznik: {bezpiecznik}")

        przeciazony_jakikolwiek = any(d["aktualna_moc"] > d["limit"] for d in obciazenie_bezpiecznikow.values())

        st.markdown("---")
        st.subheader("📊 Wyniki analizy i bilans mocy obwodów")

        if nieprzypisane > 0:
            st.error(f"❌ Wykryto {nieprzypisane} urządzeń bez przypisanego bezpiecznika!")

        if bledy:
            with st.expander("🔍 Szczegółowa lista wykrytych ostrzeżeń", expanded=False):
                for b in bledy:
                    st.markdown(f"- {b}")

        if przeciazony_jakikolwiek:
            if calkowita_moc_urzadzen > calkowity_limit_bezpiecznikow:
                st.error(
                    "🛑 **Krytyczny brak mocy w gospodarstwie domowym!**\n\n"
                    "Całkowite zapotrzebowanie energetyczne Twoich urządzeń przewyższa maksymalną łączną przepustowość wszystkich dostępnych bezpieczników.\n"
                    "* **Zalecane działania:** Fizycznie nie jest możliwe uruchomienie tego zestawu urządzeń jednocześnie. Zwiększ liczbę bezpieczników (lub moc przyłączeniową u dostawcy), wymień część urządzeń na mniej prądożerne lub bezwzględnie podziel ich pracę na różne pory dnia."
                )
            else:
                st.error(
                    "🔴 **Uwaga: Niektóre bezpieczniki są przeciążone!**\n\n"
                    "Problem wynika z nierównomiernego rozłożenia urządzeń na obwodach. Rozważ następujące opcje:\n"
                    "1. **Zmiana wtyczek:** Przepnij urządzenia do gniazdek podłączonych do innych, mniej obciążonych obwodów.\n"
                    "2. **Modernizacje w rozdzielnicy:** Zleć elektrykowi zmianę przypisania obwodów (**TYLKO Z POMOCĄ ELEKTRYKA**).\n"
                    "3. **Zarządzanie czasem:** Nie korzystaj ze wszystkich tych urządzeń w tym samym momencie."
                )

            st.markdown("### ⚡ Wykryte konflikty energetyczne (urządzenia kluczowe):")
            st.info("💡 Na podstawie analizy obciążenia, poniższe pary urządzeń na przeciążonych obwodach najczęściej powodują zadziałanie zabezpieczeń (wybicie bezpiecznika) podczas jednoczesnej pracy:")

            for f_name, dane in obciazenie_bezpiecznikow.items():
                if dane["aktualna_moc"] > dane["limit"]:
                    urzadzenia_posortowane = sorted(dane["urzadzenia"], key=lambda x: x["moc"], reverse=True)
                    if len(urzadzenia_posortowane) >= 2:
                        u1 = urzadzenia_posortowane[0]
                        u2 = urzadzenia_posortowane[1]
                        st.markdown(f"- **Obwód '{f_name}':** Konflikt między **{u1['nazwa']}** ({u1['moc']} W) a **{u2['nazwa']}** ({u2['moc']} W). Ich jednoczesne włączenie generuje {u1['moc'] + u2['moc']}W, co natychmiast przekracza limit obwodu ({dane['limit']}W).")
        else:
            st.success("✅ **Brak przeciążeń!** Instalacja elektryczna bez problemu poradzi sobie z bieżącym zestawem urządzeń.")

        st.markdown("#### 📈 Szczegółowe obciążenie poszczególnych bezpieczników:")
        
        if not obciazenie_bezpiecznikow:
            st.info("ℹ️ Brak zdefiniowanych bezpieczników na liście powyżej (Krok 1). Dodaj bezpieczniki, aby wykonać pełny bilans.")
        else:
            for f_name, dane in obciazenie_bezpiecznikow.items():
                moc_calkowita = dane["aktualna_moc"]
                prad_ampery = moc_calkowita / 230.0
                limit = dane["limit"]
                
                procent_obciazenia = min(int((moc_calkowita / limit) * 100), 100) if limit > 0 else 0
                
                col_res1, col_res2 = st.columns([3, 1])
                with col_res1:
                    st.write(f"**{f_name}** — Suma mocy: **{moc_calkowita} W** ({prad_ampery:.2f} A) / Limit: {limit} W")
                    st.progress(procent_obciazenia / 100.0)
                with col_res2:
                    if moc_calkowita > limit:
                        st.markdown("<p style='color: #ff4b4b; font-weight: bold; margin-top: 5px;'>🔴 Przeciążenie!</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='color: #09ab3b; font-weight: bold; margin-top: 5px;'>🟢 W normie</p>", unsafe_allow_html=True)