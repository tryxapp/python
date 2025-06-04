import psutil
import shutil
import requests
import subprocess
import time
import win32ts
import win32con
import win32api

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

# Cek apakah sesi RDP sedang aktif
def is_rdp_connected():
    try:
        sessions = win32ts.WTSEnumerateSessions(None, 1, 0)
        for session in sessions:
            session_id = session[0]
            state = win32ts.WTSQuerySessionInformation(None, session_id, win32ts.WTSConnectState)
            username = win32ts.WTSQuerySessionInformation(None, session_id, win32ts.WTSUserName)
            client_address = win32ts.WTSQuerySessionInformation(None, session_id, win32ts.WTSClientAddress)

            # Cek apakah user terkoneksi dari client dan bukan sesi kosong
            if username and state in [win32ts.WTSActive, win32ts.WTSConnected]:
                return True
        return False
    except Exception as e:
        print("Error cek sesi :", e)
        return False

# Bandwidth usage (Tx+Rx sejak boot)
def get_bandwidth_usage():
    net_io = psutil.net_io_counters()
    tx = net_io.bytes_sent / (1024 * 1024)
    rx = net_io.bytes_recv / (1024 * 1024)
    return round(tx, 2), round(rx, 2)

# Storage info
def get_storage_info():
    total, used, free = shutil.disk_usage("C:/")
    return round(used / (1024**3), 2), round(free / (1024**3), 2)

# Main loop
def monitor():
    last_rdp_state = None
    while True:
        rdp_connected = is_rdp_connected()
        tx, rx = get_bandwidth_usage()
        used_gb, free_gb = get_storage_info()

        message = f"📡 <b>Monitoring RDP {RDP_IP}</b>\n"
        message += f"👥 RDP Status: {'🟢 Connected' if rdp_connected else '🔴 Disconnected'}\n"
        message += f"📶 Bandwidth: {rx} MB Received | {tx} MB Sent\n"
        message += f"💽 Storage: {used_gb} GB Used | {free_gb} GB Free\n"

        # Kirim notifikasi hanya jika status berubah atau setiap 5 menit
        if last_rdp_state != rdp_connected:
            send_telegram_message(message)
            last_rdp_state = rdp_connected

        # Kirim update setiap 5 menit
        if int(time.time()) % 300 < 5:
            send_telegram_message(message)

        time.sleep(30)

if __name__ == "__main__":
    send_telegram_message("🚀 Memulai monitoring RDP...")
    monitor()
