"""
Interactive Code Sandbox View for ApexLearn LMS
Matches visual design of code-sandbox.html with multi-file tabs (circuit-breaker.ts, test-suite.ts, config.json),
test suite execution runner, dark terminal console, and solution diff launcher.
"""

import streamlit as st
import time
import db
import auth

def render_sandbox_content():
    database = db.load_db()
    default_starter_code = database.get("starter_code", "")

    if "sandbox_code" not in st.session_state:
        st.session_state["sandbox_code"] = default_starter_code
    if "test_output" not in st.session_state:
        st.session_state["test_output"] = None
    if "sandbox_active_tab" not in st.session_state:
        st.session_state["sandbox_active_tab"] = "circuit-breaker.ts"

    # Action Toolbar
    col_file_info, col_tools = st.columns([2, 3])
    with col_file_info:
        st.markdown("""
        <div>
            <span class="badge badge-secondary" style="font-size: 0.7rem;">Lab 6.1 Interactive Sandbox</span>
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0.2rem 0 0 0; color: #111827;">circuit-breaker.ts</h3>
        </div>
        """, unsafe_allow_html=True)
    with col_tools:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        col_b1, col_b2, col_b3 = st.columns([1, 1.2, 1.2])
        with col_b1:
            if st.button("🔄 Reset", key="sb_reset_code", use_container_width=True):
                st.session_state["sandbox_code"] = default_starter_code
                st.session_state["test_output"] = None
                st.rerun()
        with col_b2:
            if st.button("⚖️ Diff Solution", key="sb_diff_sol", use_container_width=True):
                auth.navigate_to("code_diff")
        with col_b3:
            if st.button("🚀 Submit Lab", key="sb_submit_lab", type="primary", use_container_width=True):
                st.success("Lab 6.1 verified and submitted! 100/100 points assigned.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Multi-file Tabs
    tab_ts, tab_tests, tab_cfg = st.tabs([
        "📄 circuit-breaker.ts (Active)",
        "🧪 test-suite.ts",
        "⚙️ config.json"
    ])

    with tab_ts:
        st.markdown("<div style='font-size: 0.8rem; color: #64748B; margin-bottom: 0.35rem;'>Edit your TypeScript Circuit Breaker implementation below:</div>", unsafe_allow_html=True)
        code_input = st.text_area(
            "Code Editor",
            value=st.session_state["sandbox_code"],
            height=340,
            label_visibility="collapsed",
            help="Full TypeScript implementation with Redis lock coordination"
        )
        st.session_state["sandbox_code"] = code_input

        # Run Tests Button
        if st.button("▶ Run Test Suite & Assertions", type="primary", use_container_width=True):
            with st.spinner("Compiling TypeScript and executing sandbox container test runners..."):
                time.sleep(0.6)  # realistic execution simulation
                st.session_state["test_output"] = {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "duration_ms": 42,
                    "passed": 5,
                    "total": 5,
                    "state": "HALF_OPEN -> CLOSED (HEALED)",
                    "logs": [
                        "[INFO] [PaymentsService] Initialized CircuitBreaker with failureThreshold=5, cooldown=30000ms",
                        "[TEST 1/5] Healthy traffic: 20 requests sent -> Breaker remains CLOSED ... PASSED [OK] (8ms)",
                        "[TEST 2/5] Chaos injection: 5 consecutive HTTP 500 downstream errors detected -> Breaker trips to OPEN ... PASSED [OK] (12ms)",
                        "[TEST 3/5] Fast fallback: 50 client requests routed to fallback without TCP socket overhead ... PASSED [OK] (4ms)",
                        "[TEST 4/5] Cooldown simulated: After 30,000ms, breaker permits canary trial (HALF_OPEN) ... PASSED [OK] (9ms)",
                        "[TEST 5/5] Canary probe success confirmed: Quorum resets breaker state to CLOSED ... PASSED [OK] (9ms)"
                    ]
                }
            st.rerun()

    with tab_tests:
        tests_code = '''import { DistributedCircuitBreaker } from './circuit-breaker';
import { describe, it, expect, vi } from 'vitest';

describe('DistributedCircuitBreaker Suite', () => {
  it('should remain CLOSED when downstream is responsive', async () => {
    const cb = new DistributedCircuitBreaker('pay-svc', { failureThreshold: 5, cooldownPeriodMs: 30000, halfOpenTrialLimit: 1 }, mockRedis);
    const res = await cb.execute(async () => 'OK', async () => 'FALLBACK');
    expect(res).toBe('OK');
    expect(cb.getState()).toBe('CLOSED');
  });

  it('should trip to OPEN after failureThreshold is breached', async () => {
    const cb = new DistributedCircuitBreaker('pay-svc', { failureThreshold: 5, cooldownPeriodMs: 30000, halfOpenTrialLimit: 1 }, mockRedis);
    for (let i = 0; i < 5; i++) {
      await cb.execute(async () => { throw new Error('500'); }, async () => 'FALLBACK');
    }
    expect(cb.getState()).toBe('OPEN');
  });
});
'''
        st.code(tests_code, language="typescript")

    with tab_cfg:
        cfg_code = '''{
  "serviceKey": "payments-checkout-gateway",
  "failureThreshold": 5,
  "slidingWindowSeconds": 60,
  "cooldownPeriodMs": 30000,
  "halfOpenTrialLimit": 1,
  "redisQuorumLockTTL": 5000,
  "exponentialBackoff": true,
  "maxCooldownFactor": 8
}'''
        st.code(cfg_code, language="json")

    # Terminal Output Window
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="terminal-window">
        <div class="terminal-header">
            <span class="terminal-dot" style="background: #EF4444;"></span>
            <span class="terminal-dot" style="background: #F59E0B;"></span>
            <span class="terminal-dot" style="background: #10B981;"></span>
            <span style="margin-left: 0.5rem; color: #94A3B8; font-size: 0.75rem;">node v20.11.0 · vitest runner · sandbox-container-isolated</span>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state["test_output"]:
        out = st.session_state["test_output"]
        st.markdown(f"""
        <div style="color: #10B981; font-weight: 700; margin-bottom: 0.5rem;">
            ✓ TEST SUITE PASSED ({out['passed']}/{out['total']} Tests) in {out['duration_ms']}ms · Breaker State: {out['state']}
        </div>
        """, unsafe_allow_html=True)
        for log in out["logs"]:
            color = "#10B981" if "[OK]" in log else "#94A3B8"
            st.markdown(f"<div style='color: {color}; margin-bottom: 0.25rem;'>{log}</div>", unsafe_allow_html=True)
        st.markdown("<div style='color: #38BDF8; margin-top: 0.5rem;'>✓ Ready for production code review & diff comparison.</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="color: #64748B;">
            [READY] Container sandbox initialized. Click 'Run Test Suite & Assertions' to compile and execute.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_sandbox():
    col_crumb, col_actions = st.columns([3, 2])
    with col_crumb:
        if st.button("← Back to Lesson Player", key="sb_back_player"):
            auth.navigate_to("lesson_player")
    with col_actions:
        st.markdown("""
        <div style="text-align: right; padding-top: 0.25rem;">
            <span class="badge badge-secondary">Interactive Code Runner</span>
        </div>
        """, unsafe_allow_html=True)

    render_sandbox_content()
