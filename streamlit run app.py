import streamlit as st
import fitz  # PyMuPDF
from pdf2docx import Converter

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DUSC PDF Converter",
    page_icon="📄",
    layout="centered"
)

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

# ---------------- FILE UPLOAD ----------------
uploaded_pdf = st.file_uploader(
    "📤 Upload PDF File",
    type=["pdf"]
)

option = st.selectbox(
    "🔄 Select Conversion Type",
    ["PDF to Word", "PDF to JPG", "PDF to PNG"]
)

# ---------------- PROCESS ----------------
if uploaded_pdf:
    with open("input.pdf", "wb") as f:
        f.write(uploaded_pdf.read())

    if st.button("🚀 Convert Now"):
        # ---------- PDF TO WORD ----------
        if option == "PDF to Word":
            output_word = "converted.docx"
            cv = Converter("input.pdf")
            cv.convert(output_word)
            cv.close()

            st.success("✅ PDF → Word Conversion Successful")
            with open(output_word, "rb") as f:
                st.download_button(
                    "⬇️ Download Word File",
                    f,
                    file_name="converted.docx"
                )

        # ---------- PDF TO JPG / PNG ----------
        else:
            doc = fitz.open("input.pdf")
            st.success("✅ Conversion Successful")

            for i in range(len(doc)):
                page = doc[i]
                pix = page.get_pixmap(dpi=200)

                if option == "PDF to JPG":
                    img_name = f"page_{i+1}.jpg"
                    mime = "image/jpeg"
                else:
                    img_name = f"page_{i+1}.png"
                    mime = "image/png"

                pix.save(img_name)

                st.image(img_name, caption=f"Page {i+1}", use_container_width=True)

                with open(img_name, "rb") as img:
                    st.download_button(
                        f"⬇️ Download Page {i+1}",
                        img,
                        file_name=img_name,
                        mime=mime
                    )

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<div class='footer'>© 2025 Daffodil University School & College</div>",
    unsafe_allow_html=True
)
