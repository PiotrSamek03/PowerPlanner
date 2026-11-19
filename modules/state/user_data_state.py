import streamlit as st

from modules.services.fuse_service import load_user_fuses
from modules.services.project_service import load_user_project

def load_user_data_from_cloud(user_id: str):
    if not st.session_state.get("data_loaded", False):
        
        fuses = load_user_fuses(user_id)
        if fuses:
            st.session_state["fuses_list"] = fuses
            st.session_state["fuses"] = fuses
        else:
            st.session_state["fuses_list"] = []
            
        project = load_user_project(user_id)
        if project:
            if project.get("canvas_json"):
                st.session_state["canvas_data"] = project.get("canvas_json")
                
            if project.get("agd_list_json"):
                loaded_agd = project.get("agd_list_json")
                
                for item in loaded_agd:
                    if isinstance(item, dict):
                        item["saved"] = True
                        item["status"] = "Zapisany"
                        item["synced"] = True
                        
                st.session_state["agd_list"] = loaded_agd

        try:
            pass
        except Exception as e:
            print(f"Błąd podczas automatycznego przeliczania obwodów: {e}")

        st.session_state["data_loaded"] = True

def get_fuse_id(fuse) -> str | None:
    fuse_id = getattr(fuse, "id", None)
    if fuse_id is None and isinstance(fuse, dict):
        fuse_id = fuse.get("id")
    return str(fuse_id) if fuse_id else None


def remove_fuse_at_index(fuses_list: list, fuse_index: int) -> tuple[list, str | None]:
    """Zwraca nową listę bezpieczników bez elementu `fuse_index` oraz ID usuniętego bezpiecznika."""
    if not (0 <= fuse_index < len(fuses_list)):
        return list(fuses_list), None

    updated_fuses = list(fuses_list)
    removed_fuse = updated_fuses.pop(fuse_index)
    return updated_fuses, get_fuse_id(removed_fuse)        