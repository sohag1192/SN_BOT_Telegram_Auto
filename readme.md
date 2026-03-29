
```markdown
# SN_BOT-Telegram-Services

A lightweight automation project that deploys two Python-based services:
- **SN FTP Server** – simple FTP server script
- **SN TV Bot** – Telegram bot for streaming/automation

This repository includes installation scripts and systemd service files to run both components automatically on Ubuntu.

---

## 🚀 Features
- Auto-install Python and dependencies
- Systemd service integration for auto-start on boot
- Log redirection to `/var/log/` for monitoring
- Easy deployment with a single shell script

---

## 📦 Requirements
- Ubuntu 20.04+ (tested on 22.04)
- Python 3.x
- pip3
- Git

---

## 🔧 Installation

Clone the repository:
```bash
git clone https://github.com/sohag1192/SN_BOT_Telegram_Auto.git
cd SN_BOT_Telegram_Auto
```

Run the installer:
```bash
chmod +x install.sh
./install.sh
```

This will:
- Install Python and pip
- Install `pyTelegramBotAPI`
- Copy scripts into `/root`
- Create and enable systemd services

---

## ▶️ Usage

Start services manually:
```bash
sudo systemctl start sn_ftp_server.service
sudo systemctl start sn_tv_bot.service
```

Check status:
```bash
sudo systemctl status sn_ftp_server.service
sudo systemctl status sn_tv_bot.service
```

View logs:
```bash
tail -f /var/log/sn_ftp_server.log
tail -f /var/log/sn_tv_bot.log
```

---

## 📂 Project Structure
```
SN_BOT_Telegram_Auto/
├── sn_ftp_server.py   # FTP server script
├── sn_tv_bot.py       # Telegram bot script
├── tele.py            # Helper module
├── install.sh         # Auto-install shell script
└── README.md          # Documentation
```

---

## ⚠️ Notes
- Services run as **root** by default. For better security, consider creating a dedicated user.
- Logs are stored in `/var/log/` for easy monitoring.
- Extend `install.sh` if additional Python packages are required.

---

## 📜 License
MIT License – free to use, modify, and distribute.
```

