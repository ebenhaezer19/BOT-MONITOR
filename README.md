```markdown
# Shopee Stealth Monitor

A bot to monitor product availability on Shopee with screenshot, OCR analysis, and Discord notification features.

## System Requirements

### Windows
1. Python 3.8 or newer
2. Google Chrome
3. Tesseract OCR
   - Download from: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
   - Install to `C:\Program Files\Tesseract-OCR`
   - Add `C:\Program Files\Tesseract-OCR` to your system's Environment Variables PATH

### Linux/Ubuntu
1. Python 3.8 or newer
2. Google Chrome
3. Tesseract OCR and dependencies:
   ```bash
   sudo apt update
   sudo apt install -y tesseract-ocr libtesseract-dev tesseract-ocr-eng tesseract-ocr-ind
   ```

### macOS
1. Python 3.8 or newer
2. Google Chrome
3. Tesseract OCR:
   ```bash
   brew install tesseract
   ```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up Discord Webhook:
   - Create a webhook in your Discord server (Server Settings > Integrations > Webhooks > New Webhook).
   - Copy the Webhook URL and replace the `DISCORD_WEBHOOK_URL` value in `stealth_monitor.py`.

## Usage

1. Run the program:
   ```bash
   python stealth_monitor.py
   ```

2. URL Setup:
   - Choose between the default URL or a custom URL.
   - Default URL: `https://shopee.sg/Pokémon-Center-Original-TCG-Prismatic-Evolutions-Booster-Bundle-i.270785126.27278435146`
   - For custom URL, enter a valid Shopee Singapore product URL containing a product ID (format: `i.xxx.xxx`).

3. Monitoring Process:
   - Chrome will open automatically with the selected product page.
   - The program checks availability every 20-60 seconds (random interval).
   - Screenshots are taken and analyzed using OCR.
   - Results are sent to Discord if a webhook is configured.
   - Old screenshots are automatically cleaned up.
   - Press `Ctrl+C` to stop monitoring.

## Features

- **URL Configuration**:
  - Default URL support
  - Custom URL input with validation
  - Automatic product ID extraction

- **Automatic Chrome Control**:
  - Direct product page loading
  - Remote debugging support
  - Anti-bot detection measures

- **Advanced Monitoring**:
  - Screenshot-based analysis
  - OCR text recognition
  - Automatic screenshot cleanup
  - Multiple price detection patterns
  - Stock availability checking
  - Random delay intervals

- **Stealth Features**:
  - Random user agent rotation
  - Anti-detection measures
  - Browser fingerprint protection
  - No direct web scraping

- **Discord Integration**:
  - Real-time notifications via Discord Webhook
  - Detailed status updates (stock, price, availability)
  - Error reporting

- **User Interface**:
  - Clean console output
  - Detailed status updates
  - Progress indicators
  - Error handling and reporting

## Troubleshooting

### Windows
- **Tesseract Not Detected**: Verify Tesseract is installed at `C:\Program Files\Tesseract-OCR` and added to PATH.
- **Chrome Won't Open**: Ensure Chrome is installed in a default location (e.g., `C:\Program Files\Google\Chrome\Application\chrome.exe`).

### Linux/Ubuntu
- **Permission Errors**: Use `sudo` for Tesseract or Chrome installation if needed.
- **Chrome Not Installed**: Install Chrome manually:
  ```bash
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo dpkg -i google-chrome-stable_current_amd64.deb
  sudo apt --fix-broken install
  ```

### macOS
- **Permission Errors**: Use `sudo` if needed during Tesseract installation.
- **Chrome Issues**: Ensure Chrome is installed from the official website or App Store.

### General
- **Discord Notifications Not Working**: Verify the `DISCORD_WEBHOOK_URL` in `stealth_monitor.py` is correct and the webhook is active.
- **Dependencies Missing**: Run `pip install -r requirements.txt` again to ensure all libraries are installed.

## Project Structure
```
Your-Project-Folder/
├── stealth_monitor.py    # Main program file
├── requirements.txt      # Python dependencies
├── README.md             # This documentation
├── screenshots/          # Screenshot storage (auto-cleaned)
├── chrome_debug_profile/ # Chrome debug profile (auto-created)
```

## Requirements File (`requirements.txt`)
```
selenium
requests
pytesseract
pillow
opencv-python
numpy
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.  
Made by Krisopras Eben Haezer (email: krisoprasebenhaezer@gmail.com)

## Note
- This project is a work in progress and may not work perfectly in all scenarios.
- I am not responsible for any damage caused by this project.
- Use at your own risk.
```

