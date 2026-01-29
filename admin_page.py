import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Gunakan plotly untuk grafik yang lebih interaktif dan cantik
import plotly.express as px 

def render_dashboard():
    st.title("📊 Panel Dashboard Admin")
    st.markdown("---")
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        
        if not df.empty:
            # 1. BARIS RINGKASAN (METRICS)
            total_scan = len(df)
            baik = len(df[df['Hasil'] == "KUALITAS BAIK"])
            buruk = len(df[df['Hasil'] == "KURANG SEHAT"])
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Scan", f"{total_scan} Ikan")
            m2.metric("Kualitas Baik", baik, delta_color="normal")
            m3.metric("Kurang Sehat", buruk, delta="-", delta_color="inverse")
            
            st.markdown("---")
            
            # 2. BAGIAN GRAFIK
            col_chart1, col_chart2 = st.columns([1.5, 1])
            
            with col_chart1:
                st.subheader("📈 Tren Hasil Analisis")
                # Grafik Batang Berwarna
                fig_bar = px.bar(
                    df['Hasil'].value_counts().reset_index(), 
                    x='Hasil', 
                    y='count',
                    color='Hasil',
                    color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'},
                    labels={'count': 'Jumlah', 'Hasil': 'Status'},
                    template="plotly_white"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_chart2:
                st.subheader("🍩 Persentase")
                # Grafik Lingkaran (Donut)
                fig_pie = px.pie(
                    df, 
                    names='Hasil', 
                    hole=0.4,
                    color='Hasil',
                    color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'}
                )
                fig_pie.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("---")

            # 3. TABEL DATA
            st.subheader("📑 Data Log Lengkap")
            st.dataframe(df, use_container_width=True)
            
            # Tombol Logout diletakkan di sidebar atau bawah
            if st.button("🚪 Keluar dari Panel Admin"):
                st.session_state.logged_in = False
                st.rerun()
                
        else:
            st.info("💡 Belum ada data di Google Sheets untuk dianalisis.")
            
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memuat dashboard: {e}")
