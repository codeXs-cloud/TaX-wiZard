# 🏦 ET AI Tax Wizard: Intelligent Tax Architecture

[![Built with Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Powered by Gemini](https://img.shields.io/badge/Powered_by-Gemini_2.5_Flash-8E75B2?logo=google)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **ET AI Hackathon 2026 Submission** | **Track:** AI Money Mentor (Problem Statement 9)

## 📌 The Vision
95% of Indians lack a formal financial plan, leaking thousands of rupees annually to sub-optimal tax regimes and missed deductions (like HRA and NPS). Traditional advisory costs upwards of ₹25,000/year. 

The **ET AI Tax Wizard** democratizes wealth management. It is an autonomous, agentic AI money mentor that analyzes your financial profile and engineers the optimal tax strategy—turning confused savers into confident investors in under 30 seconds.

---

## ✨ Core Features (MVP)
* **🧠 Zero-Hallucination Architecture:** The AI acts as a semantic router, using strict "Tool Calling" to pass data to a deterministic Python rules engine. The AI never guesses your math.
* **⚖️ Dual-Regime Modeling:** Instantly compares the Old vs. New Indian Income Tax regimes (FY 2024-25).
* **🏠 Smart HRA Optimizer:** Calculates complex House Rent Allowance exemptions based on Metro/Non-Metro geographic rules.
* **🎯 Proactive Wealth Triggers:** Automatically detects unused Section 80C limits and intelligently pushes users to utilize Section 80CCD(1B) (NPS) for an extra ₹50,000 deduction.
* **📄 Exportable Wealth Blueprint:** Generates a secure, downloadable PDF playbook of your personalized tax strategy.

---

## 🏗️ Architecture: Single-Node Agentic Monolith

To ensure 100% mathematical accuracy while maintaining conversational fluidity, we decoupled the LLM's reasoning from the mathematical calculations.

```text
[ 🧑‍💼 User Interface ] 
      │ (Inputs & Chat via Streamlit)
      ▼
[ 🧠 Cognitive Router ] 
  (Google Gemini 2.5 Flash API)
      │ • Extracts variables via NLP
      │ • Triggers Tool Calling (No AI Math!)
      ▼
[ ⚙️ Deterministic Python Engine ] 
  (tax_calculator.py)
      │ • Calculates HRA limits
      │ • Runs Old vs. New Regime logic
      │ • Flags Missing Deductions
      ▼
[ 📄 Output Generation ]
  (Streamlit UI + FPDF)
      │ • Renders AI conversational advice
      │ • Generates downloadable PDF Blueprint
