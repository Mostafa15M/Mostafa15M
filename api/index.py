from flask import Flask, jsonify
import pandas as pd
import os
import telebot

app = Flask(__name__)

# --- بياناتك ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
bot = telebot.TeleBot(TOKEN)

# تحديد مسار الملف في Vercel (الملف بجانب الكود في مجلد api)
current_dir = os.path.dirname(__file__)
CSV_FILE = os.path.join(current_dir, 'crash.csv')

def get_prediction(df):
    """معادلة بسيطة للتوقع بناءً على آخر التحركات"""
    if len(df) < 5:
        return "بيانات غير كافية للتوقع"
    
    # حساب المتوسط لآخر 5 أرقام
    recent_avg = df.iloc[-5:, 0].mean()
    
    # إذا كان المتوسط منخفض، التوقع يميل للزيادة والعكس (معادلة تقريبية)
    if recent_avg < 2.0:
        prediction = "متوقع صعود (فوق 2.00x)"
    else:
        prediction = "حذر: احتمال هبوط (تحت 1.50x)"
    return prediction

@app.route('/')
def run_analyzer():
    try:
        # 1. التأكد من وجود الملف
        if not os.path.exists(CSV_FILE):
            return jsonify({"status": "error", "msg": "ملف crash.csv غير موجود بجانب الكود"})

        # 2. قراءة ملف CSV
        # قراءة الملف بدون رؤوس أعمدة لأن بياناتك عبارة عن أرقام فقط
        df = pd.read_csv(CSV_FILE, header=None)
        
        if df.empty:
            return jsonify({"status": "empty", "msg": "الملف موجود لكنه فارغ"})

        # 3. استخراج آخر رقم وتوقعات
        last_odd = df.iloc[-1, 0]
        prediction = get_prediction(df)
        total_games = len(df)

        # 4. إرسال الرسالة لتليجرام
        message = (
            f"📊 **تحليل البيانات من Vercel**\n\n"
            f"✅ إجمالي الأدوار المسجلة: {total_games}\n"
            f"🚀 آخر رقم (Odd): {last_odd}x\n"
            f"🔮 {prediction}\n\n"
            f"🕒 تم التحديث من ملف crash.csv"
        )
        
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")

        return jsonify({
            "status": "success",
            "last_odd": float(last_odd),
            "prediction": prediction
        })

    except Exception as e:
        error_msg = f"❌ خطأ في السيرفر: {str(e)}"
        bot.send_message(CHAT_ID, error_msg)
        return jsonify({"status": "error", "details": str(e)})

if __name__ == "__main__":
    app.run()
