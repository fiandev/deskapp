import re, requests, os, sys
from lib.Browser import Browser
from utils.functions import get_file_extension_from_bytes
from utils.env import env

class Socialist (Browser):
    def __init__(self, pathDestination = "./results"):
        """
        Initialize a new instance of the Socialist class.

        The pathDestination parameter defaults to "./results", and is used to specify the directory
        where the downloaded media will be saved.

        The validations dictionary contains regular expressions that match URLs from various social media
        platforms. The keys of the dictionary are the names of the platforms, and the values are the regular
        expressions that match URLs from those platforms.
        """
        super().__init__()

        if not os.path.exists(pathDestination):
            os.makedirs(pathDestination)
        
        self.pathDestination = pathDestination
        self.validations = {
            "instagram": r"(https?:\/\/)?(www\.)?instagram\.com\/(.+)",
            "twitter": r"(https?:\/\/)?(www\.)?twitter\.com\/(.+)",
            "facebook": r"(https?:\/\/)?(www\.)?facebook\.com\/(.+)",
            "linkedin": r"(https?:\/\/)?(www\.)?linkedin\.com\/(.+)",
            "tiktok": r"(https?:\/\/)?(vt|www)?\.?tiktok\.com\/(.+)",
        }
    def get_platform(self, url):
        for platform, pattern in self.validations.items():
            if re.match(pattern, url):
                return platform
    
    def get_media (self, url):
        platform = self.get_platform(url)
        
        match platform:
            case "instagram":
                return self.instagram_downloader(url)
            case "twitter":
                return "twitter.com"
            case "facebook":
                return self.facebook_downloader(url)
            case "tiktok":
                return self.tiktok_downloader(url)
    
    def download (self, media):
        try:
            response = requests.get(media["url"], stream=True)
            byteContent = response.content
            filename = media["filename"][0:12]
            extension = get_file_extension_from_bytes(byteContent)
            totalSize = int(response.headers.get("content-length"))
            
            with open(f"{self.pathDestination}/{filename}.{extension}", "wb") as file:
                # Initialize progress bar variables
                chunk_size = 1024  # 1 KB per chunk
                downloaded_size = 0

                print(f"Downloading {filename}.{extension}...")

                # Download the file in chunks and show the progress
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Calculate progress percentage
                        percent = (downloaded_size / totalSize) * 100

                        # Print the progress bar
                        bar = '=' * int(percent // 2)  # 50 characters width bar
                        spaces = ' ' * (50 - len(bar))
                        sys.stdout.write(f"\r[{bar}{spaces}] {percent:.2f}%")
                        sys.stdout.flush()

                print(f"\nDownload complete: {self.pathDestination}/{filename}.{extension}")
            print (f"media saved to { self.pathDestination }/{filename}")
        except Exception as err:
            if not env("APP_ENV") == "production":
                print (f"[{ self.__class__.__name__ }] failed downloading media with url: { media['url'] }")
                raise err