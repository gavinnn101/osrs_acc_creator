"""
Solves and returns the captcha answer via the anti-captcha.com service
Documentation: https://pypi.org/project/python-anticaptcha/
Requirements: pip install python-anticaptcha
"""
import sys
try:
    from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask, AnticaptchaException
    from modules.helper_modules.utility import get_site_settings, get_user_settings
except ImportError as error:
    print(error)



SITE_URL = get_site_settings()[1]
SITE_KEY = get_site_settings()[0]  # osrs site key
API_KEY = get_user_settings()[3]  # api key read from settings.ini

def anticaptcha_solver():
    """Solves repcatcha via AntiCaptcha service"""
    print("Solving captcha, please wait...")
    client = AnticaptchaClient(API_KEY)
    task = NoCaptchaTaskProxylessTask(SITE_URL, SITE_KEY, is_invisible=True)
    
    while True:
        try:
            try:
                job = client.createTask(task)
            except AnticaptchaException as e:
                print(e)
                if e.error_id(2):
                    print("No captcha solver available.. Retrying.")
                    return True
                else:
                    raise
            else:
                job.join()
                print('Captcha solved. Continuing.')
                return job.get_solution_response(), False
        except AnticaptchaException:
            sys.exit(AnticaptchaException)