import sys
import os
import time
import logging
import socket
import subprocess
import platform
import webbrowser
import signal
import zipfile
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import cv2
import numpy as np
from PIL import Image
import pytesseract
import json
from selenium.webdriver.chrome.service import Service
import re

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Ganti dengan URL Webhook Discord Anda
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1356075531610620074/Pq6XsV_yp_gZ3N5pDhM3GJoLC_QWV1L7FI8SQY_ByfALM9AIB3eGV3b-TzS3qOkH7BR1"

def send_discord_notification(message, embed=None):
    """Mengirim notifikasi ke Discord via Webhook."""
    try:
        data = {"content": message}
        if embed:
            data["embeds"] = [embed]
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            logger.info("Successfully sent notification to Discord")
        else:
            logger.error(f"Failed to send Discord notification: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending Discord notification: {str(e)}")

def is_port_in_use(port):
    """Check if port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return False
        except socket.error:
            return True

def find_chrome_path():
    """Find Chrome path based on operating system."""
    if platform.system() == "Windows":
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
            chrome_path = winreg.QueryValue(key, None)
            if os.path.exists(chrome_path):
                return chrome_path
        except:
            pass

        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe")
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                return path
                
    elif platform.system() == "Darwin":  # macOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
                
    else:  # Linux
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium"
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
    
    raise Exception("Could not find Chrome installation. Please install Chrome and try again.")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
]

def get_random_delay(min_seconds=15, max_seconds=45):
    return random.uniform(min_seconds, max_seconds)

def start_chrome_with_debugging(port=9222, user_data_dir=None, url=None):
    if is_port_in_use(port):
        logger.info(f"Chrome is already running on port {port}")
        return True
        
    try:
        chrome_path = find_chrome_path()
        logger.info(f"Chrome path: {chrome_path}")
        
        if user_data_dir is None:
            user_data_dir = os.path.abspath("./chrome_debug_profile")
        
        os.makedirs(user_data_dir, exist_ok=True)
        
        options = [
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized",
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            f"--user-agent={random.choice(USER_AGENTS)}",
            "--disable-notifications",
            "--disable-popup-blocking"
        ]
        
        if url:
            options.append(url)
        
        cmd = [chrome_path] + options
        
        logger.info(f"Starting Chrome with command: {' '.join(cmd)}")
        chrome_process = subprocess.Popen(cmd)
        
        max_attempts = random.randint(8, 12)
        for i in range(max_attempts):
            if is_port_in_use(port):
                logger.info(f"Chrome started successfully on port {port}")
                return True
            time.sleep(random.uniform(1.0, 2.0))
            logger.info(f"Waiting for Chrome to start... ({i+1}/{max_attempts})")
        
        logger.warning(f"Chrome might not have started properly on port {port}")
        return False
        
    except Exception as e:
        logger.error(f"Failed to start Chrome: {str(e)}")
        return False

def connect_to_chrome(port=9222):
    try:
        logger.info(f"Connecting to Chrome on port {port}...")
        
        options = Options()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("Successfully connected to Chrome")
        
        return driver
    except Exception as e:
        logger.error(f"Error connecting to Chrome: {str(e)}")
        return None

def configure_tesseract():
    """Configure Tesseract path based on operating system."""
    system = platform.system()
    
    if system == "Windows":
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            os.path.expandvars(r'%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe')
        ]
        
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract path set to: {path}")
                return True
                
        logger.error("Tesseract not found. Please install it from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
        
    elif system == "Linux":
        tesseract_paths = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract'
        ]
        
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract path set to: {path}")
                return True
                
        logger.error("Tesseract not found. Please install it using: sudo apt install tesseract-ocr")
        return False
        
    elif system == "Darwin":  # macOS
        tesseract_paths = [
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract'
        ]
        
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                logger.info(f"Tesseract path set to: {path}")
                return True
                
        logger.error("Tesseract not found. Please install it using: brew install tesseract")
        return False
        
    else:
        logger.error(f"Unsupported operating system: {system}")
        return False

def cleanup_old_screenshots():
    """Cleanup old screenshots and OCR text files."""
    try:
        screenshots_dir = os.path.abspath("./screenshots")
        if os.path.exists(screenshots_dir):
            for filename in os.listdir(screenshots_dir):
                if filename.endswith('.png') or filename.endswith('_text.txt'):
                    file_path = os.path.join(screenshots_dir, filename)
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted old file: {filename}")
                    except Exception as e:
                        logger.error(f"Error deleting {filename}: {str(e)}")
    except Exception as e:
        logger.error(f"Error cleaning up screenshots: {str(e)}")

def check_product_availability(driver):
    """Check product availability using OCR and send Discord notification."""
    try:
        cleanup_old_screenshots()
        
        screenshots_dir = os.path.abspath("./screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"page_{timestamp}.png")
        
        time.sleep(random.uniform(2.0, 4.0))
        
        logger.info("Taking screenshot...")
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved as {screenshot_path}")
        
        if not configure_tesseract():
            logger.error("Failed to configure Tesseract. Please install it first.")
            return None
        
        try:
            text = pytesseract.image_to_string(Image.open(screenshot_path))
            logger.info("OCR completed successfully")
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            return None
        
        text_file = f"{screenshot_path}_text.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(text)
            
        text_lower = text.lower()
        
        print("\nRaw OCR Text:")
        print("-" * 40)
        print(text_lower)
        print("-" * 40)
        
        is_unlisted = 'unlisted' in text_lower
        
        pieces_available = 0
        stock_patterns = [
            r'(\d+)\s*pieces?\s*available',
            r'quantity.*?(\d+)',
            r'(\d+)\s*pieces',
            r'0\s*pieces'
        ]
        
        for pattern in stock_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    pieces_available = int(match.group(1))
                    print(f"Found stock count: {pieces_available} using pattern: {pattern}")
                    break
                except ValueError:
                    continue
        
        buy_keywords = ['add to cart', 'buy now']
        can_buy = any(keyword in text_lower for keyword in buy_keywords)
        
        price_patterns = [
            r'\$(\d+\.?\d*)',
            r'sgd\s*(\d+\.?\d*)'
        ]
        price = None
        for pattern in price_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    price = float(match.group(1))
                    print(f"Found price: ${price} using pattern: {pattern}")
                    break
                except ValueError:
                    continue
        
        if is_unlisted:
            status = 'UNLISTED'
        elif '0 pieces available' in text_lower or pieces_available == 0:
            status = 'OUT OF STOCK'
        elif can_buy and pieces_available > 0:
            status = 'IN STOCK'
        else:
            status = 'UNKNOWN'
        
        result = {
            'status': status,
            'pieces_available': pieces_available,
            'can_buy': can_buy,
            'is_unlisted': is_unlisted,
            'price': price,
            'raw_text': text,
            'screenshot_path': screenshot_path,
            'text_file': text_file
        }
        
        print("\n" + "="*80)
        print("PRODUCT AVAILABILITY CHECK RESULTS".center(80))
        print("="*80)
        print(f"Status: {result['status']}")
        print(f"Pieces Available: {result['pieces_available']}")
        print(f"Can Buy: {'Yes' if result['can_buy'] else 'No'}")
        print(f"Is Unlisted: {'Yes' if result['is_unlisted'] else 'No'}")
        print(f"Price: ${result['price'] if result['price'] else 'N/A'}")
        print("="*80)
        
        print(f"\nScreenshot saved: {screenshot_path}")
        print(f"OCR text saved: {text_file}")
        
        embed = {
            "title": "Shopee Product Status Update",
            "description": f"**URL:** {driver.current_url}",
            "color": 5814783 if status == 'IN STOCK' else (15158332 if status == 'OUT OF STOCK' else 10181046),
            "fields": [
                {"name": "Status", "value": status, "inline": True},
                {"name": "Pieces Available", "value": str(pieces_available), "inline": True},
                {"name": "Can Buy", "value": "Yes" if can_buy else "No", "inline": True},
                {"name": "Price", "value": f"${price}" if price else "N/A", "inline": True},
                {"name": "Timestamp", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "inline": False}
            ],
            "footer": {"text": "Shopee Stealth Monitor"}
        }
        send_discord_notification("", embed=embed)
        
        return result
        
    except Exception as e:
        logger.error(f"Error checking product availability: {str(e)}")
        send_discord_notification(f"Error occurred: {str(e)}")
        return None

def get_product_url():
    """Get product URL from user input or use default."""
    print("\n" + "="*80)
    print("SHOPEE STEALTH MONITOR - URL SETUP".center(80))
    print("="*80)
    print("\nDefault product URL:")
    print("https://shopee.sg/Pok%C3%A9mon-Center-Original-TCG-Prismatic-Evolutions-Booster-Bundle-i.270785126.27278435146")
    print("\nOptions:")
    print("1. Use default URL")
    print("2. Enter custom URL")
    
    while True:
        try:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            if choice == "1":
                return "https://shopee.sg/Pok%C3%A9mon-Center-Original-TCG-Prismatic-Evolutions-Booster-Bundle-i.270785126.27278435146"
            elif choice == "2":
                custom_url = input("\nEnter the Shopee product URL: ").strip()
                if "shopee.sg" in custom_url and "i." in custom_url:
                    return custom_url
                else:
                    print("\nError: Invalid Shopee URL. URL must be from shopee.sg and contain product ID")
                    continue
            else:
                print("\nError: Please enter 1 or 2")
        except Exception as e:
            print(f"\nError: {str(e)}")

def stealth_monitor():
    product_url = get_product_url()
    
    try:
        product_id = re.search(r'i\.\d+\.\d+', product_url).group(0)
    except:
        product_id = None
    
    port = 9222
    user_data_dir = os.path.abspath("./chrome_debug_profile")
    
    try:
        print("\n" + "="*80)
        print("SHOPEE STEALTH MONITOR".center(80))
        print("="*80)
        print(f"\nMonitoring product: {product_url}")
        
        if not is_port_in_use(port):
            print("\nChrome is not running on port 9222. Starting Chrome...")
            chrome_started = start_chrome_with_debugging(port, user_data_dir, product_url)
            
            if not chrome_started:
                logger.error("Failed to start Chrome. Please check if Chrome is installed correctly.")
                return
                
            print("Chrome has been started successfully with product page.")
            time.sleep(random.uniform(3.0, 7.0))
        else:
            print("Chrome is already running on port 9222.")
        
        print("\nConnecting to Chrome...")
        driver = connect_to_chrome(port)
        
        if not driver:
            logger.error("Failed to connect to Chrome.")
            return
        
        check_count = 0
        
        try:
            while True:
                check_count += 1
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n{'='*80}")
                print(f"CHECK #{check_count} - {current_time}".center(80))
                print('='*80)
                
                current_url = driver.current_url
                print(f"\nCurrent URL: {current_url}")
                
                if product_id and product_id not in current_url:
                    print("\nCorrect product page is not open.")
                    print(f"Please open product URL: {product_url}")
                    print("Please open the product page manually in the browser.")
                    input("Press Enter after opening the correct product page...")
                    continue
                
                pre_check_delay = random.uniform(2.0, 5.0)
                print(f"\nPreparing to check availability... ({pre_check_delay:.1f}s)")
                time.sleep(pre_check_delay)
                
                logger.info("\nChecking product availability...")
                product_info = check_product_availability(driver)
                
                if not product_info:
                    logger.error("Failed to check product availability")
                    continue
                
                next_check_delay = get_random_delay(20, 60)
                print(f"\nWaiting {next_check_delay:.1f} seconds before next check...")
                print("Press Ctrl+C to stop monitoring")
                time.sleep(next_check_delay)
                
        except KeyboardInterrupt:
            logger.info("\nProgram stopped by user")
            print(f"\nTotal checks performed: {check_count}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        if 'driver' in locals() and driver:
            logger.info("Cleaning up...")
            try:
                driver.quit()
            except:
                pass
    
    logger.info("Done")

if __name__ == "__main__":
    stealth_monitor()