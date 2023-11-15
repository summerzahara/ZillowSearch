from bs4 import BeautifulSoup
from icecream import ic
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

google_form = "https://docs.google.com/forms/d/e/1FAIpQLSc3RMaiZw6Uq2YSJsZZcvwVhD1DdreOYxlnng0Xm5FCE77HGw/viewform?usp=sf_link"
zillow_url = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(zillow_url)
data = response.text
soup = BeautifulSoup(data, "html.parser")

# Create a list of addresses
addresses = soup.find_all(name="address")
addr_list = []

for address in addresses:
    text = address.get_text().strip()
    addr_list.append(text)

# Create a list of links
links = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
link_list = []

for link in links:
    href = link.get("href")
    link_list.append(href)

# Create a list of prices
prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = []

for price in prices:
    text = price.get_text().split("+")[0]
    text = text.split("/")[0]
    price_list.append(text)


# Setup selenium for chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Setup driver
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(addr_list)):
    driver.get(google_form)
    time.sleep(3)
    form_addr = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_addr.send_keys(addr_list[n])
    time.sleep(3)


    form_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price.send_keys(price_list[n])
    time.sleep(3)

    form_href = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_href.send_keys(link_list[n])
    time.sleep(3)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_btn.click()

