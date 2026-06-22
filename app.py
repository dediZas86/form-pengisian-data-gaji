import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Data Potongan Gaji", layout="centered")
st.title("===Data Potongan Gaji===")
st.caption("Keterangan: Sebelum kirim Cek Kembali Data yang anda kirimkan")

# List karyawan awal - bisa lu edit sendiri di sini
karyawan_list = ["Pilih...", "Tambah Karyawan Baru"]

with st.form("form_potongan"):
    nama_kantor = st.text_input("Nama Kantor")
    
    # Mode dropdown + tambah baru
    pilih_karyawan = st.selectbox("Nama Karyawan", karyawan_list)
    if pilih_karyawan == "Tambah Karyawan Baru":
        nama_karyawan = st.text_input("Ketik Nama Karyawan Baru")
    else:
        nama_karyawan = st.text_input("Nama Karyawan", value="" if pilih_karyawan=="Pilih..." else pilih_karyawan)
    
    jumlah_hari_kerja = st.number_input("Jumlah Hari Kerja", min_value=0, step=1)
    
    st.subheader("Bon Panjar")
    potongan_bon = st.number_input("Potongan Bon Panjar", min_value=0)
    sisa_bon = st.number_input("Sisa Bon Panjar", min_value=0)
    
    st.subheader("Kredit Lunak")
    potongan_kredit = st.number_input("Potongan Kredit Lunak", min_value=0)
    sisa_kredit = st.number_input("Sisa Kredit Lunak", min_value=0)
    
    st.subheader("Kecerobohan")
    potongan_kecerobohan = st.number_input("Potongan Kecerobohan", min_value=0)
    sisa_kecerobohan = st.number_input("Sisa Kecerobohan", min_value=0)
    
    st.subheader("Minus")
    minus_tunai = st.number_input("Minus Tunai", min_value=0)
    potongan_minus = st.number_input("Potongan Minus", min_value=0)
    
    st.subheader("Tidak Masuk Kerja")
    jumlah_tidak_masuk = st.number_input("Jumlah Hari Karyawan Tidak Masuk Kerja", min_value=0, step=1)
    keterangan_tidak_masuk = st.text_area("Keterangan Tidak Masuk Kerja")
    potongan_tidak_masuk = st.number_input("Potongan Tidak Masuk Kerja", min_value=0)
    
    st.subheader("Potongan Lainnya")
    nama_potongan_lain = st.text_input("Potongan Lainnya (beri nama/keterangan Potongan)")
    jumlah_potongan_lain = st.number_input("Jumlah Uang yang di Potongan Lainnya", min_value=0)
    sisa_potongan_lain = st.number_input("Sisa Potongan Lainnya", min_value=0)
    
    st.subheader("Mutasi Karyawan")
    nama_keluar = st.text_input("Nama Karyawan Keluar")
    tgl_keluar = st.date_input("Tanggal Karyawan Keluar")
    nama_baru = st.text_input("Nama Karyawan Baru Masuk")
    tgl_masuk = st.date_input("Tanggal Karyawan Baru Masuk")
    
    st.subheader("Upload Dokumen")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg","png","pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit dari Dokter/Klinik/Puskesmas", type=["jpg","png","pdf"])
    
    submit = st.form_submit_button("Simpan Data")

if submit:
    # Cek file yg diupload
    nama_ktp = ktp_baru.name if ktp_baru else "-"
    nama_surat = surat_sakit.name if surat_sakit else "-"
    
    data_baru = {
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nama Kantor": nama_kantor,
        "Nama Karyawan": nama_karyawan,
        "Jumlah Hari Kerja": jumlah_hari_kerja,
        "Potongan Bon Panjar": potongan_bon,
        "Sisa Bon Panjar": sisa_bon,
        "Potongan Kredit Lunak": potongan_kredit,
        "Sisa Kredit Lunak": sisa_kredit,
        "Potongan Kecerobohan": potongan_kecerobohan,
        "Sisa Kecerobohan": sisa_kecerobohan,
        "Minus Tunai": minus_tunai,
        "Potongan Minus": potongan_minus,
        "Jumlah Hari Tidak Masuk": jumlah_tidak_masuk,
        "Keterangan Tidak Masuk": keterangan_tidak_masuk,
        "Potongan Tidak Masuk": potongan_tidak_masuk,
        "Nama Potongan Lain": nama_potongan_lain,
        "Jumlah Potongan Lain": jumlah_potongan_lain,
        "Sisa Potongan Lain": sisa_potongan_lain,
        "Nama Karyawan Keluar": nama_keluar,
        "Tanggal Keluar": tgl_keluar,
        "Nama Karyawan Baru": nama_baru,
        "Tanggal Masuk Baru": tgl_masuk,
        "File KTP": nama_ktp,
        "File Surat Sakit": nama_surat
    }
    
    st.success("✅ Data berhasil disimpan! Cek kembali sebelum kirim")
    st.dataframe(pd.DataFrame([data_baru]), use_container_width=True)
