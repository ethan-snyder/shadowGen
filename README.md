# shadowGen
A Python-based utility for generating Linux /etc/shadow format password hashes for educational purposes and authorized security training.

## Disclaimer
This tool is intended exclusively for:
* Educational purposes and learning environments
* Authorized security testing and penetration testing
* System administration and training scenarios
* Personal hash cracking practice in controlled environments

**Users are solely responsible** for ensuring they have explicit permission to use this tool on any systems or for any purpose. Unauthorized access to computer systems, networks, or data is illegal and unethical. This tool should only be used in environments where you own the systems or have written authorization from the system owner.
Purpose
shadowGen is a specialized tool designed to generate realistic Linux /etc/shadow file entries with SHA512 password hashes. The primary use case is for hash cracking training and practice, allowing security professionals and students to develop hash-breaking skills in a controlled, legal environment without compromising real systems.

# Installation
1. Ensure you have Python 3.7+.
2. Install the required packages from requirements.txt
3. Pull the repo

# Features
* **Two password generation modes**: Complex random passwords or simple word-based passphrases
* **Automated username generation**: Usernames are generated from a customizable wordlist
* **SHA512 hashing**: Uses SHA512 with 5000 rounds for Ubuntu/Linux compatibility
* **Batch generation**: Generate multiple username:hash pairs in a single session
* **Organized output**: Saves all entries to a shadow file in proper /etc/shadow format
* **Cross-platform support**: Works on Windows, macOS, and Linux

# Use Cases
* **Hash Cracking Practice**: Generate shadow entries to practice with tools like hashcat or John the Ripper
* **Security Training**: Create a safe environment for students to learn about password hashing
* **Testing**: Verify hash cracking tools and techniques in a controlled setting
* **Penetration Testing Labs**: Generate realistic data for authorized security testing environments

# Contributing
This tool is available for educational and authorized security testing purposes. Feel free to modify and adapt it for your specific training needs.

# Author
Ethan

# Disclaimer Reminder
**REMEMBER**: This tool should only be used in authorized and legal contexts. Unauthorized use is illegal. Always ensure you have explicit permission before practicing on any systems.
