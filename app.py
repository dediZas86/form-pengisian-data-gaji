import streamlit as st
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import io

st.set_page_config(page_title="Bukti Potongan PDF", layout="centered")
st.title("📝 Bukti Potongan Gaji - PDF Only")

if "potongan_list" not in st.session_state:
    st.session_state.potongan_list = [{"nama": "Bon Panjar", "jumlah": None, "sisa": None}]
if "potongan_lain_list" not in st.session_state:
    st.session_state.potongan_lain_list = []

def to_int(val):
    return int(val) if val is not None else 0

with st.form("form_pdf"):
    nama_kantor = st.text_input("Nama Kantor *")
    nama_karyawan = st.text_input("Nama Karyawan *")
    jumlah_hari_kerja = st.number_input("Jumlah Hari Kerja", min_value=0, step=1, value=None, format="%d")
    
    st.subheader("Rincian Potongan Utama")
    col1, col2 = st.columns(2)
    with col1:
        potongan_kredit = st.number_input("Potongan Kredit Lunak", min_value=0, step=1000, value=None, format="%d")
        sisa_kredit = st.number_input("Sisa Kredit Lunak", min_value=0, step=1000, value=None, format="%d")
        potongan_kecerobohan = st.number_input("Potongan Kecerobohan", min_value=0, step=1000, value=None, format="%d")
        sisa_kecerobohan = st.number_input("Sisa Kecerobohan", min_value=0, step=1000, value=None, format="%d")
        keterangan_kecerobohan = st.text_input("Keterangan Tambahan Kecerobohan")
    
    with col2:
        bon_prive = st.number_input("Bon Prive", min_value=0, step=1000, value=None, format="%d")
        minus_tunai = st.number_input("Minus Tunai", min_value=0, step=1000, value=None, format="%d")
        denda_minus = st.number_input("Denda Minus", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Potongan Dinamis - Bisa Ditambah")
    for i, pot in enumerate(st.session_state.potongan_list):
        col1, col2, col3, col4 = st.columns([3,2,2,1])
        with col1:
            pot["nama"] = st.text_input(f"Nama Potongan {i+1}", value=pot["nama"], key=f"nama_{i}")
        with col2:
            pot["jumlah"] = st.number_input(f"Jumlah {i+1}", min_value=0, step=1000, value=pot["jumlah"], format="%d", key=f"jumlah_{i}")
        with col3:
            pot["sisa"] = st.number_input(f"Sisa {i+1}", min_value=0, step=1000, value=pot["sisa"], format="%d", key=f"sisa_{i}")
        with col4:
            if i > 0:
                if st.form_submit_button("❌", key=f"del_{i}"):
                    st.session_state.potongan_list.pop(i)
                    st.rerun()
    
    if st.form_submit_button("+ Tambah Jenis Potongan"):
        st.session_state.potongan_list.append({"nama": "", "jumlah": None, "sisa": None})
        st.rerun()
    
    st.subheader("Karyawan Tidak Masuk")
    jumlah_tidak_masuk = st.number_input("Jumlah Hari Tidak Masuk", min_value=0, step=1, value=None, format="%d")
    keterangan_tidak_masuk = st.text_input("Keterangan Tidak Masuk Kerja")
    potongan_tidak_masuk = st.number_input("Potongan Tidak Masuk Kerja", min_value=0, step=1000, value=None, format="%d")
    
    st.subheader("Karyawan Masuk/Keluar")
    nama_keluar = st.text_input("Nama Karyawan Keluar")
    tgl_keluar = st.date_input("Tanggal Karyawan Keluar *", value=None)
    nama_baru = st.text_input("Nama Karyawan Baru Masuk")
    tgl_masuk = st.date_input("Tanggal Karyawan Baru Masuk *", value=None)
    
    st.subheader("Upload Lampiran")
    ktp_baru = st.file_uploader("Upload KTP Karyawan Baru", type=["jpg", "jpeg", "png", "pdf"])
    surat_sakit = st.file_uploader("Upload Surat Keterangan Sakit", type=["jpg", "jpeg", "png", "pdf"])
    
    submit = st.form_submit_button("Generate PDF Bukti", use_container_width=True)

def add_file_to_pdf(pdf_obj, uploaded_file, title):
    if uploaded_file is None:
        return
    pdf_obj.add_page()
    pdf_obj.set_font("Arial", "B", 14)
    pdf_obj.cell(0, 10, title, 0, 1, "C")
    pdf_obj.ln(5)
    
    file_bytes = uploaded_file.getvalue()
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    if file_ext in ['jpg', 'jpeg', 'png']:
        img = Image.open(io.BytesIO(file_bytes))
        img_path = f"temp_img_{datetime.now().strftime('%H%M%S%f')}.jpg"
        img.convert('RGB').save(img_path)
        
        img_w, img_h = img.size
        page_w = 190
        max_h = 250
        ratio = min(page_w / img_w, max_h / img_h)
        new_w = img_w * ratio
        new_h = img_h * ratio
        x = (210 - new_w) / 2
        
        pdf_obj.image(img_path, x=x, y=30, w=new_w, h=new_h)
        os.remove(img_path)
    else:
        pdf_obj.set_font("Arial", "", 11)
        pdf_obj.cell(0, 7, f"File terlampir: {uploaded_file.name}", 0, 1)

if submit:
    if nama_karyawan == "" or nama_kantor == "":
        st.error("❌ Nama Kantor & Nama Karyawan wajib diisi!")
        st.stop()
    if tgl_keluar is None or tgl_masuk is None:
        st.error("❌ Tanggal Keluar & Tanggal Masuk wajib dipilih!")
        st.stop()
    
    total_potongan = 0
    total_potongan += to_int(potongan_kredit) + to_int(bon_prive) + to_int(denda_minus) + to_int(minus_tunai)
    total_potongan += to_int(potongan_kecerobohan) + to_int(potongan_tidak_masuk)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BUKTI POTONGAN GAJI", 0, 1, "C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
    pdf.cell(0, 7, f"Nama Kantor: {nama_kantor}", 0, 1)
    pdf.cell(0, 7, f"Nama Karyawan: {nama_karyawan}", 0, 1)
    pdf.cell(0, 7, f"Jumlah Hari Kerja: {to_int(jumlah_hari_kerja)} hari", 0, 1)
    pdf.cell(0, 7, f"Tgl Keluar: {tgl_keluar} | Tgl Masuk Baru: {tgl_masuk}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "RINCIAN POTONGAN:", 0, 1)
    pdf.set_font("Arial", "", 11)
    
    for pot in st.session_state.potongan_list:
        if pot["nama"].strip() != "" and to_int(pot["jumlah"]) > 0:
            pdf.cell(0, 7, f"- {pot['nama']}: Rp {to_int(pot['jumlah']):,} | Sisa: Rp {to_int(pot['sisa']):,}".replace(",", "."), 0, 1)
            total_potongan += to_int(pot["jumlah"])
    
    pdf.cell(0, 7, f"- Kredit Lunak: Rp {to_int(potongan_kredit):,} | Sisa: Rp {to_int(sisa_kredit):,}".replace(",", "."), 0, 1)
    total_potongan += to_int(potongan_kredit)
    pdf.cell(0, 7, f"- Kecerobohan: Rp {to_int(potongan_kecerobohan):,} | Sisa: Rp {to_int(sisa_kecerobohan):,}".replace(",", "."), 0, 1)
    if keterangan_kecerobohan.strip() != "":
        pdf.cell(0, 7, f"  Keterangan: {keterangan_kecerobohan}", 0, 1)
    total_potongan += to_int(potongan_kecerobohan)
    
    pdf.cell(0, 7, f"- Bon Prive: Rp {to_int(bon_prive):,}".replace(",", "."), 0, 1)
    pdf.cell(0, 7, f"- Minus Tunai: Rp {to_int(minus_tunai):,}".replace(",", "."), 0, 1)
    pdf.cell(0, 7, f"- Denda Minus: Rp {to_int(denda_minus):,}".replace(",", "."), 0, 1)
    pdf.cell(0, 7, f"- Tidak Masuk {to_int(jumlah_tidak_masuk)} hari: Rp {to_int(potongan_tidak_masuk):,}".replace(",", "."), 0, 1)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, f"TOTAL POTONGAN: Rp {total_potongan:,}".replace(",", "."), 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, "TTD HRD:........................    TTD Karyawan:........................", 0, 1)

    add_file_to_pdf(pdf, ktp_baru, "LAMPIRAN: KTP KARYAWAN BARU")
    add_file_to_pdf(pdf, surat_sakit, "LAMPIRAN: SURAT KETERANGAN SAKIT")

    pdf_file = f"Bukti_{nama_karyawan}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(pdf_file)
    with open(pdf_file, "rb") as f:
        pdf_output = f.read()
    os.remove(pdf_file)

    st.success("✅ PDF berhasil dibuat!")
    st.download_button(
        label="📄 Download PDF Bukti",
        data=pdf_output,
        file_name=pdf_file,
        mime="application/pdf",
        use_container_width=True
    )
