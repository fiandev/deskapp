import os, json
import tkinter as tk
from tkinter import ttk
from app.pages.DownloaderPage import DownloaderPage
from app.pages.Homepage import HomePage
from app.pages.SocialMediaDownlaoder import SocialMediaDownloader


class Desktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modern Desktop App")
        self.geometry("800x600")
        self.minsize(600, 500)
        
        # Configure a modern style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f5f5f7"
        self.button_color = "#4a7feb"
        self.hover_color = "#3867d6"
        self.text_color = "#333333"
        
        self.configure(bg=self.bg_color)
        
        # Set up navigation container to hold different pages
        self.container = tk.Frame(self, bg=self.bg_color)
        self.container.pack(fill="both", expand=True)
        
        # Dictionary to store the different frames/pages
        self.frames = {}
        
        # Create and add the main page
        self.create_main_page()
        
        # Create and add additional pages
        self.create_pages()
        
        # Show the main page first
        self.show_frame("HomePage")
    
    def create_main_page(self):
        # Create the main page frame
        main_page = HomePage(parent=self.container, controller=self)
        self.frames["HomePage"] = main_page
        main_page.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
    def create_pages(self):
        # Create additional pages
        for page_class in [DownloaderPage, SocialMediaDownloader]:
            page = page_class(parent=self.container, controller=self)
            self.frames[page_class.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")
    
    def show_frame(self, page_name):
        # Show the specified frame and hide the others
        frame = self.frames[page_name]
        frame.tkraise()
