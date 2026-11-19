from modules.services.supabase_client import supabase

def add_fuse_to_db(user_id: str, name: str, current_amp: float):
    try:
        response = supabase.table("fuses").insert({
            "user_id": user_id,
            "name": name,
            "current_amp": current_amp,
        }).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        raise ValueError(f"Błąd podczas zapisu bezpiecznika: {e}")


def delete_fuse_from_db(fuse_id: str):
    try:
        supabase.table("fuses").delete().eq("id", fuse_id).execute()
    except Exception as e:
        raise ValueError(f"Błąd podczas usuwania bezpiecznika: {e}")


def load_user_fuses(user_id: str):
    try:
        response = supabase.table("fuses").select("*").eq("user_id", user_id).execute()
        return response.data if response.data else []
    except Exception as e:
        raise ValueError(f"Błąd podczas ładowania bezpieczników: {e}")