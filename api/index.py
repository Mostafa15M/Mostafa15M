from flask import Flask, jsonify
import pandas as pd
import os
import telebot

app = Flask(__name__)

# --- بياناتك ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
bot = telebot.TeleBot(TOKEN)

# تحديد المسار الصحيح للملف جوه مجلد api في Vercel
# السطر ده بيعرف السيرفر إن الملف جنبه في نفس الفولدر
current_dir = os.path.dirname(__file__)
CSV_FILE = os.path.join(current_dir, 'crash.csv')

@app.route('/')
def analyze_data():
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({"status": "error", "msg": f"الملف مش موجود في المسار: {CSV_FILE}"})

        # قراءة آخر سطر من ملف الـ CSV (آخر أود ظهر)
        df = pd.read_csv(CSV_FILE)
        if df.empty:
            return jsonify({"status": "empty", "msg": "الملف فاضي يا درش"})

        # سحب آخر رقم (بفرض إن العمود الأول هو اللي فيه الأرقام)
        last_odd = df.iloc[-1, 0] 
        
        bot.send_message(CHAT_ID, f"✅ تم قراءة البيانات بنجاح!\n🚀 آخر أود في الملف هو: {last_odd}x")
        
        return jsonify({
            "status": "success",
            "last_odd": str(last_odd),
            "total_rows": len(df)
        })

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == "__main__":
    app.run()
    
