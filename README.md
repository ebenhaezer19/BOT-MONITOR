# Shopee Stealth Monitor

A bot to monitor product availability on Shopee with screenshot and OCR analysis features.

## System Requirements

### Windows
1. Python 3.8 or newer
2. Google Chrome
3. Tesseract OCR
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to `C:\Program Files\Tesseract-OCR`
   - Make sure path is added to Environment Variables

### Linux/Ubuntu
1. Python 3.8 or newer
2. Google Chrome
3. Tesseract OCR and dependencies:
```bash
sudo apt update
sudo apt install -y tesseract-ocr
sudo apt install -y libtesseract-dev
sudo apt install -y tesseract-ocr-eng
sudo apt install -y tesseract-ocr-ind
```

### macOS
1. Python 3.8 or newer
2. Google Chrome
3. Tesseract OCR:
```bash
brew install tesseract
```

## Installation

1. Clone this repository
2. Create virtual environment (optional but recommended):
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

## Usage

1. Run the program:
```bash
python stealth_monitor.py
```

2. URL Setup:
   - Choose between default URL or custom URL
   - For custom URL, enter a valid Shopee Singapore product URL
   - URL must contain product ID (format: i.xxx.xxx)

3. Monitoring Process:
   - Chrome will open automatically with the selected product page
   - Program will check availability every 20-60 seconds (random interval)
   - Screenshots are taken and analyzed using OCR
   - Old screenshots are automatically cleaned up
   - Press Ctrl+C to stop monitoring

## Features

- URL Configuration:
  - Default URL support
  - Custom URL input with validation
  - Automatic product ID extraction

- Automatic Chrome Control:
  - Direct product page loading
  - Remote debugging support
  - Anti-bot detection measures

- Advanced Monitoring:
  - Screenshot-based analysis
  - OCR text recognition
  - Automatic screenshot cleanup
  - Multiple price detection patterns
  - Stock availability checking
  - Random delay intervals

- Stealth Features:
  - Random user agent rotation
  - Anti-detection measures
  - Browser fingerprint protection
  - No direct web scraping

- User Interface:
  - Clean console output
  - Detailed status updates
  - Progress indicators
  - Error handling and reporting

## Troubleshooting

### Windows
- If Tesseract is not detected, verify the path in `stealth_monitor.py`
- If Chrome doesn't open, ensure Chrome is installed in the default location

### Linux/Ubuntu
- If you get permission errors, use `sudo` for Tesseract installation
- If Chrome doesn't open, install Chrome first:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
```

### macOS
- If you get permission errors, use `sudo` for Tesseract installation
- Ensure Chrome is installed from App Store or official website

## Project Structure
```
Your-Project-Folder/
├── stealth_monitor.py    # Main program file
├── requirements.txt      # Python dependencies
├── README.md            # Documentation
├── screenshots/         # Screenshot storage (auto-cleaned)
├── chrome_extensions/   # Chrome extensions
└── chrome_debug_profile/ # Chrome debug profile
```

## License
This project is licensed under the MIT License - see the LICENSE file for details. 