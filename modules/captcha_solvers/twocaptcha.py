"""Solves the repcatcha for account creation using the 2captcha service"""
from time import sleep
try:
    import requests
    from modules.helper_modules.utility import get_site_settings, get_user_settings
except ImportError as error:
    print(error)


def twocaptcha_solver():
    """Handles and returns recaptcha answer for osrs account creation page"""
    SITE_URL = get_site_settings()[1]
    SITE_KEY = get_site_settings()[0]  # osrs site key
    API_KEY = get_user_settings()[3]  # api key read from settings.ini
    if not API_KEY:
        raise ValueError("No API key was found in settings.ini.")


    s = requests.Session()

    # here we post and parse site key to 2captcha to get captcha ID
    try:
        captcha_id = s.post(f"http://2captcha.com/in.php?key={API_KEY}"
                            f"&method=userrecaptcha&googlekey={SITE_KEY}"
                            f"&pageurl={SITE_URL}").text.split('|')[1]
    except IndexError:
        print("You likely don't have a valid 2captcha.com API key with funds"
              " in your settings.ini file. Fix and re-run the program.")

    # then we parse gresponse from 2captcha response
    recaptcha_answer = s.get(
        f"http://2captcha.com/res.php?key={API_KEY}"
        f"&action=get&id={captcha_id}").text
    print("Solving captcha...")
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        sleep(6)
        recaptcha_answer = s.get(
            f"http://2captcha.com/res.php?key={API_KEY}"
            f"&action=get&id={captcha_id}").text
    try:
        recaptcha_answer = recaptcha_answer.split('|')[1]
    except IndexError:
        print("2captcha failed to solve this one.. Returning a blank response "
              "If the program fails to continue, please msg Gavin with error.")
        recaptcha_answer = ''
    else:
        return recaptcha_answer