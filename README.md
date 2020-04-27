# osrs_acc_creator
Account creator personal project for the game Old School Runescape

Uses requests to create Old School Runescape accounts with 2captcha integration to bypass Recaptcha as well as proxy support.

Tutorial Video: https://www.youtube.com/watch?v=siFrapgOrIA

_____________________________________________________________________
Requirements:

Download python 3.x from https://www.python.org/downloads/

Make sure python is added to PATH

After Python is installed, open cmd/powershell and run: 

pip install requests

pip install requests[socks]

HOW TO USE:

1. Put acc_creator.py, my_utilities.py, proxy_list.txt, created_accs.txt, and settings.ini in the same folder.

2. Open, edit, and save settings.ini to fit your use case.
  
  2.1. YOU MUST add a 2captcha API key to the settings file (2captcha.com -> add $3 to your account -> paste API key from your account page to the settings file and save.)
  
  2.2. If you get an error when running acc_creator 'list index out of range', you didn't add a valid 2captcha api key to settings

3. Add your list of proxies to proxy_list.txt if applicable.

4. Open the folder with the files and shift+right click in the folder and click "Open powershell here"
  
  4.1. Run the command: python acc_creator.py

5. List of created accounts will save to created_accs.txt
