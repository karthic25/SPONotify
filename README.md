# spo_notification_generator
## Introduction
Checks SPO (Students' Placement Office, IITK) site for information on new announcements / pre-placement talks / tests / interviews at regular intervals, notifies through e-mail

## Python3 packages used
These are the required packages, might need to be installed using
```sh
pip3 install <package-name>
```
- `python-dotenv` for managing environment variables
- `selenium` for automation of browser login
- `logging` to ease up debugging process
- `smtplib` for connecting to outlook (host e-mail account), sending message
- `email` for managing email format

Also, the chromedriver executable is required, for selenium to use (in a headless way) to initiale login. This can be downloaded at [this site](https://chromedriver.chromium.org/downloads).
## Install
This file is to be downloaded, and run using `crontab` for linux/mac users, `schtasks` for windows users

### Using crontab
Crontab entry is to be added to run the file regularly <br />
To edit crontab entries:
```sh
crontab -e
```
Add below cronjob after executing above command:
```
0 * * * * /path/to/python3 /path/to/notification_generator.py
```
To view crontab entries:
```sh
crontab -l
```

### Using schtasks
```sh
schtasks /create /sc hourly /st 00:00 /tn "Gen_Notif" /tr \path\to\python3 \path\to\notification_generator.py
```

## Configuring .env file
This file is to be stored locally in the same folder as the notification_generator.py. <br />
It should be populated with the following variables:
- `MY_LOGIN_EMAIL_ID`, `MY_PASSWORD` -> email and password to login into email account and send emails
- `PORTAL_USR`, `PORTAL_PWD` -> portal user-id and password

**Note:** the host email set is of Outlook. This can be changed to other hosts by changing the smtp url

## Issues that may pop up
#### crontab-based
PATH variable passed to crontab might not match! <br />
This might lead to python run command working in terminal, but not using crontab. <br />
To resolve this error, set your path before crontab entries (add below line before python execution command). <br />
```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```
For more crontab related issues visit [this page](https://askubuntu.com/questions/23009/why-crontab-scripts-are-not-working)
