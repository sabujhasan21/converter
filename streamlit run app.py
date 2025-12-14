import streamlit as st
import fitz  # PyMuPDF
from pdf2docx import Converter
import os

st.set_page_config(page_title="PDF Converter", layout="centered")
st.title("📄 PDF Converter Tool")
st.write("PDF থেকে Word অথবা JPG এ কনভার্ট করুন")

uploaded_pdf = st.file_uploader("📤 PDF আপলোড করুন", type=["pdf"])

option = st.radio(
    "কনভার্সন টাইপ নির্বাচন করুন",
    ("PDF to Word", "PDF to JPG")
)

if uploaded_pdf:
    with open("input.pdf", "wb") as f:
        f.write(uploaded_pdf.read())

    if st.button("🔁 Convert"):
        # ---------------- PDF to WORD ----------------
        if option == "PDF to Word":
            output_word = "converted.docx"
            cv = Converter("input.pdf")
            cv.convert(output_word)
            cv.close()

            st.success("✅ PDF → Word সফল হয়েছে")
            with open(output_word, "rb") as f:
                st.download_button(
                    "⬇️ Download Word File",
                    f,
                    file_name="converted.docx"
                )

        # ---------------- PDF to JPG ----------------
        elif option == "PDF to JPG":
            doc = fitz.open("input.pdf")
            st.success("✅ PDF → JPG সফল হয়েছে")

            for i in range(len(doc)):
                page = doc[i]
                pix = page.get_pixmap(dpi=200)
                img_name = f"page_{i+1}.jpg"
                pix.save(img_name)

                with open(img_name, "rb") as img:
                    st.download_button(
                        label=f"⬇️ Download Page {i+1}",
                        data=img,
                        file_name=img_name,
                        mime="image/jpeg"
                    )
