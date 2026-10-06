"""
Transcript and Personal Notes View for ApexLearn LMS
Matches visual design of transcript-notes.html with synchronized searchable transcript,
live markdown notes editor, auto-saving to local JSON persistence, and markdown export.
"""

import streamlit as st
import db
import auth

TRANSCRIPT_ITEMS = [
    {"time": "00:00", "title": "Introduction to Circuit Breakers", "text": "Welcome to Lesson 6.1. In distributed microservice topologies, cascading failure is the single greatest threat to 99.99% availability. When a downstream payment processor or database lags, calling services accumulate hanging sockets, leading to total thread pool exhaustion."},
    {"time": "04:15", "title": "The 3 States of Finite State Breakers", "text": "A robust circuit breaker operates across three states: CLOSED, where requests pass without interruption; OPEN, where requests immediately return a cached or degraded fallback; and HALF-OPEN, which acts as a cautious canary test probe."},
    {"time": "09:30", "title": "Sliding Window Counters & Redis Locks", "text": "Rather than calculating errors over all time, we maintain a 60-second sliding window counter. In edge-distributed deployments with multiple Vercel or Cloudflare workers, state must be coordinated via Upstash Redis quorum locks to prevent split-brain canary triggers."},
    {"time": "18:45", "title": "The Half-Open Canary Probe Protocol", "text": "After the 30-second cooldown expires, the breaker transitions to HALF-OPEN. Crucially, we do not let 100% of user traffic hit the recovering service. Instead, we allow exactly ONE trial request. If it succeeds, the breaker resets to CLOSED; if it fails, it trips back to OPEN with exponential backoff."},
    {"time": "28:10", "title": "Zero-Downtime Fallback Responses", "text": "Fallbacks can return stale cached data from Redis, static graceful defaults, or queue mutations for asynchronous outbox processing, guaranteeing the customer never observes a blank error screen."}
]

def render_transcript_notes_content():
    user = auth.get_current_user() or {}
    user_email = user.get("email", "student@apexlearn.io")

    col_trans, col_notes = st.columns([1.3, 1.7])

    with col_trans:
        st.markdown("""
        <div class="apex-card" style="height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0; color: #111827;">Synchronized Transcript</h3>
                <span class="badge badge-secondary">Audio & Video Aligned</span>
            </div>
        """, unsafe_allow_html=True)

        search_query = st.text_input("🔍 Search transcript...", placeholder="e.g. Canary, Redis, Fallback", label_visibility="collapsed")

        st.markdown("<div style='max-height: 480px; overflow-y: auto; padding-right: 0.25rem;'>", unsafe_allow_html=True)

        for item in TRANSCRIPT_ITEMS:
            if search_query:
                q = search_query.lower()
                if q not in item["title"].lower() and q not in item["text"].lower():
                    continue

            st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.65rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <span style="font-weight: 700; color: #4F46E5; font-size: 0.85rem;">{item['title']}</span>
                    <span style="font-family: monospace; font-size: 0.75rem; background: #EEF2FF; color: #4F46E5; padding: 0.15rem 0.45rem; border-radius: 4px; font-weight: 600;">{item['time']}</span>
                </div>
                <div style="font-size: 0.825rem; color: #475569; line-height: 1.5;">
                    {item['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_notes:
        st.markdown("""
        <div class="apex-card" style="height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0; color: #111827;">Personal Notes & Code Snippets</h3>
                <span class="badge badge-primary">Auto-Persisted</span>
            </div>
        """, unsafe_allow_html=True)

        saved_notes = db.get_user_notes(user_email)

        note_tab_edit, note_tab_preview = st.tabs(["✏️ Edit Markdown Notes", "👁️ Live Preview"])

        with note_tab_edit:
            notes_input = st.text_area(
                "Notes Content",
                value=saved_notes,
                height=320,
                label_visibility="collapsed",
                help="Type Markdown notes; supports headers, code blocks, lists, and LaTeX math"
            )

            btn_save, btn_dl = st.columns([1, 1])
            with btn_save:
                if st.button("💾 Save Notes", key="save_notes_btn", type="primary", use_container_width=True):
                    db.save_user_notes(user_email, notes_input)
                    st.success("Notes saved and persisted to local database!")
            with btn_dl:
                st.download_button(
                    label="📥 Export Notes (.md)",
                    data=notes_input,
                    file_name="lesson_6_1_circuit_breakers_notes.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        with note_tab_preview:
            st.markdown(f"""
            <div style="background: #FAFAFA; border: 1px solid #E5E7EB; border-radius: 8px; padding: 1rem; min-height: 320px; font-size: 0.9rem; color: #1F2937;">
            """, unsafe_allow_html=True)
            st.markdown(notes_input)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

def render_transcript_notes():
    # Breadcrumbs & Navigation Bar
    col_crumb, col_actions = st.columns([3, 2])
    with col_crumb:
        if st.button("← Back to Lesson Player", key="tn_back_player"):
            auth.navigate_to("lesson_player")
    with col_actions:
        st.markdown("""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="badge badge-secondary">Lesson 6.1 Study Deck</span>
        </div>
        """, unsafe_allow_html=True)

    render_transcript_notes_content()
