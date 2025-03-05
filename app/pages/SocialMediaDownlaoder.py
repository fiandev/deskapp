import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import json
import os
from lib.Socialist import Socialist

class SocialMediaDownloader(tk.Frame):
    PATH_HISTORY = "./.history"
    SAVED_HISTORY_FILENAME = "data.json"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        self.controller = controller
        self.sosialist = Socialist()
        
        # make history directories
        if not os.path.exists(self.PATH_HISTORY):
            os.makedirs(self.PATH_HISTORY)
        
        # Main container with padding
        main_container = tk.Frame(self, bg=controller.bg_color, padx=40, pady=30)
        main_container.pack(fill="both", expand=True)
        
        # Header section
        header_frame = tk.Frame(main_container, bg=controller.bg_color)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_font = tk.font.Font(family="Helvetica", size=20, weight="bold")
        title = tk.Label(header_frame, 
                text="Social Media Downloader", 
                font=title_font, bg=controller.bg_color, fg=controller.text_color)
        title.pack(anchor="w")
        
        subtitle_font = tk.font.Font(family="Helvetica", size=12)
        subtitle = tk.Label(header_frame, text="Paste a link to download content from social media", 
                font=subtitle_font, bg=controller.bg_color, fg=controller.text_color)
        subtitle.pack(anchor="w", pady=(5, 0))
        
        # URL input section
        input_frame = tk.Frame(main_container, bg=controller.bg_color, pady=15)
        input_frame.pack(fill="x")
        
        # Create a container for URL input and button (side by side)
        url_container = tk.Frame(input_frame, bg=controller.bg_color)
        url_container.pack(fill="x")
        
        # URL entry with modern styling
        self.url_var = tk.StringVar()
        url_entry = tk.Entry(url_container, textvariable=self.url_var, 
                            font=("Helvetica", 12), bg="white", fg="#333333",
                            relief="flat", highlightthickness=1, 
                            highlightbackground="#dddddd", highlightcolor=controller.button_color)
        url_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        
        # Download button
        download_button = tk.Button(url_container, text="Download", 
                            font=("Helvetica", 11, "bold"),
                            bg=controller.button_color, fg="white",
                            activebackground=controller.hover_color,
                            activeforeground="white", relief="flat",
                            padx=15, pady=8, command=self.start_download)
        download_button.pack(side="right")
        
        # Create a separator
        separator = ttk.Separator(main_container, orient="horizontal")
        separator.pack(fill="x", pady=20)
        
        # Results list section - title
        results_header = tk.Frame(main_container, bg=controller.bg_color)
        results_header.pack(fill="x", pady=(0, 10))
        
        results_title = tk.Label(results_header, text="Download History", 
                                font=("Helvetica", 14, "bold"),
                                bg=controller.bg_color, fg=controller.text_color)
        results_title.pack(anchor="w")
        
        # Create a scrollable frame for the download list
        self.list_container = tk.Frame(main_container, bg=controller.bg_color)
        self.list_container.pack(fill="both", expand=True)
        
        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self.list_container, bg=controller.bg_color, 
                                highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.list_container, orient="vertical", 
                                command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas to hold the items
        self.scroll_frame = tk.Frame(self.canvas, bg=controller.bg_color)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scroll_frame, 
                                                    anchor="nw")
        
        # Configure canvas to adjust with window resizing
        self.scroll_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Navigation button to go back to the main page
        back_frame = tk.Frame(main_container, bg=controller.bg_color, pady=10)
        back_frame.pack(fill="x")
        
        back_button = tk.Button(back_frame, text="Back to Main Menu", 
                                font=("Helvetica", 11),
                                bg="#f0f0f0", fg=controller.text_color,
                                activebackground="#e0e0e0",
                                activeforeground=controller.text_color, 
                                relief="flat", padx=10, pady=5,
                                command=lambda: controller.show_frame("HomePage"))
        back_button.pack(side="left")
        self.histories = self.load_history()
    
    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Resize the inner frame to match the canvas"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def start_download(self):
        """Simulate starting a download with the provided URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Input Required", "Please enter a valid URL")
            return
        
        # Create a new "downloading" item
        item_frame = self.create_download_item("Downloading...", url, None, "pending")
        
        # Clear the input field
        self.url_var.set("")
        
        # Simulate download process in a background thread
        threading.Thread(target=self.simulate_download, args=(item_frame, url)).start()
    
    def simulate_download(self, item_frame, url):
        """Simulate the download process"""
        # Simulate processing time
        time.sleep(2)
        
        media = self.sosialist.get_media(url)
        
        # Update the UI in the main thread
        self.after(0, lambda: self.update_download_item(item_frame, media, "complete"))
    
    def create_download_item(self, title, url, media, status):
        """Create a new download item in the list"""
        # Create a frame for the item
        item_frame = tk.Frame(self.scroll_frame, bg="white", padx=15, pady=15,
                                highlightbackground="#e0e0e0", highlightthickness=1)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Left side - video details
        details_frame = tk.Frame(item_frame, bg="white")
        details_frame.pack(side="left", fill="both", expand=True)
        
        # Title
        title_label = tk.Label(details_frame, text=title, font=("Helvetica", 12, "bold"),
                                bg="white", fg=self.controller.text_color, 
                                anchor="w")
        title_label.pack(fill="x", anchor="w")
        
        # URL (truncated if too long)
        url_display = url if len(url) < 50 else url[:47] + "..."
        url_label = tk.Label(details_frame, text=url_display, font=("Helvetica", 9),
                            bg="white", fg="#666666", anchor="w")
        url_label.pack(fill="x", anchor="w", pady=(3, 0))
        
        # Right side - download button
        button_frame = tk.Frame(item_frame, bg="white")
        button_frame.pack(side="right", padx=(10, 0))
        
        if status == "pending":
            download_button = tk.Label(button_frame, text="Processing...", 
                                font=("Helvetica", 10),
                                bg="#f0f0f0", fg="#666666",
                                padx=10, pady=5)
        else:
            download_button = tk.Button(button_frame, text="Download", 
                                font=("Helvetica", 10),
                                bg=self.controller.button_color, fg="white",
                                activebackground=self.controller.hover_color,
                                activeforeground="white", relief="flat",
                                padx=10, pady=5,
                                command=lambda: self.download_file(media))
        
        download_button.pack()
        
        # Store references to the updateable elements
        item_frame.title_label = title_label
        item_frame.download_button = download_button
        
        return item_frame
    
    def update_download_item(self, item_frame, media, status):
        """Update an existing download item with new information"""
        item_frame.title_label.config(text=media["filename"])
        
        if status == "complete":
            # Replace the processing label with an actual button
            item_frame.download_button.destroy()
            
            download_button = tk.Button(item_frame.download_button.master, text="Download", 
                                font=("Helvetica", 10),
                                bg=self.controller.button_color, fg="white",
                                activebackground=self.controller.hover_color,
                                activeforeground="white", relief="flat",
                                padx=10, pady=5,
                                command=lambda: self.download_file(media))
            download_button.pack()
            self.save_history(media)
            item_frame.download_button = download_button
    
    def download_file(self, media):
        """Simulate downloading the actual file"""
        messagebox.showinfo("Download Started", f"Downloading: {media["filename"]}")
        self.sosialist.download(media)
        messagebox.showinfo(media["filename"], "Download Finished")

    
    def generate_title(self, url):
        """Generate a random video title based on the URL"""
        platforms = {
            "youtube": ["Entertaining Video", "Tutorial", "Vlog", "Music Video", "Review"],
            "tiktok": ["Dance Challenge", "Comedy Skit", "Life Hack", "Funny Moment"],
            "instagram": ["Reel", "Story Highlight", "Photo Collection", "Short Clip"],
            "facebook": ["Live Video", "Shared Memory", "Group Video", "Event Recording"],
            "twitter": ["Viral Tweet Video", "Short Clip", "Sports Highlight"]
        }
        
        # Determine platform from URL
        platform = "other"
        for key in platforms.keys():
            if key in url.lower():
                platform = key
                break
        
        # Select random title elements
        adjectives = ["Amazing", "Funny", "Awesome", "Best", "Popular", "Viral", "Trending"]
        creators = ["Creator", "Channel", "User", "Influencer", "Artist"]
        
        if platform in platforms:
            content_type = random.choice(platforms[platform])
        else:
            content_type = "Video"
        
        adjective = random.choice(adjectives)
        creator = random.choice(creators)
        
        return f"{adjective} {content_type} by {platform.capitalize()} {creator}"
    
    def load_history (self):
        """Add some sample videos to the list for demonstration"""
        pathHistoryFile = f"{self.PATH_HISTORY}/{self.SAVED_HISTORY_FILENAME}"

        histories = [] if not os.path.exists(pathHistoryFile) else json.loads(open(pathHistoryFile, "r").read())
        
        for media in histories:
            media["filename"] = f"{ media["filename"][0:50] }{ '...' if len(media['filename']) > 50 else '' }"
            self.create_download_item(media["filename"], media["url"], media, "complete")
        
        return histories
    
    def save_history (self, media):
        pathHistoryFile = f"{self.PATH_HISTORY}/{self.SAVED_HISTORY_FILENAME}"

        self.histories.append(media)
        with open(pathHistoryFile, "w+") as file:
            file.write(json.dumps(self.histories))
            file.close()
        print (json.dumps(self.histories))
    
    # Add this new page to the pages being created in the App class
    def create_pages(self):
        # Create additional pages (modify this in your main App class)
        for page_class in [PageOne, PageTwo, PageThree, PageFour, SocialMediaDownloader]:
            page = page_class(parent=self.container, controller=self)
            self.frames[page_class.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

# Update your MainPage class to add a button for the downloader
# In the MainPage.__init__ method, update the pages list to add:
# ("Social Media Downloader", "Download content from social networks", "SocialMediaDownloader")