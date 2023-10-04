#!/usr/bin/env python
import os
import smtplib
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

POST_ID_FILENAME = 'recent_post.txt',
LOGGING_FILENAME = 'spo_portal_notification.log'

def read_dotenv():
    return {
        'EMAIL_ID': os.getenv("EMAIL_ID"),
        'EMAIL_PWD': os.getenv("EMAIL_PWD"),
        'PORTAL_USR': os.getenv("PORTAL_USR"),
        'PORTAL_PWD': os.getenv("PORTAL_PWD")
    }

def setup_logging(log_path):
    logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(message)s')
    print('Logging initialized')

def get_previous_post_id(post_id_path):
    if os.path.exists(post_id_path):
        with open(post_id_path, 'r') as f:
            prev_id = int(f.read())
        return prev_id
    else:
        with open(post_id_path, 'w') as f:
            f.write(str(0))
        return 0

def update_post_id(post_id_path, new_id):
    with open(post_id_path, 'w') as f:
        f.write(str(new_id))

def notify_user(email, password):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(email, password)
    
    msg = MIMEMultipart()
    message = 'You have new notifications!'
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Placement iitk!!'
    
    msg.attach(MIMEText(message, 'plain'))
    
    s.send_message(msg)
    s.quit()

def main():
    # load SPO portal login and email login details from ENV variables
    load_dotenv()
    env = read_dotenv()

    # set paths for logging test and interview schedules
    CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    POST_ID_PATH = os.path.join(CURR_DIR, POST_ID_FILENAME)
    LOGGING_PATH = os.path.join(CURR_DIR, LOGGING_FILENAME)

    setup_logging(LOGGING_PATH)

    # initialize options to run chrome
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    try:
        # go to placement site
        driver.get('https://placement.iitk.ac.in/')
        logging.info('Connected with placement.iitk')

        # login
        driver.find_element_by_id('id_username').send_keys(env['PORTAL_USR'])
        driver.find_element_by_id('id_password').send_keys(env['PORTAL_PWD'])

        driver.find_element_by_css_selector("input.btn").click()
        logging.info('Signed in')

        # get most recent tests/interviews
        recent_post = driver.find_element_by_css_selector('div.panel-collapse.collapse')
        recent_post_id = recent_post.get_attribute('id').split('collapse')[1]
        logging.info('Post ID: %s', recent_post_id)

        # get previous test/interview received
        prev_id = get_previous_post_id(POST_ID_PATH)
        logging.info('Previous ID: %s', prev_id)
        
        curr_id = int(recent_post_id)
        logging.info('Current ID: %s', curr_id)

        # send email if previous test/interview differs from most recent one
        if curr_id > prev_id:
            update_post_id(POST_ID_PATH, curr_id)
            notify_user(env['EMAIL_ID'], env['EMAIL_PWD'])
            logging.info('User notified')
    
    except Exception as e:
        logging.error('An error occurred: %s', str(e))
    
    finally:
        # quit driver (even during unexpected exits)
        driver.quit()

if __name__ == "__main__":
    main()
