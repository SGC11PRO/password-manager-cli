import getpass
import sys
from src import crypto_utils
from src import storage

VAULT_FILE = "vault.json"

def create_new_vault() -> tuple[bytes, str, dict]:
    """
    Guía al usuario en la creación de una contraseña maestra nueva
    y devuelve el salt, el hash y el diccionario de contraseñas vacío.
    """
    print("No se encontró ninguna bóveda. Vamos a crear una nueva.")
    master_password = getpass.getpass("Crea tu contraseña maestra: ")
    confirm = getpass.getpass("Confírmala de nuevo: ")

    if master_password != confirm:
        print("Las contraseñas no coinciden. Inténtalo de nuevo.")
        sys.exit(1)

    salt = crypto_utils.generate_salt()
    master_hash = crypto_utils.hash_master_password(master_password, salt)
    passwords = {}

    storage.save_vault(VAULT_FILE, salt, master_hash, passwords)
    print("Bóveda creada correctamente.\n")

    return salt, master_hash, passwords

def load_existing_vault() -> tuple[bytes, str, bytes, dict]:
    """
    Pide la contraseña maestra, la verifica, y devuelve todo lo necesario
    para trabajar con la bóveda sin volver a leer el archivo.
    """
    vault_data = storage.load_vault(VAULT_FILE)
    master_password = getpass.getpass("Introduce tu contraseña maestra: ")

    entered_hash = crypto_utils.hash_master_password(master_password, vault_data["salt"])

    if entered_hash != vault_data["master_hash"]:
        print("Contraseña maestra incorrecta.")
        sys.exit(1)

    key = crypto_utils.derive_key(master_password, vault_data["salt"])
    print("Acceso correcto.\n")

    return vault_data["salt"], vault_data["master_hash"], key, vault_data["passwords"]

def add_password(key: bytes, passwords: dict) -> None:
    """
    Pide un servicio y una contraseña, la cifra, y la añade al diccionario.
    """
    service = input("Nombre del servicio (ej. Netflix): ").strip()
    password = getpass.getpass(f"Contraseña para {service}: ")

    encrypted = crypto_utils.encrypt_password(password, key)
    passwords[service] = encrypted

    print(f"Contraseña de '{service}' guardada correctamente.\n")


def view_password(key: bytes, passwords: dict) -> None:
    """
    Pide un servicio y muestra su contraseña descifrada, si existe.
    """
    service = input("¿Qué servicio quieres ver?: ").strip()

    if service not in passwords:
        print(f"No hay ninguna contraseña guardada para '{service}'.\n")
        return

    decrypted = crypto_utils.decrypt_password(passwords[service], key)
    print(f"Contraseña de '{service}': {decrypted}\n")
    

def main() -> None:
    if storage.vault_exists(VAULT_FILE):
        salt, master_hash, key, passwords = load_existing_vault()
    else:
        salt, master_hash, passwords = create_new_vault()
        master_password = getpass.getpass("Vuelve a introducir tu contraseña maestra para continuar: ")
        key = crypto_utils.derive_key(master_password, salt)

    while True:
        print("1. Añadir contraseña")
        print("2. Ver contraseña")
        print("3. Listar servicios guardados")
        print("4. Salir")
        choice = input("Elige una opción: ").strip()

        if choice == "1":
            add_password(key, passwords)
            storage.save_vault(VAULT_FILE, salt, master_hash, passwords)
        elif choice == "2":
            view_password(key, passwords)
        elif choice == "3":
            if passwords:
                print("Servicios guardados:", ", ".join(passwords.keys()), "\n")
            else:
                print("No hay ninguna contraseña guardada todavía.\n")
        elif choice == "4":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.\n")


if __name__ == "__main__":
    main()