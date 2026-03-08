# ============================================================
#   PYTHON FILE ENCRYPTION & DECRYPTION — Task 2 (Level 3)
#   Methods : Caesar Cipher + Fernet Encryption
#   Features: Encrypt file, Decrypt file, Save as new file
# ============================================================
#
#   BEFORE RUNNING install library (for Fernet only):
#       pip install cryptography
#
#   Caesar Cipher works with NO extra libraries!
#
# ============================================================

import os
import string
from datetime import datetime

# Colors
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_success(msg): print(f"{GREEN}✅ {msg}{RESET}")
def print_error(msg):   print(f"{RED}❌ {msg}{RESET}")
def print_info(msg):    print(f"{YELLOW}ℹ️  {msg}{RESET}")
def print_section(msg): print(f"\n{BLUE}{BOLD}{'═'*52}\n   {msg}\n{'═'*52}{RESET}")


# ============================================================
#   METHOD 1 — CAESAR CIPHER
#   Shifts every letter by a key number
#   Example: key=3, A→D, B→E, Z→C
# ============================================================

def caesar_encrypt(text, key):
    """Encrypt text using Caesar Cipher"""
    result = []
    key    = key % 26   # keep key in range 0-25

    for char in text:
        if char.isalpha():
            # Shift uppercase letters
            if char.isupper():
                shifted = chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            # Shift lowercase letters
            else:
                shifted = chr((ord(char) - ord('a') + key) % 26 + ord('a'))
            result.append(shifted)
        else:
            result.append(char)   # keep numbers, spaces, symbols unchanged

    return ''.join(result)


def caesar_decrypt(text, key):
    """Decrypt Caesar Cipher — just shift backwards"""
    return caesar_encrypt(text, -key)


# ============================================================
#   METHOD 2 — FERNET ENCRYPTION
#   Real military-grade encryption using cryptography library
# ============================================================

def generate_fernet_key():
    """Generate a new encryption key and save it"""
    try:
        from cryptography.fernet import Fernet
        key      = Fernet.generate_key()
        key_file = "encryption_key.key"

        with open(key_file, "wb") as f:
            f.write(key)

        print_success(f"New encryption key saved to '{key_file}'")
        print_info("IMPORTANT: Keep this key file safe! You need it to decrypt!")
        return key

    except ImportError:
        print_error("cryptography library not found!")
        print_info("Run: pip install cryptography")
        return None


def load_fernet_key():
    """Load existing encryption key from file"""
    key_file = "encryption_key.key"

    if not os.path.exists(key_file):
        print_info("No key found. Generating new key...")
        return generate_fernet_key()

    with open(key_file, "rb") as f:
        return f.read()


def fernet_encrypt(text, key):
    """Encrypt text using Fernet"""
    try:
        from cryptography.fernet import Fernet
        f         = Fernet(key)
        encrypted = f.encrypt(text.encode('utf-8'))
        return encrypted.decode('utf-8')
    except ImportError:
        print_error("cryptography library not installed!")
        print_info("Run: pip install cryptography")
        return None


def fernet_decrypt(text, key):
    """Decrypt Fernet encrypted text"""
    try:
        from cryptography.fernet import Fernet
        from cryptography.fernet import InvalidToken
        f = Fernet(key)
        decrypted = f.decrypt(text.encode('utf-8'))
        return decrypted.decode('utf-8')
    except ImportError:
        print_error("cryptography library not installed!")
        return None
    except Exception:
        print_error("Decryption failed! Wrong key or corrupted file.")
        return None


# ============================================================
#   FILE OPERATIONS
# ============================================================

def read_file(filepath):
    """Read content from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print_success(f"File read: '{filepath}' ({len(content)} characters)")
        return content
    except FileNotFoundError:
        print_error(f"File not found: '{filepath}'")
        return None
    except PermissionError:
        print_error(f"Permission denied: '{filepath}'")
        return None
    except Exception as e:
        print_error(f"Error reading file: {e}")
        return None


def save_file(content, filepath):
    """Save content to a file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        size = os.path.getsize(filepath)
        print_success(f"Saved to '{filepath}' ({size} bytes)")
        return True
    except PermissionError:
        print_error(f"Permission denied to save: '{filepath}'")
        return False
    except Exception as e:
        print_error(f"Error saving file: {e}")
        return False


def generate_output_filename(input_file, action, method):
    """Generate a smart output filename"""
    name, ext  = os.path.splitext(input_file)
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag        = "encrypted" if action == "encrypt" else "decrypted"
    return f"{name}_{tag}_{method}_{timestamp}{ext}"


# ============================================================
#   MAIN ENCRYPT FUNCTION
# ============================================================

def encrypt_file():
    print_section("ENCRYPT A FILE")

    # Step 1: Get input file
    filepath = input("\n  Enter file path to encrypt: ").strip()
    if not filepath:
        print_error("File path cannot be empty!")
        return

    content = read_file(filepath)
    if content is None:
        return

    # Show preview
    preview = content[:100] + "..." if len(content) > 100 else content
    print(f"\n  {CYAN}Preview of original content:{RESET}")
    print(f"  {preview}\n")

    # Step 2: Choose method
    print(f"  {BOLD}Choose encryption method:{RESET}")
    print("    1. Caesar Cipher  (simple, no extra library)")
    print("    2. Fernet         (strong, needs: pip install cryptography)")
    method_choice = input("\n  Enter choice (1/2): ").strip()

    if method_choice == "1":
        # Caesar Cipher
        try:
            key = int(input("  Enter shift key (1-25): ").strip())
            if not 1 <= key <= 25:
                print_error("Key must be between 1 and 25!")
                return
        except ValueError:
            print_error("Key must be a number!")
            return

        print_info("Encrypting with Caesar Cipher...")
        encrypted = caesar_encrypt(content, key)

        # Add header info
        header = (
            f"# CAESAR CIPHER ENCRYPTED FILE\n"
            f"# Key: {key}\n"
            f"# Encrypted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"# Original file: {filepath}\n"
            f"{'='*50}\n"
        )
        final_content = header + encrypted

        # Save
        output_file = generate_output_filename(filepath, "encrypt", "caesar")
        if save_file(final_content, output_file):
            print(f"\n  {CYAN}Preview of encrypted content:{RESET}")
            print(f"  {encrypted[:100]}...\n")
            print_success(f"File encrypted successfully!")
            print_info(f"Remember your key: {key}")
            print_info(f"You need key '{key}' to decrypt this file!")

    elif method_choice == "2":
        # Fernet Encryption
        print_info("Loading/generating encryption key...")
        key = load_fernet_key()
        if key is None:
            return

        print_info("Encrypting with Fernet (strong encryption)...")
        encrypted = fernet_encrypt(content, key)
        if encrypted is None:
            return

        # Add header
        header = (
            f"# FERNET ENCRYPTED FILE\n"
            f"# Encrypted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"# Original file: {filepath}\n"
            f"# Key file: encryption_key.key\n"
            f"{'='*50}\n"
        )
        final_content = header + encrypted

        output_file = generate_output_filename(filepath, "encrypt", "fernet")
        if save_file(final_content, output_file):
            print(f"\n  {CYAN}Preview of encrypted content:{RESET}")
            print(f"  {encrypted[:80]}...\n")
            print_success("File encrypted with strong Fernet encryption!")
            print_info("Key saved in 'encryption_key.key' — KEEP IT SAFE!")

    else:
        print_error("Invalid choice!")


# ============================================================
#   MAIN DECRYPT FUNCTION
# ============================================================

def decrypt_file():
    print_section("DECRYPT A FILE")

    # Step 1: Get encrypted file
    filepath = input("\n  Enter encrypted file path: ").strip()
    if not filepath:
        print_error("File path cannot be empty!")
        return

    content = read_file(filepath)
    if content is None:
        return

    # Remove header lines (lines starting with #)
    lines = content.split('\n')
    data_lines = []
    for line in lines:
        if not line.startswith('#') and not line.startswith('='):
            data_lines.append(line)
    encrypted_content = '\n'.join(data_lines).strip()

    # Step 2: Choose method
    print(f"\n  {BOLD}Choose decryption method:{RESET}")
    print("    1. Caesar Cipher")
    print("    2. Fernet")
    method_choice = input("\n  Enter choice (1/2): ").strip()

    if method_choice == "1":
        # Caesar Decrypt
        try:
            key = int(input("  Enter the shift key used for encryption: ").strip())
        except ValueError:
            print_error("Key must be a number!")
            return

        print_info("Decrypting with Caesar Cipher...")
        decrypted = caesar_decrypt(encrypted_content, key)

        output_file = generate_output_filename(filepath, "decrypt", "caesar")
        if save_file(decrypted, output_file):
            print(f"\n  {CYAN}Preview of decrypted content:{RESET}")
            preview = decrypted[:150] + "..." if len(decrypted) > 150 else decrypted
            print(f"  {preview}\n")
            print_success("File decrypted successfully!")

    elif method_choice == "2":
        # Fernet Decrypt
        print_info("Loading encryption key...")
        key = load_fernet_key()
        if key is None:
            return

        print_info("Decrypting with Fernet...")
        decrypted = fernet_decrypt(encrypted_content, key)
        if decrypted is None:
            return

        output_file = generate_output_filename(filepath, "decrypt", "fernet")
        if save_file(decrypted, output_file):
            print(f"\n  {CYAN}Preview of decrypted content:{RESET}")
            preview = decrypted[:150] + "..." if len(decrypted) > 150 else decrypted
            print(f"  {preview}\n")
            print_success("File decrypted successfully!")

    else:
        print_error("Invalid choice!")


# ============================================================
#   CREATE SAMPLE FILE FOR TESTING
# ============================================================

def create_sample_file():
    sample_content = """Hello! This is a sample text file for testing encryption.

My name is Python Developer.
I am learning file encryption using Python.

This file contains:
- Some personal information
- Secret project details
- Confidential data: 1234-5678-9012

After encryption, this content will be unreadable.
After decryption, it will come back exactly like this!

Python is amazing for security projects!
"""
    filename = "sample_file.txt"
    with open(filename, 'w') as f:
        f.write(sample_content)
    print_success(f"Sample file created: '{filename}'")
    print_info("You can now encrypt this file to test!")
    return filename


# ============================================================
#   SHOW HOW CAESAR CIPHER WORKS
# ============================================================

def show_caesar_demo():
    print_section("HOW CAESAR CIPHER WORKS")
    print(f"""
  {BOLD}Caesar Cipher shifts every letter by a fixed number:{RESET}

  Key = 3:
  A → D    B → E    C → F    ...    Z → C

  Example:
  Original : Hello World
  Key      : 3
  Encrypted: Khoor Zruog

  To decrypt: shift back by same key
  Khoor Zruog → Hello World
    """)

    test = input("  Enter a word to see live encryption (key=3): ").strip()
    if test:
        encrypted = caesar_encrypt(test, 3)
        decrypted = caesar_decrypt(encrypted, 3)
        print(f"\n  Original  : {CYAN}{test}{RESET}")
        print(f"  Encrypted : {RED}{encrypted}{RESET}")
        print(f"  Decrypted : {GREEN}{decrypted}{RESET}\n")


# ============================================================
#   MAIN MENU
# ============================================================

def main():
    print(f"""
{BLUE}{BOLD}
╔══════════════════════════════════════════════════╗
║       FILE ENCRYPTION & DECRYPTION TOOL         ║
║           Level 3 Task 2 — Python               ║
║                                                 ║
║  Method 1: Caesar Cipher  (simple)              ║
║  Method 2: Fernet         (strong, real-world)  ║
╚══════════════════════════════════════════════════╝
{RESET}""")

    while True:
        print(f"{BOLD}  MAIN MENU:{RESET}")
        print("    1. Encrypt a file")
        print("    2. Decrypt a file")
        print("    3. Create sample file for testing")
        print("    4. See how Caesar Cipher works (demo)")
        print("    5. Exit")

        choice = input(f"\n  Enter choice (1-5): ").strip()

        if choice == "1":
            encrypt_file()

        elif choice == "2":
            decrypt_file()

        elif choice == "3":
            create_sample_file()

        elif choice == "4":
            show_caesar_demo()

        elif choice == "5":
            print(f"\n{GREEN}{BOLD}  Goodbye! Stay secure! 🔐{RESET}\n")
            break

        else:
            print_error("Invalid choice! Enter 1-5.")

        print()


if __name__ == "__main__":
    main()
