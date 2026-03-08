from flask import Flask, jsonify
import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

app = Flask(__name__)

# --- بياناتك الشخصية ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
# رابط البحث المباشر اللي بعته لتخطي الحجب
TARGET_URL = "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://eg-1xbet.com/en/games/crash&ved=2ahUKEwi8i7bUhZCTAxXBExAIHbGNAncQFnoECA4QAQ&sqi=2&usg=AOvVaw1bKgFmCJ2IxL3E2iVatmUO"

bot = telebot.TeleBot(TOKEN)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # تحسينات السرعة لبيئة السيرفر
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # هوية Chrome 139 الحديثة
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # تفعيل وضع التخفي (Stealth) للهروب من كشف البوتات
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

@app.route('/')
def run_radar():
    driver = None
    try:
        bot.send_message(CHAT_ID, "📡 جاري الفحص من سيرفر Vercel (وضع التخفي)..")
        driver = get_driver()
        driver.get(TARGET_URL)
        
        # انتظار التحميل (السيرفرات العالمية أسرع بكتير)
        time.sleep(20)
        
        # لقطة شاشة للتأكد من تخطي الشاشة الزرقاء
        driver.save_screenshot("vercel_check.png")
        with open("vercel_check.png", "rb") as f:
            bot.send_photo(CHAT_ID, f, caption="🖼️ لقطة من داخل السيرفر - تتبع الرابط")

        # محاولة سحب العداد
        counter = driver.find_elements(By.XPATH, "//*[contains(@class, 'counter-val')]")
        if counter:
            val = counter[0].text
            bot.send_message(CHAT_ID, f"🚀 اخترقنا الحجب! العداد الآن: {val}")
            return jsonify({"status": "success", "value": val})
        
        return jsonify({"status": "loading", "message": "الموقع فتح بس العداد لسه بيحمل"})
    
    except Exception as e:
        bot.send_message(CHAT_ID, f"❌ خطأ في السيرفر: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    app.run()
    
