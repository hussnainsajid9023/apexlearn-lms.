"""
Course Syllabus and Overview View for ApexLearn LMS
Matches visual design of course.html with instructor details, module accordions,
interactive lesson launch buttons, and curriculum progress tracking.
"""

import streamlit as st
import db
import auth

def render_course():
    database = db.load_db()
    course = database.get("course", {})

    # Breadcrumb & Navigation
    col_back, col_actions = st.columns([2, 2])
    with col_back:
        if st.button("← Back to Dashboard", key="course_back_dash"):
            auth.navigate_to("dashboard")
    with col_actions:
        st.markdown("""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="badge badge-primary">Accredited Engineering Track</span>
        </div>
        """, unsafe_allow_html=True)

    # Course Banner Hero Card
    st.markdown(f"""
    <div class="apex-hero-card">
        <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem;">
            <span class="badge badge-secondary">{course.get('code', 'CS-804')}</span>
            <span style="font-size: 0.85rem; color: #4B5563; font-weight: 500;">Graduate Level · 4.0 Credits</span>
        </div>
        <h1 style="font-size: 1.75rem; font-weight: 800; color: #111827; margin: 0 0 0.5rem 0;">
            {course.get('title', 'Advanced Full-Stack Engineering with Next.js & Distributed Systems')}
        </h1>
        <p style="color: #4B5563; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1.25rem;">
            {course.get('description', '')}
        </p>
        <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; align-items: center; padding-top: 0.75rem; border-top: 1px solid #E0E7FF;">
            <div>
                <span style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase;">Lead Instructor</span>
                <div style="font-weight: 700; color: #111827; font-size: 0.95rem;">{course.get('instructor', 'Prof. Alex Vance')}</div>
            </div>
            <div>
                <span style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase;">Rating</span>
                <div style="font-weight: 700; color: #D97706; font-size: 0.95rem;">★ {course.get('rating', 4.9)} / 5.0 ({course.get('reviews_count', 328)} reviews)</div>
            </div>
            <div>
                <span style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase;">Curriculum Duration</span>
                <div style="font-weight: 700; color: #111827; font-size: 0.95rem;">{course.get('estimated_hours', 32)} Hours · {course.get('total_modules', 8)} Modules</div>
            </div>
            <div>
                <span style="font-size: 0.75rem; color: #6B7280; text-transform: uppercase;">Current Standing</span>
                <div style="font-weight: 700; color: #4F46E5; font-size: 0.95rem;">Module 5 of 8 Completed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resume Lesson Callout
    call_col1, call_col2 = st.columns([3, 1])
    with call_col1:
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            <strong style="color: #111827; font-size: 1.1rem;">Next Unit in Schedule:</strong>
            <span style="color: #4B5563; font-size: 0.95rem; margin-left: 0.5rem;">
                Lesson 6.1: Resilient Circuit Breakers & Fallbacks
            </span>
        </div>
        """, unsafe_allow_html=True)
    with call_col2:
        if st.button("▶ Resume Lesson 6.1", key="course_resume_btn", type="primary", use_container_width=True):
            auth.navigate_to("lesson_player")

    st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 1.25rem 0;'>", unsafe_allow_html=True)

    # Curriculum Structure Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2 style="font-size: 1.35rem; font-weight: 700; color: #111827; margin: 0;">Curriculum Modules</h2>
        <span style="font-size: 0.85rem; color: #6B7280;">8 Modules · Self-Paced Cohort</span>
    </div>
    """, unsafe_allow_html=True)

    modules = course.get("modules", [])
    for mod in modules:
        num = mod["number"]
        status = mod["status"]
        status_badge = {
            "completed": "✅ COMPLETED",
            "in_progress": "🟡 IN PROGRESS",
            "locked": "🔒 LOCKED"
        }.get(status, status)

        with st.expander(f"Module {num}: {mod['title']} ({status_badge})", expanded=(status == "in_progress")):
            st.markdown(f"""
            <div style="margin-bottom: 0.75rem; color: #6B7280; font-size: 0.85rem;">
                Estimated Duration: <strong>{mod.get('duration', '4 Hours')}</strong> · Lessons: <strong>{mod.get('lessons_count', 4)}</strong>
            </div>
            """, unsafe_allow_html=True)

            if status == "in_progress":
                st.markdown("<h4 style='font-size: 0.95rem; color: #111827; margin: 0.75rem 0 0.5rem 0;'>Interactive Units:</h4>", unsafe_allow_html=True)

                u1, u2 = st.columns([3, 1])
                with u1:
                    st.markdown("""
                    <div style="padding: 0.4rem 0;">
                        <strong>6.1 Resilient Circuit Breakers & Fallbacks</strong>
                        <div style="font-size: 0.8rem; color: #6B7280;">Video Lecture & State Machine Visualizer (38 mins)</div>
                    </div>
                    """, unsafe_allow_html=True)
                with u2:
                    if st.button("Launch 6.1", key="launch_6_1", use_container_width=True):
                        auth.navigate_to("lesson_player")

                u3, u4 = st.columns([3, 1])
                with u3:
                    st.markdown("""
                    <div style="padding: 0.4rem 0;">
                        <strong>6.2 Cascading Failure Prevention & Bulkheads</strong>
                        <div style="font-size: 0.8rem; color: #6B7280;">Architecture Deep Dive & Saturation Simulator (42 mins)</div>
                    </div>
                    """, unsafe_allow_html=True)
                with u4:
                    if st.button("Launch 6.2", key="launch_6_2", use_container_width=True):
                        auth.navigate_to("lesson_6_2")

                u5, u6 = st.columns([3, 1])
                with u5:
                    st.markdown("""
                    <div style="padding: 0.4rem 0;">
                        <strong>Quiz 6: Distributed Mutations & Concurrency</strong>
                        <div style="font-size: 0.8rem; color: #DC2626; font-weight: 500;">Required Assessment · 5 Questions · 70% Pass Mark</div>
                    </div>
                    """, unsafe_allow_html=True)
                with u6:
                    if st.button("Start Quiz 6", key="course_start_quiz", type="primary", use_container_width=True):
                        auth.navigate_to("quiz")

                u7, u8 = st.columns([3, 1])
                with u7:
                    st.markdown("""
                    <div style="padding: 0.4rem 0;">
                        <strong>Lab 6: Redis Quorum Circuit Breaker</strong>
                        <div style="font-size: 0.8rem; color: #0D9488;">Interactive Code Sandbox & Unit Test Suite</div>
                    </div>
                    """, unsafe_allow_html=True)
                with u8:
                    if st.button("Open Sandbox", key="course_open_box", use_container_width=True):
                        auth.navigate_to("code_sandbox")

            elif status == "completed":
                st.markdown("""
                <div style="color: #059669; font-size: 0.85rem; padding: 0.5rem 0;">
                    ✓ All video lectures, hands-on lab sandboxes, and module assessments successfully completed.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="color: #94A3B8; font-size: 0.85rem; padding: 0.5rem 0;">
                    🔒 This module unlocks upon passing Quiz 6 and submitting Lab 6.
                </div>
                """, unsafe_allow_html=True)
