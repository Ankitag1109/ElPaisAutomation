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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

def get_driver():
    USERNAME = os.getenv("BROWSERSTACK_USERNAME")
    ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

    if not USERNAME or not ACCESS_KEY:
        raise Exception("BrowserStack credentials not found in .env")

    options = Options()
    options.set_capability("browserName", "Chrome")
    options.set_capability("browserVersion", "latest")
    options.set_capability("bstack:options", {
        "os": "Windows",
        "osVersion": "11",
        "sessionName": "ElPais Tests",
        "userName": USERNAME,
        "accessKey": ACCESS_KEY
    })

    driver = webdriver.Remote(
        command_executor="https://hub.browserstack.com/wd/hub",
        options=options
    )

    return driver


def close_popups(driver):
    """Close cookie banners or overlays if present."""
    wait = WebDriverWait(driver, 5)
    try:
        # Example: cookie banner inside iframe
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe")))
        accept = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        driver.execute_script("arguments[0].click();", accept)
        driver.switch_to.default_content()
    except TimeoutException:
        driver.switch_to.default_content()
    except Exception:
        driver.switch_to.default_content()


def safe_click(driver, element):
    """Click element safely, scroll into view if needed."""
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", element)


def test_open_website():
    driver = get_driver()
    driver.get("https://elpais.com/")
    driver.set_window_size(1920, 1080)

    assert "EL PAÍS" in driver.title
    driver.quit()


def test_open_opinion():
    driver = get_driver()
    driver.get("https://elpais.com/opinion/")
    driver.set_window_size(1920, 1080)

    close_popups(driver)
    time.sleep(1)

    assert "opinion" in driver.current_url.lower()
    driver.quit()


def test_get_first_5_articles():
    driver = get_driver()
    driver.get("https://elpais.com/opinion/")
    driver.set_window_size(1920, 1080)

    close_popups(driver)
    time.sleep(1)

    links = get_first_5_articles(driver)

    assert len(links) == 5

    print("\nFirst 5 Article Links:")
    for link in links:
        print(link)

    driver.quit()


def test_scrape_articles():
    driver = get_driver()
    driver.get("https://elpais.com/opinion/")
    driver.set_window_size(1920, 1080)

    close_popups(driver)
    time.sleep(1)

    links = get_first_5_articles(driver)
    articles = scrape_articles(driver, links)

    assert len(articles) == 5
    driver.quit()


def test_translate_and_count():
    driver = get_driver()
    driver.get("https://elpais.com/opinion/")
    driver.set_window_size(1920, 1080)

    close_popups(driver)
    time.sleep(1)

    links = get_first_5_articles(driver)
    articles = scrape_articles(driver, links)

    titles = [a["title"] for a in articles]

    print("\nTranslated Titles:")
    translated_titles = []

    for t in titles:
        eng = translate_to_english(t)
        translated_titles.append(eng)
        print(eng)

    count_words(translated_titles)
    driver.quit()
