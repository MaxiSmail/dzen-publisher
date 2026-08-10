import sys
import os
import config
import image_gen
import publisher

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def publish_lead_magnet_post():
    print("=" * 60)
    print("ПУБЛИКАЦИЯ ЗАКРЕПЛЕННОГО ЛИД-МАГНИТА ДЛЯ РОСТА ПОДПИСКОВ")
    print("=" * 60)
    
    lead_magnet_text = (
        "🎁 <b>ПОДАРОК ДЛЯ ПОДПИСЧИКОВ КАНАЛА: БАЗА 50 ЛУЧШИХ ПРОМПТОВ 2026 ГОДА</b>\n\n"
        "Мы собрали эксклюзивный набор готовых шаблонов запросов для ChatGPT, Midjourney и Gemini, которые экономят по 15+ часов работы в неделю:\n\n"
        "🔹 <b>Бизнес и Продажи:</b> Промпты для анализа конкурентов, написания КП и генерации идей стартапов.\n"
        "🔹 <b>Дизайн и Медиа:</b> Готовые стилевые промпты для 3D-фоторендер генерации без ватермарок.\n"
        "🔹 <b>Программирование и ИИ:</b> Запросы для рефакторинга кода, написания скриптов и поиска багов.\n\n"
        "👇 <b>Как использовать:</b>\n"
        "Сохраните этот пост в 'Избранное', используйте шаблоны в ежедневной работе и делитесь с коллегами!\n\n"
        "📩 <b>Реклама и сотрудничество:</b> @Maks61921\n"
        "🚀 Подписывайтесь на <a href=\"https://t.me/neuro_tech2026\">НейроСети 2026</a>!"
    )
    
    prompt = "A glowing golden gift box floating in a futuristic digital cyber space, surrounded by holographic code particles, 3d render, cinematic lighting, 8k resolution"
    
    print("Генерация обложки для Лид-Магнита...")
    image_path = image_gen.generate_image(prompt)
    
    print("Отправка Лид-Магнита в Telegram-канал...")
    success = publisher.publish_to_telegram(lead_magnet_text, image_path)
    
    if success:
        print("Лид-Магнит успешно опубликован! Зайдите в канал и ЗАКРЕПИТЕ этот пост.")
    else:
        print("Ошибка публикации Лид-Магнита.")

if __name__ == "__main__":
    publish_lead_magnet_post()
