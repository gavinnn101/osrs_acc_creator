"""Creates accounts based on settings.ini using our logic modules"""
#!/usr/bin/env python3

import random
import string
import sys
from socket import error as socket_error
import requests
try:
    from modules.helper_modules.utility import (get_index,
    get_user_settings, get_site_settings, get_tribot_settings, get_osbot_settings)
    from modules.captcha_solvers.twocaptcha import twocaptcha_solver
    from modules.captcha_solvers.anticaptcha import anticaptcha_solver
    from modules.bot_client_cli.tribot_cli import use_tribot
    from modules.bot_client_cli.osbot_cli import use_osbot
except ImportError as error:
    print(error)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.36'}
try:
    PROXY_LIST = open("settings/proxy_list.txt", "r")
except FileNotFoundError:
    sys.exit("proxy_list.txt wasn't found. "
             "Make sure it's in the same directory.")

# Settings pulled from utility.py -> settings.ini file
USE_PROXIES = get_user_settings()[0]
NUM_OF_ACCS = get_user_settings()[4]
SITE_URL = get_site_settings()[1]
TRIBOT_ACTIVE = get_tribot_settings()[0]
OSBOT_ACTIVE = get_osbot_settings()[0]



def get_ip() -> str:
    """
    Gets the user's external IP that will be used to create the account.
    Because of external dependency, we have a backup site to pull from if needed
    """
    users_ip = requests.get('https://api.ipify.org').text
    if not users_ip:
        users_ip = requests.get('http://ip.42.pl/raw').text
    return users_ip



def get_proxy() -> dict:
    """
    Returns our next proxy to use from the proxy_list.txt file.
    If we run out of proxies before we make all of the accounts, return to top.
    """
    try:
        proxy = {"https": (next(PROXY_LIST))}
        return proxy
    except StopIteration:
        # We'll return to the top of our list once we run out of proxies
        PROXY_LIST.seek(0)
        proxy = {"https": (next(PROXY_LIST))}
        return proxy



def access_page(proxy=None):
    """
    Sends a get request to our account creation url
    params:
    proxy (str): Proxy to use for get request (Default=None)
    returns:
    bool: True if the get request succeeds, false otherwise.
    """
    if USE_PROXIES:
        try:
            response = requests.get(SITE_URL, proxies=proxy, headers=HEADERS)
        except socket_error as error:
            print(error)
            print(f"Something with your proxy: {proxy} is likely bad.")
    else:
        response = requests.get(SITE_URL, headers=HEADERS)

    if response.ok:
        print("\nLoaded page successfully. Continuing.")
        return True
    else:
        print(f"Failed to load page. Status code: {response}")
        return False


def get_payload(captcha) -> dict:
    """
    Generates and fills out our payload.
    returns:
    payload (dict): account creation payload data
    """
    # Get username/password options from settings.ini
    email = get_user_settings()[5]
    password = get_user_settings()[6]

    if not email:  # We aren't using a custom username prefix -> make it random
        email = ''.join([random.choice(string.ascii_lowercase + string.digits)
                         for n in range(6)]) + '@gmail.com'
    else:  # We're using a custom prefix for our usernames
        email = email + str(random.randint(1000, 9999)) + '@gmail.com'

    if not password:
        password = email[:-10] + str(random.randint(1, 1000))

    # Generate random birthday for the account
    day = str(random.randint(1, 25))
    month = str(random.randint(1, 12))
    year = str(random.randint(1980, 2006))  # Be at least 13 years old

    payload = {
        'theme': 'oldschool',
        'email1': email,
        'onlyOneEmail': '1',
        'password1': password,
        'onlyOnePassword': '1',
        'day': day,
        'month': month,
        'year': year,
        'create-submit': 'create',
        'g-recaptcha-response': captcha
    }
    return payload


def check_account(submit):
    """Checks to make sure the account was successfully created"""
    submit_page = submit.text
    success = '<p>You can now begin your adventure with your new account.</p>'
    if success in submit_page:
        print("Account was successfully created.\n")
        return True
    elif 'Warning!' in submit_page: # If account creation fails, print the error
        print("\nAccount was not created successfully - error below:")
        error_text = submit_page[get_index(submit_page, 'Warning!', 1)+23:]
        error_text = error_text[:get_index(error_text, '<', 1)]
        print(error_text)
        return False
    else:
        print("Account was not created successfully "
              "and we weren't able to catch the error.. ")
        print("\nThis is very likely to be an unhandled captcha solve issue.")
        return False



def save_account(payload, proxy=None):
    """Save the needed account information to created_accs.txt"""
    if USE_PROXIES:
        proxy_auth_type = get_user_settings()[1]
        if proxy_auth_type == 1: # Formatting based on user:pass auth
            # Formatting our proxy string to only save the IP
            proxy = str(proxy)
            proxy = proxy[proxy.find('@')+1:]
            proxy = proxy[:proxy.find(':')]
        else: # Formatting based on IP authentication
            proxy = str(proxy)
            proxy = proxy[proxy.find('/')+2:]
            proxy = proxy[:proxy.find("'")]
    else:
        proxy = get_ip()

    # Check if we want user friendly formatting or bot manager friendly
    acc_details_format = get_user_settings()[7]
    if acc_details_format:
        formatted_payload = (f"\nemail:{payload['email1']}, password:{payload['password1']},"
                             f" Birthday:{payload['month']}/{payload['day']}/{payload['year']},"
                             f" Proxy:{proxy}")
    else:
        formatted_payload = (f"\n{payload['email1']}:{payload['password1']}")

    with open("created_accs.txt", "a+") as acc_list:
        acc_list.write(formatted_payload)
    if acc_details_format:
        print(f"Created account and saved to created_accs.txt"
              f" with the following details:{formatted_payload}")
    else:
        print(f"Created account and saved to created_accs.txt"
              f" with the following details: {formatted_payload}:{proxy}")


def create_account():
    """Creates our account and returns the registration info"""
    captcha_service = get_user_settings()[2]
    requests.session()
    if USE_PROXIES:
        proxy = get_proxy()
        if access_page(proxy):
            if captcha_service == 1:
                payload = get_payload(twocaptcha_solver())
            else:
                payload = get_payload(anticaptcha_solver())
            submit = requests.post(SITE_URL, data=payload, proxies=proxy)
            if submit.ok:
                if check_account(submit):
                    save_account(payload, proxy=proxy)
                    if TRIBOT_ACTIVE:
                        use_tribot(payload['email1'], payload['password1'], proxy)
                    elif OSBOT_ACTIVE:
                        use_osbot(payload['email1'], payload['password1'], proxy)
                else:
                    print("We submitted our account creation request "
                          "but didn't get to the creation successful page.")
                    print(submit.status_code)
            else:
                print(f"Creation failed. Error code {submit.status_code}")
    else:  # Not using proxies so we'll create the account(s) with our real IP
        if access_page():
            if captcha_service == 1:
                payload = get_payload(twocaptcha_solver())
            else:
                payload = get_payload(anticaptcha_solver())
            submit = requests.post(SITE_URL, data=payload)
            if submit.ok:
                if check_account(submit):
                    save_account(payload)
                    if TRIBOT_ACTIVE:
                        use_tribot(payload['email1'], payload['password1'])
                    elif OSBOT_ACTIVE:
                        use_osbot(payload['email1'], payload['password1'])
                else:
                    print("We submitted our account creation request "
                          "but didn't get to the creation successful page.")
                    print(submit.status_code)
            else:
                print(f"Creation failed. Error code {submit.status_code}")


def main():
    """Shows user info in the command line and runs the account creator"""
    counter = 0
    try:
        print(f"We'll make: {NUM_OF_ACCS} accounts.")
        print(f"Will we use proxies?: {USE_PROXIES}")
        print(f"Will we use Tribot CLI?: {TRIBOT_ACTIVE}")
        print(f"Will we use OSBot CLI?: {OSBOT_ACTIVE}")

        while counter < NUM_OF_ACCS:
            counter += 1
            create_account()
    except KeyboardInterrupt:
        print("User stopped the account creator.")


if __name__ == "__main__":
    main()