from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.livenation.com/search?fbclid=IwAR2N2Y7Ur1M3rYdioihRUKwNzXx06q-xmUG815tqwqjJAnI8LK26hwetlbw')

rock_button = driver.find_element(By.XPATH, "//div[@class='css-qyb0nm']/a[@class='chakra-linkbox__overlay css-bq12ai']")
rock_button.click() 
time.sleep(2)

def scroll_to_bottom():
    band_name = []
    date = []
    us_state = []

    while True:
        # Scroll to load more content
        for i in range(5):  # Scroll 5 times to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Find all ticket elements
        tickets = driver.find_elements(By.XPATH, '//div[@class = "css-7oafjj"]/a[contains(@role,"button")]')

        # Scrape data from each ticket
        for ticket in tickets:
            band_name.append(ticket.find_element(By.XPATH, './/div[@class = "css-a3j06d"]/h6[contains(@class,"css-1hlf402")]').text)
            date.append(ticket.find_element(By.XPATH, './/div[@class = "css-ysbv3r"]/div[contains(@class,"css-4e8jdi")]/time[contains(@role,"presentation")]').text)
            us_state.append(ticket.find_element(By.XPATH, './/div[@class = "css-a3j06d"]/p[contains(@class,"css-nk4tcj")]/span[contains(@class,"chakra-text")]').text)

        # Check if there are no more elements to load
        if not driver.find_elements(By.XPATH, '//div[@class = "css-7olkrp"]/span[contains(@style,"display: inherit;")]'):
            break

    # Create a DataFrame
    df = pd.DataFrame({'State': us_state, 'Band Name': band_name, 'Date': date})
    df.to_csv('data1.csv', index=False)

# Call the function to start scraping and saving data
scroll_to_bottom()

# Quit the WebDriver
driver.quit()
