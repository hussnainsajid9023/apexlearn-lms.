"""
Lesson Player View for ApexLearn LMS
Matches visual design of lesson-player.html with interactive video player controls,
state machine visualizer, lab objectives, key takeaways, and lesson subnavigation.
"""

import streamlit as st
import auth

def render_lesson_player():
    # Breadcrumbs & Navigation Bar
    col_crumb, col_actions = st.columns([3, 2])
    with col_crumb:
        st.markdown("""
        <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 0.25rem;">
            <span>Module 6: Distributed System Resilience</span> &nbsp;›&nbsp; <strong style="color: #111827;">Lesson 6.1</strong>
        </div>
        """, unsafe_allow_html=True)
    with col_actions:
        st.markdown("""
        <div style="text-align: right;">
            <span class="badge badge-secondary">Interactive Video & Lab</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="font-size: 1.65rem; font-weight: 800; color: #111827; margin: 0.25rem 0 1rem 0;">
        6.1 Resilient Circuit Breakers & Fallbacks
    </h1>
    """, unsafe_allow_html=True)

    # Sub-Navigation Tabs matching Stitch
    tab_overview, tab_transcript, tab_qa, tab_sandbox = st.tabs([
        "📺 Video Lecture & Objectives",
        "📝 Transcript & Personal Notes",
        "💬 Lesson Q&A Forum",
        "💻 Code Sandbox Lab"
    ])

    with tab_overview:
        # Video Simulation Screen Box
        st.markdown("""
        <div style="background: #0F172A; border-radius: 14px; padding: 1.5rem; color: #FFFFFF; position: relative; margin-bottom: 1.25rem; box-shadow: 0 4px 20px rgba(0,0,0,0.25);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid #1E293B; padding-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #EF4444; animation: pulse 2s infinite;"></span>
                    <span style="font-size: 0.85rem; font-weight: 600; color: #E2E8F0;">STREAM 1080p60 · EDGE CDN CACHED</span>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8;">
                    Chapter 3: Half-Open State Machine & Canary Logic
                </div>
            </div>
            
            <div style="min-height: 220px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: radial-gradient(circle, #1E293B 0%, #0F172A 100%); border-radius: 10px; border: 1px solid #334155; margin-bottom: 1rem; text-align: center; padding: 1.5rem;">
                <div style="width: 64px; height: 64px; border-radius: 50%; background: #4F46E5; display: flex; align-items: center; justify-content: center; margin-bottom: 0.75rem; box-shadow: 0 0 20px rgba(79,70,229,0.5);">
                    <span style="font-size: 2rem; margin-left: 4px;">▶</span>
                </div>
                <h3 style="font-size: 1.25rem; font-weight: 700; color: #FFFFFF; margin: 0 0 0.25rem 0;">
                    Distributed Circuit Breaker Architecture
                </h3>
                <p style="color: #94A3B8; font-size: 0.85rem; max-width: 450px; margin: 0;">
                    Lecturer: Prof. Alex Vance · Upstash Redis Lock Patterns & Zero-Downtime Fallback Mechanisms
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Video Player Controls
        v_col1, v_col2, v_col3, v_col4 = st.columns([1, 4, 1.5, 1.5])
        with v_col1:
            playing = st.button("⏯ Play/Pause", key="v_play_btn")
        with v_col2:
            time_pos = st.slider("Playback Position", 0, 38, 14, format="%d:00 min", label_visibility="collapsed")
        with v_col3:
            speed = st.selectbox("Speed", ["1.0x", "1.25x", "1.5x", "2.0x"], index=0, label_visibility="collapsed")
        with v_col4:
            quality = st.selectbox("Quality", ["1080p HD", "720p", "480p"], index=0, label_visibility="collapsed")

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        # State Machine Visualizer Card
        st.markdown("""
        <div class="apex-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2rem;">🔄</span>
                    <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0; color: #111827;">Circuit Breaker 3-State Finite Automata</h3>
                </div>
                <span class="badge badge-secondary">Live System Topology</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 0.75rem;">
                <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px; padding: 1rem; text-align: center;">
                    <div style="color: #16A34A; font-weight: 800; font-size: 1rem;">1. CLOSED ✅</div>
                    <div style="font-size: 0.8rem; color: #166534; margin: 0.35rem 0;">Normal Healthy Traffic</div>
                    <div style="font-size: 0.75rem; color: #4B5563;">Requests pass directly. Failures increment sliding counter.</div>
                </div>
                <div style="background: #FEF2F2; border: 1px solid #FECACA; border-radius: 10px; padding: 1rem; text-align: center;">
                    <div style="color: #DC2626; font-weight: 800; font-size: 1rem;">2. OPEN 🚨</div>
                    <div style="font-size: 0.8rem; color: #991B1B; margin: 0.35rem 0;">Failure Threshold Exceeded</div>
                    <div style="font-size: 0.75rem; color: #4B5563;">&gt; 5 errors in 60s. Trips OPEN! Immediate fast fallback returned.</div>
                </div>
                <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 1rem; text-align: center;">
                    <div style="color: #D97706; font-weight: 800; font-size: 1rem;">3. HALF-OPEN 🟡</div>
                    <div style="font-size: 0.8rem; color: #92400E; margin: 0.35rem 0;">Canary Probe Period</div>
                    <div style="font-size: 0.75rem; color: #4B5563;">After 30s cooldown: 1 trial request allowed. Success resets to CLOSED.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2 Column Split: Objectives vs Key Takeaways
        col_obj, col_takeaways = st.columns([1.5, 1.5])

        with col_obj:
            st.markdown("""
            <div class="apex-card">
                <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0 0 0.75rem 0; color: #111827;">
                    Interactive Lab Objectives
                </h3>
            """, unsafe_allow_html=True)

            o1 = st.checkbox("Analyze sliding window error thresholds (5 errors in 60s)", value=True, key="obj_1")
            o2 = st.checkbox("Configure Redis distributed lock for canary election", value=True, key="obj_2")
            o3 = st.checkbox("Implement exponential backoff with jitter on trips", value=False, key="obj_3")
            o4 = st.checkbox("Execute integration test assertions in Sandbox", value=False, key="obj_4")

            st.markdown("</div>", unsafe_allow_html=True)

        with col_takeaways:
            st.markdown("""
            <div class="apex-card">
                <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0 0 0.75rem 0; color: #111827;">
                    Lecture Key Takeaways
                </h3>
                <ul style="font-size: 0.85rem; color: #374151; line-height: 1.6; margin: 0; padding-left: 1.25rem;">
                    <li><strong>Fail Fast:</strong> Don't keep downstream clients waiting on hanging TCP sockets when a service is drowning.</li>
                    <li><strong>Thundering Herd Mitigation:</strong> Canary probing in HALF-OPEN prevents stampedes upon service reboot.</li>
                    <li><strong>Monotonic Lock Fencing:</strong> Prevents competing Edge nodes from duplicating recovery traffic.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Bottom Lesson Action Bar
        st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 1.5rem 0 1rem 0;'>", unsafe_allow_html=True)
        col_b1, col_b2, col_b3 = st.columns([1.5, 2, 1.5])
        with col_b1:
            if st.button("← Course Syllabus", use_container_width=True):
                auth.navigate_to("course")
        with col_b2:
            if st.button("💻 Open Lab Code Sandbox", use_container_width=True, type="primary"):
                auth.navigate_to("code_sandbox")
        with col_b3:
            if st.button("Next: Lesson 6.2 →", use_container_width=True):
                auth.navigate_to("lesson_6_2")

    with tab_transcript:
        from views.transcript_notes_view import render_transcript_notes_content
        render_transcript_notes_content()

    with tab_qa:
        from views.qa_view import render_qa_content
        render_qa_content()

    with tab_sandbox:
        from views.sandbox_view import render_sandbox_content
        render_sandbox_content()
