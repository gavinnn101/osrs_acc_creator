"""Module with utility functions"""
from configparser import ConfigParser
import sys

def get_index(input_string, sub_string, ordinal):
    """Returns the index of substring provided"""
    current = -1
    for _ in range(ordinal):
        current = input_string.index(sub_string, current + 1)
    return current


def read_proxy(proxy, proxy_auth_type):
	proxy = str(proxy)
	if proxy_auth_type == 1: # Formatting based on user:pass authentication

		proxy_username = proxy[get_index(proxy, '/', 2)+1:get_index(proxy, ':', 3)]
		proxy_password = proxy[get_index(proxy, ':', 3)+1:get_index(proxy, '@', 1)]
		proxy_ip = proxy[get_index(proxy, '@', 1)+1:get_index(proxy, ':', 4)]
		proxy_port = proxy[get_index(proxy, ':', 4)+1:get_index(proxy, '\\', 1)]

		return (proxy_username, proxy_password, proxy_ip, proxy_port)

	else: # Formatting based on IP authentication
		proxy_username = None
		proxy_password = None
		proxy_ip = proxy[get_index(proxy, '@', 1)+1:get_index(proxy, ':', 4)]
		proxy_port = proxy[get_index(proxy, ':', 4)+1:get_index(proxy, '\\', 1)]

		return (proxy_username, proxy_password, proxy_ip, proxy_port)


def get_user_settings():
    """Gets and returns the USER_SETTINGS from settings.ini"""
    config = ConfigParser()
    try:
        config.read('settings/settings.ini')
    except FileNotFoundError:
        sys.exit("settings.ini file not found. "
                 "Make sure it's in the same directory.")

    use_proxies = config['USER_SETTINGS'].getboolean('use_proxies')
    proxy_auth_type = config['USER_SETTINGS'].getint('proxy_auth_type')
    captcha_service = config['USER_SETTINGS'].getint('captcha_service')
    captcha_api_key = config['USER_SETTINGS'].get('captcha_api_key')
    num_of_accs = config['USER_SETTINGS'].getint('num_of_accs')
    username_prefix = config['USER_SETTINGS'].get('username_prefix')
    password = config['USER_SETTINGS'].get('password')
    acc_details_format = config['USER_SETTINGS'].getboolean('acc_details_format')

    return (use_proxies, proxy_auth_type,
            captcha_service, captcha_api_key,
            num_of_accs, username_prefix, password, acc_details_format)


def get_site_settings():
    """Return our [SITE_SETTINGS]"""
    config = ConfigParser()
    try:
        config.read('settings/settings.ini')
    except FileNotFoundError:
        sys.exit("settings.ini file not found. "
                 "Make sure it's in the same directory.")

    site_key = config['SITE_SETTINGS'].get('site_key')
    site_url = config['SITE_SETTINGS'].get('site_url')

    return site_key, site_url


def get_tribot_settings():
    """Return our [TRIBOT_CLI_SETTINGS]"""
    config = ConfigParser()
    try:
        config.read('settings/settings.ini')
    except FileNotFoundError:
        sys.exit("settings.ini file not found. "
                 "Make sure it's in the same directory.")

    use_tribot = config['TRIBOT_CLI_SETTINGS'].getboolean('use_tribot')
    tribot_username = config['TRIBOT_CLI_SETTINGS'].get('tribot_username')
    tribot_password = config['TRIBOT_CLI_SETTINGS'].get('tribot_password')
    tribot_script = config['TRIBOT_CLI_SETTINGS'].get('tribot_script')
    tribot_script_args = config['TRIBOT_CLI_SETTINGS'].get('script_args')

    return (use_tribot, tribot_username, tribot_password,
            tribot_script, tribot_script_args)


def get_osbot_settings():
    """Return our [OSBOT_CLI_SETTINGS]"""
    config = ConfigParser()
    try:
        config.read('settings/settings.ini')
    except FileNotFoundError:
        sys.exit("settings.ini file not found. "
                 "Make sure it's in the same directory.")

    use_osbot = config['OSBOT_CLI_SETTINGS'].getboolean('use_osbot')
    osbot_username = config['OSBOT_CLI_SETTINGS'].get('osbot_username')
    osbot_password = config['OSBOT_CLI_SETTINGS'].get('osbot_password')
    osbot_script = config['OSBOT_CLI_SETTINGS'].get('osbot_script')
    osbot_script_args = config['OSBOT_CLI_SETTINGS'].get('script_args')

    return (use_osbot, osbot_username, osbot_password,
            osbot_script, osbot_script_args)
