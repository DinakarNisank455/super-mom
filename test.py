from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    # Open the login page
    driver.get("http://127.0.0.1:5000/login")  # Adjust URL if necessary
    return driver


def test_login():
    driver = setup()

    # Wait for the elements to be visible
    wait = WebDriverWait(driver, 10)  # wait up to 10 seconds

    # Locate input fields and login button with correct IDs
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.NAME, "login-button")))

    # Input valid credentials
    username_field.send_keys("nisank.nukala4@gmail.com")
    password_field.send_keys("nisank.nukala4@gmail.com")

    # Click login button
    login_button.click()
    time.sleep(3)  # Allow login to process

    # Verify login success (check for the dashboard element)
    try:
        driver.find_element(By.NAME, "dashboard")  # Update this with the correct ID
        print("✅ Test Passed: Login Successful")
    except:
        print("❌ Test Failed: Login Unsuccessful")

    # Test invalid login
    driver.get("http://127.0.0.1:5000/login")
    time.sleep(2)

    # Re-enter credentials for invalid login
    username_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.NAME, "login-button")

    username_field.clear()
    password_field.clear()

    username_field.send_keys("wronguser")
    password_field.send_keys("wrongpassword")
    login_button.click()
    time.sleep(15)

    try:
        error_message = driver.find_element(By.ID, "error-message")  # Ensure this ID is correct
        print("✅ Test Passed: Invalid Login Blocked")
    except:
        print("❌ Test Failed: Invalid Login Not Blocked")

    teardown(driver)


def teardown(driver):
    driver.quit()


# Run the test
if __name__ == "__main__":
    test_login()
