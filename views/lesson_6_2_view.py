"""
Lesson 6.2 View for ApexLearn LMS
Matches visual design of lesson-6-2.html with interactive Thread Pool Saturation simulator,
bulkhead topology monitor, cascading failure theory, and direct launch to Module 6 Quiz.
"""

import streamlit as st
import auth

def render_lesson_6_2():
    # Breadcrumbs & Navigation
    col_crumb, col_actions = st.columns([3, 2])
    with col_crumb:
        if st.button("← Previous: Lesson 6.1", key="l62_back_61"):
            auth.navigate_to("lesson_player")
    with col_actions:
        st.markdown("""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="badge badge-secondary">Lesson 6.2 · Architecture Lab</span>
        </div>
        """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
    <div class="apex-hero-card">
        <span class="badge badge-primary" style="margin-bottom: 0.5rem;">Distributed Systems Resilience</span>
        <h1 style="font-size: 1.75rem; font-weight: 800; color: #111827; margin: 0.25rem 0 0.5rem 0;">
            6.2 Cascading Failure Prevention & Bulkhead Isolation
        </h1>
        <p style="color: #4B5563; font-size: 0.95rem; margin: 0; line-height: 1.5;">
            Explore the Thread Pool Saturation Trap, Little's Law queue dynamics, and how isolating thread pools into dedicated compartments protects high-availability applications.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Interactive Thread Pool Saturation & Bulkhead Simulator
    st.markdown("""
    <div class="apex-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.25rem;">⚙️</span>
                <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0; color: #111827;">Interactive Bulkhead & Latency Simulator</h3>
            </div>
            <span class="badge badge-secondary">Little's Law Engine</span>
        </div>
        <p style="font-size: 0.85rem; color: #64748B; margin-bottom: 1.25rem;">
            Adjust downstream latency and incoming load to visualize how unisolated services exhaust the Node.js / Java worker thread pool.
        </p>
    """, unsafe_allow_html=True)

    sim_c1, sim_c2, sim_c3 = st.columns(3)
    with sim_c1:
        downstream_latency_ms = st.slider("Downstream Latency (ms)", min_value=50, max_value=3000, value=650, step=50)
    with sim_c2:
        incoming_rps = st.slider("Incoming Load (RPS)", min_value=50, max_value=800, value=250, step=25)
    with sim_c3:
        bulkhead_pool_limit = st.slider("Bulkhead Pool Limit (Threads)", min_value=20, max_value=200, value=60, step=10)

    # Mathematical Simulation based on Little's Law: L = λ * W
    required_concurrency = (incoming_rps * downstream_latency_ms) / 1000.0
    saturation_pct = min(100.0, (required_concurrency / bulkhead_pool_limit) * 100.0)
    queue_overflow = max(0.0, required_concurrency - bulkhead_pool_limit)

    is_healthy = saturation_pct < 75
    is_warning = 75 <= saturation_pct < 100
    is_exhausted = saturation_pct >= 100

    status_color = "#10B981" if is_healthy else ("#F59E0B" if is_warning else "#EF4444")
    status_label = "HEALTHY (Threads Available)" if is_healthy else ("HEAVILY LOADED" if is_warning else "🚨 THREAD POOL SATURATED (Requests Dropped!)")

    # Metrics Display
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Concurrency Required", f"{required_concurrency:.1f} Threads", help="Calculated using Little's Law: RPS × Latency")
    with m_col2:
        st.metric("Bulkhead Capacity", f"{bulkhead_pool_limit} Threads", help="Maximum concurrent threads allocated to this dependency")
    with m_col3:
        st.metric("Pool Saturation", f"{saturation_pct:.1f}%", delta="Normal" if is_healthy else "High Load")
    with m_col4:
        st.metric("Rejected Requests", f"{queue_overflow:.0f}/sec", delta="Zero Loss" if queue_overflow == 0 else "- DROPPING TRAFFIC")

    st.markdown(f"""
    <div style="background: {status_color}15; border: 1px solid {status_color}40; border-radius: 8px; padding: 0.85rem 1rem; margin-top: 1rem; text-align: center;">
        <span style="font-weight: 800; font-size: 0.95rem; color: {status_color};">
            SYSTEM STATE: {status_label}
        </span>
    </div>
    </div>
    """, unsafe_allow_html=True)

    # Architecture Theory & Diagram
    col_th1, col_th2 = st.columns([1.5, 1.5])

    with col_th1:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem 0; color: #111827;">
                The Thread Pool Saturation Trap
            </h3>
            <p style="font-size: 0.85rem; color: #4B5563; line-height: 1.6;">
                In a standard server architecture without bulkheads, all microservice dependencies share a single global thread pool.
                When a non-critical third-party analytics vendor begins responding in <strong>2,500ms</strong> instead of <strong>50ms</strong>, 
                worker threads remain blocked waiting on network sockets.
            </p>
            <p style="font-size: 0.85rem; color: #4B5563; line-height: 1.6;">
                Within seconds, all available CPU execution slots are consumed, causing core login and payment endpoints to fail with HTTP 504 Gateway Timeouts.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_th2:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.1rem; font-weight: 700; margin: 0 0 0.5rem 0; color: #111827;">
                Bulkhead Quarantine Pattern
            </h3>
            <p style="font-size: 0.85rem; color: #4B5563; line-height: 1.6;">
                By provisioning isolated thread compartments with strict timeout fences:
            </p>
            <ul style="font-size: 0.85rem; color: #4B5563; line-height: 1.6; padding-left: 1.25rem;">
                <li><strong>Payment Bulkhead:</strong> 50 dedicated threads</li>
                <li><strong>Search Bulkhead:</strong> 30 dedicated threads</li>
                <li><strong>Analytics Bulkhead:</strong> 10 dedicated threads</li>
            </ul>
            <p style="font-size: 0.85rem; color: #059669; font-weight: 600; line-height: 1.5; margin-top: 0.5rem;">
                ✓ Even if Analytics completely halts, 90% of platform threads remain 100% available for payments!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Launch Quiz Assessment Callout Card
    st.markdown("""
    <div class="apex-card" style="background: linear-gradient(135deg, #EEF2FF 0%, #FFFFFF 100%); border: 1px solid #C7D2FE; margin-top: 1.5rem; text-align: center; padding: 2rem;">
        <span class="badge badge-primary" style="margin-bottom: 0.5rem;">Module 6 Certification Ready</span>
        <h2 style="font-size: 1.4rem; font-weight: 800; color: #111827; margin: 0.25rem 0 0.5rem 0;">
            Ready to Validate Your Knowledge?
        </h2>
        <p style="color: #4B5563; font-size: 0.9rem; max-width: 550px; margin: 0 auto 1.25rem auto;">
            Take the 5-question timed assessment covering Next.js Server Actions, Redis locks, Circuit Breakers, and Bulkhead Isolation.
        </p>
    """, unsafe_allow_html=True)

    q_col1, q_col2, q_col3 = st.columns([1.5, 2, 1.5])
    with q_col2:
        if st.button("📝 Start Module 6 Quiz Assessment", key="l62_start_quiz", type="primary", use_container_width=True):
            auth.navigate_to("quiz")

    st.markdown("</div>", unsafe_allow_html=True)
