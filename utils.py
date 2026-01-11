import tensorflow as tf
import os
import gdown
import streamlit as st
import numpy as np

@st.cache_resource
def load_model_cloud():
    file_id = '1i6RBVKi9BmSY_jvlypbMWOwvoO5Dyn1t'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_ready_petani.h5'
    
    if not os.path.exists(output):
        with st.spinner("✨ Mengaktifkan Sistem AI Petani_Abies..."):
            gdown.download(url, output, quiet=False)
            
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    # Mengubah ukuran gambar sesuai input ResNet (224x224)
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x
