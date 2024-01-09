from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
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
      "download.default_directory": "/mnt/backups/",
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

    driver.find_element("xpath", "//input[@name='username']").send_keys(USERNAME)
    driver.find_element("xpath", "//input[@name='password']").send_keys(PASSWORD)
    driver.find_element("xpath", "//input[@name='password']").submit()
    driver.get(f"{WEB_URL}/Tools/Diagnostics")
    time.sleep(5)
    driver.find_element("xpath", "//body").send_keys(Keys.END)
    time.sleep(5)
    driver.find_element("xpath", "//input[@value='Download']").click()
    time.sleep(60 * 5)
    driver.quit()

finally:
    if driver is not None:
        driver.quit()