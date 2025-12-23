# 🛡️ ARBITER

![Project Banner](static/logo_A.png)

> **Next-Gen Email Forensics & Phishing Analysis Tool powered by AI.**

Arbiter is an advanced OSINT and forensic analysis tool designed for SOC analysts and cybersecurity researchers. It leverages **Llama 3 AI** to detect social engineering patterns and utilizes dual-engine geo-tracking to pinpoint attacker origins.

---

## ⚡ Key Features

* **🧠 AI-Driven Analysis:** Uses Large Language Models (LLM) to detect phishing intent, urgency, and coercion in email bodies.
* **🌍 Live Geo-Tracking:** pinpoint the sender's location using a dual-engine fallback mechanism (IP-API & IPWhoIs).
* **📍 Interactive Intel Map:** Visualizes the attack origin on a dark-mode Leaflet map.
* **🔗 IOC Extraction:** Automatically extracts URLs and IPs for further investigation.
* **📄 PDF Dossier:** Generates professional forensic reports with one click.
* **🛡️ Risk Scoring:** Calculates a dynamic threat score (0-100%) based on headers and content analysis.

---

## 🛠️ Technology Stack

* **Backend:** Python, Flask
* **AI Engine:** Groq API (Llama-3-70b)
* **Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript
* **Mapping:** Leaflet.js
* **Geolocation:** IP-API, IPWhoIs

---

## 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/RealFiras/Arbiter-Threat-Intel.git](https://github.com/RealFiras/Arbiter-Threat-Intel.git)
    cd Arbiter-Threat-Intel
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Groq API key:
    ```text
    GROQ_API_KEY=gsk_your_api_key_here
    ```

4.  **Run the System:**
    ```bash
    python app.py
    ```
    Access the tool at `http://127.0.0.1:5000`

---

## 📸 Screenshots

![Dashboard View](static/main.png)
---

## ⚠️ Disclaimer

This tool is developed for **educational and defensive purposes only**. The developer (FRL) is not responsible for any misuse of this tool.

---

<p align="center">
  Engineered by <strong>Firas Mahmoud (FRL)</strong> | 2025
</p>
