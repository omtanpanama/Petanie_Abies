import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Reset & Background */
        .stApp { background-color: #f8fafc; }

        /* 2. TOMBOL SCAN UTAMA (Paksa Berubah) */
        /* Kita pakai selector yang sangat spesifik agar tidak meleset */
        .main-content div.stButton > button {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
            color: white !important;
            border-radius: 15px !important;
            border: none !important;
            height: 60px !important;
            width: 85% !important;
            display: block !important;
            margin: 0 auto !important;
            transition: all 0.3s ease !important;
        }

        /* EFEK HOVER SCAN */
        .main-content div.stButton > button:hover {
            background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%) !important;
            transform: scale(1.03) !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
        }

        /* 3. TOMBOL DI DALAM KOLOM (Login & Batal) */
        /* Kolom 1: LOGIN (HIJAU) */
        [data-testid="column"]:nth-of-type(1) button {
            background-color: #10b981 !important;
            color: white !important;
            border: none !important;
            transition: 0.3s !important;
        }
        [data-testid="column"]:nth-of-type(1) button:hover {
            background-color: #059669 !important;
            transform: translateY(-3px) !important;
        }

        /* Kolom 2: BATAL (MERAH) */
        [data-testid="column"]:nth-of-type(2) button {
            background-color: #ef4444 !important;
            color: white !important;
            border: none !important;
            transition: 0.3s !important;
        }
        [data-testid="column"]:nth-of-type(2) button:hover {
            background-color: #b91c1c !important;
            transform: translateY(-3px) !important;
        }

        /* Fix agar tombol di kolom tidak lonjong */
        [data-testid="column"] div.stButton > button {
            width: 100% !important;
        }

        </style>
        """, unsafe_allow_html=True)
