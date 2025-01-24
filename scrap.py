import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Initialize WebDriver with options."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def sort_reviews(driver):
    """Click the sort button and select the 'Newest' option."""
    try:
        
        try:
            review_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@tabindex='-1']"))
            )
            review_button.click()
        except Exception:
            print("Review button not found, proceeding with sorting.")
        #wait for Review to load
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
        df.to_csv("latestreviewer.csv", index=False, encoding="utf-8")

    except Exception as e:
        print("Could not find the latest reviewer:", e)

def main():

    start = time.time()
    """Main function to execute the script."""
    url = "https://maps.app.goo.gl/qxMxeropJE1P7G2x5"
    
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
