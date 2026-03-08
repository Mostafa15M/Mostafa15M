from flask import Flask, jsonify
import requests
import re
import pandas as pd
import os
import telebot

app = Flask(__name__)

# --- بياناتك الشخصية ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
bot = telebot.TeleBot(TOKEN)

# رابط اللعبة المباشر (المصدر اللي هيحلل منه)
TARGET_URL = "https://1xlite-65342.top/en/allgamesentrance/crash"

# مسار الملف التاريخي (اللى انت رفعته)
current_dir = os.path.dirname(__file__)
CSV_FILE = os.path.join(current_dir, 'crash.csv')

@app.route('/')
def live_analysis():
    try:
        # 1. سحب الرقم الحي من موقع اللعبة
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"
        }
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        
        live_odd = "جاري السحب..."
        if response.status_code == 200:
            # البحث عن الرقم العشري (الأود) في كود الصفحة
            find_odds = re.findall(r'(\d+\.\d+)x', response.text)
            if find_odds:
                live_odd = find_odds[0]

        # 2. قراءة وتحليل ملف crash.csv
        df = pd.read_csv(CSV_FILE, header=None)
        
        # معادلة توقع بسيطة: لو آخر 3 أدوار في الملف واطيين، يتوقع صعود
        avg_last_3 = df.iloc[-3:, 0].mean() if len(df) >= 3 else 2.0
        prediction = "🔥 صعود متوقع (فوق 2.00x)" if avg_last_3 < 1.8 else "⚠️ حذر: هبوط محتمل"

        # 3. إرسال التقرير لتليجرام
        msg = (
            f"📡 **رادار التحليل المباشر**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🕹️ الرقم الحي الآن: `{live_odd}x`\n"
            f"📊 بناءً على ملفك (`{len(df)}` دور)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔮 التوقع القادم: **{prediction}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"✅ السيرفر يعمل بنجاح من Vercel"
        )
        
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        return jsonify({"status": "success", "live": live_odd, "prediction": prediction})

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == "__main__":
    app.run()
