import json
import os
import base64

def vault_exists (filepath: str) -> bool:
    # Comprueba si ya existe un archivo de bóveda (vault) en la ruta dada
    
    return os.path.isfile(filepath)

def save_vault (filepath: str, salt: bytes, master_hash: str, passwords: dict) -> None: 
    # Guarda el estado completo de la bóveda en un archivo JSON
    
    data = {
        "salt": base64.urlsafe_b64encode(salt).decode(),
        "master_hash": master_hash,
        "passwords": {
            service: encrypted.decode()
            for service, encrypted in passwords.items()
        },
    }
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
        
        
def load_vault (filepath: str) -> dict: 
    # Carga la bóveda desde el archivo JSON y devuelve sus datos,
    # reconstruyendo el salt y las contraseñas cifradas como bytes.
    
    with open(filepath, "r") as f:
        data = json.load(f)
        
    salt = base64.urlsafe_b64decode(data['salt'])
    passwords = {
        service: encrypted.encode()
        for service, encrypted in data['passwords'].items()
    }
    
    return {
        "salt": salt,
        "master_hash": data['master_hash'],
        "passwords": passwords,
    }
    