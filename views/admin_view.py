"""
Admin View for ApexLearn LMS
Handles platform-wide governance, user role modification, adding new users,
system metrics, and database reset controls.
"""

import streamlit as st
import pandas as pd
import db
import auth

def render_admin_dashboard():
    user = auth.get_current_user() or {}
    database = db.load_db()
    users = database.get("users", {})

    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <span class="badge badge-primary">Super Administrator Console</span>
        <h1 style="font-size: 1.85rem; font-weight: 800; color: #111827; margin: 0.25rem 0 0.25rem 0;">
            Platform Governance & Users
        </h1>
        <p style="color: #6B7280; font-size: 0.95rem; margin: 0;">
            Logged in as {user.get('name', 'Sarah Chen')} (Admin)
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Admin Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Users", f"{len(users)} Accounts")
    with m2:
        st.metric("Platform Availability", "99.98%", delta="Operational")
    with m3:
        st.metric("Storage Layer", "Local JSON DB", delta="data/apexlearn_db.json")
    with m4:
        st.metric("Security", "SHA-256 Salted", delta="SOC2 Type II")

    st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)

    tab_users, tab_add_user, tab_system = st.tabs([
        "👥 Registered User Accounts",
        "➕ Add New User",
        "🛠️ System Maintenance & Reset"
    ])

    with tab_users:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 1rem 0; color: #111827;">
                User Directory & Role Management
            </h3>
        """, unsafe_allow_html=True)

        user_rows = []
        for email, u in users.items():
            user_rows.append({
                "Full Name": u.get("name", "User"),
                "Email": email,
                "Role": u.get("role", "Student"),
                "Joined": u.get("joined", "2026-01-01"),
                "Progress": f"{u.get('overall_progress', 0)}%"
            })

        df = pd.DataFrame(user_rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("<h4 style='font-size: 1rem; font-weight: 700; margin: 1.25rem 0 0.5rem 0;'>Change User Role:</h4>", unsafe_allow_html=True)
        col_sel_user, col_sel_role, col_btn_update = st.columns([2, 1.5, 1])
        with col_sel_user:
            selected_email = st.selectbox("Select User Email", list(users.keys()), key="admin_sel_user")
        with col_sel_role:
            new_role = st.selectbox("Assign Role", ["Student", "Instructor", "Admin"], key="admin_sel_role")
        with col_btn_update:
            st.markdown("<div style='padding-top: 1.7rem;'></div>", unsafe_allow_html=True)
            if st.button("Update Role", type="primary", use_container_width=True):
                database["users"][selected_email]["role"] = new_role
                db.save_db(database)
                st.success(f"Updated {selected_email} to {new_role} role!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_add_user:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 1rem 0; color: #111827;">
                Provision New LMS User
            </h3>
        """, unsafe_allow_html=True)

        new_name = st.text_input("Full Name", placeholder="e.g. David Hassel")
        new_email = st.text_input("Institution Email", placeholder="e.g. d.hassel@apexlearn.io")
        new_role_choice = st.selectbox("Role", ["Student", "Instructor", "Admin"])
        new_pass = st.text_input("Temporary Password", value="password123", type="password")

        if st.button("Create Account in JSON Database", type="primary"):
            success, msg = db.register_user(new_name, new_email, new_pass, new_role_choice)
            if success:
                st.success(f"User {new_email} successfully provisioned as {new_role_choice}!")
                st.rerun()
            else:
                st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_system:
        st.markdown("""
        <div class="apex-card">
            <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 0.5rem 0; color: #111827;">
                Database Reset & Seed Data
            </h3>
            <p style="font-size: 0.85rem; color: #6B7280; margin-bottom: 1.25rem;">
                Reset the local JSON database (<code>data/apexlearn_db.json</code>) back to the clean initial mock dataset with Jordan Alvarez (Student), Prof. Alex Vance (Instructor), and Sarah Chen (Admin).
            </p>
        """, unsafe_allow_html=True)

        confirm_reset = st.checkbox("I confirm that I want to reset all user progress, notes, and quiz results to default mock state.")
        if st.button("⚠️ Reset Database to Defaults", type="primary", disabled=not confirm_reset):
            db.reset_database_to_default()
            st.success("Database successfully reset to initial mock state!")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
