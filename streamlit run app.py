import streamlit as st
from pdf2docx import Converter
import fitz  # PyMuPDF
from PIL import Image
import os
import zipfile

st.set_page_config(page_title="PDF Converter", layout="centered")

st.title("📄 PDF Converter Tool")
st.write("PDF থেকে Word অথবা JPG এ কনভার্ট করুন সহজেই")

uploaded_pdf = st.file_uploader("📤 আপনার PDF ফাইল আপলোড করুন", type=["pdf"])

option = st.radio(
    "আপনি কী করতে চান?",
    ("PDF to Word", "PDF to JPG")
)

if uploaded_pdf:
    with open("input.pdf", "wb") as f:
        f.write(uploaded_pdf.read())

    if st.button("🔁 Convert Now"):
        if option == "PDF to Word":
            output_word = "output.docx"
            cv = Converter("input.pdf")
            cv.convert(output_word)
            cv.close()

            st.success("✅ PDF সফলভাবে Word এ কনভার্ট হয়েছে")
            with open(output_word, "rb") as f:
                st.download_button(
                    "⬇️ Download Word File",
                    f,
                    file_name="converted.docx"
                )

        elif option == "PDF to JPG":
            doc = fitz.open("input.pdf")
            img_folder = "images"
            os.makedirs(img_folder, exist_ok=True)

            image_files = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                pix = page.get_pixmap(dpi=200)
                img_path = f"{img_folder}/page_{page_num+1}.jpg"
                pix.save(img_path)
                image_files.append(img_path)

            zip_name = "pdf_images.zip"
            with zipfile.ZipFile(zip_name, "w") as zipf:
                for img in image_files:
                    zipf.write(img)

            st.success("✅ PDF সফলভাবে JPG তে কনভার্ট হয়েছে")
            with open(zip_name, "rb") as f:
                st.download_button(
                    "⬇️ Download Images (ZIP)",
                    f,
                    file_name="pdf_images.zip"
                )
