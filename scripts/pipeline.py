import os
import sys
import json
import urllib.request
import urllib.error
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# API keys (Environment arqalı alınadı, kod ishinde ashıq jazılmaydı)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "@jaslargrant")
TRANSLATOR_API = "https://karakalpak-translator-api.onrender.com/translate"

def translate_to_karakalpak(russian_text):
    payload = {
        "text": russian_text,
        "target_script": "latin"
    }
    headers = {
        "Content-Type": "application/json",
        "x-gemini-api-key": GEMINI_API_KEY
    }
    req = urllib.request.Request(TRANSLATOR_API, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("translated_latin") or data.get("translated_text")
    except Exception as e:
        print(f"Translator API qátelik: {e}")
        return None

def polish_with_gemini(karakalpak_text, grant_link):
    prompt = f"""
Siz Qaraqalpaq tili qánigesisiz. Tómendegi Telegram kanalı ushın tayarlanǵan grant postın tekserip shıǵıń.
Post shama menen 90-110 sóz bolıwı, oqıwǵa qolaylı, qaraqalpaq ádebiy tilinde (lotin álipbesinde: á, ó, ú, ǵ, ń, ı, w háripleri durıs qollanılǵan halda) bolıwı kerek.

QÁDELER:
1. Qوپal grammatikalıq, orfografiyalıq yamasa stilistikalıq qáteliklerdi (foolish mistakes) dúzetiń.
2. Emojilerdi, qalıń tekst (HTML <b>...</b> tegleri) hám strukturanı saqlań.
3. Rásmiy siltemeni mına kóriniste qaldırıń: 🔗 <b>Arza tapsırıw:</b> <a href="{grant_link}">{grant_link}</a>
4. Sońına mina qatardı qosıń:
👉 <b>Kanalǵa aǵza bolıń:</b> @jaslargrant
5. Tek ǵana tayar Telegram post tekstin (HTML formatında) qaytarıń, hesh qanday artıqsha túsindirme jazbań!

POST TEKSTI:
{karakalpak_text}
"""
    models = ["gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-flash-latest"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_API_KEY}"
        data = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4}
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                polished = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                # Markdown bloklarini tozalash
                if polished.startswith("```html"):
                    polished = polished[7:]
                if polished.startswith("```"):
                    polished = polished[3:]
                if polished.endswith("```"):
                    polished = polished[:-3]
                return polished.strip()
        except Exception as e:
            print(f"Model {m} polish qáteligi: {e}")
            time.sleep(1)
    return karakalpak_text

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("ok", False)
    except Exception as e:
        print(f"Telegram jiberiw qáteligi: {e}")
        return False
