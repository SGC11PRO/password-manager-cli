import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

import hashlib

def generate_salt() -> bytes:
    """
    Genera un salt aleatorio y criptográficamente seguro de 16 bytes.
    """
    return os.urandom(16)

def derive_key(master_password: str, salt: bytes) -> bytes:
    # Deriva una clave de cifrado a partir de la contraseña maestra y un salt.
    # Usa PBKDF2 con SHA-256 y 480.000 iteraciones (recomendación de OWASP).
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    
    key_bytes = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key_bytes)

def encrypt_password (password: str, key: bytes) -> bytes:
    # Cifra una contraseña en texto plano usando la clave derivada.
    
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def decrypt_password (encrypted_password: bytes, key: bytes) -> str:
    # Descifra una contraseña previamente cifrada con la misma clave
    
    fernet = Fernet(key)
    decrypted_bytes = fernet.decrypt(encrypted_password)
    return decrypted_bytes.decode()


def hash_master_password (master_password: str, salt: bytes) -> str:
    # Genera un hash de la contraseña maestra para poder verificarla después, 
    # sin necesidad de guardar la contraseña real en ningún sitio.
    
    return hashlib.sha256(salt + master_password.encode()).hexdigest()