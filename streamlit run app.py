import streamlit as st
import fitz  # PyMuPDF
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image

st.set_page_config(page_title="DUSC PDF Converter", page_icon="📄")

st.title("📄 DUSC PDF Converter")
st.caption("Powered by Md Shahriar Hasan Sabuj")
st.divider()

tool = st.selectbox(
    "Select Tool",
    [
        "PDF to Word",
        "PDF to JPG",
        "PDF to PNG",
        "JPG/PNG to PDF",
        "Compress PDF",
        "Merge PDF",
        "Split PDF",
        "Watermark PDF",
        "Sign PDF",
        "Password Protect PDF"
    ]
)

files = st.file_uploader("Upload file(s)", accept_multiple_files=True)

def save(f, name):
    with open(name, "wb") as w:
        w.write(f.read())

if files and st.button("Process"):

    if tool == "PDF to Word":
        save(files[0], "input.pdf")
        cv = Converter("input.pdf")
        cv.convert("output.docx")
        cv.close()
        st.download_button("Download Word", open("output.docx","rb"), "output.docx")

    elif tool in ["PDF to JPG", "PDF to PNG"]:
        save(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        for i, p in enumerate(doc):
            pix = p.get_pixmap(dpi=200)
            ext = "jpg" if tool.endswith("JPG") else "png"
            name = f"page_{i+1}.{ext}"
            pix.save(name)
            st.image(name)
            st.download_button(name, open(name,"rb"), name)

    elif tool == "JPG/PNG to PDF":
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save("output.pdf", save_all=True, append_images=imgs[1:])
        st.download_button("Download PDF", open("output.pdf","rb"), "output.pdf")

    elif tool == "Compress PDF":
        save(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        doc.save("compressed.pdf", garbage=4, deflate=True)
        st.download_button("Download", open("compressed.pdf","rb"), "compressed.pdf")

    elif tool == "Merge PDF":
        merged = fitz.open()
        for f in files:
            save(f, f.name)
            merged.insert_pdf(fitz.open(f.name))
        merged.save("merged.pdf")
        st.download_button("Download", open("merged.pdf","rb"), "merged.pdf")

    elif tool == "Split PDF":
        save(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        for i in range(len(doc)):
            n = fitz.open()
            n.insert_pdf(doc, from_page=i, to_page=i)
            name = f"page_{i+1}.pdf"
            n.save(name)
            st.download_button(name, open(name,"rb"), name)

    elif tool == "Watermark PDF":
        text = st.text_input("Watermark Text", "DUSC")
        save(files[0], "input.pdf")
        doc = fitz.open("input.pdf")
        for p in doc:
            p.insert_text((72,72), text, fontsize=40, rotate=45, opacity=0.2)
        doc.save("watermarked.pdf")
        st.download_button("Download", open("watermarked.pdf","rb"), "watermarked.pdf")

    elif tool == "Sign PDF":
        sig = st.file_uploader("Upload signature", type=["png","jpg"])
        if sig:
            save(files[0], "input.pdf")
            doc = fitz.open("input.pdf")
            rect = fitz.Rect(300,700,500,780)
            doc[-1].insert_image(rect, stream=sig.read())
            doc.save("signed.pdf")
            st.download_button("Download", open("signed.pdf","rb"), "signed.pdf")

    elif tool == "Password Protect PDF":
        pwd = st.text_input("Password")
        save(files[0], "input.pdf")
        r = PdfReader("input.pdf")
        w = PdfWriter()
        for p in r.pages:
            w.add_page(p)
        w.encrypt(pwd)
        with open("protected.pdf","wb") as f:
            w.write(f)
        st.download_button("Download", open("protected.pdf","rb"), "protected.pdf")

st.divider()
st.caption("© 2025 Daffodil University School & College")
