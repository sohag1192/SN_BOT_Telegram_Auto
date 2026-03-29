#!/bin/bash
# install.sh - Auto install SN_BOT_Telegram_Auto on Ubuntu

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip git

# Install dependencies
pip3 install pyTelegramBotAPI

# Clone the repository
git clone https://github.com/sohag1192/SN_BOT_Telegram_Auto.git
cd SN_BOT_Telegram_Auto

# Copy scripts to /root
sudo cp sn_ftp_server.py sn_tv_bot.py tele.py /root/

# Create systemd service for sn_ftp_server
cat <<EOF | sudo tee /etc/systemd/system/sn_ftp_server.service
[Unit]
Description=SN FTP Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/sn_ftp_server.py
Restart=always
User=root
StandardOutput=append:/var/log/sn_ftp_server.log
StandardError=append:/var/log/sn_ftp_server.log

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for sn_tv_bot
cat <<EOF | sudo tee /etc/systemd/system/sn_tv_bot.service
[Unit]
Description=SN TV Bot
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/sn_tv_bot.py
Restart=always
User=root
StandardOutput=append:/var/log/sn_tv_bot.log
StandardError=append:/var/log/sn_tv_bot.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable services
sudo systemctl daemon-reload
sudo systemctl enable sn_ftp_server.service
sudo systemctl enable sn_tv_bot.service
sudo systemctl start sn_ftp_server.service
sudo systemctl start sn_tv_bot.service

echo "SN_BOT_Telegram_Auto installation and service setup complete."
echo "Logs: /var/log/sn_ftp_server.log and /var/log/sn_tv_bot.log"