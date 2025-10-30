#!/bin/bash
# install_dork_tool.sh

echo "Installing Google CSE Dorking Tool..."
echo ""

# Check if script exists
if [ ! -f "dork_tool.py" ]; then
    echo "Error: dork_tool.py not found in current directory!"
    exit 1
fi

# Install Python dependencies
echo "[*] Installing Python dependencies..."
pip3 install requests beautifulsoup4 urllib3

# Install system dependencies
echo "[*] Installing system dependencies..."
sudo apt update
sudo apt install -y python3-requests python3-bs4 python3-urllib3

# Make the script executable
chmod +x dork_tool.py

# Remove old symlink if exists
sudo rm -f /usr/local/bin/dorktool

# Create new symlink
sudo ln -s $(pwd)/dork_tool.py /usr/local/bin/dorktool

echo ""
echo "[+] Installation completed successfully!"
echo ""
echo "IMPORTANT: You need a Google API Key for CSE functionality!"
echo "Get one from: https://developers.google.com/custom-search/v1/introduction"
echo ""
echo "USAGE EXAMPLES:"
echo "  dorktool --help"
echo "  dorktool -u '?id=' -n 20 --google-api-key 'YOUR_API_KEY'"
echo "  dorktool -d 'example.com' -u '?page=' -s 200 301 302 --google-api-key 'YOUR_API_KEY'"
echo "  dorktool -d '*.co.id' -u '?view=' -n 15 -o results.txt --json --google-api-key 'YOUR_API_KEY'"
echo ""
echo "FEATURES:"
echo "  ✓ Google Custom Search Engine (CSE) API integration"
echo "  ✓ Bing and DuckDuckGo fallback search"
echo "  ✓ Multi-threading support"
echo "  ✓ Status code filtering"
echo "  ✓ JSON export"
echo "  ✓ SSL error handling"
echo "  ✓ Page title extraction"
echo "  ✓ Comprehensive reporting"
echo ""
echo "NOTE: This tool performs real web searches. Use responsibly and ethically."