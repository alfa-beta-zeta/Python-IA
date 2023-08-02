import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode without opening a browser window
driver = webdriver.Chrome(service=service, options=options)

url = 'https://facebook.com'  # Facebook mobile view URL
username = ''  # Replace with your Facebook username
password = ''  # Replace with your Facebook password

driver.get(url)

# Find the login elements and populate the username and password
username_input = driver.find_element(By.ID, 'email')
password_input = driver.find_element(By.ID, 'pass')

username_input.send_keys(username)
password_input.send_keys(password)

# Submit the login form
password_input.send_keys(Keys.RETURN)

driver.implicitly_wait(10)  # Wait for the page to load after login (adjust the time as needed)

hashtag = 'election'  # Replace with the desired hashtag
url = f'https://free.facebook.com/hashtag/{hashtag}'

driver.get(url)

SCROLL_PAUSE_TIME = 2  # Adjust the pause time based on the page loading speed

last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
articles = soup.find_all('article')

for article in articles:
    # Extract and process the desired information from each article
    # Example: Extract the article title and print it
    title_element = article.find('h3')
    if title_element:
        title = title_element.text.strip()
        print(title)

