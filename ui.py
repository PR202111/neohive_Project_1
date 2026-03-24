import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Resume Builder", layout="centered")

st.title("📄 AI Resume Builder")

# ─────────────────────────────
# Form Inputs
# ─────────────────────────────

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")

skills = st.text_area("Skills (comma separated)")
education = st.text_area("Education")
projects = st.text_area("Projects")
experience = st.text_area("Experience")
clubs = st.text_area("Clubs / Activities")

data = {
    "name": name,
    "email": email,
    "phone": phone,
    "skills": skills,
    "education": education,
    "projects": projects,
    "experience": experience,
    "clubs": clubs,
}

# ─────────────────────────────
# Buttons
# ─────────────────────────────

col1, col2, col3 = st.columns(3)

with col1:
    preview_btn = st.button("👀 Preview")

with col2:
    download_docx_btn = st.button("⬇️ Download DOCX")

with col3:
    download_pdf_btn = st.button("⬇️ Download PDF")

# ─────────────────────────────
# Preview
# ─────────────────────────────

if preview_btn:
    with st.spinner("Generating preview..."):
        res = requests.post(f"{API_URL}/preview-docx", json=data)

        if res.status_code == 200:
            st.components.v1.html(res.text, height=800, scrolling=True)
        else:
            st.error("Preview failed")

# ─────────────────────────────
# Download DOCX
# ─────────────────────────────

if download_docx_btn:
    with st.spinner("Generating DOCX..."):
        res = requests.post(f"{API_URL}/download?format=docx", json=data)

        if res.status_code == 200:
            st.download_button(
                label="Download DOCX",
                data=res.content,
                file_name="resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        else:
            st.error("Download failed")

# ─────────────────────────────
# Download PDF
# ─────────────────────────────

if download_pdf_btn:
    with st.spinner("Generating PDF..."):
        res = requests.post(f"{API_URL}/download?format=pdf", json=data)

        if res.status_code == 200:
            st.download_button(
                label="Download PDF",
                data=res.content,
                file_name="resume.pdf",
                mime="application/pdf",
            )
        else:
            st.error("Download failed")