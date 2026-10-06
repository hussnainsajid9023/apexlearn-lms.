"""
Authentication and Session State Management for ApexLearn LMS
Handles session state initialization, login, logout, registration, and role-based redirects.
"""

import streamlit as st
from typing import Optional, Dict, Any
import db

def init_session_state():
    """Initialize all session state variables."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if "user" not in st.session_state:
        st.session_state["user"] = None
        
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
        
    if "selected_qa_id" not in st.session_state:
        st.session_state["selected_qa_id"] = "qa-1"
        
    if "diff_mode" not in st.session_state:
        st.session_state["diff_mode"] = "portrait"  # or landscape
        
    if "sandbox_active_tab" not in st.session_state:
        st.session_state["sandbox_active_tab"] = "circuit-breaker.ts"
        
    if "quiz_timer_start" not in st.session_state:
        st.session_state["quiz_timer_start"] = None
        
    if "quiz_time_limit_mins" not in st.session_state:
        st.session_state["quiz_time_limit_mins"] = 15
        
    if "quiz_current_q" not in st.session_state:
        st.session_state["quiz_current_q"] = 1
        
    if "quiz_user_answers" not in st.session_state:
        st.session_state["quiz_user_answers"] = {}
        
    if "quiz_flagged" not in st.session_state:
        st.session_state["quiz_flagged"] = set()

def navigate_to(page_name: str, **kwargs):
    """Navigate to a given page and update state."""
    st.session_state["page"] = page_name
    for key, value in kwargs.items():
        st.session_state[key] = value
    st.rerun()

def login_user(user: Dict[str, Any]):
    """Set authenticated user session and redirect based on role."""
    st.session_state["authenticated"] = True
    st.session_state["user"] = user
    
    role = user.get("role", "Student")
    if role == "Instructor":
        navigate_to("instructor_dashboard")
    elif role == "Admin":
        navigate_to("admin_users")
    else:
        navigate_to("dashboard")

def logout_user():
    """Clear user session and redirect to login."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["page"] = "login"
    st.session_state["quiz_user_answers"] = {}
    st.session_state["quiz_timer_start"] = None
    st.rerun()

def get_current_user() -> Optional[Dict[str, Any]]:
    """Return currently logged-in user or None."""
    return st.session_state.get("user")

def get_current_role() -> str:
    """Return role of current user."""
    user = get_current_user()
    if user:
        return user.get("role", "Student")
    return "Guest"
