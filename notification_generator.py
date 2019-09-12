#!/usr/bin/env python
# coding: utf-8

# In[28]:

from dotenv import load_dotenv
load_dotenv()

import os
LOGIN_EMAIL_ID = os.getenv("MY_LOGIN_EMAIL_ID")
PASSWORD = os.getenv("MY_PASSWORD")
usr = os.getenv("PORTAL_USR")
pwd = os.getenv("PORTAL_PWD")
POST_ID_FILENAME = 'recent_post.txt'
LOGGING_FILENAME = 'spo_portal_notification.log'
# CURR_DIR = os.getcwd()
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
POST_ID_PATH = os.path.join(CURR_DIR, POST_ID_FILENAME)
LOGGING_PATH = os.path.join(CURR_DIR, LOGGING_FILENAME)
print(POST_ID_PATH, LOGGING_PATH)


# In[14]:


import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import sys
import os
import logging
logging.basicConfig(filename=LOGGING_PATH,level=logging.INFO,format='%(asctime)s %(message)s')
print('logging')


# In[15]:
options = Options()
options.headless = True
driver=webdriver.Chrome(options=options)
# driver=webdriver.Chrome()
driver.get('https://placement.iitk.ac.in/')
logging.info('connected with placement.iitk')
print('log: connected with placement.iitk')

# In[16]:


driver.find_element_by_id('id_username').send_keys(usr)
driver.find_element_by_id('id_password').send_keys(pwd)


# In[17]:


driver.find_element_by_css_selector("input.btn").click()
logging.info('signed in')
print('log: signed in')


# In[18]:


recent_post = driver.find_element_by_css_selector('div.panel-collapse.collapse')
recent_post_id = recent_post.get_attribute('id')
recent_post_id = recent_post_id.split('collapse')[1]
logging.info('Post ID: %s', recent_post_id)
print('Post ID: ', recent_post_id)


# In[19]:


if os.path.exists(POST_ID_PATH):
    f = open(POST_ID_PATH, 'r')
    prev_id = int(f.read())
    f.close()
else:
    f = open(POST_ID_PATH, 'w')
    prev_id = 0
    f.write(str(prev_id))
    f.close()
print('Prev ID: ', prev_id)


# In[20]:


curr_id = int(recent_post_id)
print('Curr ID: ', curr_id)


# In[ ]:





# In[21]:


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def notify_usr():
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(LOGIN_EMAIL_ID, PASSWORD)
    
    msg = MIMEMultipart()
    message = 'You have new notifications!'
    msg['From'] = LOGIN_EMAIL_ID
    msg['To'] = 'pkarthic@iitk.ac.in'
    msg['Subject'] = 'Placement iitk'

    msg.attach(MIMEText(message, 'plain'))

    s.send_message(msg)


# In[ ]:





# In[22]:


if curr_id > prev_id:
    f = open(POST_ID_PATH, 'w')
    f.write(str(curr_id))
    f.close()

    notify_usr()
    logging.info('user notified')
    print('user notified')

driver.quit()
# In[23]:


# f = open(POST_ID_PATH, 'w')
# f.write(str(0))
# f.close()


# In[ ]:




