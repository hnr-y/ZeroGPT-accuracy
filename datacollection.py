from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


# from selenium.webdriver.chrome.service import Service
def freeChatGPT(text):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9221")
    driver = webdriver.Chrome(options=chrome_options)
    # print(driver.window_handles)
    # exit()
    driver.switch_to.window("A88AF065B492DD8F50D8152262E5EB8E")
    # time.sleep(0.5)
    # driver.get('https://chatgpt.com')

    driver.find_element(By.CSS_SELECTOR, "textarea#prompt-textarea").send_keys(" ")

    driver.execute_script('document.querySelector("textarea#prompt-textarea").value = `' + text + '`')
    time.sleep(0.4)
    initial_messages = driver.find_elements(By.CSS_SELECTOR, "div.w-full.text-token-text-primary")
    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Send prompt"]').click()
    while True:
        try:
            initial = driver.find_elements(By.CSS_SELECTOR,
                                           'div[class="result-streaming markdown prose w-full break-words dark:prose-invert light"]')[
                -1].text
            break
        except:
            pass
    while True:
        try:
            initial = driver.find_elements(By.CSS_SELECTOR,
                                           'div[class="result-streaming markdown prose w-full break-words dark:prose-invert light"]')[
                -1].text
        except:
            break

    results = \
        driver.find_elements(By.CSS_SELECTOR, 'div[class="markdown prose w-full break-words dark:prose-invert light"')[
            -1].text
    return results


if __name__ == '__main__':
    while True:
        text = []
        for i in range(10):
            text.append(freeChatGPT("Write a 5 paragraph essay on crime and punishment"))
        data = {
            "text": text,
            "generated": ["1"] * 10
        }
        df = pd.DataFrame(data)
        df.to_csv('Labeled_Data.csv', mode='a', index=False, header=False)
        print("finished 10 entries")


