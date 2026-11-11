import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_connection() -> Client:
    """Inicjalizuje i buforuje połączenie z bazą Supabase."""
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

# Tworzymy instancję klienta, którą będziemy importować w innych plikach
supabase = init_connection()