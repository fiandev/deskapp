# import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType


class Browser:
    INSTAGRAM_HOST_DOWNLOADER = "https://snapinst.app/"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')

        self.options = options
        self.driver = None
    
    def instagram_downloader (self, url) -> dict:
        
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.INSTAGRAM_HOST_DOWNLOADER)
        
        WebDriverWait(self.driver, timeout=3000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "form[name='formurl'] #url")))
        
        self.driver.find_element(By.CSS_SELECTOR, "form[name='formurl'] #url").send_keys(url)
        self.driver.find_element(By.CSS_SELECTOR, "form[name='formurl'] #btn-submit").click()

        WebDriverWait(self.driver, timeout=3000).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button#close-modal"))).click
        WebDriverWait(self.driver, timeout=3000).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".download-bottom a")))
        
        mediaUrl = self.driver.find_element(By.CSS_SELECTOR, ".download-bottom a").get_attribute("href")
        
        return {
            "url": mediaUrl,
            "title": time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),
        }