import os
import sys
import json
import urllib.request
import urllib.error
import time
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pipeline import translate_to_karakalpak, polish_with_gemini, send_telegram, GEMINI_API_KEY

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GRANTS_FILE = os.path.join(DATA_DIR, "grants.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Oqıw qáteligi {path}: {e}")
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_new_grant_in_russian(existing_titles):
    titles_str = ", ".join([f'"{t}"' for t in existing_titles[-20:]])
    prompt = f"""
Ты эксперт по международным и узбекистанским грантам, стипендиям и программам обмена для молодежи.
Подготовь ОДИН новый, актуальный, престижный грант или стипендиальную программу для студентов и абитуриентов из Узбекистана / Каракалпакстана.

НЕ ПОВТОРЯЙ следующие гранты, они уже были опубликованы:
[{titles_str}]

Грант должен быть реальным и всемирно известным (например: Chevening, Fulbright, Visby Sweden, Romanian Government, MEXT Japan, GKS Korea, CSC China, DSU Italy, Eiffel France, Swiss Government, Erasmus Mundus, DAAD, Türkiye Bursları, Stipendium Hungaricum, El-yurt umidi и т.д.).

Формат строго JSON:
{{
  "grant_name": "Название гранта (кратко)",
  "country": "Страна",
  "official_link": "https://официальный-сайт-программы",
  "degree": "Бакалавриат / Магистратура / Докторантура / Стажировка",
  "coverage": "Полный грант (что входит)",
  "deadline": "Крайний срок подачи",
  "russian_post_text": "Красивый текст поста на русском языке со структурой для Telegram (заголовок с эмодзи флага страны, уровни обучения, финансирование с буллетами, требования к кандидатам, дедлайн). Объем около 80-100 слов."
}}
"""
    models = ["gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-flash-latest"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_API_KEY}"
        data = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"}
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                return json.loads(text)
        except Exception as e:
            print(f"Model {m} генерацияда qátelik: {e}")
            time.sleep(1)
    return None

def main():
    print("=== KÚNLIK GRANT GENERATSIYASI HÁM TELEGRAMǴA JIBERIW ===")
    history = load_json(HISTORY_FILE, [])
    grants = load_json(GRANTS_FILE, [])

    print(f"Bazadaǵı aldınǵı grantlar sanı: {len(history)}")
    new_grant_data = generate_new_grant_in_russian(history)
    if not new_grant_data:
        print("Gemini AI arqalı jańa grant jaratıp bolmadı.")
        return

    grant_name = new_grant_data.get("grant_name", "Belgisiz grant")
    ru_text = new_grant_data.get("russian_post_text", "")
    link = new_grant_data.get("official_link", "https://t.me/jaslargrant")

    print(f"Yaratilgan grant: {grant_name}")
    print("1. Translator API arqalı qaraqalpaqshaga awdarılmaqta...")
    translated = translate_to_karakalpak(ru_text)
    if not translated:
        print("Awdarmada qátelik boldı.")
        return

    print("2. Gemini AI arqalı qátelikler tekserilip, qaraqalpaqsha sazlanbaqta...")
    polished = polish_with_gemini(translated, link)

    print("3. Telegram @jaslargrant kanalına jiberilmekte...")
    sent = send_telegram(polished)
    if sent:
        print(f"✅ Muvaffaqiyatli jiberildi: {grant_name}")
        history.append(grant_name)
        save_json(HISTORY_FILE, history)

        # Sayt ushın grants.json ga qosıw
        site_entry = {
            "id": f"grant-{int(time.time())}",
            "title": grant_name,
            "country": new_grant_data.get("country", "Xalıqaralıq"),
            "degree": new_grant_data.get("degree", "Bakalavr / Magistr"),
            "coverage": new_grant_data.get("coverage", "Tolıq grant"),
            "deadline": new_grant_data.get("deadline", "Rásmiy saytta"),
            "summary": polished.replace("<b>", "").replace("</b>", "")[:180] + "...",
            "official_link": link,
            "date_posted": datetime.now().strftime("%Y-%m-%d")
        }
        grants.insert(0, site_entry)
        save_json(GRANTS_FILE, grants)
        print("grants.json hám history.json jańalandı.")
    else:
        print("❌ Telegramǵa jiberiwde qátelik boldı.")

if __name__ == "__main__":
    main()
