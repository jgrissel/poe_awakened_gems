# Deployment Guide: PoE Gem Profit Calculator (Ubuntu VPS)

This guide assumes you have a fresh Ubuntu VPS and root/sudo access.

## 1. System Setup
Update your system packages:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y
```

## 2. Application Setup
Navigate to your desired directory (e.g., `/var/www` or your home folder):
```bash
cd /home/ubuntu  # or your preferred path
mkdir poe_gem_calc
cd poe_gem_calc
```

**Option A: Copy files manually**
Upload the `src` folder and `requirements.txt` to this directory using SCP or SFTP (e.g., FileZilla).

**Option B: Git Clone (if you push this to GitHub)**
```bash
git clone <your-repo-url> .
```

## 3. Python Environment
Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## 4. Test Gunicorn
Try running the app with Gunicorn to ensure it starts:
```bash
# Navigate to src where app.py is located
cd src
# Run gunicorn (module:app_instance)
../venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
```
*Visit `http://<your-server-ip>:5000` in your browser. If it works, press `Ctrl+C` to stop it.*

## 5. Setup Systemd Service
Create a service file to keep the app running in the background:

```bash
sudo nano /etc/systemd/system/poe_calc.service
```

Paste the following (adjust paths/user as needed):
```ini
[Unit]
Description=Gunicorn instance to serve PoE Gem Calc
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/poe_gem_calc/src
Environment="PATH=/home/ubuntu/poe_gem_calc/venv/bin"
ExecStart=/home/ubuntu/poe_gem_calc/venv/bin/gunicorn --workers 3 --bind unix:poe_calc.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

Start and enable the service:
```bash
sudo systemctl start poe_calc
sudo systemctl enable poe_calc
sudo systemctl status poe_calc
```

## 6. Setup Nginx (Reverse Proxy)
Configure Nginx to forward traffic to Gunicorn:

```bash
sudo nano /etc/nginx/sites-available/poe_calc
```

Paste the following:
```nginx
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/poe_gem_calc/src/poe_calc.sock;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/poe_calc /etc/nginx/sites-enabled
sudo nginx -t  # Test config
sudo systemctl restart nginx
```

## 7. Firewall (UFW)
Ensure port 80 is open:
```bash
sudo ufw allow 'Nginx Full'
```

## Done!
Your application should now be accessible at `http://<your-server-ip>`.
