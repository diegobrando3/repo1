import psutil
import json
import time
from datetime import datetime
import os

DOSYA = "system_stats.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_system_stats():
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": {
            "kullanim_yuzde": psutil.cpu_percent(interval=1),
            "cekirdek_fiziksel": psutil.cpu_count(logical=False),
            "cekirdek_mantiksal": psutil.cpu_count(logical=True)
        },
        "ram": {
            "kullanim_yuzde": psutil.virtual_memory().percent,
            "toplam_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "kullanilan_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "bos_gb": round(psutil.virtual_memory().available / (1024**3), 2)
        },
        "disk": {
            "kullanim_yuzde": psutil.disk_usage('/').percent,
            "toplam_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
            "kullanilan_gb": round(psutil.disk_usage('/').used / (1024**3), 2)
        }
    }
    return stats


def save_to_json(stats):
    try:
        with open(DOSYA, "r", encoding="utf-8") as f:
            tum_veriler = json.load(f)
    except:
        tum_veriler = []
    
    tum_veriler.append(stats)
    
    if len(tum_veriler) > 100:        # son 100 kaydı tut
        tum_veriler = tum_veriler[-100:]
    
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(tum_veriler, f, ensure_ascii=False, indent=4)


def show_dashboard():
    stats = get_system_stats()
    save_to_json(stats)
    
    clear_screen()                    # <-- Ekranı temizle
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                    SYSTEM DASHBOARD                          ║")
    print(f"║                    {stats['timestamp']}                       ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    print(f"CPU Kullanımı     : {stats['cpu']['kullanim_yuzde']:6.1f}%")
    print(f"RAM Kullanımı     : {stats['ram']['kullanim_yuzde']:6.1f}%   ({stats['ram']['kullanilan_gb']}/{stats['ram']['toplam_gb']} GB)")
    print(f"Disk Kullanımı    : {stats['disk']['kullanim_yuzde']:6.1f}%   ({stats['disk']['kullanilan_gb']}/{stats['disk']['toplam_gb']} GB)")
    print("-" * 60)


if __name__ == "__main__":
    print("System Dashboard başlatılıyor... (Çıkmak için Ctrl + C)")
    time.sleep(1)
    
    try:
        while True:
            show_dashboard()
            time.sleep(2)        # 2 saniyede bir yenile
    except KeyboardInterrupt:
        clear_screen()
        print("Dashboard kapatıldı.")