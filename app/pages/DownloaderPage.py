from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk

class DownloaderPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ecf0f1")
        
        # Input Form
        self.entry_label = ttk.Label(self, text="Sosial Media Downlaoder")
        # self.entry_label.pack(pady=5)
        
        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(pady=5)
        
        self.submit_btn = ttk.Button(self, text="Submit", command=self.submit_action)
        self.submit_btn.pack(pady=5)
        
        # List of items with images
        self.list_frame = tk.Frame(self, bg="#ecf0f1")
        self.list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.populate_list()
    
    def submit_action(self):
        print("Submitted:", self.entry.get())
    
    def populate_list(self):
        items = [("image1.png", "Title 1"), ("image2.png", "Title 2"), ("image3.png", "Title 3")]
        
        for img_path, title in items:
            frame = tk.Frame(self.list_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
            frame.pack(pady=5, padx=10, fill=tk.X)
            
            # Load image placeholder (You should replace with actual image loading)
            img = Image.new('RGB', (50, 50), color='gray')
            img = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(frame, image=img, bg="#ffffff")
            img_label.image = img
            img_label.pack(side=tk.LEFT, padx=5, pady=5)
            
            title_label = ttk.Label(frame, text=title, font=("Arial", 12))
            title_label.pack(side=tk.LEFT, padx=10)
            
            download_btn = ttk.Button(frame, text="Download")
            download_btn.pack(side=tk.RIGHT, padx=10)
