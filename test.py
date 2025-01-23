import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Initialize WebDriver with options."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

def sort_reviews(driver):
    """Click the sort button and select the 'Newest' option."""
    try:
        sort_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='IAbLGd']"))
        )
        sort_button.click()
        # Wait for the 'Newest' option and click it
        newest_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='fxNQSd' and @data-index='1']"))
        )

        newest_option.click()
    except Exception as e:
        print("Error clicking sort or newest option:", e)

def extract_reviewer_name(driver):
    """Extract the latest reviewer's name after sorting reviews."""
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "jftiEf")))
    try:
        reviewer_name = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "d4r55"))
        ).text

        print("Latest Reviewer's Name:", reviewer_name)

        # Save to CSV using pandas
        df = pd.DataFrame([{"Reviewer Name": reviewer_name}])
        df.to_csv("latest_reviewer.csv", index=False, encoding="utf-8")

    except Exception as e:
        print("Could not find the latest reviewer:", e)

def main():

    start = time.time()
    """Main function to execute the script."""
    url = "https://www.google.com/maps/place/Camion+jo+pizza/@48.6159141,-1.4913629,17z/data=!4m18!1m9!3m8!1s0x89d4cb91e43a6ceb:0x1c880722f7dd12aa!2sAccess+Storage+-+Downtown+Toronto!8m2!3d43.661974!4d-79.31946!9m1!1b1!16s%2Fg%2F11bw420bj_!3m7!1s0x480eaf36fdfc5eeb:0x79df0e6acac777d2!8m2!3d48.6159141!4d-1.488788!9m1!1b1!16s%2Fg%2F11ry9gqbzc?hl=ne&entry=ttu&g_ep=EgoyMDI1MDEyMC4wIKXMDSoASAFQAw%3D%3D"
    
    # Set up WebDriver
    driver = setup_driver()
    driver.get(url)

    sort_reviews(driver)
    extract_reviewer_name(driver)

    driver.quit()
    end = time.time()
    total_time = end - start
    print(f'Total time is : {total_time}')

if __name__ == "__main__":
    main()
