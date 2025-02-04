from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def login_to_facebook(driver, email, password):
    driver.get("https://www.facebook.com/login")
    time.sleep(2)

    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, "pass")
    password_field.send_keys(password)

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    time.sleep(5)

def scrape_facebook_page(username, email=None, password=None):
    url = f"https://www.facebook.com/{username}"
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Comment this line for debugging
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        if email and password:
            login_to_facebook(driver, email, password)

        driver.get(url)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "meta[property='og:title']"))
        )

        # Extract page name and profile picture
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_name = soup.find("meta", property="og:title")["content"] if soup.find("meta", property="og:title") else None
        profile_pic = soup.find("meta", property="og:image")["content"] if soup.find("meta", property="og:image") else None

        # Extract follower count
        try:
            followers_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'followers') or contains(text(), 'Followers')]"))
            )
            followers_count = int(followers_element.text.replace(",", "").split()[0])
        except TimeoutException:
            print("Follower count element did not load within the timeout.")
            followers_count = None
        except NoSuchElementException:
            print("Follower count element not found.")
            followers_count = None

        page_data = {
            "username": username,
            "url": url,
            "page_name": page_name,
            "profile_pic": profile_pic,
            "followers_count": followers_count,
            "category": None,
            "email": None
        }
        
        return page_data
    
    finally:
        driver.quit()
scraped_data = scrape_facebook_page("boat.lifestyle", email="", password="")
print(scraped_data)