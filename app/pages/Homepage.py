import tkinter as tk
import tkinter.font as tkFont

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        self.controller = controller
        
        # Create a container for content
        content_frame = tk.Frame(self, bg=controller.bg_color, padx=40, pady=40)
        content_frame.pack(expand=True, fill="both")
        
        # Add a header/logo section
        header_frame = tk.Frame(content_frame, bg=controller.bg_color)
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(header_frame, text="Tkinter App", font=title_font, bg=controller.bg_color, fg=controller.text_color)
        title.pack()
        
        subtitle_font = tkFont.Font(family="Helvetica", size=14)
        subtitle = tk.Label(header_frame, text="Click menu to navigate", font=subtitle_font, bg=controller.bg_color, fg=controller.text_color)
        subtitle.pack(pady=(5, 0))
        
        # Create a frame for the LinktTree-style buttons
        button_container = tk.Frame(content_frame, bg=controller.bg_color)
        button_container.pack(expand=True, fill="both", padx=100)
        
        # List of page names and their descriptions
        pages = [
            ("Sosial Media Downloader", "universal downloder for social media", "SocialMediaDownloader"),
            ("Bitcoin Wallet", "a bitcoin self custody btc wallet", "BitcoinWalletPage"),
        ]
        
        # Create a button for each page
        for i, (title, desc, page) in enumerate(pages):
            self.create_button(button_container, title, desc, page, i)
    
    def create_button(self, container, title, description, page, index):
        # Create a frame for each button for better styling
        button_frame = tk.Frame(container, bg=self.controller.bg_color, pady=10)
        button_frame.pack(fill="x")
        
        # Create a modern-looking button with padding and rounded corners
        button = tk.Frame(button_frame, bg=self.controller.button_color, padx=20, pady=15)
        button.pack(fill="x")
        
        # Make the frame have a "button feel"
        def on_enter(e):
            button.config(bg=self.controller.hover_color)
            title_label.config(bg=self.controller.hover_color)
            desc_label.config(bg=self.controller.hover_color)
        
        def on_leave(e):
            button.config(bg=self.controller.button_color)
            title_label.config(bg=self.controller.button_color)
            desc_label.config(bg=self.controller.button_color)
        
        def on_click(e):
            self.controller.show_frame(page)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_click)
        
        # Title and description for the button
        title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        title_label = tk.Label(button, text=title, font=title_font, 
                                bg=self.controller.button_color, fg="white", 
                                anchor="w")
        title_label.pack(fill="x")
        
        desc_font = tkFont.Font(family="Helvetica", size=10)
        desc_label = tk.Label(button, text=description, font=desc_font, bg=self.controller.button_color, fg="white", anchor="w")
        desc_label.pack(fill="x")
        
        # Also bind the labels to the click event
        title_label.bind("<Button-1>", on_click)
        desc_label.bind("<Button-1>", on_click)
