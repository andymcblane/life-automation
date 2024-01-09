from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time 
import os 
import csv
from datetime import datetime, timedelta
from glob import glob

driver = None

try:
    USERNAME = os.environ["USERNAME"]
    PASSWORD = os.environ["PASSWORD"]
    WEB_URL = os.environ["WEB_URL"]
    HUB_URL = os.environ["HUB_URL"]

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
      "download.default_directory": "/mnt/energy/",
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
    time.sleep(10)
    driver.find_element(By.NAME, "email").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "password").submit()
    time.sleep(10)
    driver.get(f"{WEB_URL}/usage")
    time.sleep(5)
    download_button = driver.find_element(By.XPATH, '//span[text()="Download"]').click()
    time.sleep(30)
    driver.quit()


    # Configurable values
    cost_per_kwh = 0.37488 # Cost per kWh
    tariff_hours = range(11, 14)  # Tariff hours (11am-2pm)

    # Function to calculate cost based on tariff
    def calculate_cost(consumption, timestamp):
        hour = timestamp.hour
        if hour in tariff_hours:
            return 0
        else:
            return consumption * cost_per_kwh

    # Directory containing downloaded files
    download_directory = "/mnt/energy/"

    # Find the most recently modified CSV file in the specified directory
    csv_file_path = max(glob(os.path.join(download_directory, "*.csv")), key=os.path.getmtime)

    # Read CSV file
    with open(csv_file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Filter out "E2" records
        filtered_records = [record for record in reader if record["Register"] != "E2"]

        # Calculate energy usage for the previous two days
        today = datetime.now().date()
        two_days_ago = today - timedelta(days=2)

        costs = {two_days_ago: 0, two_days_ago + timedelta(days=1): 0}
        usages = {two_days_ago: 0, two_days_ago + timedelta(days=1): 0}

        for record in filtered_records:
            record_date = datetime.strptime(record["ReadDate"], "%Y/%m/%d").date()

            if two_days_ago <= record_date <= today:
                consumption = float(record["ReadConsumption"])
                timestamp = datetime.strptime(record["ReadTime"], "%H:%M:%S")
                cost = calculate_cost(consumption, timestamp)

                costs[record_date] += cost
                usages[record_date] += consumption

        for day, cost in costs.items():
            print(f"Day: {day}, Usage: {usages[day]:.5f} kWh, Cost: ${cost:.2f}")


finally:
    if driver is not None:
        driver.quit()