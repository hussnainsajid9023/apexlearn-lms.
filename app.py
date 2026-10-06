"""
ApexLearn LMS - Main Application Entry Point
A multi-page enterprise Streamlit Learning Management System application.
Designed after Google Stitch HTML visual specifications with full interactivity,
JSON data persistence, role routing, and auto-graded assessments.
"""

import os
import streamlit as st
from PIL import Image

import db
import auth
import theme

# Page configuration
st.set_page_config(
    page_title="ApexLearn LMS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and session state
db.init_db()
auth.init_session_state()

# Inject Stitch-matching custom styling
theme.apply_custom_theme()

def render_sidebar():
    """Render the sidebar with logo.png, user status, role badge, navigation links, and logout."""
    with st.sidebar:
        # Logo rendering
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        if os.path.exists(logo_path):
            try:
                logo_img = Image.open(logo_path)
                st.image(logo_img, use_container_width=True)
            except Exception:
                st.markdown("<h2 style='color:#4F46E5; font-weight:800;'>⚡ ApexLearn LMS</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#4F46E5; font-weight:800;'>⚡ ApexLearn LMS</h2>", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

        user = auth.get_current_user()
        is_auth = st.session_state.get("authenticated", False)

        if is_auth and user:
            role = user.get("role", "Student")
            role_badge_class = {
                "Student": "badge-primary",
                "Instructor": "badge-secondary",
                "Admin": "badge-danger"
            }.get(role, "badge-primary")

            # User profile card
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 0.85rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                    <div style="width: 42px; height: 42px; border-radius: 50%; background: #4F46E5; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem; box-shadow: 0 2px 6px rgba(79,70,229,0.3);">
                        {user.get('name', 'J')[0]}
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #111827; font-size: 0.925rem; line-height: 1.2;">
                            {user.get('name', 'Jordan Alvarez')}
                        </div>
                        <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 0.25rem;">
                            {user.get('email', '')}
                        </div>
                        <span class="badge {role_badge_class}" style="font-size: 0.65rem;">
                            {role}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<p style='font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.05em; margin-bottom: 0.35rem;'>Platform Navigation</p>", unsafe_allow_html=True)

            current_p = st.session_state.get("page", "dashboard")

            # Navigation buttons
            nav_items = [
                ("📊 Dashboard", "dashboard"),
                ("📋 Course Syllabus", "course"),
                ("📺 Lesson 6.1 Player", "lesson_player"),
                ("📝 Transcript & Notes", "transcript_notes"),
                ("💬 Q&A Discussion", "lesson_qa"),
                ("💻 Code Sandbox", "code_sandbox"),
                ("⚖️ Code Solution Diff", "code_diff"),
                ("🛡️ Lesson 6.2 Bulkhead", "lesson_6_2"),
                ("📝 Module 6 Quiz", "quiz"),
                ("🏆 Quiz Results", "quiz_result")
            ]

            # Role-specific items
            if role == "Instructor":
                nav_items.insert(0, ("👨‍🏫 Faculty Portal", "instructor_dashboard"))
            elif role == "Admin":
                nav_items.insert(0, ("👑 Admin Console", "admin_users"))

            for label, p_name in nav_items:
                btn_type = "primary" if current_p == p_name else "secondary"
                if st.button(label, key=f"nav_{p_name}", use_container_width=True, type=btn_type):
                    auth.navigate_to(p_name)

            st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 1rem 0;'>", unsafe_allow_html=True)

            # Quick role switcher for testing / presentation
            with st.expander("🔄 Switch Active Role", expanded=False):
                st.markdown("<div style='font-size: 0.8rem; color: #64748B; margin-bottom: 0.4rem;'>Switch user context to preview role-based views:</div>", unsafe_allow_html=True)
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    if st.button("Student", key="switch_stud", use_container_width=True):
                        _, u, _ = db.authenticate_user("student@apexlearn.io", "password123")
                        if u: auth.login_user(u)
                with col_r2:
                    if st.button("Teacher", key="switch_inst", use_container_width=True):
                        _, u, _ = db.authenticate_user("instructor@apexlearn.io", "password123")
                        if u: auth.login_user(u)
                with col_r3:
                    if st.button("Admin", key="switch_adm", use_container_width=True):
                        _, u, _ = db.authenticate_user("admin@apexlearn.io", "password123")
                        if u: auth.login_user(u)

            if st.button("🚪 Sign Out", key="logout_btn", use_container_width=True):
                auth.logout_user()

        else:
            # Guest sidebar navigation
            st.markdown("""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; text-align: center;">
                <p style="font-weight: 700; color: #111827; font-size: 0.95rem; margin-bottom: 0.25rem;">Enterprise Access</p>
                <p style="font-size: 0.8rem; color: #6B7280; margin: 0;">Sign in to resume coursework, code sandboxes, and module quizzes.</p>
            </div>
            """, unsafe_allow_html=True)

            current_p = st.session_state.get("page", "login")
            if st.button("🔐 Sign In", key="guest_nav_login", use_container_width=True, type="primary" if current_p == "login" else "secondary"):
                auth.navigate_to("login")
            if st.button("🚀 Register Account", key="guest_nav_reg", use_container_width=True, type="primary" if current_p == "register" else "secondary"):
                auth.navigate_to("register")

        # Sidebar footer
        st.markdown("""
        <div style="margin-top: 2rem; font-size: 0.7rem; color: #94A3B8; text-align: center;">
            ApexLearn LMS v2.4 Enterprise<br>
            Designed with Google Stitch Architecture
        </div>
        """, unsafe_allow_html=True)

def main():
    # Render common sidebar
    render_sidebar()

    current_page = st.session_state.get("page", "login")
    is_auth = st.session_state.get("authenticated", False)

    # Protect pages that require authentication
    unprotected_pages = ["login", "register"]
    if not is_auth and current_page not in unprotected_pages:
        current_page = "login"
        st.session_state["page"] = "login"

    # Route to appropriate view
    if current_page == "login":
        from views.login_view import render_login
        render_login()
    elif current_page == "register":
        from views.register_view import render_register
        render_register()
    elif current_page == "dashboard":
        theme.render_brand_header("Student Learning Dashboard")
        from views.dashboard_view import render_dashboard
        render_dashboard()
    elif current_page == "course":
        theme.render_brand_header("Curriculum & Syllabus")
        from views.course_view import render_course
        render_course()
    elif current_page == "lesson_player":
        theme.render_brand_header("Interactive Lesson Player")
        from views.lesson_player_view import render_lesson_player
        render_lesson_player()
    elif current_page == "transcript_notes":
        theme.render_brand_header("Transcript & Notes")
        from views.transcript_notes_view import render_transcript_notes
        render_transcript_notes()
    elif current_page == "lesson_qa":
        theme.render_brand_header("Lesson Q&A Forum")
        from views.qa_view import render_qa
        render_qa()
    elif current_page == "qa_thread":
        theme.render_brand_header("Discussion Thread")
        from views.qa_thread_view import render_qa_thread
        render_qa_thread()
    elif current_page == "code_sandbox":
        theme.render_brand_header("Interactive Code Sandbox")
        from views.sandbox_view import render_sandbox
        render_sandbox()
    elif current_page == "code_diff":
        theme.render_brand_header("Solution Code Diff")
        from views.diff_view import render_diff
        render_diff()
    elif current_page == "lesson_6_2":
        theme.render_brand_header("Cascading Failure & Bulkhead")
        from views.lesson_6_2_view import render_lesson_6_2
        render_lesson_6_2()
    elif current_page == "quiz":
        theme.render_brand_header("Timed Assessment")
        from views.quiz_view import render_quiz
        render_quiz()
    elif current_page == "quiz_result":
        theme.render_brand_header("Assessment Diagnostics & Results")
        from views.quiz_result_view import render_quiz_result
        render_quiz_result()
    elif current_page == "instructor_dashboard":
        theme.render_brand_header("Instructor Faculty Portal")
        from views.instructor_view import render_instructor_dashboard
        render_instructor_dashboard()
    elif current_page == "admin_users":
        theme.render_brand_header("Super Admin Governance")
        from views.admin_view import render_admin_dashboard
        render_admin_dashboard()
    else:
        # Fallback to dashboard
        from views.dashboard_view import render_dashboard
        render_dashboard()

if __name__ == "__main__":
    main()
