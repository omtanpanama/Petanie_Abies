import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* 1. Background Dasar */
        .stApp { 
            background-color: #f8fafc; 
        }
        
        /* 2. Styling Tombol Utama (Hanya untuk tombol Scan di halaman depan) */
        /* Kita menargetkan tombol yang BUKAN berada di dalam kolom */
        div[data-testid="stVerticalBlock"] > div.stButton > button {
            display: block;
            margin: 20px auto;
            width: 85%;
            background-color: #1e3a8a;
            color: white;
            padding: 12px 20px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            border: none;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        div[data-testid="stVerticalBlock"] > div.stButton > button:hover {
            background-color: #1e40af;
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        }

        /* 3. Styling Tombol di dalam Kolom (Login & Batal agar tidak lonjong) */
        /* Ini akan memperbaiki tombol di Panel Admin */
        [data-testid="column"] div.stButton > button {
            width: 100% !important;
            margin: 5px 0 !important;
            padding: 8px !important;
            font-size: 14px !important;
            border-radius: 8px !important;
            background-color: #ffffff; /* Warna dasar putih untuk tombol batal */
            color: #1e3a8a;
            border: 1px solid #e2e8f0 !important;
        }
        
        /* Warna khusus untuk tombol Login Sekarang agar tetap biru */
        [data-testid="column"]:first-child div.stButton > button {
            background-color: #1e3a8a !important;
            color: white !important;
            border: none !important;
        }

        /* 4. Footer Fixed */
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
        .footer-text { 
            color: #94a3b8; 
            font-size: 11px; 
            margin: 0; 
        }
        
        /* Padding bawah agar konten tidak tertutup footer */
        .main-content { 
            margin-bottom: 80px; 
        }
        
        /* Styling Input Password agar lebih rapi */
        .stTextInput input {
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

def render_footer():
    st.markdown('<div class="footer-fixed"><p class="footer-text">© 2026 Petani_Abies AI | Sistem Deteksi Kualitas Benih</p></div>', unsafe_allow_html=True)
