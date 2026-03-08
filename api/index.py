from flask import Flask, jsonify
import requests
import re
import os
import telebot

app = Flask(__name__)

# --- بياناتك ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
TARGET_URL = "https://1xlite-65342.top/en/allgamesentrance/crash"
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def scrape_html():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        }
        
        # سحب كود الـ HTML بالكامل من الموقع
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        html_content = response.text

        # 🔍 البحث عن الرقم اللي جنبه x (مثلاً 2.50x) في الـ HTML
        # جربنا أكتر من طريقة بحث (Regex) عشان نضمن الوصول للرقم
        find_odds = re.findall(r'(\d+\.\d+)x', html_content)
        
        if not find_odds:
            # محاولة تانية لو الرقم مكتوب بصيغة تانية في الـ HTML
            find_odds = re.findall(r'class="crash-game__coefficient">(\d+\.\d+)<\/div>', html_content)

        if find_odds:
            current_val = find_odds[0]
            bot.send_message(CHAT_ID, f"🎯 تم سحب الرقم من الـ HTML بنجاح: {current_val}x")
            return jsonify({"status": "success", "odd": current_val})
        else:
            # لو فشل، هيبعتلك جزء من الكود عشان نشوف الـ HTML فيه إيه
            bot.send_message(CHAT_ID, "⚠️ الكود شغال بس مش لاقي أرقام في الـ HTML حالياً")
            return jsonify({"status": "not_found", "html_sample": html_content[:200]})

    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ في السيرفر: {str(e)}")
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == "__main__":
    app.run()
