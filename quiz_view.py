"""
Quiz Assessment View for ApexLearn LMS
Matches visual design of quiz.html with live timer, question navigation row,
multiple-choice and true/false questions, flag for review, and auto-grading persistence.
"""

import streamlit as st
import time
import datetime
import db
import auth

def render_quiz():
    database = db.load_db()
    questions = database.get("quiz_questions", [])
    total_q = len(questions)

    # Initialize timer if not already started
    if "quiz_timer_start" not in st.session_state or st.session_state["quiz_timer_start"] is None:
        st.session_state["quiz_timer_start"] = time.time()
        
    time_limit_secs = st.session_state.get("quiz_time_limit_mins", 15) * 60
    elapsed_secs = time.time() - st.session_state["quiz_timer_start"]
    remaining_secs = max(0, int(time_limit_secs - elapsed_secs))

    mins = remaining_secs // 60
    secs = remaining_secs % 60
    timer_str = f"{mins:02d}:{secs:02d}"

    # Top Quiz Navigation & Timer Bar
    col_back, col_title, col_timer = st.columns([1.5, 3.5, 2])
    with col_back:
        if st.button("← Exit to Dashboard", key="exit_quiz_btn"):
            auth.navigate_to("dashboard")
    with col_title:
        st.markdown("""
        <div style="text-align: center;">
            <span class="badge badge-secondary" style="font-size: 0.7rem;">Module 6 Assessment</span>
            <h2 style="font-size: 1.25rem; font-weight: 700; margin: 0.15rem 0 0 0; color: #111827;">
                Quiz 6: Distributed Mutations & Concurrency
            </h2>
        </div>
        """, unsafe_allow_html=True)
    with col_timer:
        timer_color = "#DC2626" if remaining_secs < 180 else "#4F46E5"
        st.markdown(f"""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="timer-pill" style="color: {timer_color}; border-color: {timer_color}40;">
                ⏱️ {timer_str} Left
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 0.75rem 0 1.25rem 0;'>", unsafe_allow_html=True)

    # Question Navigation Row (Circles 1 to N)
    current_q_idx = st.session_state.get("quiz_current_q", 1) - 1
    user_answers = st.session_state.setdefault("quiz_user_answers", {})
    flagged_set = st.session_state.setdefault("quiz_flagged", set())

    answered_count = len(user_answers)
    pct_complete = int((answered_count / total_q) * 100)

    col_prog_text, col_prog_bar = st.columns([2, 5])
    with col_prog_text:
        st.markdown(f"<span style='font-size: 0.85rem; font-weight: 600; color: #4B5563;'>Question {current_q_idx + 1} of {total_q} · {pct_complete}% Done</span>", unsafe_allow_html=True)
    with col_prog_bar:
        st.progress(answered_count / total_q)

    # Numbered pill selectors
    q_cols = st.columns(total_q)
    for idx, col in enumerate(q_cols):
        q_num = idx + 1
        q_id = str(questions[idx]["id"])
        is_current = (idx == current_q_idx)
        is_answered = q_id in user_answers
        is_flagged = q_id in flagged_set

        # Label styling
        label = f"{q_num}"
        if is_flagged:
            label += " 🚩"
        elif is_answered:
            label += " ✓"

        with col:
            btn_type = "primary" if is_current else "secondary"
            if st.button(label, key=f"q_nav_{q_num}", type=btn_type, use_container_width=True):
                st.session_state["quiz_current_q"] = q_num
                st.rerun()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # Active Question Box
    curr_q = questions[current_q_idx]
    q_id_str = str(curr_q["id"])

    st.markdown("""<div class="apex-card" style="padding: 1.75rem;">""", unsafe_allow_html=True)

    # Category and Flag indicator
    col_meta, col_flag = st.columns([3, 1])
    with col_meta:
        type_str = "Single Choice" if curr_q["type"] == "multiple_choice" else "True / False"
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <span class="badge badge-primary">{curr_q['category']}</span>
            <span style="font-size: 0.8rem; color: #6B7280; font-weight: 500;">
                Question {current_q_idx + 1} · {curr_q['points']} Pts · {type_str}
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col_flag:
        is_currently_flagged = q_id_str in flagged_set
        flag_label = "🚩 Flagged" if is_currently_flagged else "🏳️ Flag for Review"
        if st.button(flag_label, key=f"flag_btn_{q_id_str}"):
            if is_currently_flagged:
                flagged_set.remove(q_id_str)
            else:
                flagged_set.add(q_id_str)
            st.rerun()

    # Question text
    st.markdown(f"""
    <h3 style="font-size: 1.15rem; font-weight: 700; color: #111827; margin: 0.75rem 0 1.25rem 0; line-height: 1.5;">
        {curr_q['question']}
    </h3>
    """, unsafe_allow_html=True)

    # Options
    options = curr_q["options"]
    current_selected = user_answers.get(q_id_str, None)
    
    # Format options for radio
    selected_option = st.radio(
        "Select your answer:",
        options=options,
        index=current_selected if current_selected is not None else None,
        key=f"radio_q_{curr_q['id']}",
        label_visibility="collapsed"
    )

    if selected_option is not None:
        user_answers[q_id_str] = options.index(selected_option)

    st.markdown("</div>", unsafe_allow_html=True)

    # Footer Navigation Controls (Previous, Next, Submit)
    col_prev, col_next, col_submit = st.columns([1.5, 1.5, 2])
    with col_prev:
        if current_q_idx > 0:
            if st.button("← Previous Question", use_container_width=True):
                st.session_state["quiz_current_q"] = current_q_idx
                st.rerun()
    with col_next:
        if current_q_idx < total_q - 1:
            if st.button("Next Question →", use_container_width=True, type="primary"):
                st.session_state["quiz_current_q"] = current_q_idx + 2
                st.rerun()

    with col_submit:
        confirm_submit = st.checkbox("Ready to submit assessment", key="confirm_sub_check")
        if st.button("🚀 Finalize & Submit Quiz", use_container_width=True, type="primary", disabled=not confirm_submit):
            # Grade quiz
            total_points = sum(q["points"] for q in questions)
            earned_points = 0
            competency_scores = {}
            competency_totals = {}

            for q in questions:
                cat = q["category"]
                competency_totals[cat] = competency_totals.get(cat, 0) + q["points"]
                qid = str(q["id"])
                user_choice = user_answers.get(qid)
                if user_choice is not None and user_choice == q["correct_index"]:
                    earned_points += q["points"]
                    competency_scores[cat] = competency_scores.get(cat, 0) + q["points"]
                else:
                    competency_scores.setdefault(cat, 0)

            # Compute percentage
            pct = int(round((earned_points / total_points) * 100)) if total_points > 0 else 0
            passed = (pct >= 70)

            # Competency percentage
            final_competency = {}
            for cat, tot in competency_totals.items():
                sc = competency_scores.get(cat, 0)
                final_competency[cat] = int(round((sc / tot) * 100)) if tot > 0 else 0

            time_spent = int(time.time() - st.session_state["quiz_timer_start"])

            result_payload = {
                "score_percent": pct,
                "passed": passed,
                "points_earned": earned_points,
                "total_points": total_points,
                "time_taken_seconds": time_spent,
                "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "competency": final_competency,
                "answers": user_answers
            }

            user = auth.get_current_user()
            user_email = user.get("email", "student@apexlearn.io") if user else "student@apexlearn.io"
            db.save_quiz_result(user_email, result_payload)

            auth.navigate_to("quiz_result")
