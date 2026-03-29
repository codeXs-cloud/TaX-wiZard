import streamlit as st
from agent import get_tax_wizard_chat
from fpdf import FPDF
import base64

# --- 1. CORE SETUP & METADATA ---
st.set_page_config(page_title="ET Tax Wizard | Your Personal AI Money Mentor", page_icon="🏦", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE CSS SAAS INJECTION (Fixing Visibility & Enhancing Hover) ---
st.markdown("""
<style>
    /* Import Premium UI Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* 1. Solid Foundation & Background Mesh (Orbs) */
    .stApp {
        background-color: #f8fafc !important; 
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(224, 242, 254, 0.7) 0px, transparent 400px),
            radial-gradient(circle at 85% 10%, rgba(219, 234, 254, 0.7) 0px, transparent 400px),
            radial-gradient(circle at 50% 90%, rgba(241, 245, 249, 0.9) 0px, transparent 400px) !important;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove unnecessary space from the top */
    .block-container {
        padding-top: 1rem !important;
        margin-top: 0 !important;
    }
    
    /* 2. Responsive Hero Section */
    .hero-container {
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 2rem;
        padding: 0 1rem;
    }
    .hero-title {
        font-size: clamp(2rem, 5vw, 3.5rem); 
        font-weight: 800;
        letter-spacing: -1px;
        color: #2563eb !important; 
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: clamp(1rem, 2.5vw, 1.2rem);
        color: #475569 !important;
        font-weight: 400;
        max-width: 800px;
        margin: 0 auto;
    }

    /* =========================================================
       SILVER BULLET: FORCE BLACK TEXT ON ALL ELEMENTS
       ========================================================= */
    .stApp p, .stApp span, .stApp label, div[data-baseweb="input"], .stMarkdown {
        color: #0f172a !important; /* Deep Slate/Black */
    }
    
    /* Force Input Values to be strictly black */
    input[type="number"], input[type="text"], textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important; 
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* 3. EXTREME HOVER EFFECT (Targeting ONLY the Left Column Blocks 1, 2, 3) */
    [data-testid="column"]:nth-of-type(1) [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 2px solid transparent !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* Block 1: Income Architecture (Green tint) */
    [data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) {
        background: linear-gradient(135deg, #ffffff, #f0fdf4) !important;
        border-color: #dcfce7 !important;
    }
    [data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1):hover {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 0 30px 40px -10px rgba(34, 197, 94, 0.3), 0 15px 15px -10px rgba(34, 197, 94, 0.2) !important;
        border-color: #22c55e !important;
        background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
    }

    /* Block 2: Living & Exemptions (Yellow tint) */
    [data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2) {
        background: linear-gradient(135deg, #ffffff, #fefce8) !important;
        border-color: #fef08a !important;
    }
    [data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2):hover {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 0 30px 40px -10px rgba(234, 179, 8, 0.3), 0 15px 15px -10px rgba(234, 179, 8, 0.2) !important;
        border-color: #eab308 !important;
        background: linear-gradient(135deg, #fefce8, #fef08a) !important;
    }

    /* Block 3: Wealth Creation (Blue tint) */
    [data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(3) {
        background: linear-gradient(135deg, #ffffff, #eff6ff) !important;
        border-color: #dbeafe !important;
    }
    [data-testid="column"]:nth-of-type(1) div[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(3):hover {
        transform: translateY(-12px) scale(1.03) !important;
        box-shadow: 0 30px 40px -10px rgba(59, 130, 246, 0.3), 0 15px 15px -10px rgba(59, 130, 246, 0.2) !important;
        border-color: #3b82f6 !important;
        background: linear-gradient(135deg, #eff6ff, #dbeafe) !important;
    }

    /* Section Titles inside the blocks */
    .section-title {
        color: #000000 !important;
        font-size: 1.3rem;
        font-weight: 800;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 8px;
        margin-bottom: 15px;
        text-align: center;
    }

    /* 4. Buttons Hover Effect */
    [data-testid="baseButton-primary"] {
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    [data-testid="baseButton-primary"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4) !important;
    }

    /* 5. Premium Chatbot Styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.7) !important; 
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        animation: fadeIn 0.4s ease-out;
    }
    
    /* Specific styles for Assistant vs User */
    [data-testid="stChatMessage"]:has([aria-label="🏦"]) {
        border-left: 4px solid #3b82f6 !important; /* Blue indicator for Tax Wizard */
    }
    [data-testid="stChatMessage"]:has([aria-label="🧑‍💼"]) {
        background: rgba(241, 245, 249, 0.8) !important; /* Slightly distinct background for User */
        border-left: 4px solid #94a3b8 !important;
    }

    .stChatMessage p {
        color: #0f172a !important; /* Deep text */
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }

    /* Keyframes for smooth chat rendering */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 6. Chatbot Input Box (Premium Glassmorphism) */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stChatInput"]:hover {
        box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-1px);
    }
    [data-testid="stChatInput"]:focus-within {
        box-shadow: 0 10px 30px -5px rgba(59, 130, 246, 0.2) !important;
        transform: translateY(-2px);
    }
    [data-testid="stChatInput"] textarea {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important; 
        font-weight: 500 !important;
        font-size: 1.05rem !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        opacity: 0.5 !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to generate PDF
def create_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="ECONOMIC TIMES: AI MONEY MENTOR", ln=True, align='C')
    pdf.cell(200, 10, txt="Confidential Tax & Wealth Playbook", ln=True, align='C')
    pdf.cell(200, 10, txt="---------------------------------------------------------", ln=True, align='C')
    pdf.ln(10)
    
    for msg in chat_history:
        role = "YOUR INPUT" if msg["role"] == "user" else "AI MENTOR ANALYSIS"
        clean_text = msg["content"].replace("₹", "Rs. ")
        text = clean_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.set_font("Arial", 'B', 10)
        pdf.multi_cell(0, 8, txt=f"{role}:")
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 8, txt=text)
        pdf.ln(5)
    
    return pdf.output(dest="S").encode("latin-1")


# --- 3. HERO SECTION (Centered & Blue) ---
st.markdown("""
<div class="hero-container">
    <div class="hero-title">TaX wiZard</div>
    <div class="hero-subtitle">Intelligent Tax Architecture. Let Ai Do youR Tax Planning</div>
</div>
""", unsafe_allow_html=True)

# --- 4. MAIN APPLICATION LAYOUT ---
# Columns automatically stack on mobile devices
left_col, right_col = st.columns([1.1, 1.4], gap="large")

with left_col:
    # BLOCK 1: Income Architecture
    with st.container(border=True):
        st.markdown('<div class="section-title"> Income Architecture</div>', unsafe_allow_html=True)
        basic_salary = st.number_input("Annual Basic Salary (₹)", min_value=0, value=800000, step=50000)
        
        col_a, col_b = st.columns(2)
        with col_a:
            hra_received = st.number_input("HRA Received (₹)", min_value=0, value=300000, step=10000)
        with col_b:
            other_allowances = st.number_input("Special Allowances (₹)", min_value=0, value=200000, step=10000)
            
    # BLOCK 2: Living Expanses & Exemptions
    with st.container(border=True):
        st.markdown('<div class="section-title"> Living & Exemptions</div>', unsafe_allow_html=True)
        rent_paid = st.number_input("Annual Rent Paid (₹)", min_value=0, value=240000, step=10000)
        is_metro = st.toggle("Resident of a Metro City? (Delhi/Mumbai/Chennai)", value=False)

    # BLOCK 3: Wealth Creation
    with st.container(border=True):
        st.markdown('<div class="section-title"> Wealth Creation</div>', unsafe_allow_html=True)
        sec_80c = st.slider(
            "Sec 80C (EPF, ELSS, Life Ins.)", 
            0, 200000, 150000, step=5000,
            help="Section 80C offers a max deduction of ₹1.5 Lakhs. Covers Employee Provident Fund (EPF), Public Provident Fund (PPF), Equity Linked Savings Scheme (ELSS), Life Insurance Premiums, etc."
        )
        
        col_c, col_d = st.columns(2)
        with col_c:
            nps = st.number_input(
                "NPS Tier-1 (80CCD 1B)", 
                min_value=0, max_value=50000, value=0, step=5000,
                help="Extra deduction up to ₹50,000 for National Pension System (NPS) voluntary contributions, above the ₹1.5L 80C limit."
            )
        with col_d:
            sec_80d = st.number_input(
                "Health Ins. (Sec 80D)", 
                min_value=0, max_value=75000, value=15000, step=5000,
                help="Deduction for medical insurance premiums. Up to ₹25,000 for self/family, and an additional ₹50,000 for senior citizen parents."
            )
        
    gross = basic_salary + hra_received + other_allowances
    profile_summary = f"Gross Income: {gross}. Basic: {basic_salary}, HRA Received: {hra_received}, Rent Paid: {rent_paid}, Metro: {is_metro}, 80C: {sec_80c}, 80D: {sec_80d}, NPS: {nps}."

with right_col:
    # Right side contains the terminal (no extreme hover effect here to keep focus on input)
    st.markdown('<div class="section-title">⚡ AI Mentor Terminal</div>', unsafe_allow_html=True)
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = get_tax_wizard_chat()
        st.session_state.messages = [{"role": "assistant", "content": "Welcome. I am synced with your data. Click 'Execute Tax Audit' below to generate your personalized blueprint."}]

    if st.button(" Execute Comprehensive Tax Audit", type="primary", use_container_width=True):
        prompt = f"Analyze this profile and generate a definitive tax strategy: {profile_summary}"
        st.session_state.messages.append({"role": "user", "content": "Execute Tax Audit based on my current data."})
        
        with st.spinner("Processing formulas and dual-regime brackets..."):
            response = st.session_state.chat_session.send_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()
 
    # The chat display box
    chat_container = st.container(height=550, border=False)
    with chat_container:
        for msg in st.session_state.messages:
            avatar = "🧑‍💼" if msg["role"] == "user" else "🏦"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
    
    user_input = st.chat_input("Ask a follow-up (e.g., 'What if I increase my rent to 30k/month?')")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_container.chat_message("user", avatar="🧑‍💼"):
            st.markdown(user_input)
        
        with chat_container.chat_message("assistant", avatar="🏦"):
            with st.spinner("Analyzing tax structures..."):
                contextual_prompt = f"[Current Profile: {profile_summary}] User asks: {user_input}"
                response = st.session_state.chat_session.send_message(contextual_prompt)
                st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()

    if len(st.session_state.messages) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        pdf_bytes = create_pdf(st.session_state.messages)
        st.download_button(
            label="📄 Export Verified Tax Blueprint (PDF)", 
            data=pdf_bytes, 
            file_name="ET_Wealth_Blueprint.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )