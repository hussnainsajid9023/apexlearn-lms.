"""
Code Diff View for ApexLearn LMS
Matches visual design of code-diff.html and code-diff-landscape.html with unified & side-by-side
diff toggle, color-coded lines, architectural rationale, and sandbox synchronization.
"""

import streamlit as st
import difflib
import db
import auth

def render_diff():
    database = db.load_db()
    solution_code = database.get("reference_solution_code", "")
    student_code = st.session_state.get("sandbox_code", database.get("starter_code", ""))

    # Header & Mode Switcher
    col_back, col_title, col_view_mode = st.columns([1.5, 3, 2.5])
    with col_back:
        if st.button("← Back to Sandbox", key="diff_back_sb"):
            auth.navigate_to("code_sandbox")
    with col_title:
        st.markdown("""
        <div>
            <h2 style="font-size: 1.35rem; font-weight: 800; color: #111827; margin: 0;">Diff with Reference Solution</h2>
            <span style="font-size: 0.8rem; color: #6B7280;">Lab 6.1 · Production Pattern Benchmark</span>
        </div>
        """, unsafe_allow_html=True)
    with col_view_mode:
        diff_mode = st.radio(
            "View Mode:",
            ["Portrait (Unified Diff)", "Landscape (Side-by-Side)"],
            index=0 if st.session_state.get("diff_mode", "portrait") == "portrait" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state["diff_mode"] = "portrait" if "Portrait" in diff_mode else "landscape"

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # Architectural Rationale Callout Card
    st.markdown("""
    <div class="apex-hero-card" style="padding: 1.15rem; margin-bottom: 1.25rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
            <span style="font-size: 1.2rem;">💡</span>
            <strong style="color: #4F46E5; font-size: 0.95rem;">Why this Reference Implementation Matters:</strong>
        </div>
        <p style="font-size: 0.85rem; color: #374151; margin: 0; line-height: 1.5;">
            The reference solution introduces <strong>Exponential Backoff with Full Jitter</strong> and <strong>Redis Monotonic Canary Leases</strong>. 
            If a downstream system crashes repeatedly, a fixed 30-second cooldown causes a cyclical retry stampede. Multiplying cooldown by <code>2^trips</code> allows backend databases to safely repopulate caching layers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Compute Diff Lines
    student_lines = student_code.splitlines()
    solution_lines = solution_code.splitlines()

    if st.session_state["diff_mode"] == "landscape":
        # Side-by-Side Landscape Mode (code-diff-landscape.html)
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px 8px 0 0; padding: 0.5rem 0.75rem; font-weight: 700; font-size: 0.85rem; color: #475569;">
                Your Implementation (circuit-breaker.ts)
            </div>
            """, unsafe_allow_html=True)
            st.code(student_code, language="typescript")
        with col_right:
            st.markdown("""
            <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px 8px 0 0; padding: 0.5rem 0.75rem; font-weight: 700; font-size: 0.85rem; color: #065F46;">
                Reference Solution (Production Architecture)
            </div>
            """, unsafe_allow_html=True)
            st.code(solution_code, language="typescript")
    else:
        # Portrait Unified Diff Mode (code-diff.html)
        st.markdown("""
        <div class="apex-card" style="padding: 1rem; margin-bottom: 1rem;">
            <div style="display: flex; gap: 1rem; font-size: 0.8rem; margin-bottom: 0.75rem;">
                <span style="display: flex; align-items: center; gap: 0.35rem; color: #065F46; font-weight: 600;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #10B981; border-radius: 2px;"></span> + Reference Additions
                </span>
                <span style="display: flex; align-items: center; gap: 0.35rem; color: #991B1B; font-weight: 600;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #EF4444; border-radius: 2px;"></span> - Student Code
                </span>
            </div>
            <div style="border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden; background: #FAFAFA;">
        """, unsafe_allow_html=True)

        diff = list(difflib.unified_diff(
            student_lines,
            solution_lines,
            fromfile="your_code/circuit-breaker.ts",
            tofile="reference/circuit-breaker.ts",
            lineterm=""
        ))

        diff_html = ""
        for line in diff[2:]:  # skip headers
            if line.startswith("+"):
                diff_html += f"<div class='diff-line diff-add'>+ {line[1:]}</div>"
            elif line.startswith("-"):
                diff_html += f"<div class='diff-line diff-del'>- {line[1:]}</div>"
            elif line.startswith("@@"):
                diff_html += f"<div class='diff-line' style='background: #EEF2FF; color: #4F46E5; font-weight: bold;'>{line}</div>"
            else:
                diff_html += f"<div class='diff-line diff-neutral'>  {line}</div>"

        st.markdown(diff_html, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    # Action Toolbar
    col_act1, col_act2, col_act3 = st.columns([2, 2, 2])
    with col_act1:
        if st.button("📥 Adopt Reference Solution", use_container_width=True, type="primary"):
            st.session_state["sandbox_code"] = solution_code
            st.success("Reference code copied to your sandbox!")
            auth.navigate_to("code_sandbox")
    with col_act2:
        if st.button("↩ Return to My Code", use_container_width=True):
            auth.navigate_to("code_sandbox")
    with col_act3:
        if st.button("⏩ Proceed to Lesson 6.2", use_container_width=True):
            auth.navigate_to("lesson_6_2")
