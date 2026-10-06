"""
Register View for ApexLearn LMS
Matches visual design of register.html with role selection (Student / Instructor / Admin),
password validation, duplicate email prevention, and auto-login redirection.
"""

import streamlit as st
import db
import auth

def render_register():
    col_left, col_center, col_right = st.columns([1, 2, 1])

    with col_center:
        # Header
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem; padding-top: 1rem;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; background: #CCFBF1; border-radius: 16px; border: 1px solid #99F6E4; margin-bottom: 0.75rem; box-shadow: 0 2px 8px rgba(13,148,136,0.1);">
                <span style="font-size: 2rem;">🚀</span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-secondary" style="font-size: 0.75rem; letter-spacing: 0.05em;">
                    Create ApexLearn Profile
                </span>
            </div>
            <h1 style="font-size: 1.85rem; font-weight: 800; color: #111827; margin: 0 0 0.25rem 0; letter-spacing: -0.03em;">
                Start Your Learning Journey
            </h1>
            <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">
                Join our cohort of modern distributed systems architects
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="apex-card">', unsafe_allow_html=True)

        # Full Name
        name = st.text_input("Full Name", placeholder="e.g. Jordan Alvarez", help="Your official academic or professional display name")

        # Email
        email = st.text_input("Institution Email", placeholder="e.g. jordan.alvarez@apexlearn.io", help="Must be unique across the platform")

        # Role Selector
        st.markdown("""
        <label style="font-size: 0.875rem; font-weight: 600; color: #111827; display: block; margin-bottom: 0.25rem;">
            Account Role
        </label>
        """, unsafe_allow_html=True)

        role = st.radio(
            "Select Role",
            options=["Student", "Instructor", "Admin"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
            help="Determines your personalized dashboard and access permissions"
        )

        role_descriptions = {
            "Student": "🎓 Access course syllabus, interactive video player, sandbox labs, and take quizzes.",
            "Instructor": "👨‍🏫 Manage curriculum modules, grade submissions, review quiz analytics, and answer forum questions.",
            "Admin": "👑 Platform-wide governance, user management, system diagnostics, and catalog administration."
        }
        st.markdown(f"""
        <div style="background: #F3F4F6; border-radius: 8px; padding: 0.6rem 0.85rem; font-size: 0.825rem; color: #4B5563; margin-bottom: 1rem; border-left: 3px solid #4F46E5;">
            {role_descriptions[role]}
        </div>
        """, unsafe_allow_html=True)

        # Passwords
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            password = st.text_input("Password", type="password", placeholder="Min 8 characters", help="At least 8 characters recommended")
        with col_p2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")

        # Password strength hint
        if password:
            if len(password) >= 8:
                st.markdown('<span style="color: #059669; font-size: 0.8rem; font-weight: 500;">✓ Password meets minimum length criteria</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span style="color: #DC2626; font-size: 0.8rem; font-weight: 500;">✗ Must be at least 8 characters</span>', unsafe_allow_html=True)

        terms = st.checkbox("I agree to the Enterprise Academic Honor Code & Privacy Policies", value=True)

        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)

        if st.button("Complete Registration & Enter LMS", use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Please provide your full name.")
            elif not email.strip() or "@" not in email:
                st.error("Please provide a valid institutional email address.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters in length.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please re-enter identical passwords.")
            elif not terms:
                st.error("You must accept the Academic Honor Code to create an account.")
            else:
                success, msg = db.register_user(name, email, password, role)
                if not success:
                    st.error(msg)
                else:
                    st.success("Account successfully created!")
                    # Auto-login
                    _, user, _ = db.authenticate_user(email, password)
                    if user:
                        auth.login_user(user)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin-top: 1rem; color: #6B7280; font-size: 0.9rem;">
            Already have an account?
        </div>
        """, unsafe_allow_html=True)

        if st.button("Sign In to Existing Account", use_container_width=True, key="go_to_login"):
            auth.navigate_to("login")
