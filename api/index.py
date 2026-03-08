from flask import Flask, jsonify
import requests
import re
import pandas as pd
import os
import telebot

app = Flask(__name__)

# --- بياناتك ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
TARGET_URL = "https://1xlite-65342.top/en/allgamesentrance/crash"
bot = telebot.TeleBot(TOKEN)

# مسار الملف جوه مجلد api
current_dir = os.path.dirname(__file__)
CSV_FILE = os.path.join(current_dir, 'crash.csv')

@app.route('/')
def live_analysis():
    try:
        # 1. الدخول للموقع وسحب الرقم الحي (Live Odd)
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"}
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        
        live_odd = "0.0"
        if response.status_code == 200:
            find_odds = re.findall(r'(\d+\.\d+)x', response.text)
            if find_odds:
                live_odd = find_odds[0]

        # 2. قراءة الملف القديم للتحليل
        df = pd.read_csv(CSV_FILE, header=None)
        last_history = df.iloc[-1, 0] if not df.empty else "N/A"
        
        # 3. منطق التوقع (لو الأرقام الأخيرة واطية يبقى اللي جاي عالي)
        avg_recent = df.iloc[-5:, 0].mean() if len(df) >= 5 else 2.0
        prediction = "صعود 📈" if avg_recent < 1.8 else "هبوط 📉"

        # 4. إرسال التقرير النهائي
        msg = (
            f"🎯 **رادار اللعبة المباشر**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🕹️ الرقم الحالي في الموقع: `{live_odd}x`\n"
            f"📜 آخر رقم في الملف: `{last_history}x`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔮 التوقع للدور القادم: **{prediction}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📡 المصدر: سيرفر Vercel (USA)"
        )
        
        bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
        return jsonify({"status": "success", "live": live_odd, "predict": prediction})

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == "__main__":
    app.run()
    
