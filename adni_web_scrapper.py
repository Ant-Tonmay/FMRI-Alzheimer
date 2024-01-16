from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random

def login():
    accept_cookies = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'ida-cookie-policy-accept'))
    )
    accept_cookies.click()
    login_menu = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'ida-user-menu-icon'))
    )
    login_menu.click()
    # Find the username input field by class name
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "userEmail"))
    )

    # Enter the username
    username_input.send_keys("your username ")

    # Find the password input field by class name
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "userPassword"))
    )
    # Enter the password
    password_input.send_keys("your password")

    login_btn = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.NAME, 'login-btn'))
    )
    login_btn.click()
    WebDriverWait(driver, 100).until(
        EC.url_contains("https://ida.loni.usc.edu/home/")
    )


def configure_firefox_options():
    firefox_options = Options()
    #firefox_options.headless = True
    # Set download directory
    download_directory = '~/Documents/ws/machine_learning/scrapper_chess_data/'
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.dir", download_directory)
    firefox_options.set_preference("browser.download.useDownloadDir", True)
    firefox_options.set_preference("browser.download.viewableInternally.enabledTypes", "")
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)

    return firefox_options

def download_data(driver, container_id):
   
    # Check Box
    container = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, container_id))
    )

    # Find the checkbox within the container
    checkbox = container.find_element(By.XPATH, './/input[@type="checkbox"]')
    checkbox.click()

    #one click download btn
    ocd = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, 'simple-download-button'))
    )
    ocd.click()
    #zip file
    _zip = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, 'simple-download-link'))
    )
    _zip.click()
    #meta data
    # meta_data = WebDriverWait(driver, 100).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, 'simple-download-metadata-link-text'))
    # )
    # meta_data.click()
    #close button
    meta_data = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, 'simple-download-close-button'))
    )
    meta_data.click()
    #got_it button
    got_it = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.ID, 'simple-download-gotit-button'))
    )
    got_it.click()
    
     



# Set up the Firefox WebDriver with configured options
firefox_options = configure_firefox_options()
driver = webdriver.Firefox(options=firefox_options)
# gecko_driver_path = '/usr/bin/firefox'
# driver = webdriver.Firefox(executable_path=gecko_driver_path)



# Replace 'number_of_pages' with the total number of pages you want to download
number_of_pages = 84


# Visit the login page
driver.get("https://ida.loni.usc.edu/login.jsp")



print("Please manually login to chess.com. After logging in, press Enter.")
input()

# Wait for the user to manually login
print("Waiting for login to complete... (you may adjust the time based on your login speed)")
WebDriverWait(driver, 100).until(
    EC.url_contains("https://ida.loni.usc.edu/home/")
)

# Replace 'your_archive_url' with the URL of the archive page you want to start from
#login()
image_col_url = 'https://ida.loni.usc.edu/pages/access/search.jsp?tab=collection&project=ADNI&page=DOWNLOADS&subPage=IMAGE_COLLECTIONS'
driver.get(image_col_url)
#My collection 
collection = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.ID, 'ygtvlabelel1'))
)
collection.click()

# FMRI
FMRI = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.ID, 'ygtvlabelel8'))
)
FMRI.click()

# Downloaded
download = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.ID, 'ygtvlabelel10'))
)
download.click()




# Loop through pages and download data
for page_number in range(5):
    unique_random_numbers = random.sample(range(0, 18), 5)
    for i in range (2):
        download_data(driver, 'cell11_' + str(unique_random_numbers[i]))

    #scroll down
    input_element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='image' and @src='/pages/images/Scroll-Arrow-Down.png']"))
    )
    input_element.click()

        
        
    

# Close the browser when done
#driver.quit()


