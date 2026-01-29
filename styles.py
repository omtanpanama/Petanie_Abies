import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        
        /* 1. Tombol Utama (Warna Biru) */
        /* Kita hapus width 85% dan display block agar tidak lonjong */
        div.stButton > button {
            background-color: #1e3a8a !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: none !important;
            transition: 0.3s !important;
            padding: 10px 20px !important;
        }

        /* Efek saat disentuh (Hover) */
        div.stButton > button:hover {
            background-color: #3b82f6 !important; /* Berubah jadi biru terang */
            transform: translateY(-2px) !important;
        }

        /* 2. Tombol Khusus di Panel Admin (Warna Berbeda) */
        /* Login jadi Hijau */
        [data-testid="column"]:nth-of-type(1) div.stButton > button {
            background-color: #10b981 !important;
        }
        
        /* Batal jadi Merah */
        [data-testid="column"]:nth-of-type(2) div.stButton > button {
            background-color: #ef4444 !important;
        }

        /* 3. Footer Tetap */
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
