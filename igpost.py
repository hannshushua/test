from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pickle
import os

#Aimer is love~

url = input(">>Type your link : ")

#設定使用者的位置
home = os.path.expanduser('~')

#定位下載的位置
download = os.path.join(home, 'Downloads')
foldername = input(">>Choose a folder : ")

#最後把C:\使用者\下載\filename 串起來
save_folder = os.path.join(download, foldername)

#沒有這個名稱的資料夾就創一個
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

#若無cookie紀錄 第一次就要使用帳號密碼都入IG
USERNAME = ''
PASSWORD = ''

# 初始化 webdriver
options = Options()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging']) #把多餘的log關掉
driver = webdriver.Chrome(options=options)


#先處理登入問題
try:
    driver.get('https://www.instagram.com/')
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    print("🍪 用 Cookie 登入")
except Exception as e:
    print("⚠️ Cookie 無效，執行帳密登入")
    driver.get('https://www.instagram.com/accounts/login/')

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.NAME, 'username')))

    username_input = driver.find_element(By.NAME, 'username')
    for char in USERNAME:
        username_input.send_keys(char)
        time.sleep(0.1)

    password_input = driver.find_element(By.NAME, 'password')
    for char in PASSWORD:
        password_input.send_keys(char)
        time.sleep(0.1)

    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    print('✅ 已送出登入')

    time.sleep(5)
    # 登入成功後儲存 cookies
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    print("✅ 已儲存新 Cookie")

driver.get(url)
wait = WebDriverWait(driver, 3)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aagv img, div._aagv video')))

file_count = len(os.listdir(save_folder))
img_count = file_count + 1

#判斷是否為多圖
next_btns = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="下一步"]')
is_multi = len(next_btns) > 0

totalcount = 1

#多圖
if is_multi:
    while True:
        try:
            #看有沒有下一步按鈕
            next_btns = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="下一步"]')
            if not next_btns:
                break
            # 抓圖片或跳過影片
            
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aagv img, div._aagv video')))

            ul_element = driver.find_element(By.CSS_SELECTOR, 'ul._acay')
            lis = ul_element.find_elements(By.TAG_NAME, 'li')
            

            if img_count - file_count == 1:
                current_li = lis[-1 - 1]
            else:
                current_li = lis[-1]

            #檢查是否有影片
            is_video = False
            try:
                current_li.find_element(By.CSS_SELECTOR, 'video')
                is_video = True
            except:
                is_video = False

            if is_video:
                print(f"❌ 第 {img_count} 項是影片，已跳過")
            else:
                img_src = current_li.find_element(By.CSS_SELECTOR, 'img')
                img_url = img_src.get_attribute('src')

                img_data = requests.get(img_url).content
                img_filename = f"pic{img_count}.jpg"
                filepath = os.path.join(save_folder, img_filename)

                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"✅ 第 {img_count} 張照片已下載好!")

            
            next_btns[0].click()
            img_count += 1
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._aagv img, div._aagv video')))

        except Exception as e:
            break
        
        time.sleep(0.5)

#只有一張照片
else:
    try:
        current_li = driver.find_element(By.CSS_SELECTOR, 'div._aagv')
        img_src = current_li.find_element(By.CSS_SELECTOR, 'img')
        img_url = img_src.get_attribute('src')

        img_data = requests.get(img_url).content
        img_filename = f"pic{img_count}.jpg"
        filepath = os.path.join(save_folder, img_filename)

        with open(filepath, 'wb') as f:
            f.write(img_data)
        print(f"✅ 第 {img_count} 張照片已下載好!")
        first = True
    except Exception as e:
        print(f"❌ 無法下載圖片：{e}")

print('Finish~')

# time.sleep(3)
driver.quit() 
