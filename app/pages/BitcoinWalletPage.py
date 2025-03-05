import tkinter as tk
from tkinter import ttk, messagebox
from bitcoinrpc.authproxy import AuthServiceProxy
from utils.env import env
import requests
import threading
import tarfile
import os
import shutil
import platform
from constants.paths import THIRD_PARTY_PROGRAM_PATH, DOWNLOAD_PATH

BTC_CORE_VERSION = "bitcoin-25.0"
BTC_CORE_FILENAME = f"{BTC_CORE_VERSION}.tar.gz"
BTC_CORE_DOWNLOAD_PATH = f"{DOWNLOAD_PATH}/{BTC_CORE_FILENAME}"
BTC_CORE_INSTALLATION_PATH = f"{THIRD_PARTY_PROGRAM_PATH}/{BTC_CORE_VERSION}"
BTC_CORE_URL = f"https://bitcoincore.org/bin/{BTC_CORE_VERSION}/{BTC_CORE_VERSION}-x86_64-linux-gnu.tar.gz"  # Change to the latest version


class BitcoinWalletPage(tk.Frame):
    def __init__(self, parent, controller):
        # Initialize the parent class
        tk.Frame.__init__(self, parent, bg=controller.bg_color)
        self.controller = controller

        # Main container
        main_container = tk.Frame(self, bg=controller.bg_color, padx=40, pady=30)
        main_container.pack(fill="both", expand=True)

        # Header
        header_frame = tk.Frame(main_container, bg=controller.bg_color)
        header_frame.pack(fill="x", pady=(0, 20))

        title_font = tk.font.Font(family="Helvetica", size=20, weight="bold")
        title = tk.Label(header_frame, text="Bitcoin Wallet", font=title_font, 
                            bg=controller.bg_color, fg=controller.text_color)
        title.pack(anchor="w")

        subtitle_font = tk.font.Font(family="Helvetica", size=12)
        subtitle = tk.Label(header_frame, text="Check and install Bitcoin Core", 
                            font=subtitle_font, bg=controller.bg_color, fg=controller.text_color)
        subtitle.pack(anchor="w", pady=(5, 0))

        # Download section
        download_frame = tk.Frame(main_container, bg=controller.bg_color, pady=15)
        download_frame.pack(fill="x")

        # Download button
        if not self.is_btc_installed():
            download_button = tk.Button(download_frame, text="Check & Download Bitcoin Core", 
                                font=("Helvetica", 11, "bold"),
                                bg=controller.button_color, fg="white",
                                activebackground=controller.hover_color,
                                activeforeground="white", relief="flat",
                                padx=15, pady=8, command=self.download_btc_core)
            download_button.pack()
        
        # Install path display
        path_label = tk.Label(main_container, text="Installation Path:", 
                            font=("Helvetica", 12, "bold"),
                            bg=controller.bg_color, fg=controller.text_color)
        path_label.pack(anchor="w")

        self.install_path_var = tk.StringVar(value=BTC_CORE_INSTALLATION_PATH)
        install_path_display = tk.Label(main_container, textvariable=self.install_path_var, 
                            font=("Helvetica", 11), bg=controller.bg_color, fg="#666")
        install_path_display.pack(anchor="w", pady=(0, 10))

        # Separator
        separator = ttk.Separator(main_container, orient="horizontal")
        separator.pack(fill="x", pady=20)

        # initlize rpc connection
        self.rpcUrl = f"http://{env('BTC_RPC_USER')}:{env('BTC_RPC_PASSWORD')}@127.0.0.1:8332"
        self.rpc = self.connect_to_rpc(self.rpcUrl)

        # list wallets
        self.wallets = self.rpc.listwallets()
        self.wallets_frame = tk.Frame(main_container, bg=controller.bg_color, pady=10)
        self.wallets_frame.pack(fill="x")
        self.wallets_label = tk.Label(self.wallets_frame, text="Wallets:", 
                            font=("Helvetica", 12, "bold"),
                            bg=controller.bg_color, fg=controller.text_color)
        self.wallets_label.pack(anchor="w")

        self.load_wallets()

        # button add wallet
        add_wallet_button = tk.Button(self.wallets_frame, text="Add Wallet", 
                            font=("Helvetica", 11),
                            bg="#f0f0f0", fg=controller.text_color,
                            activebackground="#e0e0e0",
                            activeforeground=controller.text_color, 
                            relief="flat", padx=10, pady=5,
                            command=self.add_wallet)
        add_wallet_button.pack(side="left")

        # Back button
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

    
    def connect_to_rpc(self, rpcUrl):
        try:
            conn = AuthServiceProxy(rpcUrl)
            if not conn:
                raise Exception("Could not connect to RPC")
            return conn
        except Exception as e:
            popup = tk.Toplevel(self)
            popup.title("Error connecting to RPC")
            popup.geometry("300x100")

            label_status = tk.Label(popup, text=e, pady=5)
            label_status.pack()

            popup.after(1000, popup.destroy)
            return None
    
    def add_wallet (self):
        newWallet = self.rpc.createwallet("new_wallet")
        self.wallets.append(newWallet)
    
    def load_wallets(self):
        rpc_connection = AuthServiceProxy(self.rpcUrl)
        self.wallets = rpc_connection.listwallets()

        for wallet in self.wallets:
            print(f"\n=== Wallet: {wallet} ===")

            # Koneksi ke wallet tertentu
            wallet_rpc_url = f"{self.rpcUrl}/wallet/{wallet}"
            wallet_rpc_connection = AuthServiceProxy(wallet_rpc_url)

            # **Ambil Saldo**
            balance = float(wallet_rpc_connection.getbalance())
            print(f"Balance: {balance} BTC")

            # **Ambil Address Baru**
            new_address = wallet_rpc_connection.getnewaddress()
            print(f"New Address: {new_address}")

            # **Buat Frame untuk Wallet**
            wallet_frame = tk.Frame(self.wallets_frame, bg=self.controller.bg_color)
            wallet_frame.pack(fill="x", pady=5)

            # **Label Nama Wallet + Address + Saldo**
            wallet_label = tk.Label(
                wallet_frame, 
                text=f"{wallet} | {new_address} | {balance} BTC", 
                font=("Helvetica", 11), 
                bg=self.controller.bg_color, 
                fg="#666"
            )
            wallet_label.pack(side="left", padx=5)

            # **Tombol "Use"**
            use_button = tk.Button(
                wallet_frame, 
                text="Use", 
                font=("Helvetica", 10), 
                bg="#4CAF50", 
                fg="white", 
                command=lambda w=wallet: self.use_wallet(w)
            )
            use_button.pack(side="right", padx=5)

    def use_wallet(self, wallet_name):
        print(f"Wallet {wallet_name} selected for use!")
        # Anda bisa menambahkan aksi lain di sini, misalnya membuka detail wallet.

    def is_btc_installed(self):
        """Check if Bitcoin Core is installed"""
        return os.path.exists(BTC_CORE_INSTALLATION_PATH)
    
    def is_btc_core_downloaded(self):
        """Check if Bitcoin Core is installed"""
        return os.path.exists(BTC_CORE_DOWNLOAD_PATH)

    def download_btc_core(self):
        """Check installation and download Bitcoin Core if not installed"""
        if self.is_btc_installed():
            messagebox.showinfo("Info", "Bitcoin Core is already installed.")
            return
        
        def download():
            # Create popup window
            popup = tk.Toplevel(self)
            popup.title("Downloading Bitcoin Core...")
            popup.geometry("300x100")

            label_status = tk.Label(popup, text="Downloading...", pady=5)
            label_status.pack()

            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(popup, variable=progress_var, length=250)
            progress_bar.pack(pady=10)
            response = requests.get(BTC_CORE_URL, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # Download block size

            with open(BTC_CORE_DOWNLOAD_PATH, "wb") as file:
                downloaded = 0
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded += len(data)
                    progress_var.set((downloaded / total_size) * 100)
                    popup.update_idletasks()

            label_status.config(text="Download Completed!")
            popup.after(2000, popup.destroy)
        if not self.is_btc_core_downloaded():
            threading.Thread(target=download, daemon=True).start()
        
        self.extract_btc_core()
    
    def extract_btc_core(self):
        """Extract the downloaded Bitcoin Core archive to the appropriate path."""
        if not os.path.exists(BTC_CORE_DOWNLOAD_PATH):
            print("Error: Bitcoin Core archive not found!")
            return

        # Extract the archive
        with tarfile.open(BTC_CORE_DOWNLOAD_PATH, "r:gz") as tar:
            tar.extractall(f"{THIRD_PARTY_PROGRAM_PATH}/")
            tar.close()

        print(f"Bitcoin Core extracted successfully to {BTC_CORE_INSTALLATION_PATH}")

