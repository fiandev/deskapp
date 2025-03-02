import os, json
import tkinter as tk
from tkinter import ttk
from app.pages.DownloaderPage import DownloaderPage

class Desktop(tk.Tk):
    CACHE_PATH = "./.desktop-cache/"

    def __init__(self):
        super().__init__()
        self.title("Sosialist - Social Media Downloader")
        self.geometry("500x500")
        self.configure(bg="#2c3e50")
        self.cache = self.get_cache()

        if not os.path.exists(self.CACHE_PATH):
            os.makedirs(self.CACHE_PATH)
        
        # Style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 14), background="#2c3e50", foreground="white")
        
        # Container for pages
        self.container = tk.Frame(self, bg="#ecf0f1")
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.pages = {}
        for Page in (DownloaderPage, DownloaderPage):
            page = Page(self.container, self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        # Navigation bar
        self.navbar = tk.Frame(self, bg="#34495e")
        self.navbar.pack(side=tk.TOP, fill=tk.X)
        
        menu_items = [("Downloader", "DownloaderPage"), ("Profile", "ProfilePage"), ("Settings", "SettingsPage"), ("Help", "HelpPage"), ("Exit", None)]
        
        for item, page in menu_items:
            btn = ttk.Button(self.navbar, text=item, command=lambda p=page: self.show_page(p) if p else self.quit())
            btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.show_page("DownloaderPage")
    
    def get_cache(self):
        try:
            with open(self.CACHE_PATH + "cache.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

