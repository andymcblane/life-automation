from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
import os 

driver = None

try:
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
    WEB_URL = os.environ["WEB_URL"]
    HUB_URL = os.environ["HUB_URL"]

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
      "download.default_directory": "/mnt/energy",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-crash-reporter")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('--disable-dev-shm-usage')        

    driver = webdriver.Remote(HUB_URL, options=chrome_options)

    driver.get(WEB_URL)


    driver.find_element_by_name("email").send_keys(USERNAME)
    driver.find_element_by_name("password").send_keys(PASSWORD)
    driver.find_element_by_name("password").submit()
    time.sleep(10)
    driver.get(f"{WEB_URL}/usage")
    time.sleep(5)
    download_button = driver.find_element(By.XPATH, '//span[text()="Download"]').click()
    time.sleep(30)
    driver.quit()
    # do some calc with the new file in /mnt/energy 

finally:
    if driver is not None:
        driver.quit()