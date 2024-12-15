import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "D:\codeFolder\PythonCodeForMore\Game_coockie_Clicker\chrome/chromedriver.exe"
serve = Service(chrome_driver_path)
driver = webdriver.Chrome(service=serve)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Cookie link
cookie = driver.find_element(By.ID, "cookie")

# Get store items and their ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5 minutes

while True:
    cookie.click()

    if time.time() > timeout:
        # Get all upgrade <b> tags using CSS_SELECTOR (not ID)
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                try:
                    cost = int(element_text.split("-")[1].strip().replace(",", ""))
                    item_prices.append(cost)
                except ValueError:
                    continue  # Skip if conversion fails

        # Create dictionary of store items and prices
        cookie_upgrades = {item_prices[n]: item_ids[n] for n in range(len(item_prices))}
        
        # Get current money
        cmoney = driver.find_element(By.CSS_SELECTOR, "#money").text
        try:
            current_money = int(cmoney.replace(",", ""))  # Removing commas
        except ValueError:
            current_money = 0  # Default if conversion fails

        # Find upgrades that can be afforded
        affordable_upgrades = {cost: id for cost, id in cookie_upgrades.items() if current_money >= cost}

        if affordable_upgrades:
            # Purchase the most expensive affordable upgrade
            highest_price_affordable_upgrade = max(affordable_upgrades)
            print(f"Purchasing upgrade with price: {highest_price_affordable_upgrade}")
            to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
            driver.find_element(By.ID, to_purchase_id).click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes, stop the bot and check the cookies per second count
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(f"Cookies per second: {cookie_per_s}")
        break

# driver.quit()  # Uncomment to quit the driver when the loop ends
