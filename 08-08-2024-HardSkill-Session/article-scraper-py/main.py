import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'C:\\Users\\alper\\Downloads\\medium-articles-419211-a53e34489baa.json'

def create_sheet(service, title):
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')

def update_sheet(service, spreadsheet_id, data):
    body = {
        'values': data
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range='A1',
        valueInputOption='RAW', body=body).execute()

def share_sheet(drive_service, spreadsheet_id, email_addresses):
    for email in email_addresses:
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
        }
        drive_service.permissions().create(
            fileId=spreadsheet_id,
            body=permission,
            fields='id',
            sendNotificationEmail=True
        ).execute()
    print(f"Sheet shared with: {', '.join(email_addresses)}")

# Setup the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # Google Sheets Authentication
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Create a new Google Sheet
    sheet_title = f"Code Maze Articles - {time.strftime('%Y-%m-%d %H:%M:%S')}"
    spreadsheet_id = create_sheet(sheets_service, sheet_title)
    print(f"Created new Google Sheet with ID: {spreadsheet_id}")

    # Share the sheet with specified email addresses
    email_addresses = ['alper.tunga@blazor.design', 'iclal.cetin.s.e@gmail.com', "doga.cetinkaya@yahoo.de", "seval.zeynep@gmail.com", "bzsezer1@gmail.com"]  # Add your desired email addresses here
    share_sheet(drive_service, spreadsheet_id, email_addresses)

    # Prepare data for Google Sheets
    sheet_data = [['Title', 'Link']]  # Header row

    for page in range(3, 6):  # Loop through the first 20 pages
        url = f"https://code-maze.com/latest-posts-on-code-maze/page/{page}/"
        driver.get(url)
        print(f"Navigating to: {url}")
        time.sleep(2)

        titles = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title")

        for title in titles:
            try:
                title_text = title.find_element(By.CSS_SELECTOR, "a").text
                title_link = title.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                print(f"Title: {title_text}")
                print(f"Link: {title_link}")

                # Add data to sheet_data
                sheet_data.append([title_text, title_link])

                time.sleep(2)
            except Exception as e:
                print(f"Error processing title: {e}")

    # Update Google Sheet with all data
    update_sheet(sheets_service, spreadsheet_id, sheet_data)
    print(f"Updated Google Sheet with {len(sheet_data) - 1} articles")

except HttpError as error:
    print(f"An error occurred: {error}")

finally:
    time.sleep(5)
    driver.quit()