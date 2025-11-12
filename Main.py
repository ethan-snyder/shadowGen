import random
import string
import os
import platform
import subprocess
from passlib.hash import sha512_crypt
from colorama import Fore, Style, init
init(autoreset=True)

# Public vars
file_name = "output/shadow.txt"
passwd_file = "output/passwd.txt"
pass_file = "textFiles/pass_file.txt"  # File containing dictionary words
uname_file = "textFiles/uname_file.txt"  # File containing username words

def cli():
    print(f"{Style.BRIGHT}{Fore.BLUE}Welcome to Shadow Generator{Style.RESET_ALL}")

    if not os.path.exists(pass_file):
        print(f"{Fore.RED}Error: {pass_file} not found. Please create a word list file first.")
        return
    if not os.path.exists(uname_file):
        print(f"{Fore.RED}Error: {uname_file} not found. Please create a username word list file first.")
        return

    shadow_entries = []
    usernames = []           # Collect usernames for /etc/passwd

    while True:
        print(f"\n{Fore.YELLOW}1. Generate a random/complex password")
        print(f"{Fore.YELLOW}2. Generate a simple password consisting of words{Style.RESET_ALL}")

        q1_input = input(f"\n{Fore.CYAN}Please enter your choice (1 or 2): {Style.RESET_ALL}").strip()

        if q1_input not in ["1", "2"]:
            print(f"{Fore.RED}Error: Invalid choice. Please enter 1 or 2")
            continue

        try:
            q2_input = int(input(f"\n{Fore.CYAN}Please enter the number of password(s) you wish to generate: {Style.RESET_ALL}"))
            if q2_input <= 0:
                print(f"{Fore.RED}Error: Number of passwords must be positive")
                continue

            if q1_input == "1":
                pass_len = int(input(f"{Fore.CYAN}Please enter password length for your random/complex password: {Style.RESET_ALL}"))
                if pass_len <= 0:
                    print(f"{Fore.RED}Error: Password length must be positive")
                    continue
                for _ in range(q2_input):
                    shadow_entry, username = gen_hard_pass(pass_len)
                    shadow_entries.append(shadow_entry)
                    usernames.append(username)

            elif q1_input == "2":
                num_words = int(input(f"{Fore.CYAN}Please enter number of words for your simple password: {Style.RESET_ALL}"))
                if num_words <= 0:
                    print(f"{Fore.RED}Error: Number of words must be positive")
                    continue
                for _ in range(q2_input):
                    password = gen_simple_pass(num_words)
                    password_hash = gen_hash(password)
                    username = gen_username()
                    print(f"\n{Fore.YELLOW}Username: {Fore.CYAN}{username}")
                    print(f"{Fore.YELLOW}Password: {Fore.GREEN}{password}")
                    print(f"{Fore.YELLOW}Hash: {Fore.MAGENTA}{password_hash}")
                    print(f"{Style.RESET_ALL}{'-'*40}\n")
                    shadow_entry = f"{username}:{password_hash}"
                    shadow_entries.append(shadow_entry)
                    usernames.append(username)

            another = input(f"\n{Fore.CYAN}Would you like to generate more entries? (yes/no): {Style.RESET_ALL}").strip().lower()
            if another not in ["yes", "y"]:
                break

        except ValueError:
            print(f"{Fore.RED}Error: Please enter a valid number")
            continue

    if shadow_entries:
        gen_shadow(shadow_entries)
        gen_passwd(usernames)
        notify_completion()

def gen_pass_random(pass_len):
    char_sets = [string.ascii_letters, string.punctuation, string.digits]
    password = ''.join(random.choice(random.choice(char_sets)) for _ in range(pass_len))
    return password

def gen_simple_pass(num_words=2):
    try:
        with open(pass_file, 'r') as f:
            words = [word.strip().lower() for word in f.readlines() if word.strip()]
        if not words:
            print(f"{Fore.RED}Error: {pass_file} is empty")
            return ""
        selected_words = random.choices(words, k=num_words)
        passphrase = '-'.join(selected_words)
        return passphrase

    except FileNotFoundError:
        print(f"{Fore.RED}Error: {pass_file} not found")
        return ""
    except Exception as e:
        print(f"{Fore.RED}Error generating passphrase: {e}")
        return ""

def gen_username():
    try:
        with open(uname_file, 'r') as f:
            words = [word.strip().lower() for word in f.readlines() if word.strip()]
        if not words:
            print(f"{Fore.RED}Error: {uname_file} is empty")
            return ""
        selected_words = random.choices(words, k=2)
        username = '-'.join(selected_words)
        return username

    except FileNotFoundError:
        print(f"{Fore.RED}Error: {uname_file} not found")
        return ""
    except Exception as e:
        print(f"{Fore.RED}Error generating username: {e}")
        return ""

def gen_hash(password):
    password_hash = sha512_crypt.using(rounds=5000).hash(password)
    return password_hash

def gen_hard_pass(pass_len):
    username = gen_pass_random(pass_len)
    password = gen_pass_random(pass_len)
    password_hash = gen_hash(password)

    print(f"\n{Fore.YELLOW}Username: {Fore.CYAN}{username}")
    print(f"{Fore.YELLOW}Password: {Fore.GREEN}{password}")
    print(f"{Fore.YELLOW}Hash: {Fore.MAGENTA}{password_hash}")
    print(f"{Style.RESET_ALL}{'-'*40}\n")

    shadow_entry = f"{username}:{password_hash}"
    return shadow_entry, username    # Now returns username too

def gen_shadow(shadow_entries):
    try:
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "w") as f:
            for entry in shadow_entries:
                f.write(entry + "\n")
        abs_path = os.path.abspath(file_name)
        print(f"\n{Fore.CYAN}Text file saved at: {Fore.YELLOW}{abs_path}{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error writing file: {e}")

def gen_passwd(usernames):
    try:
        os.makedirs(os.path.dirname(passwd_file), exist_ok=True)
        passwd_lines = []
        starting_uid = 1001
        starting_gid = 1001
        for i, username in enumerate(usernames):
            uid = starting_uid + i
            gid = starting_gid + i
            gecos = f"{username.capitalize()} User"
            homedir = f"/home/{username}"
            shell = "/bin/bash"
            entry = f"{username}:x:{uid}:{gid}:{gecos}:{homedir}:{shell}"
            passwd_lines.append(entry)
        with open(passwd_file, "w") as f:
            for line in passwd_lines:
                f.write(line + "\n")
        abs_path = os.path.abspath(passwd_file)
        print(f"\n{Fore.CYAN}/etc/passwd file saved at: {Fore.YELLOW}{abs_path}{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error writing passwd file: {e}")

def notify_completion():
    abs_path = os.path.abspath(file_name)
    folder_path = os.path.dirname(abs_path)

    print("\n" + "=" * 60)
    print(f"{Fore.GREEN}Shadow Generator process completed successfully!")
    print(f"{Fore.CYAN}File location: {Fore.YELLOW}{abs_path}{Style.RESET_ALL}")
    print("=" * 60)

    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", folder_path])
        else:
            subprocess.Popen(["xdg-open", folder_path])
    except Exception as e:
        print(f"\n{Fore.RED}Could not automatically open folder. Here is the directory:")
        print(f"Folder path: {folder_path}")

if __name__ == "__main__":
    cli()
