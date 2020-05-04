# osrs_acc_creator
Account creator personal project for the game Old School Runescape

Uses requests to create Old School Runescape accounts with 2captcha/anticaptcha integration to bypass Recaptcha, proxy support, and Tribot and OSBot CLI integration.

Tutorial Video: https://www.youtube.com/watch?v=siFrapgOrIA

Discord: GaviNNN#3281

twocaptcha.com referral: https://2captcha.com?from=8817486

anticaptcha.com referral: http://getcaptchasolution.com/njbmecwjpo

_____________________________________________________________________
Requirements:

Download python 3.x from https://www.python.org/downloads/

Make sure python is added to PATH during installation!(Bottom left corner checkbox)

After Python is installed, open cmd/powershell and run: 

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

pip install requests

pip install requests[socks]

pip install python-anticaptcha

HOW TO USE:

1. Download the git repo folder with all of the files and place the folder on your desktop

2. Open, edit, and save settings.ini to fit your use case.
  
  2.1. YOU MUST add a 2captcha or AntiCaptcha API key to the settings file (2captcha.com or anticaptcha.com -> add $3-10 to your account -> paste API key from your account page to the settings file and save.)

3. Add your list of proxies to proxy_list.txt if applicable.

4. Open the folder with the files and shift+right click in the folder and click "Open powershell here"
  
  4.1. Run the command: python acc_creator.py

5. List of created accounts will save to created_accs.txt
