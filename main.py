import requests, os, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ZILLOW_CLONE = os.environ['clone']

response = requests.get(ZILLOW_CLONE)
soup = BeautifulSoup(response.text, 'html.parser')

listingsNumber = soup.find(class_='result-count').text
listingsNumber = int(listingsNumber.split()[0])


addresses_elements = soup.find_all(name='address', attrs={'data-test':'property-card-addr'})
prices_elements = soup.find_all(name='span', attrs={'data-test':'property-card-price'})
links_elements = soup.find_all(name='a', attrs={'data-test':'property-card-link'})

addresses = [address.get_text().replace(" | ", " ").strip() for address in addresses_elements]
prices = [price.get_text().replace("/mo", "").split("+")[0] for price in prices_elements if "$" in price.text]
links = [link.get('href') for link in links_elements]


chrome_settings = webdriver.ChromeOptions()
chrome_settings.add_experimental_option('detach', True)

driver = webdriver.Chrome(chrome_settings)
wait = WebDriverWait(driver, 10)

for i in range(0, len(addresses)-1):
    driver.get('https://forms.gle/SEGqypqZRLeSpm2T7')
    time.sleep(2)
    address_input = wait.until(EC.visibility_of_element_located((By.XPATH,
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))

    price_input = wait.until(EC.presence_of_element_located((By.XPATH,
                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))

    link_input = wait.until(EC.presence_of_element_located((By.XPATH,
                          '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))

    send_button = wait.until(EC.presence_of_element_located((By.XPATH,
                          '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')))

    address_input.send_keys(addresses[i])
    price_input.send_keys(prices[i])
    link_input.send_keys(links[i])
    send_button.click()

driver.quit()