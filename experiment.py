import pandas as pd
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# from selenium.webdriver.chrome.service import Service

df = pd.read_csv('AI_Human.csv', chunksize=100)
# 0 = Human, 1 = AI
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")
driver = webdriver.Chrome(options=chrome_options)
driver.switch_to.window("ID Of The Chrome Tab")

# print(driver.window_handles)
# exit()

with pd.read_csv("AI_Human.csv", chunksize=100) as reader:
    for chunk in reader:
        ids = []
        confidence = []
        suspected = []
        for id, row in chunk.iterrows():
            ids.append(id)
            driver.execute_script('document.querySelector("textarea#textArea").value = arguments[0]', row.iloc[0])
            driver.find_element(By.CSS_SELECTOR, 'textarea#textArea').send_keys(" ")
            time.sleep(0.2)
            driver.find_element(By.CSS_SELECTOR, "button.scoreButton").click()


            while True:
                try:
                    confidence.append(
                        driver.find_element(By.CSS_SELECTOR, "div.percentage-div span").text.split("\n")[0])
                    break
                except:
                    pass
                time.sleep(0.2)
            highlights = driver.find_elements(By.CSS_SELECTOR, "mark.highlight")
            highlighted_text = []
            if highlights != []:
                for highlight in highlights:
                    highlighted_text.append(highlight.text)
            suspected.append(highlighted_text)
            # break
        data = {
            "id": ids,
            "zeroGPT confidence": confidence,
            "zeroGPT suspected sentences": suspected
        }
        df = pd.DataFrame(data)
        df.to_csv('data.csv', mode='a', index=False, header=False)
        # break
        print("just finished 100 entries")

# print(df.to_string())
