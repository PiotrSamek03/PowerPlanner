import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase() -> Client:
    """Inicjalizuje i buforuje klienta Supabase na podstawie st.secrets."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase = init_supabase()

def load_user_fuses(user_id: str):
    """Pobiera listę bezpieczników dla danego użytkownika z bazy."""
    try:
        response = supabase.table("fuses").select("*").eq("user_id", user_id).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Błąd podczas ładowania bezpieczników: {e}")
        return []

def add_fuse_to_db(user_id: str, name: str, current_amp: float):
    """Dodaje nowy bezpiecznik do bazy danych."""
    try:
        response = supabase.table("fuses").insert({
            "user_id": user_id,
            "name": name,
            "current_amp": current_amp
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        st.error(f"Błąd podczas zapisu bezpiecznika: {e}")
        return None

def delete_fuse_from_db(fuse_id: str):
    """Usuwa bezpiecznik z bazy danych po jego ID."""
    try:
        supabase.table("fuses").delete().eq("id", fuse_id).execute()
    except Exception as e:
        st.error(f"Błąd podczas usuwania bezpiecznika: {e}")

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