from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv  
import json
import os
import re
import requests

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ Error: GROQ_API_KEY is missing from .env file!")

client = Groq(api_key=api_key)

app = Flask(__name__)

def track_ip_robust(ip_text):
    ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(ip_text))
    if not ip_match:
        return {"found": False, "error": "Invalid IP Format"}
    
    clean_ip = ip_match.group(0)
    
    if clean_ip.startswith(('127.', '192.168.', '10.', '172.')):
        return {"found": False, "error": "Local IP"}

    print(f"📡 Tracking Target: {clean_ip}...")

    try:
        response = requests.get(f"http://ip-api.com/json/{clean_ip}", timeout=3)
        data = response.json()
        if data.get('status') == 'success':
            return {
                "found": True,
                "country": data.get('country', 'Unknown'),
                "city": data.get('city', 'Unknown'),
                "lat": data.get('lat', 0),
                "lon": data.get('lon', 0),
                "isp": data.get('isp', 'Unknown ISP')
            }
    except Exception as e:
        print(f"   ⚠️ Engine 1 Failed: {e}")

    try:
        response = requests.get(f"http://ipwho.is/{clean_ip}", timeout=3)
        data = response.json()
        if data.get('success') is True:
            return {
                "found": True,
                "country": data.get('country', 'Unknown'),
                "city": data.get('city', 'Unknown'),
                "lat": data.get('latitude', 0),
                "lon": data.get('longitude', 0),
                "isp": data.get('connection', {}).get('isp', 'Unknown ISP')
            }
    except Exception as e:
        print(f"   ⚠️ Engine 2 Failed: {e}")

    return {"found": False, "error": "All Tracking Engines Failed"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_email():
    try:
        data = request.json
        email_content = data.get('email_text', '')

        if not email_content:
             return jsonify({"risk_score": 0, "verdict": "NO INPUT", "explanation": "Please provide email content."})

        scan_content = email_content[:15000]

        system_prompt = """
        You are ARBITER, an elite Cybersecurity AI. 
        Analyze this email for phishing, spoofing, and social engineering.
        
        Return a JSON object with:
        - risk_score: Integer (0-100).
        - risk_level: "SAFE", "SUSPICIOUS", or "DANGEROUS".
        - verdict: Short title (max 5 words).
        - explanation: Technical analysis (max 2 sentences).
        - origin_ip: Extract sender IP from headers if present, else "Hidden".
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze:\n{scan_content}"}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(completion.choices[0].message.content)
        
        current_ip = result.get('origin_ip', 'Hidden')
        
        if current_ip in ['Hidden', 'N/A'] or not re.search(r'\d+\.\d+\.\d+\.\d+', str(current_ip)):
            ip_candidates = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', scan_content)
            for ip in ip_candidates:
                if not ip.startswith(('127.', '10.', '192.168.', '172.')):
                    current_ip = ip
                    result['origin_ip'] = ip 
                    break
        
        
        if current_ip and current_ip not in ['Hidden', 'N/A']:
            geo_info = track_ip_robust(current_ip)
            result['geo_data'] = geo_info
        else:
            result['geo_data'] = {"found": False}

        
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', scan_content)
        result['extracted_urls'] = list(set(urls))

        return jsonify(result)

    except Exception as e:
        print(f"🔥 Critical Error: {e}")
        return jsonify({
            "risk_score": 0, 
            "verdict": "SYSTEM ERROR", 
            "explanation": f"Internal Server Error: {str(e)}"
        })

if __name__ == '__main__':
    app.run(debug=True)