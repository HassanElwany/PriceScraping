from requests_html import HTMLSession
import csv
import time
import smtplib
import schedule
from dotenv import load_dotenv
import os
import sqlite3

conn = sqlite3.connect('tracker.db')

c = conn.cursor()


load_dotenv('.env')

previous_price = None

s = HTMLSession()

products = []

# open csv file and loop through it to get all products id
with open('products.csv', 'r') as f:
    file = csv.reader(f)
    for row in file:
        products.append(row[0])

    # print(products)


def check_price():
    global previous_price

    for product in products:

        r = s.get(f'https://www.amazon.sa/-/en/gp/product/{product}/')

        r.html.render(sleep=1)

        price = float(r.html.find(
            '.a-offscreen')[0].text.replace('SAR', '').replace(',', '').strip())
        title = r.html.find('#productTitle')[0].text.strip().split()

        # Create the prices table if it doesn't already exist
        conn.execute(
            ''' CREATE TABLE IF NOT EXISTS prices(title TEXT, price FLOAT)''')
        # Insert the new values of title and prices
        c.execute('''INSERT INTO prices(title, price) VALUES (?, ?)''',
                  (' '.join(title), price))
    conn.commit()

    c.execute("SELECT price FROM prices")
    results = c.fetchall()

    if results:
        for row in results:
            if previous_price is None:
                previous_price = row[0]
                send_email_no_change()
            elif previous_price < row[0]:
                send_email(row[0], ' '.join(title))
    else:
        print('Error')


def send_email(price, title):
    sender_email = os.getenv("sender_email")
    sender_password = os.getenv("sender_password")
    receiver_email = os.getenv("receiver_email")

    subject = 'Price Drop Alert!'

    body = f'The price of {title} your tracked product has dropped to {price}. Check it on Amazon!'

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)


def send_email_no_change():
    sender_email = os.getenv("sender_email")
    sender_password = os.getenv("sender_password")
    receiver_email = os.getenv("receiver_email")

    subject = 'Price has no change Alert!'

    body = f'The price is the same!'

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message)


schedule.every().day.at('19:29').do(check_price)


while True:
    schedule.run_pending()
    time.sleep(1)
