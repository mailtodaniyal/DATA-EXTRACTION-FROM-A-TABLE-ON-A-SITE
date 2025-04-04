from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

driver = webdriver.Chrome()
driver.get("https://your-auction-site.com")
time.sleep(2)

data = []
auctions = driver.find_elements(By.CLASS_NAME, "auction-list-item")
for auction in auctions:
    auction.click()
    time.sleep(2)
    lots = driver.find_elements(By.CLASS_NAME, "lot-item")
    for lot in lots:
        lot.click()
        time.sleep(2)
        lot_number = driver.find_element(By.CLASS_NAME, "lot-number").text
        status = driver.find_element(By.CLASS_NAME, "status").text
        highest_bid = driver.find_element(By.CLASS_NAME, "highest-bid").text
        data.append([lot_number, status, highest_bid])
        driver.back()
        time.sleep(1)
    driver.back()
    time.sleep(1)

driver.quit()
df = pd.DataFrame(data, columns=["Lot Number", "Status", "Highest Bid"])
df.to_excel("Auction_Data.xlsx", index=False)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your-credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Auction Data").sheet1
data.insert(0, ["Lot Number", "Status", "Highest Bid"])
sheet.update("A1", data)
print("Data saved successfully!")
