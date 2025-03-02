# import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

from utils.functions import create_slug, try_catch

class Browser:
    INSTAGRAM_HOST_DOWNLOADER = "https://snapinst.app/"
    TIKTOK_HOST_DOWNLOADER = "https://snaptik.app/"

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
            "filaname": time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),
        }
    
    def tiktok_downloader (self, url) -> dict:
        MODAL_CLOSE_SELECTOR = ".modal-close"
        ADS_BOX_SELECTOR = "#ad_position_box #dismiss-button"
        INPUT_SELECTOR = "input#url"
        BUTTON_SUBMIT_SELECTOR = "button[type='submit']"
        ANCHOR_DOWNLOAD_SELECTOR = "a.button.download-file"
        POST_TITLE_SELECTOR = ".info .video-title"

        mediaUrl = None
        filename = None

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.TIKTOK_HOST_DOWNLOADER)

        while True:
            try:
                try_catch(lambda: self.driver.find_element(By.CSS_SELECTOR, MODAL_CLOSE_SELECTOR).click())
                try_catch(lambda: self.driver.find_element(By.CSS_SELECTOR, ADS_BOX_SELECTOR).click())

                self.driver.find_element(By.CSS_SELECTOR, INPUT_SELECTOR).send_keys(url)
                self.driver.find_element(By.CSS_SELECTOR, BUTTON_SUBMIT_SELECTOR).click()
                
                self.driver.implicitly_wait(3)

                mediaUrl = self.driver.find_element(By.CSS_SELECTOR, ANCHOR_DOWNLOAD_SELECTOR).get_attribute("href")
                filename = create_slug(self.driver.find_element(By.CSS_SELECTOR, POST_TITLE_SELECTOR).text)
                self.driver.quit()
                break
            except Exception as err:
                print (f"[{ Browser.__class__.__name__ }]: { err }")
        return {
            "url": mediaUrl,
            "filename": filename
        }