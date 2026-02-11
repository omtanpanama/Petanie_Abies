import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st
import pandas as pd
import cv2
from streamlit_gsheets import GSheetsConnection
from lime import lime_image
from skimage.segmentation import mark_boundaries

@st.cache_resource
def load_model_cloud():
    file_id = '1kcCLln1DIDCVyEC_Qw26k8fKu2clLI2f'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_petani_siap.keras'
    if not os.path.exists(output):
        with st.spinner("✨ Menghubungkan ke Cloud AI..."):
            gdown.download(url, output, quiet=False)
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x

def generate_lime_explanation(img, model):
    """
    Menggunakan LIME untuk mendeteksi area fisik ikan secara spesifik.
    """
    # Konversi image ke array untuk LIME
    img_array = np.array(img.resize((224, 224)))
    
    explainer = lime_image.LimeImageExplainer()
    
    # Fungsi prediksi untuk LIME
    def predict_fn(images):
        preds = model.predict(tf.keras.applications.resnet50.preprocess_input(images), verbose=0)
        # ResNet50 kamu mungkin binary (1 output) atau 2 output
        if preds.shape[1] == 1:
            return np.hstack([1-preds, preds]) 
        return preds

    explanation = explainer.explain_instance(
        img_array.astype('double'), 
        predict_fn, 
        top_labels=1, 
        hide_color=0, 
        num_samples=1000 # Atur ke 200 agar tetap cepat di Streamlit
    )

    # Ambil area (mask) yang paling berpengaruh terhadap label Kurang Sehat
    temp, mask = explanation.get_image_and_mask(
        explanation.top_labels[0], 
        positive_only=True, 
        num_features=10, 
        hide_rest=False
    )
    
    # Overlay visualisasi
    img_lime = mark_boundaries(temp / 255.0, mask)
    img_lime = (img_lime * 255).astype(np.uint8)

    return img_lime, mask

def get_explanation(label, mask, is_dry=False):
    if label == "KUALITAS BAIK":
        return "Fisik proporsional, simetris, dan sirip lengkap."
    
    reasons = []
    if is_dry:
        reasons.append("Kondisi tubuh pucat atau kering")

    # Ambil semua koordinat titik kuning
    coords = np.argwhere(mask > 0)
    
    if len(coords) > 0:
        # Cek apakah ada titik yang jauh dari tengah (Radius > 40)
        # 112 adalah titik tengah gambar 224x224
        distances = np.sqrt((coords[:, 1] - 112)**2 + (coords[:, 0] - 112)**2)
        
        # Jika ada titik kuning di area luar, berarti sirip bermasalah
        if np.max(distances) > 40: 
            reasons.append("Sirip atau ekor tidak utuh/sobek")
            
        # Jika banyak titik kuning menumpuk di tengah
        if np.mean(distances) < 70:
            reasons.append("Bentuk tubuh kurang proporsional")
            
        # Cek area kepala (Y rendah) untuk mata
        if np.min(coords[:, 0]) < 80:
             reasons.append("Indikasi kelainan pada area mata")

    if not reasons:
        return "Terdeteksi adanya kelainan fisik pada benih."
            
    return ", ".join(reasons)

def save_to_google_sheets(new_data_df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
    except Exception as e:
        st.error(f"Gagal simpan ke Sheets: {e}")
