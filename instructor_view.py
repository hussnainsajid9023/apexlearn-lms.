"""
Instructor Dashboard and Course Management View for ApexLearn LMS
Provides class analytics, quiz grading overviews, student submission tracking, and curriculum moderation.
"""

import streamlit as st
import db
import auth

def render_instructor_dashboard():
    user = auth.get_current_user() or {}
    database = db.load_db()
    users = database.get("users", {})
    quiz_results = database.get("quiz_results", {})
    qa_posts = database.get("qa_posts", [])

    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <span class="badge badge-secondary">Instructor Faculty Portal</span>
        <h1 style="font-size: 1.85rem; font-weight: 800; color: #111827; margin: 0.25rem 0 0.25rem 0;">
            Welcome, {user.get('name', 'Prof. Alex Vance')} 👨‍🏫
        </h1>
        <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">
            Principal Instructor · Advanced Full-Stack Engineering (CS-804)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # High level Instructor Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Enrolled Cohort", "124 Students", delta="+12 this month")
    with m2:
        st.metric("Avg Quiz Score", "84.2%", delta="+3.1% vs last cohort")
    with m3:
        st.metric("Pass Rate", "91.8%", delta="Threshold 70%")
    with m4:
        st.metric("Q&A Discussions", f"{len(qa_posts)} Threads", delta="1 Pending Review")

    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

    # 2 Tabs: Cohort Submissions & Q&A Forum Queue
    tab_cohort, tab_qa_mod, tab_course_settings = st.tabs([
        "📊 Student Quiz Results & Grading",
        "💬 Forum Moderation Queue",
        "⚙️ Curriculum & Module Settings"
    ])

    with tab_cohort:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 1rem 0; color: #111827;">
                Quiz 6 Assessment Submissions
            </h3>
        """, unsafe_allow_html=True)

        # Build table of students and their quiz results
        student_rows = []
        for email, udata in users.items():
            if udata.get("role") == "Student":
                q_res = quiz_results.get(email)
                if q_res:
                    student_rows.append({
                        "Student": udata.get("name", "Student"),
                        "Email": email,
                        "Score": f"{q_res.get('score_percent', 0)}%",
                        "Points": f"{q_res.get('points_earned', 0)} / {q_res.get('total_points', 25)}",
                        "Status": "PASSED ✅" if q_res.get("passed") else "FAILED ❌",
                        "Submitted At": q_res.get("completed_at", "Recently")
                    })
                else:
                    student_rows.append({
                        "Student": udata.get("name", "Student"),
                        "Email": email,
                        "Score": "Not Taken",
                        "Points": "0 / 25",
                        "Status": "PENDING 🟡",
                        "Submitted At": "N/A"
                    })

        import pandas as pd
        df = pd.DataFrame(student_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_qa_mod:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 0.75rem 0; color: #111827;">
                Discussion Threads Awaiting Instructor Attention
            </h3>
        """, unsafe_allow_html=True)

        for post in qa_posts:
            has_instructor_resp = post.get("has_verified_instructor_answer", False)
            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                    <span class="badge badge-primary">{post.get('category')}</span>
                    <span style="font-size: 0.8rem; color: #64748B;">{post.get('created_at')}</span>
                </div>
                <div style="font-weight: 700; color: #111827; font-size: 0.95rem;">{post['title']}</div>
                <div style="font-size: 0.8rem; color: #4B5563; margin: 0.35rem 0;">Author: {post.get('author')} · Upvotes: {post.get('upvotes')}</div>
                <div style="font-size: 0.8rem; color: {'#059669' if has_instructor_resp else '#D97706'}; font-weight: 600;">
                    {'✓ Verified Answer Posted' if has_instructor_resp else '⚠️ Needs Instructor Review'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Review Thread & Post Official Response", key=f"inst_qa_{post['id']}"):
                st.session_state["selected_qa_id"] = post["id"]
                auth.navigate_to("qa_thread")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_course_settings:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 0.75rem 0; color: #111827;">
                Course Management Quick Links
            </h3>
            <p style="font-size: 0.85rem; color: #6B7280; margin-bottom: 1rem;">
                Jump directly to the student view of any lesson, sandbox lab, or assessment:
            </p>
        """, unsafe_allow_html=True)

        col_j1, col_j2, col_j3, col_j4 = st.columns(4)
        with col_j1:
            if st.button("📋 View Syllabus", use_container_width=True):
                auth.navigate_to("course")
        with col_j2:
            if st.button("📺 Lesson 6.1 Player", use_container_width=True):
                auth.navigate_to("lesson_player")
        with col_j3:
            if st.button("💻 Code Sandbox", use_container_width=True):
                auth.navigate_to("code_sandbox")
        with col_j4:
            if st.button("📝 Quiz 6", use_container_width=True):
                auth.navigate_to("quiz")

        st.markdown("</div>", unsafe_allow_html=True)
