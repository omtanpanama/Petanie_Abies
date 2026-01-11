import streamlit as st
import pandas as pd

def show_admin_sidebar():
    with st.sidebar:
        st.markdown("### 🔐 Panel Kontrol")
        
        if not st.session_state.get('logged_in', False):
            st.write("Masuk untuk melihat laporan")
            pwd = st.text_input("Sandi Admin", type="password")
            if st.button("Login"):
                if pwd == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Sandi Salah")
        else:
            st.success("Mode Admin Aktif")
            menu = st.radio("Pilih Menu:", ["🏠 Kembali ke Scan", "📊 Dashboard Laporan"])
            
            st.divider()
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()
            return menu
    return "🏠 Kembali ke Scan"

def render_admin_dashboard():
    st.title("📊 Laporan Aktivitas")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
        
        # Tombol Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Laporan CSV", data=csv, file_name="laporan_petani_abies.csv")
    else:
        st.info("Belum ada data scan hari ini.")
