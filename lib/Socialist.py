import re, requests, os
from lib.Browser import Browser
from utils.functions import create_slug, get_file_extension_from_bytes

class Socialist (Browser):
    def __init__(self, pathDestination = "./results"):
        super().__init__()

        if not os.path.exists(pathDestination):
            os.makedirs(pathDestination)
        
        self.pathDestination = pathDestination
        self.validations = {
            "instagram": r"(https?:\/\/)?(www\.)?instagram\.com\/(.+)",
            "twitter": r"(https?:\/\/)?(www\.)?twitter\.com\/(.+)",
            "facebook": r"(https?:\/\/)?(www\.)?facebook\.com\/(.+)",
            "linkedin": r"(https?:\/\/)?(www\.)?linkedin\.com\/(.+)",
            "tiktok": r"(https?:\/\/)?(www\.)?tiktok\.com\/(.+)",
        }
    def get_platform(self, url):
        for platform, pattern in self.validations.items():
            print (platform, pattern)
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
                return "facebook.com"
    
    def download (self, url):
        media = self.get_media(url)

        try:
            byteContent = requests.get(media["url"]).content
            filename = create_slug(media["title"])
            extension = get_file_extension_from_bytes(byteContent)

            with open (f"{ self.pathDestination }/{filename}.{extension}", "wb") as file:
                file.write(byteContent)
                file.close()
            print (f"media saved to { self.pathDestination }/{filename}")
        except Exception as err:
            print (err)
            print (f"failed downloading media with url: { url }")