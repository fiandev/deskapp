# import undetected_chromedriver as uc
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

from utils.env import env
from utils.functions import create_slug, try_catch

class Browser:
    INSTAGRAM_HOST_DOWNLOADER = "https://snapinst.app/"
    TIKTOK_HOST_DOWNLOADER = "https://snaptik.app/"
    FACEBOOK_HOST_DOWNLOADER = "https://fdownloader.net/"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--headless=true")
        options.add_argument('--disable-blink-features=AutomationControlled')

        self.options = options
        self.driver = None
    
    def instagram_downloader (self, url) -> dict:
        return self.downloader_executor(self.INSTAGRAM_HOST_DOWNLOADER, url, selectors={
            "INPUT_SELECTOR": "form[name='formurl'] #url",
            "MODAL_CLOSE_SELECTOR":"button#close-modal",
            "ADS_BOX_SELECTOR": "#ad_position_box #dismiss-button",
            "BUTTON_SUBMIT_SELECTOR": "form[name='formurl'] #btn-submit",
            "ANCHOR_DOWNLOAD_SELECTOR": ".download-bottom a",
        })
    
    def tiktok_downloader (self, url) -> dict:
        return self.downloader_executor(self.TIKTOK_HOST_DOWNLOADER, url, selectors={
            "INPUT_SELECTOR": "input#url",
            "MODAL_CLOSE_SELECTOR": ".modal-close",
            "ADS_BOX_SELECTOR": "#ad_position_box #dismiss-button",
            "BUTTON_SUBMIT_SELECTOR": "button[type='submit']",
            "ANCHOR_DOWNLOAD_SELECTOR": "a.button.download-file",
            "POST_TITLE_SELECTOR": ".info .video-title",
        })
    
    def facebook_downloader (self, url) -> dict:
        return self.downloader_executor(self.FACEBOOK_HOST_DOWNLOADER, url, selectors={
            "INPUT_SELECTOR": "input#s_input",
            "BUTTON_SUBMIT_SELECTOR": 'form button.btn-red',
            "ANCHOR_DOWNLOAD_SELECTOR": "a.download-link-fb",
        })
    
    def downloader_executor (self, host: str, url: str, selectors: dict) -> dict:
        """
        Executes the download process for a given media URL using a specified host and CSS selectors.

        This function automates the download procedure by interacting with a web interface using Selenium.
        It handles modal and ad closures, inputs the media URL, submits the form, and retrieves the download link.

        Args:
            host (str): The base URL of the downloader site.
            url (str): The media URL to be downloaded.
            selectors (dict): A dictionary containing CSS selectors for various elements:
                - "MODAL_CLOSE_SELECTOR": Selector to close any modal popups.
                - "ADS_BOX_SELECTOR": Selector to dismiss ad boxes.
                - "INPUT_SELECTOR": Selector for the input field to enter the media URL.
                - "BUTTON_SUBMIT_SELECTOR": Selector for the button to submit the form.
                - "ANCHOR_DOWNLOAD_SELECTOR": Selector to retrieve the download link.
                - "POST_TITLE_SELECTOR": Selector to retrieve the post title (optional).

        Returns:
            dict: A dictionary containing:
                - "url": The direct URL to the media file.
                - "timestamp": The timestamp of the download initiation.
                - "filename": The generated filename based on timestamp or post title.
        """
        MODAL_CLOSE_SELECTOR = selectors.get("MODAL_CLOSE_SELECTOR") or None
        ADS_BOX_SELECTOR = selectors.get("ADS_BOX_SELECTOR") or None
        INPUT_SELECTOR = selectors.get("INPUT_SELECTOR") or None
        BUTTON_SUBMIT_SELECTOR = selectors.get("BUTTON_SUBMIT_SELECTOR") or None
        ANCHOR_DOWNLOAD_SELECTOR = selectors.get("ANCHOR_DOWNLOAD_SELECTOR") or None
        POST_TITLE_SELECTOR = selectors.get("POST_TITLE_SELECTOR") or None
        
        filename = None
        timestamp = None
        mediaUrl = None

        self.driver = webdriver.Chrome(self.options)
        self.driver.get(host)

        while True:
            try:
                if MODAL_CLOSE_SELECTOR:
                    try_catch(lambda: self.driver.find_element(By.CSS_SELECTOR, MODAL_CLOSE_SELECTOR).click())
                if ADS_BOX_SELECTOR:
                    try_catch(lambda: self.driver.find_element(By.CSS_SELECTOR, ADS_BOX_SELECTOR).click())
                    
                self.driver.find_element(By.CSS_SELECTOR, INPUT_SELECTOR).send_keys(url)
                self.driver.find_element(By.CSS_SELECTOR, BUTTON_SUBMIT_SELECTOR).click()
                
                self.driver.implicitly_wait(20)

                timestamp = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                filename = timestamp if not POST_TITLE_SELECTOR else create_slug(self.driver.find_element(By.CSS_SELECTOR, POST_TITLE_SELECTOR).text)
                mediaUrl =  self.driver.find_element(By.CSS_SELECTOR, ANCHOR_DOWNLOAD_SELECTOR).get_attribute("href")

                self.driver.quit()
                break
            except Exception as err:
                print (f"[{ Browser.__class__.__name__ }]: { err }")
        return {
            "url": mediaUrl,
            "timestamp": timestamp,
            "filename": filename,
        }
