import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

@st.cache_resource
def load_model_cloud():
    file_id = '1i6RBVKi9BmSY_jvlypbMWOwvoO5Dyn1t'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_ready_petani.h5'
    if not os.path.exists(output):
        with st.spinner("✨ Menghubungkan ke Cloud AI..."):
            gdown.download(url, output, quiet=False)
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    # Resize sesuai input ResNet50
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # Normalisasi khusus ResNet50 agar prediksi akurat
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x
def save_to_google_sheets(new_data_df):
    """Menambahkan baris data baru ke bawah data yang sudah ada tanpa menimpa"""
    try:
        # Hubungkan ke Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # 1. Baca data yang sudah ada (Sheet1)
        # ttl=0 WAJIB ada agar Streamlit selalu mengecek baris terakhir di server Google
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        
        # 2. Gabungkan data lama dengan data baru
        # ignore_index=True memastikan data baru diletakkan di baris berikutnya (ke bawah)
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        
        # 3. Tulis kembali seluruh tabel yang sudah diperbarui ke Google Sheets
        conn.update(worksheet="Sheet1", data=updated_df)
        
    except Exception as e:
        st.error(f"Gagal menyimpan ke Google Sheets: {e}")
