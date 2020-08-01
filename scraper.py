import sys
import time
import smtplib
import requests
from amzsear import AmzSear
from bs4 import BeautifulSoup
from selenium import webdriver

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
EMAIL_ADDRESS = "shockwaverules11@gmail.com"
# change during each use
WANTED_PRICE = 19

def trackPrice():
    price = int(float(getPrice()))
    if price > WANTED_PRICE:
        diff = price - WANTED_PRICE
        print(f"It's still {diff} too expensive")
    else:
        print("Cheaper!")
        checkStock()
    
def findItem():
    name = raw_input("What would you like to search? (in single-quotes please)")
    amz = AmzSear(name, page=1, region='CA')
    item = amz.rget(1)
    print(item)
    URL = item.get_product_url()
    getPrice()

def getPrice():
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(class_="a-size-medium a-color-price offer-price a-text-normal").get_text()[-5:]
    print(title)
    print(price)
    return price

def checkStock():
    stock = soup.find(class_="a-size-medium a-color-success").get_text().strip()
    if "In Stock" in stock:
        print(stock)
        sendMail()
    else:
        print(title + " currently out of stock")
        sys.exit()

def sendMail():
    subject = "Amazon Price has Dropped!"
    mailtext = "Subject:" + subject + '\n\n' + URL

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_ADDRESS, 'shockwave11')
    server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, mailtext)
    print("Sent Email")
    pass

def purchaseOrder():
    driver = webdriver.Chrome()
    driver.get(URL)
    button = driver.find_element_by_id("buy-now-button")
    button.click()
    # add another method to confirm order

if __name__ == "__main__":
    while True:
        trackPrice()
        time.sleep(60)