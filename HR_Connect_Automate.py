import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Function to initialize the Chrome WebDriver
def initialize_driver(driver_path):
    service = Service(driver_path)
    return webdriver.Chrome(service=service)


# Function to process connect buttons and iterate over pages
def process_connect_buttons_recursively(driver, note_text, base_url, max_pages):
    for page in range(1, max_pages + 1):  # Start from page 2 to max_pages
        # Construct the new URL with the current page number
        new_url = f"{base_url}&page={page}"
        
        # Load the new URL in the driver
        driver.get(new_url)
        print(f"Loaded page: {new_url}")
        time.sleep(5)  # Wait for the page to load
        
        # Call the function to process connect buttons
        process_connect_buttons(driver, note_text)

# Function to click all connect buttons and add a note
def process_connect_buttons(driver, note_text):
    # Find all "Connect" buttons
    connect_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Invite') and contains(@aria-label, 'to connect')]")
    
    for index, button in enumerate(connect_buttons):
        try:
            # Click the "Connect" button
            button.click()
            print(f"Clicked Connect button {index + 1}.")
            time.sleep(2)  # Add delay to prevent rate limiting
            
            # Wait for the "Add a note" button to appear and click it
            add_note_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Send without a note']/parent::button"))
            )
            add_note_button.click()
            
            """If you want to add notes un command below codes..."""
            # print(f"Clicked Add a note button for Connect button {index + 1}.")
            # time.sleep(2)
            
            # # Find the text area and enter the note
            # text_area = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "custom-message"))
            # )
            # text_area.clear()
            # text_area.send_keys(note_text)
            # print(f"Entered note for Connect button {index + 1}.")
            
            # # Wait for the 'Send invitation' button to be clickable
            # send_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send invitation']"))
            # )

            # # Click the send button
            # send_button.click()
            
            print(f"Sent invitation for Connect button {index + 1}.")
            time.sleep(2)
            
        except Exception as e:
            print(f"Error processing button {index + 1}: {e}")
            # Optionally, close any modal that might have appeared
            try:
                close_button = driver.find_element(By.XPATH, "//button[@aria-label='Dismiss']")
                close_button.click()
            except:
                pass

# Main function
def main():
    driver_path = r"C:\Users\SudharsanDhakshinamo\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    driver = initialize_driver(driver_path)
    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)
        
        # Log in to LinkedIn
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.send_keys("example@gmail.com")
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("xyz")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("Logged in successfully.")
        input("wait")
        time.sleep(5)
        # Base URL for the LinkedIn search
        base_url = driver.current_url
        # Process Connect buttons with a note
        note_text = """This is Sudharsan With 1 year of experience in AI,Python,AWS,Automation,Web Scraping.Exploring new opportunities to make an impact.Happy to connect for potential opportunities you might be aware of."""
        # Process connect buttons recursively over 10 pages
        process_connect_buttons_recursively(driver, note_text, base_url, max_pages=10)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
