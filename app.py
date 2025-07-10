import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="📜 Contract Clause Finder", layout="centered")
st.title("📜 Contract Clause Finder (RAG + LLM)")

# -------------------------------
# STEP 1: Upload Legal Document
# -------------------------------
st.header("Step 1: Upload Legal Contract (PDF)")
pdf_file = st.file_uploader("Choose a contract PDF", type="pdf")

# Session state to avoid re-uploading on each UI interaction
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "pdf_filename" not in st.session_state:
    st.session_state.pdf_filename = None

if pdf_file and not st.session_state.uploaded:
    with st.spinner("📤 Uploading and processing..."):
        clean_name = ''.join(e for e in pdf_file.name if e.isalnum() or e in (' ', '.', '_')).replace(' ', '_')
        res = requests.post(
            f"{API_URL}/uploadfile/",
            files={"file": (clean_name, pdf_file.read(), "application/pdf")}
        )
        if res.status_code == 200:
            st.success(f"✅ Uploaded. {res.json()['clauses_stored']} clauses stored.")
            st.session_state.uploaded = True
            st.session_state.pdf_filename = clean_name
        else:
            st.error(f"❌ Upload failed: {res.text}")

st.divider()

# -------------------------------
# STEP 2: Ask a Question
# -------------------------------
st.header("Step 2: Ask a Question About the Contract")
query = st.text_input("🔍 What do you want to know?", placeholder="e.g. Termination clause")
top_k = st.slider("Number of relevant clauses to use:", 1, 10, value=5)

if st.button("🧠 Submit Query") and query and st.session_state.uploaded:
    with st.spinner("💬 Getting response..."):
        res = requests.post(
            f"{API_URL}/query/",
            json={
                "query": query,
                "top_k": top_k,
                "collection_name": st.session_state.pdf_filename
            }
        )
        if res.status_code == 200:
            response = res.json()
            st.subheader("📢 LLM Response")
            st.success(response["response"])

            st.subheader("📚 Supporting Clauses")
            for i, clause in enumerate(response["results"], 1):
                st.markdown(f"**Clause {i}:**\n\n{clause}")
        else:
            st.error(f"❌ Query failed: {res.text}")
elif not st.session_state.uploaded:
    st.info("ℹ️ Please upload a legal PDF first.")
