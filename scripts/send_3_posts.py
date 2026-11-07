import sys
import os
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pipeline import translate_to_karakalpak, polish_with_gemini, send_telegram

# 3 ta xalqaro grant ma'lumotlari (Rus tilida)
POSTS_RU = [
    {
        "title": "Stipendium Hungaricum",
        "link": "https://stipendiumhungaricum.hu",
        "ru_text": """🇭🇺 <b>Венгрия: Полный правительственный грант Stipendium Hungaricum!</b>

Для молодежи и студентов Узбекистана открыт прием заявок на престижную программу в европейских университетах.

🎓 <b>Уровни образования:</b> Бакалавриат, Магистратура, Докторантура (PhD).
💰 <b>Финансирование:</b>
• 100% бесплатное обучение в университете
• Ежемесячная стипендия
• Бесплатное проживание в общежитии или компенсация за жилье
• Медицинская страховка

📌 <b>Требования:</b>
• Хорошие оценки в аттестате или дипломе
• Знание английского языка (сертификат IELTS от 5.5 / TOEFL или знание венгерского)

⏰ <b>Крайний срок подачи:</b> 15 января 2026 года."""
    },
    {
        "title": "Türkiye Bursları",
        "link": "https://www.turkiyeburslari.gov.tr",
        "ru_text": """🇹🇷 <b>Турция: Государственный грант Türkiye Bursları!</b>

Самая популярная стипендиальная программа Турции для иностранных студентов объявляет набор.

🎓 <b>Направления:</b> Бакалавриат, Магистратура, Докторантура.
💰 <b>Что покрывает грант:</b>
• Полная оплата контракта за обучение
• Ежемесячная стипендия (для бакалавров, магистров и аспирантов)
• Бесплатное студенческое общежитие
• Авиабилет в обе стороны (туда и обратно)
• 1 год бесплатного изучения турецкого языка

📌 <b>Требования:</b>
• Успеваемость: минимум 70% для бакалавриата, 75% для магистратуры
• Возраст: до 21 года для бакалавра, до 30 лет для магистра

⏰ <b>Дедлайн:</b> 20 февраля 2026 года."""
    },
    {
        "title": "Global UGRAD USA",
        "link": "https://www.worldlearning.org/program/global-undergraduate-exchange-program/",
        "ru_text": """🇺🇸 <b>США: Программа обмена Global UGRAD в американских вузах!</b>

Государственный департамент США предоставляет студентам возможность учиться 1 семестр в университетах Америки бесплатно.

🎓 <b>Для кого:</b> Студенты 1, 2 и 3 курсов бакалавриата дневного отделения.
💰 <b>Привилегии программы:</b>
• Полная оплата обучения в университете США
• Авиаперелет в обе стороны
• Бесплатное проживание и трехразовое питание
• Ежемесячная стипендия на личные расходы
• Медицинская страховка

📌 <b>Требования:</b>
• Возраст от 18 лет
• Сертификат TOEFL / IELTS или высокий уровень владения английским
• Лидерские качества и активность

⏰ <b>Срок подачи:</b> 15 декабря 2025 года."""
    }
]

def main():
    print("=== 3 DANA TELEGRAM POST TAYARLAW HÁM JIBERIW ===")
    for i, p in enumerate(POSTS_RU, 1):
        print(f"\n--- {i}-POST: {p['title']} ---")
        print("1. Translator API arqalı qaraqalpaqshaga awdarılmaqta...")
        translated = translate_to_karakalpak(p["ru_text"])
        if not translated:
            print("Awdarmada qátelik júz berdi, toqtatıldı.")
            continue
        print("Awdarma tayar!")

        print("2. Gemini AI arqalı grammatika hám qátelikler tekserilmekte...")
        polished = polish_with_gemini(translated, p["link"])
        print("Polished tekst tayar!")
        
        print("3. Telegram @jaslargrant kanalına jiberilmekte...")
        ok = send_telegram(polished)
        if ok:
            print(f"✅ {i}-post muvaffaqiyatli jiberildi!")
        else:
            print(f"❌ {i}-postti jiberiwde qátelik boldı!")
            
        time.sleep(2)

if __name__ == "__main__":
    main()
