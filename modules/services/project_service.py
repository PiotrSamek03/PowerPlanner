import streamlit as st
from modules.services.supabase_client import supabase


def load_user_project(user_id: str):
    """Pobiera zapisany rzut i listę AGD użytkownika."""
    try:
        response = supabase.table("user_projects").select("*").eq("user_id", user_id).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Błąd podczas ładowania projektu: {e}")
        return None

def save_user_project(user_id: str, canvas_data: dict, agd_list: list):
    """Zapisuje lub aktualizuje stan projektu (mapę i AGD) w bazie."""
    try:
        # Sprawdzamy czy projekt dla tego użytkownika już istnieje
        existing = supabase.table("user_projects").select("id").eq("user_id", user_id).execute()
        
        payload = {
            "user_id": user_id,
            "canvas_json": canvas_data,
            "agd_list_json": agd_list
        }
        
        if existing.data and len(existing.data) > 0:
            proj_id = existing.data[0]["id"]
            supabase.table("user_projects").update(payload).eq("id", proj_id).execute()
        else:
            supabase.table("user_projects").insert(payload).execute()
            
        st.success("✅ Projekt został pomyślnie zapisany w chmurze!")
    except Exception as e:
        st.error(f"Błąd podczas zapisu projektu: {e}")
