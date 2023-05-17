# Amazon Price Tracker

This is a Python script for tracking prices of products on Amazon. It periodically scrapes the prices of specified products and stores them in an SQLite database. It also sends email notifications when there are price changes or when the price remains the same.

## Prerequisites

- Python 3.x
- `requests-html` library
- `schedule` library
- `dotenv` library
- SMTP email account (e.g., Outlook/Office 365 account)

## Installation

1. Clone or download the repository.

2. Install the required Python libraries by running the following command:

   ```bash
   pip install requests-html schedule python-dotenv
   ```

3. Set up a .env file in the project directory and define the following environment variables:

sender_email: Email address of the sender (your SMTP email account)
sender_password: Password of the sender email account
receiver_email: Email address of the receiver

## Usage

- Prepare a CSV file named products.csv with the list of Amazon product IDs (ASINs) to track. Each ASIN should be listed on a separate line.

- Modify the scheduling settings in the script according to your preference. The schedule.every().day.at('19:16').do(check_price) line schedules the script to run daily at 19:16 (7:16 PM).

- The script will periodically scrape the prices of the specified products and store them in an SQLite database named tracker.db. It will also send email notifications to the specified receiver email address when there are price changes or when the price remains the same.

## Customization

- You can modify the scraping logic by adjusting the HTML element selectors in the check_price() function.
- You can customize the email notification messages in the send_email() and send_email_no_change() functions.
- Adjust the scheduling settings in the schedule.every().day.at('19:16').do(check_price) line to fit your preferred frequency and timing.
