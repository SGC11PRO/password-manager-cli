# Password Manager CLI

A command-line password manager built with Python to learn and apply core cryptography concepts: key derivation, symmetric encryption, and secure password hashing.

Built as a learning project ahead of starting a Computer Engineering degree, with a focus on cybersecurity.

---

## Overview

This tool lets you store and retrieve passwords for different services (e.g. email, streaming platforms) behind a single master password. None of your saved passwords — or your master password — are ever stored in plain text.

- Your **master password** is never saved anywhere. Only a hash of it is stored, used solely to verify future logins.
- Your **saved passwords** are encrypted before being written to disk, and only decrypted in memory when you choose to view them.
- All cryptographic operations rely on Python's [`cryptography`](https://cryptography.io/) library — no custom-built crypto.

## Features

- Create a master password on first run, protected by a salted hash
- Add new passwords for any service, encrypted at rest
- View a previously saved password, decrypted on demand
- List all services currently stored in the vault
- Persistent local storage in a single JSON file (`vault.json`)

## How it works

| Step | Technique used | Why |
|---|---|---|
| Master password storage | SHA-256 hash + salt | Never needs to be reversed, only verified |
| Encryption key generation | PBKDF2-HMAC-SHA256, 480,000 iterations | Slows down brute-force attacks on the master password (OWASP recommendation) |
| Saved password storage | Fernet (AES-based symmetric encryption) | Needs to be reversible to retrieve the original password |
| Randomness | `os.urandom` | Cryptographically secure, unlike Python's `random` module |

Each user's salt is unique and stored in plain text alongside the vault — this is standard practice. The salt doesn't need to be secret; it only needs to be unique, so that identical master passwords across different vaults never produce identical cryptographic keys.

## Project structure

```
password-manager-cli/
│
├── main.py                 # CLI entry point and menu logic
├── src/
│   ├── crypto_utils.py     # Key derivation, hashing, encryption/decryption
│   └── storage.py          # Reading/writing the vault to disk
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Getting started

### Requirements

- Python 3.10+

### Installation

```bash
git clone https://github.com/SGC11PRO/password-manager-cli.git
cd password-manager-cli

python -m venv venv

venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

On first run, you'll be asked to create a master password. On subsequent runs, you'll be asked to enter it to unlock your vault. From there, a simple menu lets you add, view, and list stored passwords.

> **IMPORTANT**
> If is already an existing vault.json file, delete it, so you can set up your own vault with your own master password. If not, you won't be able to access the existing vault without the correct master password.

## What I learned building this

This project was my introduction to applied cryptography before starting my degree. Some of the key takeaways:

- The practical difference between **encryption** (reversible) and **hashing** (irreversible), and when to use each
- Why **salts** matter, and why they don't need to be secret
- Why key derivation functions like **PBKDF2** deliberately slow down computation
- Safe randomness (`os.urandom`) vs. unsafe randomness (`random`) in a security context
- Structuring a Python project with separation of concerns (crypto logic, storage, and UI in separate modules)

## Disclaimer

This project was built for educational purposes, to understand how password managers work under the hood. For real-world password management, use an established, audited tool such as [Bitwarden](https://bitwarden.com/) or [KeePass](https://keepass.info/).

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
