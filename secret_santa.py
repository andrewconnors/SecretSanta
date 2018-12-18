import pandas as pd
import sys
from string import Template
import smtpib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

try:
    if(len(sys.argv) <= 1):
        raise OSError()

    data = pd.read_csv(sys.argv[1], low_memory=False)
    names = data.Name
    emails = data.Email
    likes = data.Likes

    unshuffled_names = names
    random.shuffle(names)

    #need to verify every index was swapped
    reshuffle = True
    while(reshuffle):
        for i in len(names):
            if(unshuffled_names[i] == names[i]):
                reshuffle = True
                break
        reshuffle = False

    matches = {}

    for name,index in ennumerate(names):
        matches[name] = unshuffled_names[index]

    #email setup
    mail_server = smtplib.SMTP(host='', port='')
    mail_server.starttls()
    mail_server.login('connorsandrew1@gmail.com', '')
    message_template = read_template(sys.argv[2])

    for index,email in ennumerate(emails):
        msg = MIMEMultipart()

        message = message_template.substitute(
        PERSON_NAME=names[index],
        MATCHED_NAME=matches[names[index]],
        LIKES=likes[index]
        )

        msg['From']="connorsandrew1@gmail.com"
        msg['To']=email
        msg['Subject']="Open Happiness Secret Santa"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        mail_server.send_message(msg)

        del msg


except OSError as e:
    print("Whoops, Couldn't find that file.\n")
    print("Usage:\nRun python3 secret_santa.py name_of_file.csv\nFiles must be of csv format.\n")
    print("Merry Christmas :)")

def read_template(templatefile):
    with open(templatefile, 'r', encoding='utf-8') as template_file:
        content = template_file.read()
    return Template(content)
