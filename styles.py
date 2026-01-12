import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        
        /* Tombol Utama Scan di Tengah */
        div.stButton > button:first-child {
            display: block;
            margin: 0 auto;
            width: 85%;
            background-color: #1e3a8a;
            color: white;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            border: none;
        }

        /* Footer Fixed */
        .footer-fixed {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 45px;
            background-color: white;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999;
        }
        .footer-text { color: #94a3b8; font-size: 11px; margin: 0; }
        .main-content { margin-bottom: 70px; }
        </style>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="footer-fixed"><p class="footer-text">© 2026 Petani_Abies AI</p></div>', unsafe_allow_html=True)
