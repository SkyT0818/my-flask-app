from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # フォームデータの取得
    data = request.form
    checkin_date = data['checkin_date']
    checkout_date = data['checkout_date']
    name = data['name']
    email = data['email']
    phone = data['phone']
    
    # Seleniumの設定
    options = Options()
    options.add_argument('--headless')  # ヘッドレスモード
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service()  # Selenium Managerが自動的にドライバを設定
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # ブラウザ操作
        url = 'https://reserva.be/aiikuretreat/reserve?mode=htl&evt_no=f9eJwzNDOxMAIAAxABBg&plan_no=73eJyzMDcwBwACIADX&room_num=1&people=1.0.0.0'
        driver.get(url)

        # チェックイン日
        element = driver.find_element(By.ID, "checkin_view_str")
        element.click()
        time.sleep(1)
        # 日付選択（任意でXPathを調整）
        driver.find_element(By.XPATH, f"//*[text()='{checkin_date}']").click()

        # チェックアウト日
        driver.find_element(By.XPATH, f"//*[text()='{checkout_date}']").click()

        # 予約
        driver.find_element(By.XPATH, '//*[@id="htl_rsv_status"]/p').click()

        # フォーム入力
        driver.find_element(By.NAME, "mem_sai").send_keys(name)
        driver.find_element(By.NAME, "mem_id").send_keys(email)
        driver.find_element(By.NAME, "mem_tel").send_keys(phone)

        # 追加操作をここに記載...

        return "予約完了！"
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
