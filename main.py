import subprocess
import sqlite3
import time
import argparse
from datetime import datetime

def extract_between_spaces(text, start_space, end_space):
    parts = text.split()
    return parts[start_space:end_space][0] if len(parts) > end_space else "Yeterli boşluk bulunamadı."

def get_eth0_data():
    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    eth0_started = False
    eth0_lines = []

    for line in lines:
        if 'eth0:' in line:
            eth0_started = True
        elif eth0_started and len(eth0_lines) < 7:
            eth0_lines.append(line)

    inet_value = netmask_value = broadcast_value = None
    inet6_value = ether_value = rx_pockets = rx_error = tx_pockets = tx_error = None

    for index, line in enumerate(eth0_lines):
        if index == 0:  # 1. satır için işlem yapıyoruz
            parts = line.split()
            inet_value = parts[1]  # inet değeri
            netmask_value = parts[3]  # netmask değeri
            broadcast_value = parts[5]  # broadcast değeri
        elif index == 1:  
            inet6_value = extract_between_spaces(line, 1, 2)
        elif index == 2:  
            ether_value = extract_between_spaces(line, 1, 2)
        elif index == 3:  
            rx_pockets = extract_between_spaces(line, 2, 3)
        elif index == 4:  
            rx_error = extract_between_spaces(line, 2, 3)
        elif index == 5:  
            tx_pockets = extract_between_spaces(line, 2, 3)
        elif index == 6:  
            tx_error = extract_between_spaces(line, 2, 3)

    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'inet': inet_value or '0',
        'netmask': netmask_value or '0',
        'broadcast': broadcast_value or '0',
        'inet6': inet6_value or '0',
        'ether': ether_value or '0',
        'rx_pockets': rx_pockets or '0',
        'rx_error': rx_error or '0',
        'tx_pockets': tx_pockets or '0',
        'tx_error': tx_error or '0'
    }

    return data

def save_to_db(data, args):
    conn = sqlite3.connect('ethstats.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        inet TEXT,
        netmask TEXT,
        broadcast TEXT,
        inet6 TEXT,
        ether TEXT,
        rx_pockets TEXT,
        rx_error TEXT,
        tx_pockets TEXT,
        tx_error TEXT
    )
    ''')

    columns = ['timestamp']
    placeholders = ['?']
    values = [data['timestamp']]

    def add_column_if_specified(arg, column_name):
        if getattr(args, arg) or args.all:
            columns.append(column_name)
            placeholders.append('?')
            values.append(data[column_name])
        else:
            columns.append(column_name)
            placeholders.append('?')
            values.append('0')

    add_column_if_specified('inet', 'inet')
    add_column_if_specified('netmask', 'netmask')
    add_column_if_specified('broadcast', 'broadcast')
    add_column_if_specified('inet6', 'inet6')
    add_column_if_specified('ether', 'ether')
    add_column_if_specified('rx_pocket', 'rx_pockets')
    add_column_if_specified('rx_error', 'rx_error')
    add_column_if_specified('tx_pocket', 'tx_pockets')
    add_column_if_specified('tx_error', 'tx_error')

    columns_str = ', '.join(columns)
    placeholders_str = ', '.join(placeholders)
    cursor.execute(f'''
    INSERT INTO my_table ({columns_str})
    VALUES ({placeholders_str})
    ''', values)

    conn.commit()
    conn.close()

def delete_from_db():
    conn = sqlite3.connect('ethstats.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM my_table')

    conn.commit()
    conn.close()
    print("Veritabanı temizlendi.")

def run_program(interval, args):
    while True:
        try:
            data = get_eth0_data()
            save_to_db(data, args)
            print(f"timestamp : {data['timestamp']}")
            print(f"inet      : {data['inet']}")
            print(f"netmask   : {data['netmask']}")
            print(f"broadcast : {data['broadcast']}")
            print(f"inet6     : {data['inet6']}")
            print(f"ether     : {data['ether']}")
            print(f"rx_pockets: {data['rx_pockets']}")
            print(f"rx_error  : {data['rx_error']}")
            print(f"tx_pockets: {data['tx_pockets']}")
            print(f"tx_error  : {data['tx_error']}")
            print("-----------------------------------------")

            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nProgram durduruldu.")
            break

def print_custom_help():
    print("                                                                                                      ")
    print("                 ╔══════════════════════════════════════════════════════════════════════════════════╗ ")
    print("                 ║ Kullanım: python script.py <ARGÜMANLAR>                                          ║ ")
    print("                 ╠══════════════════════════════════════════════════════════════════════════════════╣ ")
    print("                 ║ --clear                : Veritabanını temizler.                                  ║ ")
    print("                 ║ --all                  : Tüm bilgileri kaydeder.                                 ║ ")
    print("                 ║ --inet                 : IP adresi bilgilerini alır.                             ║ ")
    print("                 ║ --netmask              : Netmask değerini alır.                                  ║ ")
    print("                 ║ --broadcast            : Broadcast adresini alır.                                ║ ")
    print("                 ║ --inet6                : IPv6 adresini alır.                                     ║ ")
    print("                 ║ --ether                : Ethernet adresini alır.                                 ║ ")
    print("                 ║ --rx_pocket            : RX paket sayısını alır.                                 ║ ")
    print("                 ║ --rx_error             : RX hata sayısını alır.                                  ║ ")
    print("                 ║ --tx_pocket            : TX paket sayısını alır.                                 ║ ")
    print("                 ║ --tx_error             : TX hata sayısını alır.                                  ║ ")
    print("                 ║ --interval <saniye>    : Programın çalışma aralığını belirler (saniye cinsinden).║ ")
    print("                 ║ --yardim               : Bu yardım mesajını gösterir.                            ║ ")
    print("                 ╚══════════════════════════════════════════════════════════════════════════════════╝ ")
    print("                                                                                                      ")

def main():
    parser = argparse.ArgumentParser(description='Script for monitoring network interfaces.')
    
    parser.add_argument("--clear", action="store_true", help="Veritabanını temizler.")
    parser.add_argument("--all", action="store_true", help="Tüm bilgileri kaydeder.")
    parser.add_argument("--inet", action="store_true", help="IP adresi bilgilerini alır.")
    parser.add_argument("--netmask", action="store_true", help="Netmask değerini alır.")
    parser.add_argument("--broadcast", action="store_true", help="Broadcast adresini alır.")
    parser.add_argument("--inet6", action="store_true", help="IPv6 adresini alır.")
    parser.add_argument("--ether", action="store_true", help="Ethernet adresini alır.")
    parser.add_argument("--rx_pocket", action="store_true", help="RX paket sayısını alır.")
    parser.add_argument("--rx_error", action="store_true", help="RX hata sayısını alır.")
    parser.add_argument("--tx_pocket", action="store_true", help="TX paket sayısını alır.")
    parser.add_argument("--tx_error", action="store_true", help="TX hata sayısını alır.")
    parser.add_argument("--interval", type=int, default=20, help="Programın çalışma aralığını belirler (saniye cinsinden).")
    parser.add_argument("--yardim", action="store_true", help="Yardım mesajını gösterir")

    args = parser.parse_args()

    # Kontrol: Hiçbir argüman kullanılmamışsa
    if not (args.clear or args.all or args.inet or args.netmask or args.broadcast or args.inet6 or args.ether or args.rx_pocket or args.rx_error or args.tx_pocket or args.tx_error or args.yardim):
        print("Lütfen bir argüman kullanın. Yardım için --yardim argümanını kullanabilirsiniz.")
        return

    if args.yardim:
        print_custom_help()
    elif args.clear:
        delete_from_db()
    else:
        run_program(args.interval, args)

if __name__ == "__main__":
    main()
