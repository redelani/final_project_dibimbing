import streamlit as st
import requests
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Read the DATABASE_URL from the environment
# 10.252.49.156
DATABASE_URL = os.environ.get("DATABASE_URL")

# Check if the environment variable is set (important!)
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set.  Did you use the -e flag when running the container?")

engine = create_engine(DATABASE_URL)
 # harus ipconfig duluuuuuuuu

# Fungsi untuk mengambil data dari database menggunakan pandas
def load_data():
    try:
        query = "SELECT * FROM products"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Gagal memuat data dari database: {e}")
        return None

df = load_data()

from PIL import Image
logo_dibimbing = Image.open('images/logo_dibimbing.jpg')

st.sidebar.title("Final Project dibimbing.id")
st.sidebar.markdown("Aplikasi analisa sentimen ulasan produk skincare berdasarkan data pada website Female Daily dan Sociolla")
st.sidebar.success("By: Renovita Edelani")
st.sidebar.image(logo_dibimbing)

st.title("Analisis Sentimen Review Produk Skincare")
st.markdown("Aplikasi ini menganalisis sentimen dari review produk skincare, membantu Anda memahami apa yang konsumen rasakan tentang produk tertentu.")
username = st.text_input("Username")
# nama_produk = df['produk'].tolist
nama_produk = ('acnes facewash', 'wardah facewash', 'originote serum')
produk = st.selectbox("Produk yang direview",nama_produk)
review_text = st.text_area("Masukkan review produk di sini")

if st.button("Analisis"):
    if review_text:
        try:
            response = requests.post("http://localhost:8000/predict", json={"text": review_text})
            if response.status_code == 200:
                result = response.json()
                st.write(f"Sentimen: {result['sentiment']}")
            else:
                st.error(f"Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Koneksi ke backend API gagal. Pastikan Docker container berjalan.")
    else:
        st.warning("Harap masukkan review produk.")

def perform_eda(df):
    # Distribution of 'produk' (using Seaborn countplot)
    st.subheader("Product Distribution")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x='produk', data=df, ax=ax)
    ax.set_title('Distribution of produk')
    # Pastikan kolom 'produk' bertipe data string
    data_produk = df['produk'].astype(str)

    # Ambil semua nilai unik dari kolom 'produk' dan urutkan
    unique_products = sorted(data_produk.unique())
    # Ambil posisi tick di sumbu x
    tick_positions = ax.get_xticks()

    # Tetapkan tick_labels dengan unique_products
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(unique_products, rotation=45, horizontalalignment='right')
    
    ax.tick_params(axis='x', which='major',labelsize=8,pad=10)  
    st.pyplot(fig)
    
    # Distribution of 'klasifikasi' for each 'produk'
    st.subheader("Klasifikasi Distribution per Product")
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.countplot(data=df, x='produk', hue='klasifikasi', ax=ax)
    ax.set_title('Distribution of Klasifikasi for Each Produk')
    ax.set_xlabel('Produk')
    ax.set_ylabel('Count')
    # Pastikan kolom 'produk' bertipe data string
    data_produk = df['produk'].astype(str)

    # Ambil semua nilai unik dari kolom 'produk' dan urutkan
    unique_products = sorted(data_produk.unique())
    # Ambil posisi tick di sumbu x
    tick_positions = ax.get_xticks()

    # Tetapkan tick_labels dengan unique_products
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(unique_products, rotation=45, horizontalalignment='right')
    ax.tick_params(axis='x', which='major',labelsize=8,pad=10)  
    ax.legend(title='Klasifikasi')
    st.pyplot(fig)
    
    
if df is not None:
    st.dataframe(df)  # Tampilkan data dalam tabel interaktif
    perform_eda(df)
        

def display_images(directory):
    """Displays images from a directory in a Streamlit app."""

    try:
        image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        image_files = [f for f in image_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))] #Filter for image types

        if not image_files:
            st.warning("No images found in the directory.")
            return

        for image_file in image_files:
            image_path = os.path.join(directory, image_file)
            try:
                image = Image.open(image_path)
                image = image.resize((300,300), Image.LANCZOS)
                st.image(image, caption=image_file, use_container_width =False) #use_column_width to make responsive image
            except Exception as e:
                st.error(f"Error displaying image {image_file}: {e}")

    except FileNotFoundError:
        st.error(f"Directory not found: {directory}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

image_directory = "images//produk"  # Relative path (recommended)
display_images(image_directory)