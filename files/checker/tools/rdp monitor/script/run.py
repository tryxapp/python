import psutil
import shutil
import requests
import time
import socket
import win32ts
import datetime
import win32api
import getpass

# Konfigurasi Telegram
TELEGRAM_TOKEN = '7883324144:AAEWrjHXB3C4Kt-bz3rp8EqUUCv_URi_te0'
CHAT_ID = '5467965623'
RDP_IP = '157.230.245.221:9999'

# Fungsi kirim pesan ke Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Gagal kirim ke Telegram:", e)

# Cek apakah RDP sedang aktif
def is_rdp_connected():
    try:
        users = psutil.users()
        active_users = [u.name for u in users if u.name and u.host != '']
        current_user = getpass.getuser()

        if active_users:
            return True, active_users[0]  # Ambil user pertama yang aktif
        else:
            return True, current_user  # fallback ke user lokal
    except Exception as e:
        print("Error checking RDP session:", e)
        return False, "Unknown"

# Bandwidth usage sejak boot
def get_bandwidth_usage():
    net_io = psutil.net_io_counters()
    tx = net_io.bytes_sent / (1024 * 1024)
    rx = net_io.bytes_recv / (1024 * 1024)
    return round(tx, 2), round(rx, 2)

# Storage info
def get_storage_info():
    total, used, free = shutil.disk_usage("C:/")
    return round(used / (1024**3), 2), round(free / (1024**3), 2)

# CPU & RAM usage
def get_cpu_ram_usage():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return cpu, ram

# Uptime server
def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    uptime_hours = round(uptime_seconds / 3600, 2)
    return uptime_hours

# IP Lokal dan Publik
def get_ip_addresses():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except:
        local_ip = "N/A"
    try:
        public_ip = requests.get("https://api.ipify.org").text
    except:
        public_ip = "N/A"
    return local_ip, public_ip

# Main monitoring loop
def monitor():
    while True:
        rdp_status, username = is_rdp_connected()
        tx, rx = get_bandwidth_usage()
        used_gb, free_gb = get_storage_info()
        cpu, ram = get_cpu_ram_usage()
        uptime = get_uptime()
        local_ip, public_ip = get_ip_addresses()

        now = datetime.datetime.now().strftime("%d %B %Y - %H:%M:%S")

        message = (
            f"📡 <b>Monitoring RDP {RDP_IP}</b>\n"
            f"👥 Status RDP: {'🟢 Connected' if rdp_status else '🔴 Disconnected'}\n"
            f"👤 User Aktif: {username}\n"
            f"🧠 CPU Usage: {cpu}%\n"
            f"🧬 RAM Usage: {ram}%\n"
            f"📶 Bandwidth: {rx} MB RX | {tx} MB TX\n"
            f"💽 Storage C:: {used_gb} GB Used | {free_gb} GB Free\n"
            f"🌐 IP Publik: {public_ip}\n"
            f"🏠 IP Lokal: {local_ip}\n"
            f"⏱️ Uptime: {uptime} jam\n"
            f"🕒 Terakhir update: {now}"
        )

        send_telegram_message(message)
        time.sleep(300)  # 5 menit

if __name__ == "__main__":
    send_telegram_message("🚀 Memulai monitoring RDP...")
    monitor()
