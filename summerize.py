from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def fetch_active_tab_content():
    # Set up the Chrome WebDriver
    service = Service('path/to/chromedriver')  # Replace with the path to your ChromeDriver
    driver = webdriver.Chrome(service=service)

    # Open the browser and fetch the active tab URL
    driver.get("chrome://newtab/")  # Opens a new tab
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the most recent tab

    # Fetch the content of the active tab
    active_url = driver.current_url
    print(f"Active Tab URL: {active_url}")

    # Visit the active URL and fetch content
    driver.get(active_url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    text = ' '.join(p.text for p in soup.find_all("p"))

    # Summarize content
    if len(text) > 500:
        summary = text[:500] + "..."
    else:
        summary = text

    print("Summary:")
    print(summary)
    driver.quit()

fetch_active_tab_content()
