import streamlit as st
from PIL import Image

from self_rag_chain import run_self_rag
from corrective_rag_chain import run_corrective_rag
from corrective_rag_v2_chain import run_corrective_rag_v2
from fallback_rag_chain import run_fallback_rag
from web_search_rag_chain import run_web_search_rag
from adaptive_rag_chain import run_adaptive_rag
from response_formatter import format_adaptive_response

# App Config
st.set_page_config(page_title="Waffestry RAG Suite", layout="wide")

# Initialize Session State
if 'selected_rag' not in st.session_state:
    st.session_state['selected_rag'] = None
if 'query' not in st.session_state:
    st.session_state['query'] = ''
if 'auto_submit' not in st.session_state:
    st.session_state['auto_submit'] = False

# Load and Resize Waffestry Logo
logo = Image.open("data/waffestry_logo_resized.png")
logo = logo.resize((300, int(logo.height * (300 / logo.width))))

# Center-Aligned Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo, use_column_width=False)

# Header Title & Tagline
st.markdown("<h1 style='text-align: center; color: #B05D38;'>Waffestry AI — Your Smart Café Assistant 🧇</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Get instant answers about our Menu, Offers, Combos, and more with AI-powered precision.</p>", unsafe_allow_html=True)
st.markdown("---")

# RAG Mode Selection (only if not selected)
if not st.session_state['selected_rag']:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Self-RAG"):
            st.session_state['selected_rag'] = "Self-RAG"
    with col2:
        if st.button("Corrective RAG"):
            st.session_state['selected_rag'] = "Corrective RAG"
    with col3:
        if st.button("Corrective RAG v2"):
            st.session_state['selected_rag'] = "Corrective RAG v2"

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("Fallback RAG"):
            st.session_state['selected_rag'] = "Fallback RAG"
    with col5:
        if st.button("Web Search RAG"):
            st.session_state['selected_rag'] = "Web Search RAG"
    with col6:
        if st.button("Adaptive RAG"):
            st.session_state['selected_rag'] = "Adaptive RAG"

# Suggestion Questions per RAG Type
suggestions = {
    "Self-RAG": ["What is a KitKat Waffle?", "Describe the Veg Combo Box."],
    "Corrective RAG": ["What is the price of Double Chocolate Waffle?", "Explain the Waffestry SOP."],
    "Corrective RAG v2": ["Verify the ingredients of Belgian Waffle.", "Correct the menu description of Oreo Waffle."],
    "Fallback RAG": ["Tell me today's offers.", "What is the new menu for this month?"],
    "Web Search RAG": ["Any new promotions running today?", "Latest events in Waffestry café?"],
    "Adaptive RAG": ["Suggest creative waffle presentation ideas.", "Give me a detailed analysis of customer preferences."]
}

# Main Interaction Section
if st.session_state['selected_rag']:
    # Back Button
    if st.button("⬅ Back to RAG Selection", key="back_button", help="Go back to select another RAG mode"):
        st.session_state['selected_rag'] = None
        st.session_state['query'] = ''
        st.rerun()

    # Custom CSS for Back Button
    st.markdown("""
        <style>
            .back-button {
                background-color: #FFA500;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                border: none;
                font-size: 16px;
                cursor: pointer;
                text-align: center;
                margin: 10px auto;
                display: block;
                width: fit-content;
            }
            .back-button:hover {
                background-color: #FF8C00;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"### Selected Mode: {st.session_state['selected_rag']}")
    st.markdown("💡 **Example Questions:**")
    for ques in suggestions[st.session_state['selected_rag']]:
        if st.button(ques, key=ques):
            st.session_state['query'] = ques
            st.session_state['auto_submit'] = True

    query = st.text_input("Ask your Question", value=st.session_state.get('query', ''))

    # Adaptive RAG - User Context Selector
    if st.session_state['selected_rag'] == "Adaptive RAG":
        user_context = st.selectbox(
            "Select your expertise level (for Adaptive RAG):",
            ("Beginner", "Intermediate", "Advanced", "Expert")
        )
    else:
        user_context = "Intermediate"

    # Submit Logic
    submit_clicked = st.button("Submit")
    if submit_clicked or st.session_state.get('auto_submit', False):
        st.session_state['auto_submit'] = False  # Reset flag
        selected_rag = st.session_state['selected_rag']

        if selected_rag == "Self-RAG":
            result = run_self_rag(query)
            st.markdown("### 🤖 Answer:")
            st.write(result["initial_answer"])

        elif selected_rag == "Corrective RAG":
            result = run_corrective_rag(query)
            st.markdown("### 🤖 Initial LLM Answer:")
            st.write(result["initial_answer"])
            if not result["verified"]:
                st.markdown("### 📚 Corrected Answer:")
                st.write(result["corrected_answer"])

        elif selected_rag == "Corrective RAG v2":
            result = run_corrective_rag_v2(query)
            st.markdown("### 📊 Context Quality:")
            st.write(result["evaluation"])
            st.markdown("### 🤖 Answer:")
            st.write(result["answer"])

        elif selected_rag == "Fallback RAG":
            result = run_fallback_rag(query)
            st.markdown(f"### Retrieval Level Used: {result['retrieval_level']}")
            st.markdown("### 🧇 Answer:")
            st.write(result["answer"])

        elif selected_rag == "Web Search RAG":
            result = run_web_search_rag(query)
            st.markdown(f"### Search Strategy: {result['strategy']}")
            st.markdown("### 🧇 Answer:")
            st.write(result["answer"])

        elif selected_rag == "Adaptive RAG":
            result = run_adaptive_rag(query, user_context)
            st.markdown("### 🔎 Query Classification:")
            st.json(result["classification"])
            st.markdown("### 🧇 Adaptive Answer:")
            formatted_answer = format_adaptive_response(result["answer"])
            st.markdown(formatted_answer)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Powered by Waffestry AI | RAG Suite</p>", unsafe_allow_html=True)