from passlib.hash import sha512_crypt
import random
import string
import diceware
import os
import platform
import subprocess

# Public vars
file_name = "shadow.txt"


def cli():
    """Main CLI interface for Shadow Generator. Takes input from user regarding the preffered complexity of the password,
    and routes the functionality likewise."""
    print("Welcome to Shadow Generator")

    shadow_entries = []

    while True:
        print("\n1. Generate a random/complex password")
        print("2. Generate a simple password consisting of words")

        q1_input = input("\nPlease enter your choice (1 or 2): ").strip()

        if q1_input not in ["1", "2"]:
            print("Error: Invalid choice. Please enter 1 or 2")
            continue

        try:
            q2_input = int(input("\nPlease enter the number of password(s) you wish to generate: "))
            if q2_input <= 0:
                print("Error: Number of passwords must be positive")
                continue

            if q1_input == "1":  # Random/complex password flow
                pass_len = int(input("Please enter password length for your random/complex password: "))
                if pass_len <= 0:
                    print("Error: Password length must be positive")
                    continue
                for _ in range(q2_input):
                    shadow_entry = gen_hard_pass(pass_len)
                    shadow_entries.append(shadow_entry)

            elif q1_input == "2":  # Simple password flow
                num_words = int(input("Please enter number of words for your simple password: "))
                if num_words <= 0:
                    print("Error: Number of words must be positive")
                    continue
                for _ in range(q2_input):
                    password = gen_simple_pass(num_words)
                    print(f"Password: {password}")
                    password_hash = gen_hash(password)
                    username = input("Please enter a username: ").strip()
                    shadow_entry = f"{username}:{password_hash}"
                    shadow_entries.append(shadow_entry)

            # Ask if user wants to generate more entries
            another = input("\nWould you like to generate more entries? (yes/no): ").strip().lower()
            if another not in ["yes", "y"]:
                break

        except ValueError:
            print("Error: Please enter a valid number")
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
    """Generate a simple passphrase using diceware."""
    simple_pass = diceware.get_passphrase(num_words=num_words)
    return simple_pass


def gen_hash(password):
    """Generate SHA512 hash with 5000 rounds for shadow/Ubuntu format."""
    password_hash = sha512_crypt.using(rounds=5000).hash(password)
    print(f"SHA512 Hash: {password_hash}")
    return password_hash


def gen_hard_pass(pass_len):
    """Generate a username and password, then create shadow entry."""
    # Generate random username
    username = gen_pass_random(pass_len)
    print(f"Username: {username}")

    # Generate random password
    password = gen_pass_random(pass_len)
    print(f"Password: {password}")

    # Generate hash
    password_hash = gen_hash(password)

    # Create shadow entry
    shadow_entry = f"{username}:{password_hash}"
    return shadow_entry


def gen_shadow(shadow_entries):
    """Write shadow entries to file."""
    try:
        with open(file_name, "w") as f:
            for entry in shadow_entries:
                f.write(entry + "\n")
        abs_path = os.path.abspath(file_name)
        print(f"\nText file saved at: {abs_path}")
    except IOError as e:
        print(f"Error writing file: {e}")


def notify_completion():
    """Notify user of completion and open file directory."""
    abs_path = os.path.abspath(file_name)
    folder_path = os.path.dirname(abs_path)

    print("\n" + "=" * 60)
    print("Shadow Generator process completed successfully!")
    print(f"File location: {abs_path}")
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
        print(f"\nCould not automatically open folder. Here is the directory:")
        print(f"Folder path: {folder_path}")


if __name__ == "__main__":
    cli()