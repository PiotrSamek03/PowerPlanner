import streamlit as st
from modules.logic.circuit_calculator import CircuitCalculator
from modules.ui.save_view import save_button

def render_calculations_section():
    if st.button("Oblicz obciążenie obwodów i sprawdź błędy", type="primary", use_container_width=True):
        if not st.session_state.agd_list:
            st.warning("⚠️ Brak urządzeń do obliczeń. Najpierw zatwierdź rzut z mapy.")
        else:
            wyniki = CircuitCalculator.calculate_load(
                st.session_state.fuses_list,
                st.session_state.agd_list
            )
            _render_results(wyniki)
            
    save_button()

def _render_results(wyniki: dict):
    st.markdown("---")
    st.subheader("📊 Wyniki analizy i bilans mocy obwodów")

    if wyniki["nieprzypisane"] > 0:
        st.error(f"❌ Wykryto {wyniki['nieprzypisane']} urządzeń bez przypisanego bezpiecznika!")

    if wyniki["bledy"]:
        with st.expander("🔍 Szczegółowa lista wykrytych ostrzeżeń", expanded=False):
            for b in wyniki["bledy"]:
                st.markdown(f"- {b}")

    if wyniki["przeciazony"]:
        if wyniki["calkowita_moc"] > wyniki["calkowity_limit"]:
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

        for k in wyniki["konflikty"]:
            u1, u2 = k["u1"], k["u2"]
            st.markdown(
                f"- **Obwód '{k['fuse_name']}':** Konflikt między **{u1['nazwa']}** ({u1['moc']} W) a **{u2['nazwa']}** ({u2['moc']} W). "
                f"Ich jednoczesne włączenie generuje {u1['moc'] + u2['moc']}W, co natychmiast przekracza limit obwodu ({k['limit']}W)."
            )
    else:
        st.success("**Brak przeciążeń!** Instalacja elektryczna bez problemu poradzi sobie z bieżącym zestawem urządzeń.")

    st.markdown("#### Szczegółowe obciążenie poszczególnych bezpieczników:")
    obciazenia = wyniki["obciazenie_bezpiecznikow"]

    if not obciazenia:
        st.info("Brak zdefiniowanych bezpieczników na liście powyżej (Krok 1). Dodaj bezpieczniki, aby wykonać pełny bilans.")
    else:
        for f_name, dane in obciazenia.items():
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