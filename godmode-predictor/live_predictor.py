
import time
import json
from collections import deque
from statistics import mean, stdev
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
from ai_engine import load_model, predict_next

# ✅ Point pytesseract to the installed Tesseract OCR binary
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# ✅ Chrome setup for user Joe
options = Options()
options.binary_location = r"C:/Users/joe/bustabit-browser/chrome-win64/chrome.exe"
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1200,800')
options.add_argument('--log-level=3')

service = Service(r"C:/Users/joe/bustabit-browser/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.bustabit.com")
time.sleep(10)

multiplier_history = deque(maxlen=20)
LOW_THRESHOLD = 2.0

model = load_model()

def extract_multiplier_from_screen():
    try:
        image_bytes = driver.find_element(By.TAG_NAME, 'body').screenshot_as_png
        with open("screenshot.png", "wb") as f:
            f.write(image_bytes)

        img = Image.open("screenshot.png")
        ocr_text = pytesseract.image_to_string(img)

        for line in ocr_text.splitlines():
            line = line.strip()
            if line.endswith("x"):
                try:
                    return float(line[:-1])
                except:
                    continue
    except Exception as e:
        print("OCR error:", e)
    return None

def compute_features():
    recent_5 = list(multiplier_history)[-5:]
    recent_10 = list(multiplier_history)[-10:]

    avg_5 = mean(recent_5) if recent_5 else 0.0
    avg_10 = mean(recent_10) if recent_10 else 0.0
    std_10 = stdev(recent_10) if len(recent_10) > 1 else 0.0

    low_streak = 0
    for val in reversed(multiplier_history):
        if val < LOW_THRESHOLD:
            low_streak += 1
        else:
            break

    return {
        "last_multiplier": multiplier_history[-1] if multiplier_history else 0.0,
        "features": {
            "avg_5": avg_5,
            "avg_10": avg_10,
            "std_10": std_10,
            "low_streak": low_streak
        }
    }

def run():
    print("🤖 Predictor running live...")
    last_seen = None
    while True:
        multiplier = extract_multiplier_from_screen()
        if multiplier and multiplier != last_seen:
            last_seen = multiplier
            multiplier_history.append(multiplier)
            print(f"📉 Crash multiplier: {multiplier}")

            features = compute_features()
            with open("latest_data.json", "w") as f:
                json.dump(features, f)

            try:
                result, confidence = predict_next(features, model)
                print(f"📊 Prediction: {'✅ Safe' if result else '❌ Risk'} ({confidence:.1f}%)")
            except Exception as e:
                print(f"⚠️ Prediction error: {e}")
        time.sleep(2)

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("🛑 Exiting...")
    finally:
        driver.quit()
