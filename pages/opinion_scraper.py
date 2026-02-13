import os
import requests
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def accept_cookies_if_present(driver):
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe")))
    except:
        pass
    try:
        accept_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Aceptar')]"))
        )
        accept_btn.click()
        driver.switch_to.default_content()
    except:
        driver.switch_to.default_content()
        pass

def get_first_5_articles(driver):
    wait = WebDriverWait(driver, 15)
    if "opinion" not in driver.current_url.lower():
        driver.get("https://elpais.com/")
        accept_cookies_if_present(driver)

        opinion = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'opinion')]"))
        )
        opinion.click()

        wait.until(EC.url_contains("opinion"))
    articles = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//article//h2/a"))
    )
    links = []
    for a in articles[:5]:
        link = a.get_attribute("href")
        if link:
            links.append(link)
    return links

def scrape_articles(driver, links):
    data = []
    if not os.path.exists("images"):
        os.makedirs("images")

    for i, link in enumerate(links):
        driver.get(link)
        time.sleep(3)
        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
        except:
            title = "No title found"
        try:
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            content = " ".join([p.text for p in paragraphs])
        except:
            content = "No content found"

        image_url = None
        try:
            image = driver.find_element(By.XPATH, "//figure//img")
            image_url = image.get_attribute("src")

            if image_url:
                img_data = requests.get(image_url, timeout=10).content
                with open(f"images/article_{i+1}.jpg", "wb") as f:
                    f.write(img_data)
        except:
            pass

        data.append({
            "title": title,
            "content": content,
            "image": image_url
        })

        print(f"\nArticle {i+1}")
        print("TITLE:", title)
        print("CONTENT LENGTH:", len(content))

    return data
