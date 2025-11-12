import random
import string

from passlib.hash import sha512_crypt
import os
import platform
import subprocess

from colorama import Fore, Style, init
init(autoreset=True)

# Public vars
file_name = "output/shadow.txt"
pass_file = "textFiles/pass_file.txt"  # File containing dictionary words
uname_file = "textFiles/uname_file.txt"  # File containing username words


def cli():
    """Main CLI interface for Shadow Generator. Takes input from user regarding the preferred complexity of the password,
    and routes the functionality likewise."""
    print(f"{Style.BRIGHT}{Fore.BLUE}Welcome to Shadow Generator{Style.RESET_ALL}")

    # Check if wordlist files exist
    if not os.path.exists(pass_file):
        print(f"{Fore.RED}Error: {pass_file} not found. Please create a word list file first.")
        return
    if not os.path.exists(uname_file):
        print(f"{Fore.RED}Error: {uname_file} not found. Please create a username word list file first.")
        return

    shadow_entries = []

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

            if q1_input == "1":  # Random/complex password flow
                pass_len = int(input(f"{Fore.CYAN}Please enter password length for your random/complex password: {Style.RESET_ALL}"))
                if pass_len <= 0:
                    print(f"{Fore.RED}Error: Password length must be positive")
                    continue
                for _ in range(q2_input):
                    shadow_entry = gen_hard_pass(pass_len)
                    shadow_entries.append(shadow_entry)

            elif q1_input == "2":  # Simple password flow
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

            # Ask if user wants to generate more entries
            another = input(f"\n{Fore.CYAN}Would you like to generate more entries? (yes/no): {Style.RESET_ALL}").strip().lower()
            if another not in ["yes", "y"]:
                break

        except ValueError:
            print(f"{Fore.RED}Error: Please enter a valid number")
            continue

    # Write all entries to file and notify user
    if shadow_entries:
        gen_shadow(shadow_entries)
        notify_completion()


def gen_pass_random(pass_len):
    """Generate a random password with letters, punctuation, and digits."""
    char_sets = [string.ascii_letters, string.punctuation, string.digits]
    password = ''.join(random.choice(random.choice(char_sets)) for _ in range(pass_len))
    return password


def gen_simple_pass(num_words=2):
    """Generate simple passphrases by selecting random words from a word list file."""
    try:
        with open(pass_file, 'r') as f:
            words = [word.strip().lower() for word in f.readlines() if word.strip()]

        if not words:
            print(f"{Fore.RED}Error: {pass_file} is empty")
            return ""

        if len(words) < num_words:
            print(f"{Fore.YELLOW}Warning: Word list only contains {len(words)} words, but {num_words} requested")

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
    """Generate a username by selecting random words from the username word list file."""
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
    """Generate SHA512 hash with 5000 rounds for shadow/Ubuntu format."""
    password_hash = sha512_crypt.using(rounds=5000).hash(password)
    return password_hash


def gen_hard_pass(pass_len):
    """Generate a username and password, then create shadow entry, print nicely."""
    username = gen_pass_random(pass_len)
    password = gen_pass_random(pass_len)
    password_hash = gen_hash(password)

    print(f"\n{Fore.YELLOW}Username: {Fore.CYAN}{username}")
    print(f"{Fore.YELLOW}Password: {Fore.GREEN}{password}")
    print(f"{Fore.YELLOW}Hash: {Fore.MAGENTA}{password_hash}")
    print(f"{Style.RESET_ALL}{'-'*40}\n")

    shadow_entry = f"{username}:{password_hash}"
    return shadow_entry


def gen_shadow(shadow_entries):
    """Write shadow entries to file."""
    try:
        with open(file_name, "w") as f:
            for entry in shadow_entries:
                f.write(entry + "\n")
        abs_path = os.path.abspath(file_name)
        print(f"\n{Fore.CYAN}Text file saved at: {Fore.YELLOW}{abs_path}{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error writing file: {e}")


def notify_completion():
    """Notify user of completion and open file directory."""
    abs_path = os.path.abspath(file_name)
    folder_path = os.path.dirname(abs_path)

    print("\n" + "=" * 60)
    print(f"{Fore.GREEN}Shadow Generator process completed successfully!")
    print(f"{Fore.CYAN}File location: {Fore.YELLOW}{abs_path}{Style.RESET_ALL}")
    print("=" * 60)

    # Try to open the folder
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux and others
            subprocess.Popen(["xdg-open", folder_path])
    except Exception as e:
        print(f"\n{Fore.RED}Could not automatically open folder. Here is the directory:")
        print(f"Folder path: {folder_path}")


if __name__ == "__main__":
    cli()
