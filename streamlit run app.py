# DUSC PDF Converter – FULL CLOUD-SAFE VERSION
# Streamlit Cloud compatible (no docx2pdf)

import streamlit as st
import fitz  # PyMuPDF
from pdf2docx import Converter
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tabula
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="DUSC PDF Converter", page_icon="📄", layout="centered")

# ---------------- BRANDING ----------------
st.markdown("""
<style>
.main {padding: 1rem;}
.title {color: #0B5ED7; font-weight: 700;}
.footer {text-align:center; color:gray; font-size:13px;}
.stButton>button {width: 100%;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 class='title'>📄 DUSC PDF Converter</h2>", unsafe_allow_html=True)
st.caption("Powered by Md Shahriar Hasan Sabuj")
st.divider()

# ---------------- OPTIONS ----------------
option = st.selectbox(
    "🔄 Select Tool",
    [
        "PDF to Word",
        "PDF to Excel",
        "PDF to JPG",
        "PDF to PNG",
        "JPG/PNG to PDF",
        "Compress PDF",
        "Merge PDF",
        "Split PDF",
        "PDF to PowerPoint",
        "Watermark PDF",
        "Sign PDF",
        "Password Protect PDF",
        "Bulk Merge PDF"
    ]
)

# ---------------- FILE UPLOAD ----------------
files = st.file_uploader("📤 Upload File(s)", accept_multiple_files=True)

# ---------------- UTILS ----------------
def save_file(uploaded, name):
    with open(name, "wb") as f:
        f.write(uploaded.read())

# ---------------- PROCESS ----------------
if files and st.button("🚀 Process"):

    # PDF → WORD
    if option == "PDF to Word":
        save_file(files[0], "input.pdf")
        cv = Converter("input.pdf")
        cv.convert("output.docx")
        cv.close()
        st.success("PDF → Word successful")
        st.download_button("⬇️ Download", open("output.docx", "rb"), "output.docx")

    # PDF → EXCEL
    elif option == "PDF to Excel":
        save_file(files[0], "input.pdf")
        tables = tabula.read_pdf("input.pdf", pages="all")
        with pd.ExcelWriter("output.xlsx") as writer:
            for i, table in enumerate(tables):
                table.to_excel(writer, sheet_name=f"Table_{i+1}", index=False)
        st.download_button("⬇️ Download", open("output.xlsx", "rb"), "output.xlsx")

    # PDF → IMAGE
    elif option in ["PDF to JPG", "PDF to PNG"]:
        save_file(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=200)
            ext = "jpg" if option.endswith("JPG") else "png"
            name = f"page_{i+1}.{ext}"
            pix.save(name)
            st.image(name)
            st.download_button(name, open(name, "rb"), name)

    # IMAGE → PDF
    elif option == "JPG/PNG to PDF":
        images = [Image.open(f).convert("RGB") for f in files]
        images[0].save("output.pdf", save_all=True, append_images=images[1:])
        st.download_button("⬇️ Download", open("output.pdf", "rb"), "output.pdf")

    # COMPRESS PDF
    elif option == "Compress PDF":
        save_file(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        doc.save("compressed.pdf", garbage=4, deflate=True)
        st.download_button("⬇️ Download", open("compressed.pdf", "rb"), "compressed.pdf")

    # MERGE PDF
    elif option == "Merge PDF":
        merged = fitz.open()
        for f in files:
            save_file(f, f.name)
            merged.insert_pdf(fitz.open(f.name))
        merged.save("merged.pdf")
        st.download_button("⬇️ Download", open("merged.pdf", "rb"), "merged.pdf")

    # SPLIT PDF
    elif option == "Split PDF":
        save_file(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        for i in range(len(doc)):
            new = fitz.open()
            new.insert_pdf(doc, from_page=i, to_page=i)
            name = f"page_{i+1}.pdf"
            new.save(name)
            st.download_button(name, open(name, "rb"), name)

    # PDF → POWERPOINT
    elif option == "PDF to PowerPoint":
        save_file(files[0], "input.pdf")
        from pptx import Presentation
        prs = Presentation()
        doc = fitz.open("input.pdf")
        for page in doc:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            pix = page.get_pixmap()
            pix.save("temp.png")
            slide.shapes.add_picture("temp.png", 0, 0, width=prs.slide_width)
        prs.save("output.pptx")
        st.download_button("⬇️ Download", open("output.pptx", "rb"), "output.pptx")

    # WATERMARK
    elif option == "Watermark PDF":
        text = st.text_input("Watermark Text", "DUSC")
        save_file(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        for p in doc:
            p.insert_text((72, 72), text, fontsize=40, rotate=45, opacity=0.2)
        doc.save("watermarked.pdf")
        st.download_button("⬇️ Download", open("watermarked.pdf", "rb"), "watermarked.pdf")

    # SIGN PDF
    elif option == "Sign PDF":
        sig = st.file_uploader("Upload Signature Image", type=["png", "jpg"])
        if sig:
            save_file(files[0], "input.pdf")
            doc = fitz.open("input.pdf")
            rect = fitz.Rect(300, 700, 500, 780)
            doc[-1].insert_image(rect, stream=sig.read())
            doc.save("signed.pdf")
            st.download_button("⬇️ Download", open("signed.pdf", "rb"), "signed.pdf")

    # PASSWORD PROTECT
    elif option == "Password Protect PDF":
        pwd = st.text_input("Password")
        save_file(files[0], "input.pdf")
        reader = PdfReader("input.pdf")
        writer = PdfWriter()
        for p in reader.pages:
            writer.add_page(p)
        writer.encrypt(pwd)
        with open("protected.pdf", "wb") as f:
            writer.write(f)
        st.download_button("⬇️ Download", open("protected.pdf", "rb"), "protected.pdf")

    # BULK MERGE
    elif option == "Bulk Merge PDF":
        merged = fitz.open()
        for f in files:
            save_file(f, f.name)
            merged.insert_pdf(fitz.open(f.name))
        merged.save("bulk.pdf")
        st.download_button("⬇️ Download", open("bulk.pdf", "rb"), "bulk.pdf")

st.divider()
st.markdown("<div class='footer'>© 2025 Daffodil University School & College</div>", unsafe_allow_html=True)
