import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Warna Tombol SCAN (Halaman Utama) */
        /* Kita beri warna biru gradasi agar terlihat modern */
        .main-content .stButton > button {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            border: none !important;
            transition: 0.3s !important;
        }
        .main-content .stButton > button:hover {
            filter: brightness(1.2) !important;
            transform: translateY(-2px) !important;
        }

        /* 2. Warna Tombol LOGIN (Kolom Pertama) */
        [data-testid="column"]:nth-of-type(1) .stButton button {
            background-color: #10b981 !important; /* Hijau */
            color: white !important;
            border: none !important;
        }
        [data-testid="column"]:nth-of-type(1) .stButton button:hover {
            background-color: #059669 !important;
        }

        /* 3. Warna Tombol BATAL (Kolom Kedua) */
        [data-testid="column"]:nth-of-type(2) .stButton button {
            background-color: #ef4444 !important; /* Merah */
            color: white !important;
            border: none !important;
        }
        [data-testid="column"]:nth-of-type(2) .stButton button:hover {
            background-color: #dc2626 !important;
        }

        /* Footer Sederhana */
        .footer-fixed {
            position: fixed; left: 0; bottom: 0; width: 100%;
            height: 40px; background: white; border-top: 1px solid #eee;
            display: flex; align-items: center; justify-content: center;
            z-index: 999;
        }
        </style>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="footer-fixed"><p style="color:#94a3b8; font-size:12px; margin:0;">© 2026 Petani_Abies AI</p></div>', unsafe_allow_html=True)
