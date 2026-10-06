"""
Theme and Custom CSS Module for ApexLearn LMS
Matches Stitch design specifications:
- Primary: #4F46E5 (Indigo)
- Secondary: #0D9488 (Teal)
- Background: #F9FAFB
- Typography: Inter font family
- Elevation: Rounded cards (border-radius: 12px to 16px), subtle borders & shadows
"""

import streamlit as st

def apply_custom_theme():
    """Inject custom CSS to restyle Streamlit components to match Google Stitch design."""
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    /* Global reset & typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #F9FAFB !important;
        color: #111827 !important;
    }

    /* Main container spacing */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #111827 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    /* Primary and Secondary button overrides */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.5rem 1.25rem !important;
        box-shadow: 0 1px 3px rgba(79, 70, 229, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
        font-size: 0.925rem !important;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #4338CA 0%, #3730A3 100%) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35) !important;
        transform: translateY(-1px) !important;
    }
    div.stButton > button:first-child:active {
        transform: translateY(0px) !important;
    }

    /* Secondary action buttons */
    button[kind="secondary"] {
        background-color: #F3F4F6 !important;
        color: #374151 !important;
        border: 1px solid #E5E7EB !important;
        box-shadow: none !important;
    }
    button[kind="secondary"]:hover {
        background-color: #E5E7EB !important;
        color: #111827 !important;
    }

    /* Rounded Cards */
    .apex-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.25rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .apex-card:hover {
        border-color: #D1D5DB;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* Hero / Highlight Card */
    .apex-hero-card {
        background: linear-gradient(135deg, #EEF2FF 0%, #FFFFFF 100%);
        border-radius: 16px;
        border: 1px solid #C7D2FE;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.08);
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
    }
    div[data-testid="stMetricLabel"] p {
        color: #6B7280 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1.65rem !important;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-primary {
        background-color: #EEF2FF;
        color: #4F46E5;
        border: 1px solid #C7D2FE;
    }
    .badge-secondary {
        background-color: #CCFBF1;
        color: #0F766E;
        border: 1px solid #99F6E4;
    }
    .badge-success {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }
    .badge-warning {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .badge-danger {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }

    /* Form Inputs */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #D1D5DB !important;
        background-color: #F9FAFB !important;
        color: #111827 !important;
        font-size: 0.95rem !important;
        transition: all 0.15s ease-in-out !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #4F46E5 !important;
        background-color: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }

    /* Progress Bar */
    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #4F46E5 0%, #0D9488 100%) !important;
        border-radius: 9999px !important;
    }
    div[data-testid="stProgress"] > div > div {
        background-color: #E5E7EB !important;
        border-radius: 9999px !important;
        height: 10px !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        color: #6B7280 !important;
        padding-top: 0.75rem !important;
        padding-bottom: 0.75rem !important;
        font-size: 0.95rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4F46E5 !important;
        border-bottom-color: #4F46E5 !important;
    }

    /* Radio buttons & Checkboxes */
    div[data-testid="stRadio"] > label {
        font-weight: 600 !important;
        color: #111827 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        padding: 0.65rem 1rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        border-color: #A5B4FC !important;
        background-color: #F8FAFC !important;
    }

    /* Code Blocks & Terminal */
    .terminal-window {
        background-color: #0F172A;
        border-radius: 12px;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        padding: 1.25rem;
        border: 1px solid #1E293B;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .terminal-header {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #334155;
    }
    .terminal-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }

    /* Diff Viewer Styling */
    .diff-line {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        padding: 0.2rem 0.6rem;
        white-space: pre-wrap;
        line-height: 1.4;
    }
    .diff-add {
        background-color: #ECFDF5;
        color: #065F46;
        border-left: 3px solid #10B981;
    }
    .diff-del {
        background-color: #FEF2F2;
        color: #991B1B;
        border-left: 3px solid #EF4444;
    }
    .diff-neutral {
        background-color: #FFFFFF;
        color: #4B5563;
        border-left: 3px solid transparent;
    }

    /* Timer Pill */
    .timer-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
    }

    /* Score Ring Presentation */
    .score-circle-container {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        border: 8px solid #4F46E5;
        background: #FFFFFF;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.15);
    }
    .score-circle-fail {
        border-color: #EF4444 !important;
        box-shadow: 0 4px 14px rgba(239, 68, 68, 0.15) !important;
    }

    /* Custom scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #F3F4F6;
    }
    ::-webkit-scrollbar-thumb {
        background: #D1D5DB;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #9CA3AF;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_brand_header(subtitle: str = "Enterprise LMS Platform"):
    """Render the top banner with the Stitch style."""
    header_html = f"""
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 1rem; margin-bottom: 1.5rem; border-bottom: 1px solid #E5E7EB;">
        <div style="display: flex; align-items: center; gap: 0.85rem;">
            <div style="background: #EEF2FF; border-radius: 12px; padding: 0.4rem 0.75rem; border: 1px solid #C7D2FE;">
                <span style="font-weight: 800; font-size: 1.25rem; color: #4F46E5; letter-spacing: -0.03em;">ApexLearn</span>
                <span style="font-weight: 500; font-size: 0.85rem; color: #0D9488; margin-left: 0.25rem;">LMS</span>
            </div>
            <div>
                <span class="badge badge-secondary" style="font-size: 0.7rem;">{subtitle}</span>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 0.85rem; color: #6B7280; font-weight: 500;">Cloud Infrastructure & Engineering</span>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
