import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="📄 AI Resume Builder", layout="centered")
st.title("📄 AI Resume Builder")

st.markdown("Fill in your details to generate a resume or upload a file to get it reviewed.")

# ─────────────────────────────
# Resume Builder Form
# ─────────────────────────────
with st.form(key="resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    skills = st.text_area("Skills (comma separated)")
    education = st.text_area("Education (degree, institution, year, grade)")
    projects = st.text_area("Projects (name, tech, description bullets)")
    experience = st.text_area("Experience (role, company, duration, description bullets)")
    clubs = st.text_area("Clubs / Activities (name, role, description)")

    # Separate buttons for each action
    preview_btn = st.form_submit_button("👀 Preview Resume")
    download_docx_btn = st.form_submit_button("⬇️ Download DOCX")
    download_pdf_btn = st.form_submit_button("⬇️ Download PDF")

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
# Resume Preview
# ─────────────────────────────
if preview_btn:
    with st.spinner("Generating preview..."):
        try:
            res = requests.post(f"{API_URL}/preview-docx", json=data)
            if res.status_code == 200:
                st.components.v1.html(res.text, height=800, scrolling=True)
            else:
                st.error(f"Preview failed: {res.text}")
        except Exception as e:
            st.error(f"Error generating preview: {e}")

# ─────────────────────────────
# Download DOCX
# ─────────────────────────────
if download_docx_btn:
    with st.spinner("Generating DOCX..."):
        try:
            res = requests.post(f"{API_URL}/download?format=docx", json=data)
            if res.status_code == 200:
                st.download_button(
                    label="⬇️ Download DOCX",
                    data=res.content,
                    file_name="resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            else:
                st.error(f"DOCX generation failed: {res.text}")
        except Exception as e:
            st.error(f"Error generating DOCX: {e}")

# ─────────────────────────────
# Download PDF
# ─────────────────────────────
if download_pdf_btn:
    with st.spinner("Generating PDF..."):
        try:
            res = requests.post(f"{API_URL}/download?format=pdf", json=data)
            if res.status_code == 200:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=res.content,
                    file_name="resume.pdf",
                    mime="application/pdf",
                )
            else:
                st.error(f"PDF generation failed: {res.text}")
        except Exception as e:
            st.error(f"Error generating PDF: {e}")

# ─────────────────────────────
# Resume Review Upload
# ─────────────────────────────
st.markdown("---")
st.subheader("📄 Upload Resume for AI Review")
uploaded_file = st.file_uploader("Upload DOCX or PDF", type=["docx", "pdf"])

if uploaded_file:
    # Only show review button after file is uploaded
    review_btn = st.button("🔍 Review Resume")

    if review_btn:
        with st.spinner("Analyzing resume..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                res = requests.post(f"{API_URL}/review-file", files=files)
                
                if res.status_code == 200:
                    review = res.json().get("review", {})
                    st.success("✅ Review Complete")
                    
                    st.metric("Overall Score", review.get("overall_score", "N/A"))
                    st.write(f"**Grade:** {review.get('grade', 'N/A')}")
                    st.write(f"**Strength Level:** {review.get('strength_level', 'N/A')}")

                    st.write("### Section Scores")
                    for section in review.get("section_scores", []):
                        st.write(f"**{section['section_name']}** — Score: {section['score']}")
                        st.write(f"Feedback: {section['feedback']}")
                        st.write(f"Suggestions: {', '.join(section['suggestions'])}")

                    st.write("### Top Strengths")
                    st.write(", ".join(review.get("top_strengths", [])))

                    st.write("### Critical Gaps")
                    st.write(", ".join(review.get("critical_gaps", [])))

                    st.write("### Quick Wins")
                    st.write(", ".join(review.get("quick_wins", [])))

                    ats = review.get("ats_analysis", {})
                    st.write("### ATS Analysis")
                    st.write(f"ATS Score: {ats.get('ats_score', 'N/A')}")
                    st.write(f"Missing Keywords: {', '.join(ats.get('missing_keywords', []))}")
                    st.write(f"Formatting Issues: {', '.join(ats.get('formatting_issues', []))}")

                    st.write("### Recruiter Verdict")
                    st.write(review.get("recruiter_verdict", ""))

                    st.write("### Rewrite Hints")
                    st.write(", ".join(review.get("rewrite_hints", [])))

                else:
                    st.error(f"Review failed: {res.text}")

            except Exception as e:
                st.error(f"Error reviewing resume: {e}")