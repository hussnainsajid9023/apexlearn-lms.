"""
Login View for ApexLearn LMS
Matches visual design of login.html / register.html with enterprise badge, clean inputs,
password hashing validation, role redirect, and demo credentials.
"""

import streamlit as st
import db
import auth

def render_login():
    # Outer container centered
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # Brand Card Header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem; padding-top: 1rem;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; background: #EEF2FF; border-radius: 16px; border: 1px solid #C7D2FE; margin-bottom: 0.75rem; box-shadow: 0 2px 8px rgba(79,70,229,0.1);">
                <span style="font-size: 2rem;">⚡</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-secondary" style="font-size: 0.75rem; letter-spacing: 0.05em;">
                    🛡️ Enterprise LMS Platform
                </span>
            </div>
            <h1 style="font-size: 1.85rem; font-weight: 800; color: #111827; margin: 0 0 0.25rem 0; letter-spacing: -0.03em;">
                Join ApexLearn LMS
            </h1>
            <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">
                Master cloud-native distributed systems and engineering
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Quick Demo Login Presets
        st.markdown("""
        <div class="apex-card" style="padding: 1rem; margin-bottom: 1rem; background: #F8FAFC; border: 1px dashed #CBD5E1;">
            <p style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: #64748B; margin-bottom: 0.5rem; letter-spacing: 0.05em;">
                ⚡ Fast Demo Login (Click to prefill & test roles):
            </p>
        </div>
        """, unsafe_allow_html=True)

        demo_cols = st.columns(3)
        with demo_cols[0]:
            if st.button("🎓 Student (Jordan)", use_container_width=True, key="demo_student"):
                st.session_state["login_email"] = "student@apexlearn.io"
                st.session_state["login_password"] = "password123"
        with demo_cols[1]:
            if st.button("👨‍🏫 Instructor (Alex)", use_container_width=True, key="demo_instructor"):
                st.session_state["login_email"] = "instructor@apexlearn.io"
                st.session_state["login_password"] = "password123"
        with demo_cols[2]:
            if st.button("👑 Admin (Sarah)", use_container_width=True, key="demo_admin"):
                st.session_state["login_email"] = "admin@apexlearn.io"
                st.session_state["login_password"] = "password123"

        # Main Login Form Card
        st.markdown('<div class="apex-card">', unsafe_allow_html=True)
        
        default_email = st.session_state.get("login_email", "")
        default_password = st.session_state.get("login_password", "")

        email = st.text_input(
            "Institution Email",
            value=default_email,
            placeholder="e.g. jordan.alvarez@apexlearn.io",
            help="Enter your registered academic or corporate email"
        )

        password = st.text_input(
            "Password",
            value=default_password,
            type="password",
            placeholder="••••••••",
            help="Passwords are securely hashed with SHA-256 and salted"
        )

        remember_col, forgot_col = st.columns([1, 1])
        with remember_col:
            remember_me = st.checkbox("Remember this device", value=True)
        with forgot_col:
            st.markdown(
                '<div style="text-align: right; font-size: 0.85rem; padding-top: 0.3rem;"><a href="#" style="color: #4F46E5; text-decoration: none; font-weight: 500;">Forgot password?</a></div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("Sign In to Account", use_container_width=True, type="primary"):
            if not email.strip() or not password.strip():
                st.error("Please enter both email and password.")
            else:
                success, user, message = db.authenticate_user(email, password)
                if success and user:
                    st.success(f"Welcome back, {user['name']}!")
                    auth.login_user(user)
                else:
                    st.error(f"Authentication Failed: {message}")

        st.markdown('</div>', unsafe_allow_html=True)

        # Switch to Register
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; color: #6B7280; font-size: 0.9rem;">
            New to ApexLearn?
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create an Account", use_container_width=True, key="go_to_register"):
            auth.navigate_to("register")

        # Security footer badge
        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem; color: #9CA3AF; font-size: 0.75rem;">
            🔒 End-to-End Encrypted Session · SOC2 Type II Certified
        </div>
        """, unsafe_allow_html=True)
