import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Background Utama */
        .stApp { background-color: #f8fafc; }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] { background-color: #f1f5f9; }

        /* Tombol Scan di Tengah */
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
            transition: 0.3s;
        }
        
        div.stButton > button:hover {
            background-color: #2563eb;
            transform: scale(1.02);
        }

        /* Footer Fixed & Copyright di Tengah */
        .footer-fixed {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 40px;
            background-color: white;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999;
        }
        .footer-text { color: #94a3b8; font-size: 11px; margin: 0; }
        
        /* Ruang agar konten tidak tertutup footer */
        .main-content { margin-bottom: 60px; }
        </style>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
        <div class="footer-fixed">
            <p class="footer-text">© 2026 Petani_Abies AI - Teknologi Cerdas Ikan Mas</p>
        </div>
    """, unsafe_allow_html=True)
