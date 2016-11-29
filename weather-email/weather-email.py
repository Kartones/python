#!/usr/bin/python
# coding: utf-8

import requests
import json
import smtplib
import datetime

import config


def send_mail(recipients, subject, body):
    headers = [
        "From: " + config.MAIL_SENDER,
        "Subject: " + subject,
        "To: " + (', '.join(recipients) if isinstance(recipients, list) else recipients),
        "MIME-Version: 1.0",
        "Content-Type: text/html"
    ]
    headers = "\r\n".join(headers)
    session = smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT)
    session.ehlo()
    session.starttls()
    session.login(config.MAIL_USER, config.MAIL_PASSWORD)
    session.sendmail(config.MAIL_SENDER, recipients, headers + "\r\n\r\n" + body)
    session.quit()


#  https://developer.yahoo.com/weather/
def query_weather(woeid):
    payload = {
        'q': 'select * from weather.forecast where woeid in ({}) and u="c"'.format(woeid),
        'format': 'json'
    }
    response = requests.get('https://query.yahooapis.com/v1/public/yql', params=payload)
    return json.loads(response.text)


def setup_mail_data(weather_data):
    recipients = config.MAIL_RECIPIENTS
    item = weather_data['query']['results']['channel']['item']
    item['description'] = item['description'].replace('<![CDATA[', '').replace(']]>', '')
    subject = "Madrid weather forecast - {}".format(datetime.date.today())
    body = "{} {}".format(item['title'], item['description'])
    return recipients, subject, body


def main():
    # Selecting place:  select woeid from geo.places(1) where text="madrid, spain"
    madrid_woeid = '766273'
    data = query_weather(woeid=madrid_woeid)
    recipients, subject, body = setup_mail_data(data)
    send_mail(recipients=recipients, subject=subject, body=body)


if __name__ == "__main__":
    main()
