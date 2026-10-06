"""
Lesson Q&A Forum View for ApexLearn LMS
Matches visual design of lesson-qa.html with filter pills, search input, upvote tallies,
instructor verified badges, and 'Ask a Question' submission form.
"""

import streamlit as st
import db
import auth

def render_qa_content():
    database = db.load_db()
    qa_posts = database.get("qa_posts", [])
    user = auth.get_current_user() or {}

    col_title, col_ask = st.columns([3, 1.5])
    with col_title:
        st.markdown("""
        <div>
            <h3 style="font-size: 1.25rem; font-weight: 700; margin: 0; color: #111827;">Lesson 6.1 Discussion Forum</h3>
            <p style="font-size: 0.85rem; color: #6B7280; margin: 0.2rem 0 0.75rem 0;">Ask questions, explore architectural trade-offs, and receive instructor feedback.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_ask:
        with st.popover("➕ Ask a Question", use_container_width=True):
            st.markdown("<h4 style='font-size: 1rem; font-weight: 700; margin: 0 0 0.5rem 0;'>Post New Question</h4>", unsafe_allow_html=True)
            new_title = st.text_input("Question Title", placeholder="e.g. How does exponential backoff prevent stampedes?")
            new_cat = st.selectbox("Category", ["Architecture", "Lab Sandbox", "Theory", "Other"])
            new_content = st.text_area("Detailed Problem Statement", placeholder="Explain your question or paste relevant error logs...", height=120)
            if st.button("Publish Question", type="primary", use_container_width=True):
                if not new_title.strip() or not new_content.strip():
                    st.error("Please provide both a title and description.")
                else:
                    new_id = db.add_qa_post(
                        title=new_title,
                        content=new_content,
                        category=new_cat,
                        author_name=user.get("name", "Jordan Alvarez"),
                        author_role=user.get("role", "Student"),
                        author_avatar=user.get("avatar", "")
                    )
                    st.success("Question published successfully!")
                    st.session_state["selected_qa_id"] = new_id
                    auth.navigate_to("qa_thread")

    # Search & Filter Controls
    search_q = st.text_input("Search questions...", placeholder="Filter by keywords (e.g. canary, redis, timeout)...", label_visibility="collapsed")

    filter_mode = st.radio(
        "Filter by status:",
        ["All Questions", "Instructor Responded", "Unanswered"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)

    # Question Cards
    for post in qa_posts:
        if search_q:
            query = search_q.lower()
            if query not in post["title"].lower() and query not in post["content"].lower():
                continue

        if filter_mode == "Instructor Responded" and not post.get("has_verified_instructor_answer"):
            continue
        if filter_mode == "Unanswered" and post.get("is_answered"):
            continue

        verified_badge = '<span class="badge badge-secondary" style="font-size: 0.7rem;">✓ Verified Instructor Answer</span>' if post.get("has_verified_instructor_answer") else ''
        replies_count = len(post.get("replies", []))

        st.markdown(f"""
        <div class="apex-card" style="padding: 1.15rem; margin-bottom: 0.85rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.4rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span class="badge badge-primary">{post.get('category', 'Architecture')}</span>
                    {verified_badge}
                </div>
                <div style="font-size: 0.8rem; color: #94A3B8;">{post.get('created_at', 'Recently')}</div>
            </div>
            <h4 style="font-size: 1.05rem; font-weight: 700; color: #111827; margin: 0.35rem 0 0.5rem 0; line-height: 1.4;">
                {post['title']}
            </h4>
            <p style="font-size: 0.85rem; color: #4B5563; margin: 0 0 0.75rem 0; line-height: 1.5;">
                {post['content'][:150]}...
            </p>
            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 0.5rem; border-top: 1px solid #F1F5F9;">
                <div style="font-size: 0.8rem; color: #64748B;">
                    Posted by <strong>{post.get('author', 'Anonymous')}</strong> ({post.get('author_role', 'Student')}) · 💬 {replies_count} Replies · 👍 {post.get('upvotes', 0)} Upvotes
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_open, col_upvote, col_pad = st.columns([1.5, 1.2, 3])
        with col_open:
            if st.button("Open Discussion →", key=f"open_qa_{post['id']}", use_container_width=True):
                st.session_state["selected_qa_id"] = post["id"]
                auth.navigate_to("qa_thread")
        with col_upvote:
            if st.button(f"👍 Upvote ({post.get('upvotes', 0)})", key=f"upvote_{post['id']}", use_container_width=True):
                db.upvote_qa_post(post["id"])
                st.rerun()

def render_qa():
    col_crumb, col_actions = st.columns([3, 2])
    with col_crumb:
        if st.button("← Back to Lesson Player", key="qa_back_player"):
            auth.navigate_to("lesson_player")
    with col_actions:
        st.markdown("""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="badge badge-secondary">Lesson 6.1 Forum</span>
        </div>
        """, unsafe_allow_html=True)

    render_qa_content()
