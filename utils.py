import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st
from streamlit_gsheets import GSheetsConnection

@st.cache_resource
def load_model_cloud():
    file_id = '1i6RBVKi9BmSY_jvlypbMWOwvoO5Dyn1t'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_ready_petani.h5'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x

def save_to_google_sheets(new_data):
    """Fungsi untuk menambahkan baris data ke Google Sheets"""
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Ambil data yang sudah ada
        existing_data = conn.read(worksheet="Sheet1")
        # Gabungkan dengan data baru
        updated_df = existing_data.append(new_data, ignore_index=True)
        # Update kembali ke Google Sheets
        conn.update(worksheet="Sheet1", data=updated_df)
    except Exception as e:
        st.error(f"Gagal menyimpan ke Google Sheets: {e}")
