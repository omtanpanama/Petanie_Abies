import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Background Utama */
        .stApp { background-color: #f8fafc; }

        /* --- TOMBOL SCAN UTAMA --- */
        .main-content .stButton > button {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            width: 85% !important;
            margin: 10px auto !important;
            display: block !important;
            transition: 0.3s !important;
            font-weight: bold !important;
        }
        .main-content .stButton > button:hover {
            transform: scale(1.02) !important;
            filter: brightness(1.2) !important;
        }

        /* --- PERBAIKAN TOMBOL ADMIN (LOGIN & BATAL) --- */
        /* Menggunakan flexbox agar tombol tidak lonjong */
        [data-testid="column"] .stButton button {
            width: 100% !important;
            min-height: 45px !important;
            border-radius: 8px !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            transition: 0.3s !important;
            white-space: nowrap !important; /* Mencegah teks terpotong ke bawah */
        }

        /* Tombol Login (Hijau) */
        [data-testid="column"]:nth-of-type(1) .stButton button {
            background-color: #10b981 !important;
        }
        [data-testid="column"]:nth-of-type(1) .stButton button:hover {
            background-color: #059669 !important;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
        }

        /* Tombol Batal (Merah) */
        [data-testid="column"]:nth-of-type(2) .stButton button {
            background-color: #ef4444 !important;
        }
        [data-testid="column"]:nth-of-type(2) .stButton button:hover {
            background-color: #dc2626 !important;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4) !important;
        }

        /* Footer */
        .footer-fixed {
            position: fixed; left: 0; bottom: 0; width: 100%;
            height: 40px; background: white; border-top: 1px solid #eee;
            display: flex; align-items: center; justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="footer-fixed"><p style="color:#94a3b8; font-size:12px;">© 2026 Petani_Abies AI</p></div>', unsafe_allow_html=True)
