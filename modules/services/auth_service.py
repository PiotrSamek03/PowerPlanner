import streamlit as st
from modules.services.supabase_client import supabase

class AuthService:
    @staticmethod
    def login(email: str, password: str) -> dict:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return {
            "user_id": res.user.id,
            "user_email": res.user.email
        }

    @staticmethod
    def register(email: str, password: str, redirect_url: str = "http://localhost:8502"):
        return supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"emailRedirectTo": redirect_url}
        })