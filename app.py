import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import os

st.title("===Data Potongan Gaji===")

# 1. FORM INPUT
with st.form("form_potongan"):
    nama_kantor = st.text_input("Nama Kantor")
    nama_karyawan = st.text_input("Nama Karyawan")
    hari_alpa = st.number_input("Jumlah Hari Alpa", min_value=0, step=1)
    gaji_pokok = st.number_input("Gaji Pokok", min_value=0, step=1000)
    nilai_per_hari = gaji_pokok / 30 if gaji_pokok > 0 else 0
    potongan = hari_alpa * nilai_per_hari

    st.write(f"Potongan: Rp {potongan:,.0f}")
    submitted = st.form_submit_button("Submit")

# 2. KALO TOMBOL SUBMIT DIKLIK
if submitted:
    # Simpan data ke Excel buat rekap lu
    data_baru = {
        "Tanggal": [datetime.date.today()],
        "Nama Kantor": [nama_kantor],
        "Nama Karyawan": [nama_karyawan],
        "Hari Alpa": [hari_alpa],
        "Gaji Pokok": [gaji_pokok],
        "Potongan": [potongan],
        "Gaji Bersih": [gaji_pokok - potongan]
    }
    df_baru = pd.DataFrame(data_baru)

    # Kalo file udah ada, tambahin baris baru. Kalo belum, bikin baru
    file_excel = "rekap_potongan.xlsx"
    if os.path.exists(file_excel):
        df_lama = pd.read_excel(file_excel)
        df_gabung = pd.concat([df_lama, df_baru], ignore_index=True)
    else:
        df_gabung = df_baru
    df_gabung.to_excel(file_excel, index=False)

    st.success("✅ Data berhasil disimpan!")

    # 3. BIKIN PDF BUAT YG NGISI - INI KUNCINYA
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BUKTI POTONGAN GAJI", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Tanggal: {datetime.date.today()}", 0, 1)
    pdf.cell(0, 8, f"Nama Kantor: {nama_kantor}", 0, 1)
    pdf.cell(0, 8, f"Nama Karyawan: {nama_karyawan}", 0, 1)
    pdf.cell(0, 8, f"Hari Alpa: {hari_alpa} hari", 0, 1)
    pdf.cell(0, 8, f"Gaji Pokok: Rp {gaji_pokok:,}", 0, 1)
    pdf.cell(0, 8, f"Potongan: Rp {potongan:,}", 0, 1)
    pdf.cell(0, 8, f"Gaji Bersih: Rp {gaji_pokok - potongan:,}", 0, 1)
    pdf.ln(10)
    pdf.cell(0, 8, "TTD HRD:........................", 0, 1)

    # 4. TOMBOL DOWNLOAD PDF - LANGSUNG DAPET YG NGISI
    pdf_output = pdf.output(dest="S").encode("latin-1")
    st.download_button(
        label="📄 Download Bukti PDF",
        data=pdf_output,
        file_name=f"Bukti_Potongan_{nama_karyawan}_{datetime.date.today()}.pdf",
        mime="application/pdf"
    )

# 5. TAMPILIN REKAP BUAT LU DOANG - OPSIONAL
if st.checkbox("Lihat Rekap Semua Data"):
    if os.path.exists(file_excel):
        st.dataframe(pd.read_excel(file_excel))
    else:
        st.info("Belum ada data masuk")
