"""
Quiz Result View for ApexLearn LMS
Matches visual design of quiz-result.html with celebratory or review banner,
score ring, competency breakdown, detailed question diagnostics, and persistence.
"""

import streamlit as st
import db
import auth

def render_quiz_result():
    user = auth.get_current_user() or {}
    user_name = user.get("name", "Jordan Alvarez")
    user_email = user.get("email", "student@apexlearn.io")

    result = db.get_user_quiz_result(user_email)
    database = db.load_db()
    questions = database.get("quiz_questions", [])

    if not result:
        st.warning("No quiz results found for your account yet. Please take the quiz first!")
        if st.button("Take Quiz Now", type="primary"):
            auth.navigate_to("quiz")
        return

    score_pct = result.get("score_percent", 0)
    passed = result.get("passed", score_pct >= 70)
    pts_earned = result.get("points_earned", 0)
    total_pts = result.get("total_points", 25)
    time_taken_s = result.get("time_taken_seconds", 360)
    mins = time_taken_s // 60
    secs = time_taken_s % 60
    time_str = f"{mins}m {secs:02d}s"
    competencies = result.get("competency", {})
    user_answers = result.get("answers", {})

    # Top Navigation Back link
    col_nav, col_actions = st.columns([2, 2])
    with col_nav:
        if st.button("← Back to Dashboard", key="res_back_dash"):
            auth.navigate_to("dashboard")
    with col_actions:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 0.35rem;">
            <span style="font-size: 0.8rem; color: #6B7280;">Completed: {result.get('completed_at', 'Recently')}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

    # Hero Result Card
    card_bg = "linear-gradient(135deg, #ECFDF5 0%, #FFFFFF 100%)" if passed else "linear-gradient(135deg, #FEF2F2 0%, #FFFFFF 100%)"
    card_border = "#A7F3D0" if passed else "#FECACA"
    badge_class = "badge-success" if passed else "badge-danger"
    badge_text = "PASSED · 70% THRESHOLD MET" if passed else "NOT PASSED · 70% THRESHOLD"
    title_text = f"Congratulations, {user_name}! 🎉" if passed else f"Review Required, {user_name}"
    subtitle_text = "You demonstrated strong mastery of distributed concurrency, locks, and state transitions." if passed else "You scored below the 70% requirement. Review the diagnostic breakdown below and retake the quiz."

    st.markdown(f"""
    <div style="background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem; text-align: center;">
        <span class="badge {badge_class}" style="margin-bottom: 0.75rem;">{badge_text}</span>
        <h1 style="font-size: 1.85rem; font-weight: 800; color: #111827; margin: 0 0 0.5rem 0;">
            {title_text}
        </h1>
        <p style="color: #4B5563; font-size: 0.95rem; max-width: 600px; margin: 0 auto 1.5rem auto;">
            {subtitle_text}
        </p>
        <div class="score-circle-container {'score-circle-fail' if not passed else ''}">
            <span style="font-size: 2rem; font-weight: 800; color: {'#10B981' if passed else '#EF4444'}; line-height: 1;">
                {score_pct}%
            </span>
            <span style="font-size: 0.7rem; font-weight: 600; color: #6B7280; text-transform: uppercase; margin-top: 0.2rem;">
                Overall Score
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Performance Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Total Score",
            value=f"{score_pct}%",
            delta="Pass at 70%" if passed else "- Required 70%"
        )
    with m2:
        st.metric(
            label="Points Earned",
            value=f"{pts_earned} / {total_pts}",
            delta="5 pts per question"
        )
    with m3:
        st.metric(
            label="Time Spent",
            value=time_str,
            delta="Under 15m limit"
        )
    with m4:
        st.metric(
            label="Certification Status",
            value="Qualified" if passed else "Pending Retry",
            delta="Module 6 Credit" if passed else "Review Needed"
        )

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    # 2 Columns: Competency Breakdown vs Retake Actions
    col_comp, col_actions_side = st.columns([1.6, 1.4])

    with col_comp:
        st.markdown("""
        <div class="apex-card">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0; color: #111827;">Competency Breakdown</h3>
                <span class="badge badge-primary">Topic Analysis</span>
            </div>
        """, unsafe_allow_html=True)

        for topic, score in competencies.items():
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; font-size: 0.875rem; font-weight: 600; color: #374151; margin-bottom: 0.25rem;">
                <span>{topic}</span>
                <span style="color: {'#059669' if score >= 70 else '#DC2626'};">{score}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(score / 100)
            st.markdown("<div style='margin-bottom: 0.65rem;'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_actions_side:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 0.5rem 0; color: #111827;">Assessment Actions</h3>
            <p style="font-size: 0.85rem; color: #6B7280; margin-bottom: 1rem;">
                ApexLearn allows unlimited retakes; your highest passing grade is preserved in your permanent academic transcript.
            </p>
        """, unsafe_allow_html=True)

        if st.button("🔄 Retake Quiz", key="retake_quiz_btn", use_container_width=True, type="primary"):
            st.session_state["quiz_user_answers"] = {}
            st.session_state["quiz_timer_start"] = None
            st.session_state["quiz_current_q"] = 1
            auth.navigate_to("quiz")

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("📖 Review Lesson 6.1 Notes", key="review_notes_btn", use_container_width=True):
            auth.navigate_to("transcript_notes")

        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("⏩ Proceed to Lesson 6.2", key="proceed_6_2_btn", use_container_width=True):
            auth.navigate_to("lesson_6_2")

        st.markdown("</div>", unsafe_allow_html=True)

    # Detailed Question Diagnostics Section
    st.markdown("""
    <div class="apex-card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
            <h3 style="font-size: 1.2rem; font-weight: 700; margin: 0; color: #111827;">Question Diagnostics & Solutions</h3>
            <span style="font-size: 0.85rem; color: #6B7280;">Detailed Architectural Explanations</span>
        </div>
    """, unsafe_allow_html=True)

    filter_choice = st.radio(
        "Filter Diagnostics:",
        ["All Questions", "Incorrect Only", "Correct Only"],
        horizontal=True,
        label_visibility="collapsed"
    )

    for q in questions:
        qid_str = str(q["id"])
        user_choice_idx = user_answers.get(qid_str)
        is_correct = (user_choice_idx is not None and user_choice_idx == q["correct_index"])

        if filter_choice == "Incorrect Only" and is_correct:
            continue
        if filter_choice == "Correct Only" and not is_correct:
            continue

        status_badge = '<span class="badge badge-success">✓ Correct (+5 Pts)</span>' if is_correct else '<span class="badge badge-danger">✗ Incorrect (0 Pts)</span>'
        user_choice_str = q["options"][user_choice_idx] if user_choice_idx is not None else "No answer provided"
        correct_choice_str = q["options"][q["correct_index"]]

        st.markdown(f"""
        <div style="background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                <span class="badge badge-primary">{q['category']}</span>
                {status_badge}
            </div>
            <div style="font-weight: 700; color: #111827; font-size: 0.95rem; margin-bottom: 0.75rem; line-height: 1.4;">
                Q{q['id']}. {q['question']}
            </div>
            <div style="font-size: 0.85rem; margin-bottom: 0.35rem;">
                <strong style="color: {'#059669' if is_correct else '#DC2626'};">Your Response:</strong> {user_choice_str}
            </div>
            {f'<div style="font-size: 0.85rem; color: #059669; margin-bottom: 0.65rem;"><strong>Correct Answer:</strong> {correct_choice_str}</div>' if not is_correct else ''}
            <div style="background: #FFFFFF; border-left: 3px solid #4F46E5; border-radius: 4px; padding: 0.75rem 1rem; margin-top: 0.5rem; font-size: 0.85rem; color: #374151; line-height: 1.5;">
                <strong style="color: #4F46E5;">Architectural Principle:</strong> {q['explanation']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
