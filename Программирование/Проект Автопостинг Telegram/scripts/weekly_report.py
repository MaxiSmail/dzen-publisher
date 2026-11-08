import sys
import requests
import json
import os
import config
import analytics

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def generate_and_send_weekly_report():
    print("=" * 60)
    print("ГЕНЕРАЦИЯ ЕЖЕНЕДЕЛЬНОГО СММ-ОТЧЕТА ДЛЯ ВЛАДЕЛЬЦА")
    print("=" * 60)
    
    history = analytics.load_analytics_history()
    total_posts = len(history)
    
    tag_counts = {}
    for item in history:
        for tag in item.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags_str = ", ".join([f"#{t[0]} ({t[1]} постов)" for t in top_tags]) if top_tags else "Нет данных"
    
    report_text = (
        f"📊 <b>ЕЖЕНЕДЕЛЬНЫЙ СММ-ОТЧЕТ ДИРЕКТОРА КАНАЛА @neuro_tech2026</b>\n\n"
        f"📈 <b>Основные показатели:</b>\n"
        f"• Всего публикаций в базе: <b>{total_posts}</b>\n"
        f"• Топ-3 популярных темы: <b>{top_tags_str}</b>\n\n"
        f"🎯 <b>Рекомендации по раскрутке и монетизации:</b>\n"
        f"1. <b>Подготовка к продаже рекламы:</b> Канал активно наполняется уникальным контентом. Рекомендуем выходить на биржи Telega.in и TGStat при достижении 500+ подписчиков.\n"
        f"2. <b>Органический рост:</b> Сделайте 1-2 взаимопиара (ВП) с близкими по теме каналами 100-300 подписчиков.\n"
        f"3. <b>Контакт продавца:</b> В постах зафиксированы ваши контакты для рекламодателей: <b>@Maks61921</b>.\n\n"
        f"🚀 <i>ИИ-СММ Директор работает полностью автономно.</i>"
    )
    
    bot_token = config.TELEGRAM_BOT_TOKEN
    admin_id = config.TELEGRAM_ADMIN_CHAT_ID
    
    if not bot_token or not admin_id:
        print("Ошибка: Не задан токен бота или TELEGRAM_ADMIN_CHAT_ID.")
        return
        
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    proxies = {"http": config.os.getenv("TELEGRAM_PROXY_URL"), "https": config.os.getenv("TELEGRAM_PROXY_URL")} if config.os.getenv("TELEGRAM_PROXY_URL") else None
    
    try:
        res = requests.post(url, json={"chat_id": admin_id, "text": report_text, "parse_mode": "HTML"}, timeout=20, proxies=proxies)
        if res.status_code == 200:
            print("Еженедельный СММ-отчет успешно доставлен владельцу!")
        else:
            print(f"Ошибка доставки отчета: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Ошибка при отправке отчета: {e}")

if __name__ == "__main__":
    generate_and_send_weekly_report()
