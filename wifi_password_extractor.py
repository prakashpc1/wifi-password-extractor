import subprocess
import os
import datetime

def list_wifi_profiles():
    cmd = ['netsh', 'wlan', 'show', 'profiles']
    output = subprocess.check_output(cmd).decode('latin-1')
    profiles = [line.split(":")[1].strip() for line in output.split('\n') if "All User Profile" in line]
    return profiles

def get_wifi_password(profile):
    cmd = ['netsh', 'wlan', 'show', 'profile', f'name={profile}', 'key=clear']
    try:
        output = subprocess.check_output(cmd).decode('latin-1')
        for line in output.split('\n'):
            if "Key Content" in line:
                return line.split(":")[1].strip()
        return None
    except:
        return None

def save_to_file(results):
    # Create filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'wifi_passwords_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        for ssid, password in results:
            f.write(f"[+] SSID: {ssid} | Password: {password}\n")
    
    print(f"\n[+] Results saved to: {os.path.abspath(filename)}")

if __name__ == "__main__":
    profiles = list_wifi_profiles()

    results = []
    for profile in profiles:
        password = get_wifi_password(profile)
        results.append((profile, password))

    print("\n[?] Show Wi-Fi passwords? (y/n): ", end="")
    choice = input().strip().lower()

    if choice == 'y':
        for ssid, password in results:
            print(f"[+] SSID: {ssid} | Password: {password}")
    else:
        print("[*] Wi-Fi passwords hidden.")
    
    # Always save to file
    save_to_file(results)

    input("\n[+] Press Enter to exit...")