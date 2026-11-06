# ⚡ PowerPlanner – Projektant Rzutu i Obwodów Elektrycznych

**PowerPlanner** to profesjonalne narzędzie webowe napisane w Pythonie (Streamlit) do szybkiego projektowania rzutu mieszkania, rozmieszczania odbiorników prądu oraz automatycznej analizy obciążenia obwodów i bezpieczników domowych.

---

## 🚀 Kluczowe Funkcjonalności

* **🎨 Rysowanie Rzutu (Interactive Canvas):** Rysowanie ścian, gniazdek oraz sprzętów AGD/oświetlenia z wyznaczonej palety kolorów.
* **📋 Zarządzanie Bezpiecznikami:** Definiowanie obwodów i bezpieczników (np. 16A / 3680W) z podglądem w tabeli.
* **⚙️ Mapowanie i Konfiguracja:** Przypisywanie nazw, mocy (W) oraz bezpieczników do wyznaczonych punktów na mapie.
* **📊 Bilans Mocy i Konflikty Energetyczne:** 
  * Automatyczna kalkulacja prądu.
  * Dwuetapowa weryfikacja błędów (przeciążenie całego domu vs. zły rozkład obwodów).
  * Wykrywanie bezpośrednich **konfliktów urządzeń** (wskazywanie par sprzętów, które najczęściej wybiją korki).

---

## 🛠️ Wymagania i Instalacja

Do uruchomienia aplikacji wymagany jest **Python 3.9+**.

### 1. Klonowanie repozytorium
```bash
git clone [https://github.com/PiotrSamek03/PowerPlanner.git](https://github.com/PiotrSamek03/PowerPlanner.git)
cd PowerPlanner


# Utworzenie i aktywacja środowiska wirtualnego
# Windows (Git Bash / CMD)
python -m venv .venv
source .venv/Scripts/activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate

#instalacja zależności
pip install streamlit streamlit-drawable-canvas Pillow

#uruchomienie aplikacji
streamlit run app.py
