# pip install selenium webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto-allow mic access (for testing)
# chrome_options.add_argument("--headless=new")  
# Comment this during testing!

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Properly format the file URL
#website = f"file:///{os.getcwd()}/index.html"
#driver.get(website)

#rec_file = os.path.join(os.getcwd(), "input.txt")

# Setting up Chrome options with specific arguments
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")

#Setting up the Chrome driver with WebDriverManager and options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

# Creating the URL for the website using the current working directory
website = "https://allorizenproject1.netlify.app/"

#Opening the website in the Chrome browser
driver.get(website)

rec_file = f"{getcwd()}\\input.txt"

def listen():
    try:
        start_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'startButton'))
        )
        start_button.click()
        print("Listening...")

        output_text = ""
        is_second_click = False
        while True:
            output_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'output'))
            )
            current_text = output_element.text.strip()
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif "listening..." in start_button.text:
                is_second_click = True
            if current_text and current_text != output_text:
                output_text = current_text
                with open(rec_file, "w") as file:
                    file.write(output_text.lower())
                print("USER:", output_text)

    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()
