import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Background Dasar */
        .stApp { 
            background-color: #f8fafc; 
        }
        
        /* 2. Tombol SCAN UTAMA (Besar & Bergradasi) */
        div[data-testid="stVerticalBlock"] > div.stButton > button {
            display: block;
            margin: 20px auto;
            width: 85%;
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            color: white;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 15px;
            border: none;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
        }

        /* Efek Sentuh Tombol Scan */
        div[data-testid="stVerticalBlock"] > div.stButton > button:hover {
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(30, 58, 138, 0.4);
            cursor: pointer;
        }

        /* 3. Tombol di dalam KOLOM (Login & Batal) */
        [data-testid="column"] div.stButton > button {
            width: 100% !important;
            margin: 5px 0 !important;
            padding: 10px !important;
            font-size: 15px !important;
            border-radius: 10px !important;
            transition: all 0.2s ease;
            font-weight: 600;
        }

        /* WARNA TOMBOL LOGIN (Kolom 1) */
        [data-testid="column"]:nth-child(1) div.stButton > button {
            background-color: #10b981 !important; /* Hijau Emerald */
            color: white !important;
            border: none !important;
        }
        [data-testid="column"]:nth-child(1) div.stButton > button:hover {
            background-color: #059669 !important; /* Hijau lebih gelap saat disentuh */
            transform: translateY(-2px);
        }

        /* WARNA TOMBOL BATAL (Kolom 2) */
        [data-testid="column"]:nth-child(2) div.stButton > button {
            background-color: #ef4444 !important; /* Merah */
            color: white !important;
            border: none !important;
        }
        [data-testid="column"]:nth-child(2) div.stButton > button:hover {
            background-color: #dc2626 !important; /* Merah lebih gelap saat disentuh */
            transform: translateY(-2px);
        }

        /* 4. Footer Fixed */
        .footer-fixed {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 45px;
            background-color: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(5px);
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999;
        }
        .footer-text { 
            color: #64748b; 
            font-size: 12px; 
            font-weight: 500;
        }
        
        .main-content { margin-bottom: 80px; }
        </style>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="footer-fixed"><p class="footer-text">© 2026 Petani_Abies AI | Diagnosa Benih Ikan Akurat</p></div>', unsafe_allow_html=True)
