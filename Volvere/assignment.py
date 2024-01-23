import os
import platform
import subprocess
import speedtest
import psutil
from screeninfo import get_monitors

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    return result.stdout.strip()


def get_installed_software():
    command = 'wmic product get name'
    return run_command(command).split('\n')[1:]


def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed

def get_screen_size():
    monitors = get_monitors()
    primary_monitor = monitors[0]
    return f"{primary_monitor.width}x{primary_monitor.height} pixels"


def get_system_info():
    system_info = {}
    #system_info['OS'] = platform.system()
    system_info['Windows Version'] = platform.version()
    system_info['Screen Resolution'] = run_command('wmic desktopmonitor get screenwidth,screenheight')
    system_info['CPU Model'] = platform.processor()
    system_info['No of Cores'] = psutil.cpu_count(logical=False)
    system_info['No of Threads'] = psutil.cpu_count(logical=True)
    system_info['GPU Model'] = run_command('wmic path win32_videocontroller get caption')[1:]
    system_info['RAM Size (GB)'] = round(psutil.virtual_memory().total / (1024 ** 3))
    system_info['Screen Size'] = get_screen_size()
    system_info['Wifi/Ethernet MAC Address'] = run_command('getmac')

    # Use 'findstr' instead of 'grep' for Windows
    system_info['Public IP Address'] = \
    run_command('nslookup myip.opendns.com. resolver1.opendns.com | findstr Address').split()[-1]

    return system_info


def main():
    installed_software = get_installed_software()

    try:
        internet_speed = get_internet_speed()
        print("\nInternet Speed:")
        print(f"Download Speed: {internet_speed[0]:.2f} Mbps")
        print(f"Upload Speed: {internet_speed[1]:.2f} Mbps")
    except speedtest.ConfigRetrievalError:
        print("\nUnable to retrieve Internet Speed information. Make sure 'speedtest-cli' is installed.")

    print("\nInstalled Software:")
    for software in installed_software:
        print(software)

    print("\nSystem Information:")
    for key, value in get_system_info().items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()