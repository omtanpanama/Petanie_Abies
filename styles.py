import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Reset Dasar */
        .stApp { background-color: #f8fafc; }

        /* 2. Warna Tombol SCAN (Halaman Utama) */
        /* Kita tembak langsung semua button yang ada di dalam class main-content */
        .main-content button {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            border: none !important;
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }
        
        .main-content button:hover {
            filter: brightness(1.2) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
        }

        /* 3. Tombol LOGIN & BATAL (Admin Panel) */
        /* Kolom Pertama - Hijau */
        [data-testid="column"]:nth-of-type(1) button {
            background-color: #10b981 !important;
            color: white !important;
            border: none !important;
        }
        [data-testid="column"]:nth-of-type(1) button:hover {
            background-color: #059669 !important;
        }

        /* Kolom Kedua - Merah */
        [data-testid="column"]:nth-of-type(2) button {
            background-color: #ef4444 !important;
            color: white !important;
            border: none !important;
        }
        [data-testid="column"]:nth-of-type(2) button:hover {
            background-color: #dc2626 !important;
        }

        /* Footer */
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
