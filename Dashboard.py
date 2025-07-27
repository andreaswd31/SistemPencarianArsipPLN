import streamlit as st
import pandas as pd
import gdown
import requests
from datetime import datetime

# ====== KONFIGURASI HALAMAN ======
st.set_page_config(
    page_title="Sistem Pencarian Rak Arsip PLN",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== SIDEBAR (LOGO & IDENTITAS) ======
with st.sidebar:
    st.image("Logo_PLN.png", width=100)  # Pastikan file logo sesuai
    st.markdown("## PLN ULP")
    st.markdown("### BLIMBING - MALANG")
    
    st.markdown("---")
    st.markdown("#### Terakhir di Update")
    st.write("**Tanggal:**", datetime.now().strftime("%d-%m-%Y"))
    
    st.markdown("---")
    st.markdown("Sistem ini membantu pencarian lokasi arsip berdasarkan ID Pelanggan.")

# ====== CSS TAMBAHAN ======
st.markdown("""
    <style>
        .stTextInput>div>div>input {
            font-size: 18px;
        }
        .stButton>button {
            background-color: #e63946;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 0.5em 2em;
            margin-top: 10px;
        }
        .stButton>button:hover {
            background-color: #d62828;
        }
        .feedback-box {
            background-color: #1d3557;
            padding: 1em;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ====== HEADER KONTEN UTAMA ======
st.markdown("<h1 style='font-size: 38px;'>🔍 Sistem Pencarian Rak Arsip</h1>", unsafe_allow_html=True)
st.write("PLN | Temukan lokasi rak & lemari berdasarkan ID Pelanggan")

# ====== UNDUH & BACA DATA ======
file_id = '1hfSjFlfTc5a_VWosC_gNpci8SON3ILfq'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'arsip_file.csv'
gdown.download(url, output, quiet=False)
arsip_df = pd.read_csv(output)

# ====== FORM INPUT ID ======
id_pelanggan_input = st.text_input("Masukkan ID Pelanggan", max_chars=13)

# ====== CARI DATA ======
def find_rack(id_pelanggan):
    try:
        id_pelanggan = int(id_pelanggan)
    except ValueError:
        return "⚠️ ID pelanggan harus berupa angka."

    for _, row in arsip_df.iterrows():
        try:
            id_awal = int(row['ID_Awal'])
            id_akhir = int(row['ID_Akhir'])
        except ValueError:
            continue

        id_awal, id_akhir = sorted([id_awal, id_akhir])

        if not (len(str(id_awal)) == 12 and len(str(id_akhir)) == 12):
            continue
        if not (str(id_awal).startswith("513") and str(id_akhir).startswith("513")):
            continue

        if id_awal <= id_pelanggan <= id_akhir:
            return f"✅ Masukkan rak <b>{row['NO RAK']}</b> di <b>{row['LEMARI']}</b>"

    return "❌ ID pelanggan tidak ditemukan dalam data."

# ====== TOMBOL CARI ======
if st.button("Cari Lokasi Arsip"):
    if id_pelanggan_input:
        hasil = find_rack(id_pelanggan_input)
        st.markdown(f'<div class="feedback-box">{hasil}</div>', unsafe_allow_html=True)
    else:
        st.warning("Mohon masukkan ID pelanggan terlebih dahulu.")

# ====== FEEDBACK ======
st.markdown("### 📝 Berikan Feedback")
st.write("Kritik, saran, atau masukan:")

if "feedback_text" not in st.session_state:
    st.session_state["feedback_text"] = ""

feedback_input = st.text_area(
    label="",
    value=st.session_state["feedback_text"],
    key="feedback_input",
    height=100,
    placeholder="Tulis masukan anda di sini..."
)

if st.button("Kirim Feedback"):
    if feedback_input.strip():
        feedback_data = {
            "feedback": feedback_input,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Ganti dengan URL sheet.best milikmu
        response = requests.post("https://api.sheetbest.com/sheets/99758839-c507-4609-a0bb-7d40262ed41f", json=feedback_data)

        if response.status_code == 200:
            st.success("✅ Terima kasih! Feedback Anda berhasil dikirim.")
            st.session_state["feedback_text"] = ""  
        else:
            st.error("❌ Gagal mengirim feedback. Coba lagi nanti.")
    else:
        st.warning("Mohon isi feedback terlebih dahulu.")
