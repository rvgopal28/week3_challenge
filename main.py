import streamlit as st
from self_rag_chain import run_self_rag
from corrective_rag_chain import run_corrective_rag

st.set_page_config(page_title="Waffestry RAG Suite", layout="centered")
st.title("Waffestry RAG Suite 🧇")

option = st.selectbox("Choose RAG Type:", ("Self-RAG", "Corrective RAG"))

query = st.text_input("Ask a Question")

if st.button("Submit") and query:
    if option == "Self-RAG":
        result = run_self_rag(query)
        if result and "initial_answer" in result:
            st.markdown("### 🤖 Initial Answer:")
            st.write(result["initial_answer"])

            if result.get("used_retrieval"):
                st.markdown("### 🔁 Retrieved Answer (RAG was used):")
                st.success(result.get("retrieved_answer", "No answer found."))
            else:
                st.info("RAG was not triggered. Initial answer was confident.")
        else:
            st.error("Failed to get a valid response.")

    elif option == "Corrective RAG":
        result = run_corrective_rag(query)
        if result and "initial_answer" in result:
            st.markdown("### 🤖 Initial LLM Answer:")
            st.write(result["initial_answer"])

            if result.get("verified"):
                st.success("✅ The answer is verified as correct.")
            else:
                st.warning("⚠️ The original answer might be incorrect. Here's the corrected version:")
                st.markdown("### 📚 Corrected Answer:")
                st.write(result.get("corrected_answer", "No corrected answer found."))
        else:
            st.error("Failed to get a valid response.")