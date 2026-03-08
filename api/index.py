from flask import Flask, jsonify
import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# --- بياناتك ---
TOKEN = "7044109545:AAF_2u9_HqVGZzFIubnIWCQ3dFm7MyQfmWw"
CHAT_ID = "5773032750"
TARGET_URL = "https://eg-1xbet.com/en/games/crash"

bot = telebot.TeleBot(TOKEN)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    # هوية Chrome 139 اللي بعتها
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

@app.route('/')
def run_bot():
    try:
        driver = get_driver()
        driver.get(TARGET_URL)
        time.sleep(15) # انتظار التحميل في سيرفرات Vercel السريعة
        
        # محاولة سحب العداد
        counter = driver.find_elements(By.XPATH, "//*[contains(@class, 'counter-val')]")
        if counter:
            val = counter[0].text
            bot.send_message(CHAT_ID, f"🚀 تم السحب من Vercel: {val}")
            driver.quit()
            return jsonify({"status": "success", "value": val})
        
        driver.quit()
        return jsonify({"status": "failed", "reason": "counter not found"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run()
  
