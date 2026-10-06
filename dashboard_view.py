"""
Dashboard View for ApexLearn LMS
Matches visual design of dashboard.html with personalized welcome banner,
high-level metrics, 'Continue Learning' hero card, action items & deadlines,
and enrolled courses overview.
"""

import streamlit as st
import db
import auth

def render_dashboard():
    user = auth.get_current_user() or {}
    user_name = user.get("name", "Jordan Alvarez")
    user_email = user.get("email", "student@apexlearn.io")
    user_role = user.get("role", "Student")
    user_title = user.get("title", "Full-Stack Track · Cohort 2026")
    user_progress = user.get("overall_progress", 68)
    user_hours = user.get("hours_learned", 42.5)
    user_streak = user.get("streak_days", 14)

    # Check if user has an existing quiz result
    quiz_res = db.get_user_quiz_result(user_email)
    quizzes_passed_str = "6 / 6" if (quiz_res and quiz_res.get("passed")) else "5 / 6"

    # Top Welcome Bar
    col_welcome, col_badge = st.columns([3, 1])
    with col_welcome:
        st.markdown(f"""
        <div style="margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <h1 style="font-size: 1.85rem; font-weight: 800; color: #111827; margin: 0;">
                    Welcome back, {user_name} 👋
                </h1>
            </div>
            <p style="color: #6B7280; font-size: 0.95rem; margin-top: 0.2rem;">
                {user_title} · Master modern distributed cloud patterns
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_badge:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 0.75rem;">
            <span class="badge badge-primary" style="font-size: 0.8rem; padding: 0.4rem 0.85rem;">
                Active Role: {user_role}
            </span>
        </div>
        """, unsafe_allow_html=True)

    # 4 Key Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Overall Course Progress",
            value=f"{user_progress}%",
            delta="+8% this module",
            help="Completed modules out of total enrolled curriculum"
        )
    with m2:
        st.metric(
            label="Learning Hours",
            value=f"{user_hours}h",
            delta="+3.5h this week",
            help="Total interactive laboratory and video time logged"
        )
    with m3:
        st.metric(
            label="Quizzes Passed",
            value=quizzes_passed_str,
            delta="83% pass rate",
            help="Assessments completed above the 70% threshold"
        )
    with m4:
        st.metric(
            label="Daily Study Streak",
            value=f"{user_streak} Days",
            delta="🔥 Personal Best",
            help="Consecutive days with interactive activity"
        )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # Continue Learning Hero Card
    st.markdown("""
    <div class="apex-hero-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.85rem;">
            <div>
                <span class="badge badge-secondary" style="margin-bottom: 0.5rem;">Continue Learning</span>
                <h2 style="font-size: 1.35rem; font-weight: 700; color: #111827; margin: 0.25rem 0 0.25rem 0;">
                    Advanced Full-Stack Engineering with Next.js & Distributed Systems
                </h2>
                <p style="color: #4F46E5; font-weight: 600; font-size: 0.95rem; margin: 0;">
                    Module 6: Distributed System Resilience & Circuit Breakers
                </p>
                <p style="color: #6B7280; font-size: 0.85rem; margin: 0.15rem 0 0.75rem 0;">
                    Current Lesson: <strong>6.1 Resilient Circuit Breakers & Fallbacks</strong> (38 mins left)
                </p>
            </div>
            <div style="background: #FFFFFF; border-radius: 12px; padding: 0.5rem 1rem; border: 1px solid #C7D2FE; text-align: center;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #4F46E5;">72%</div>
                <div style="font-size: 0.7rem; color: #6B7280; text-transform: uppercase;">Module Done</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.progress(0.72)

    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
    hero_btn_col1, hero_btn_col2, hero_btn_space = st.columns([1.5, 1.5, 3])
    with hero_btn_col1:
        if st.button("▶ Resume Lesson 6.1", use_container_width=True, type="primary"):
            auth.navigate_to("lesson_player")
    with hero_btn_col2:
        if st.button("📋 View Syllabus", use_container_width=True):
            auth.navigate_to("course")

    st.markdown("</div>", unsafe_allow_html=True)

    # 2 Column Split: Action Items / Deadlines vs Quick Practice & Q&A
    col_actions, col_quick = st.columns([1.6, 1.4])

    with col_actions:
        st.markdown("""
        <div class="apex-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2rem;">⏰</span>
                    <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0; color: #111827;">Action Items & Deadlines</h3>
                </div>
                <span class="badge badge-warning">2 Pending</span>
            </div>
        """, unsafe_allow_html=True)

        # Action Item 1: Quiz
        st.markdown("""
        <div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-weight: 600; color: #111827; font-size: 0.95rem;">Quiz 6: Distributed Mutations & Concurrency</div>
                    <div style="font-size: 0.8rem; color: #DC2626; font-weight: 500; margin-top: 0.15rem;">⚠️ Due in 2 Days · 15 mins · 5 Questions (Pass at 70%)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📝 Start Module 6 Quiz", key="dash_start_quiz", use_container_width=True):
            auth.navigate_to("quiz")

        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)

        # Action Item 2: Sandbox
        st.markdown("""
        <div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 10px; padding: 0.85rem 1rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-weight: 600; color: #111827; font-size: 0.95rem;">Lab 6.1: Circuit Breaker Implementation</div>
                    <div style="font-size: 0.8rem; color: #0D9488; font-weight: 500; margin-top: 0.15rem;">🛠️ Interactive Sandbox · Unit Tests Required</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💻 Launch Code Sandbox", key="dash_open_sandbox", use_container_width=True):
            auth.navigate_to("code_sandbox")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_quick:
        st.markdown("""
        <div class="apex-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2rem;">💬</span>
                    <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0; color: #111827;">Cohort Q&A & Community</h3>
                </div>
                <span class="badge badge-primary">Active</span>
            </div>
            <div style="font-size: 0.85rem; color: #374151; margin-bottom: 0.5rem;">
                <strong>Trending Thread:</strong> <em>"Why route a canary probe instead of letting all traffic hit recovering service at once?"</em>
            </div>
            <div style="font-size: 0.775rem; color: #6B7280; margin-bottom: 0.85rem;">
                4 replies · Verified Answer by Prof. Alex Vance
            </div>
        """, unsafe_allow_html=True)

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("💬 View Thread", key="dash_view_qa_thread", use_container_width=True):
                st.session_state["selected_qa_id"] = "qa-1"
                auth.navigate_to("qa_thread")
        with col_q2:
            if st.button("📚 Lesson Notes", key="dash_view_notes", use_container_width=True):
                auth.navigate_to("transcript_notes")

        st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 1rem 0;'>", unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size: 0.85rem; color: #374151; margin-bottom: 0.35rem;">
            <strong>Next in Curriculum:</strong> Lesson 6.2
        </div>
        <div style="font-size: 0.775rem; color: #6B7280; margin-bottom: 0.75rem;">
            Cascading Failure Prevention & Bulkhead Isolation
        </div>
        """, unsafe_allow_html=True)

        if st.button("📖 Preview Lesson 6.2", key="dash_preview_6_2", use_container_width=True):
            auth.navigate_to("lesson_6_2")

        st.markdown("</div>", unsafe_allow_html=True)

    # Enrolled Curriculum Modules Breakdown Card
    st.markdown("""
    <div class="apex-card">
        <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 0.85rem 0; color: #111827;">
            Curriculum Progress Overview
        </h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; text-align: center;">
            <div style="color: #059669; font-weight: 700; font-size: 0.8rem;">COMPLETED ✅</div>
            <div style="font-weight: 600; font-size: 0.9rem; color: #1E293B; margin: 0.35rem 0;">Mod 1: Server Components</div>
            <div style="font-size: 0.75rem; color: #64748B;">4 / 4 Lessons</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; text-align: center;">
            <div style="color: #059669; font-weight: 700; font-size: 0.8rem;">COMPLETED ✅</div>
            <div style="font-weight: 600; font-size: 0.9rem; color: #1E293B; margin: 0.35rem 0;">Mod 5: Server Actions</div>
            <div style="font-size: 0.75rem; color: #64748B;">5 / 5 Lessons</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 10px; padding: 0.85rem; text-align: center;">
            <div style="color: #4F46E5; font-weight: 700; font-size: 0.8rem;">IN PROGRESS 🟡</div>
            <div style="font-weight: 600; font-size: 0.9rem; color: #1E293B; margin: 0.35rem 0;">Mod 6: Resilience & Breakers</div>
            <div style="font-size: 0.75rem; color: #64748B;">2 / 4 Units Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.85rem; text-align: center;">
            <div style="color: #94A3B8; font-weight: 700; font-size: 0.8rem;">UPCOMING 🔒</div>
            <div style="font-weight: 600; font-size: 0.9rem; color: #64748B; margin: 0.35rem 0;">Mod 7: Kafka Streaming</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Unlocks after Module 6</div>
        </div>
        """, unsafe_allow_html=True)
