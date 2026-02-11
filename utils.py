import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st
import pandas as pd
import cv2
from streamlit_gsheets import GSheetsConnection

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

def generate_gradcam(img, model):
    img_array = preprocess_image(img)
    # Layer terakhir ResNet50 untuk heatmap yang presisi
    last_conv_layer_name = "conv5_block3_out"
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        class_channel = preds[0] 

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
    heatmap_raw = heatmap.numpy()

    img_resized = np.array(img.resize((224, 224)))
    heatmap_resized = cv2.resize(heatmap_raw, (224, 224))
    
    heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(img_resized, 0.6, heatmap_color, 0.4, 0)
    
    return superimposed_img, heatmap_resized

def get_explanation(label, heatmap_data, is_dry=False):
    if label == "KUALITAS BAIK":
        return "Morfologi simetris, tubuh proporsional, dan sirip utuh."
    
    reasons = []
    if is_dry:
        reasons.append("Kondisi tubuh pucat atau kering")

    # Pastikan heatmap dalam resolusi 224x224
    heatmap_resized = cv2.resize(heatmap_data, (224, 224))
    
    # --- LOGIKA DETEKSI AREA (PEKA SIRIP) ---
    # 1. Cek Area Pinggir (Fokus Sirip dan Ekor)
    mask_pinggir = np.ones((224, 224), dtype=np.uint8)
    cv2.circle(mask_pinggir, (112, 112), 65, 0, -1) # Melubangi tengah, ambil pinggiran saja
    
    # Hitung intensitas panas di area pinggir (Threshold 0.3)
    avg_heat_pinggir = np.mean(heatmap_resized[mask_pinggir == 1])
    
    if avg_heat_pinggir > 0.3:
        reasons.append("Sirip atau ekor tidak utuh/sobek")

    # 2. Cek Area Tengah (Fokus Bentuk Tubuh)
    mask_tengah = np.zeros((224, 224), dtype=np.uint8)
    cv2.circle(mask_tengah, (112, 112), 65, 1, -1)
    
    avg_heat_tengah = np.mean(heatmap_resized[mask_tengah == 1])
    
    if avg_heat_tengah > 0.4:
        reasons.append("Bentuk tubuh kurang proporsional")

    if not reasons:
        return "Terdeteksi adanya kelainan fisik pada benih."
            
    return ", ".join(reasons)

def save_to_google_sheets(new_data_df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Pastikan Sheet1 sesuai dengan nama di Google Sheets kamu
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
    except Exception as e:
        st.error(f"Gagal simpan ke Sheets: {e}")
