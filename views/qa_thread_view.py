"""
Q&A Thread Detail View for ApexLearn LMS
Matches visual design of qa-thread.html with full question context, upvoting,
verified instructor badge reply styling, and new reply posting.
"""

import streamlit as st
import db
import auth

def render_qa_thread():
    post_id = st.session_state.get("selected_qa_id", "qa-1")
    database = db.load_db()
    qa_posts = database.get("qa_posts", [])
    user = auth.get_current_user() or {}

    # Find the post
    post = next((p for p in qa_posts if p["id"] == post_id), None)
    if not post:
        st.warning("Thread not found.")
        if st.button("← Return to Q&A Forum"):
            auth.navigate_to("lesson_player")
        return

    # Back Navigation Bar
    col_back, col_actions = st.columns([2, 2])
    with col_back:
        if st.button("← Back to All Discussions", key="thread_back_forum"):
            auth.navigate_to("lesson_player")
    with col_actions:
        st.markdown(f"""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="badge badge-primary">{post.get('category', 'Architecture')}</span>
        </div>
        """, unsafe_allow_html=True)

    # Main Question Card
    verified_badge = '<span class="badge badge-secondary">✓ Verified Instructor Answer</span>' if post.get("has_verified_instructor_answer") else ''
    
    st.markdown(f"""
    <div class="apex-hero-card" style="margin-top: 0.5rem; margin-bottom: 1.25rem;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #4F46E5; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700;">
                    {post.get('author', 'J')[0]}
                </div>
                <div>
                    <div style="font-weight: 700; color: #111827; font-size: 0.95rem;">{post.get('author', 'Jordan Alvarez')}</div>
                    <div style="font-size: 0.75rem; color: #6B7280;">{post.get('author_role', 'Student')} · {post.get('created_at', '2 hours ago')}</div>
                </div>
            </div>
            {verified_badge}
        </div>
        <h1 style="font-size: 1.35rem; font-weight: 800; color: #111827; margin: 0.75rem 0 0.5rem 0; line-height: 1.4;">
            {post['title']}
        </h1>
        <div style="font-size: 0.95rem; color: #374151; line-height: 1.6; margin-bottom: 1rem;">
            {post['content']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upvote Bar
    col_up, col_replies_count = st.columns([1.5, 3.5])
    with col_up:
        if st.button(f"👍 Upvote Question ({post.get('upvotes', 0)})", key="thread_upvote_btn", use_container_width=True):
            new_votes = db.upvote_qa_post(post["id"])
            st.rerun()
    with col_replies_count:
        st.markdown(f"""
        <div style="padding-top: 0.5rem; font-size: 0.9rem; font-weight: 600; color: #4B5563;">
            💬 {len(post.get('replies', []))} Responses in this thread
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #E5E7EB; margin: 1.25rem 0;'>", unsafe_allow_html=True)

    # Responses List
    for reply in post.get("replies", []):
        is_inst = reply.get("is_instructor", False)
        border_style = "border: 2px solid #0D9488; background: #F0FDFA;" if is_inst else "border: 1px solid #E5E7EB; background: #FFFFFF;"
        instructor_badge = '<span class="badge badge-secondary" style="font-size: 0.7rem;">⭐ Official Instructor Answer</span>' if is_inst else ''

        st.markdown(f"""
        <div class="apex-card" style="{border_style} padding: 1.25rem; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.65rem;">
                    <div style="width: 36px; height: 36px; border-radius: 50%; background: {'#0D9488' if is_inst else '#6366F1'}; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem;">
                        {reply.get('author', 'A')[0]}
                    </div>
                    <div>
                        <div style="font-weight: 700; color: #111827; font-size: 0.9rem;">{reply.get('author', 'Author')}</div>
                        <div style="font-size: 0.75rem; color: #6B7280;">{reply.get('author_role', 'Contributor')} · {reply.get('created_at', 'Recently')}</div>
                    </div>
                </div>
                {instructor_badge}
            </div>
            <div style="font-size: 0.9rem; color: #374151; line-height: 1.6; margin-top: 0.35rem;">
                {reply.get('content', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Post a Reply Card
    st.markdown("""
    <div class="apex-card" style="margin-top: 1.5rem;">
        <h4 style="font-size: 1.05rem; font-weight: 700; color: #111827; margin: 0 0 0.5rem 0;">
            Contribute to this discussion
        </h4>
    """, unsafe_allow_html=True)

    reply_content = st.text_area(
        "Your Answer or Clarification",
        placeholder="Provide architectural insights, code samples, or follow-up observations...",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("Post Response", key="submit_reply_btn", type="primary"):
        if not reply_content.strip():
            st.error("Please enter a reply before posting.")
        else:
            is_instructor_user = (user.get("role") == "Instructor")
            db.add_qa_reply(
                post_id=post["id"],
                content=reply_content.strip(),
                author_name=user.get("name", "Jordan Alvarez"),
                author_role=user.get("role", "Student"),
                author_avatar=user.get("avatar", ""),
                is_instructor=is_instructor_user
            )
            st.success("Your reply has been published!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
