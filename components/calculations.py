import streamlit as st

def calculate_load_and_check_errors():
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