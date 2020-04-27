"""Contains all of the content to implement OSBot CLI"""
# OSBot CLI: https://osbot.org/forum/topic/118831-cli-commands-table/

import glob
import subprocess
try:
    from modules.helper_modules.utility import (get_user_settings, get_index,
    get_osbot_settings)
except ImportError as error:
    print(error)

def find_osbot():
    """Find the OSBot loader for CLI use"""
    client = str(glob.glob('OSBot*.jar'))
    client = client[2:-2]

    if not client:
        print("Couldn't find the OSBot loader. Make sure that it's in"
              " the same directory as the account creator!")
    else:
        print(f"Our OSBot client is called: {client}")

    return client

def format_current_proxy(proxy):
    """Formats and returns our current proxy for CLI use"""
    # Example returned proxy:
    # {'https': 'socks5://username:password@127.0.0.1:24613\n'}
    proxy = str(proxy)
    proxy_auth_type = get_user_settings()[1]
    # Formatting shenanigans to get the strings we need for CLI usage
    if proxy_auth_type == 1: # Formatting based on user:pass@proxy:port
        proxy_username = proxy[get_index(proxy, '/', 2)+1:get_index(proxy, ':', 3)]
        proxy_password = proxy[get_index(proxy, ':', 3)+1:get_index(proxy, '@', 1)]
        proxy_host = proxy[get_index(proxy, '@', 1)+1:get_index(proxy, ':', 4)]
        proxy_port = proxy[get_index(proxy, ':', 4)+1:get_index(proxy, "'", 4)-2]
        # Format for CLI use (ip:port:user:pass)
        proxy = (f"{proxy_host}:{proxy_port}:{proxy_username}:{proxy_password}")

        return proxy

    else: # Formatting based on proxy:port (IP authentication)
        proxy_host = proxy[get_index(proxy, '/', 2)+1:get_index(proxy, ':', 3)]
        proxy_port = proxy[get_index(proxy, ':', 3)+1:-4]
        # Format for CLI use (ip:port)
        proxy = (f"{proxy_host}:{proxy_port}")

        return proxy


def use_osbot(charname, charpass, proxy=None):
    """Launches OSBot CLI with supplies information"""
    # Grab all of our settings
    use_proxies = get_user_settings()[0]
    osbot_username = get_osbot_settings()[1]
    osbot_password = get_osbot_settings()[2]
    osbot_script = get_osbot_settings()[3]
    script_args = get_osbot_settings()[4]
    client = find_osbot()

    if use_proxies: # Format CLI with proxy param
        cli_cmd = (f'java -jar "{client}" '
                   f'-proxy {format_current_proxy(proxy)} '
                   f'-login {osbot_username}:{osbot_password} '
                   f'-bot {charname}:{charpass}:0000 '
                   f'-script {osbot_script}:{script_args} '
                   f'-world 433')
    else: # Format without a proxy param
        cli_cmd = (f'java -jar "{client}" '
                   f'-login {osbot_username}:{osbot_password} '
                   f'-bot {charname}:{charpass}:0000 '
                   f'-script {osbot_script}:{script_args} '
                   f'-world 433')

    print("")
    print("\nLoading OSBot with the following settings...")
    print(cli_cmd)

    # Run the OSBot CLI in a separate, hidden shell to decrease clutter
    create_no_window = 0x08000000
    subprocess.Popen(f"start /B start cmd.exe @cmd /k {cli_cmd}", shell=True,
                     creationflags=create_no_window)