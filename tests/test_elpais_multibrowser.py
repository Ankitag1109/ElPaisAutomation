import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from pages.opinion_scraper import get_first_5_articles, scrape_articles
from utils.translator import translate_to_english
from utils.word_counter import count_words

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BROWSERS = [
    {"os": "Windows", "osVersion": "10", "browser": "Chrome", "browserVersion": "latest"},
    {"os": "Windows", "osVersion": "11", "browser": "Edge", "browserVersion": "latest"},
    {"os": "OS X", "osVersion": "Ventura", "browser": "Safari", "browserVersion": "16.5"},
    {"os": "iOS", "device": "iPhone 14", "realMobile": True, "browser": "Safari", "browserVersion": "latest"},
    {"os": "Android", "device": "Samsung Galaxy S22", "realMobile": True, "browser": "Chrome", "browserVersion": "latest"},
]

def get_driver(cap):
    USERNAME = os.getenv("BROWSERSTACK_USERNAME")
    ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

    if not USERNAME or not ACCESS_KEY:
        raise ValueError("BrowserStack credentials are missing in .env file!")

    options = Options()

 
    bstack_options = {
        "sessionName": "ElPais MultiBrowser",
        "buildName": "Selenium Assignment - Ankita",
        "userName": USERNAME,
        "accessKey": ACCESS_KEY
    }

    if "device" not in cap:
        options.set_capability("browserName", cap["browser"])
        options.set_capability("browserVersion", cap["browserVersion"])
        bstack_options["os"] = cap["os"]
        bstack_options["osVersion"] = cap["osVersion"]


    else:
        bstack_options["deviceName"] = cap["device"]
        bstack_options["realMobile"] = True
        options.set_capability("browserName", cap["browser"])
        options.set_capability("browserVersion", cap.get("browserVersion", "latest"))
        bstack_options["os"] = cap["os"]

    options.set_capability("bstack:options", bstack_options)

    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=options
    )
    driver.implicitly_wait(10)
    return driver


def test_multibrowser_with_prints():
    for cap in BROWSERS:
        print("\n==============================")
        browser_name = cap.get("browser") or cap.get("device", "Unknown")
        os_info = f"{cap.get('os')} {cap.get('osVersion', '')}".strip()
        device_info = cap.get("device", "")
        if device_info:
            os_info += f" ({device_info})"
        print(f"Running on: {browser_name} | {os_info}")
        print("==============================")

        driver = get_driver(cap)
        try:
            driver.get("https://elpais.com/opinion/")
            time.sleep(3)

            links = get_first_5_articles(driver)
            print("\nFirst 5 Article Links:")
            for link in links:
                print(link)

            articles = scrape_articles(driver, links)

            for i, article in enumerate(articles, 1):
                print(f"\nArticle {i}")
                print("TITLE:", article["title"])
                print("CONTENT LENGTH:", len(article["content"]))

            titles = [a["title"] for a in articles]

            print("\nSpanish Titles:")
            for t in titles:
                print(t)

            print("\nTranslated Titles:")
            translated_titles = [translate_to_english(t) for t in titles]
            for eng in translated_titles:
                print(eng)

            print("\nRepeated Words:\n")
            count_words(translated_titles)

        finally:
            driver.quit()
