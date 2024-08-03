from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def navigate_to_revenue_calculator(driver):
    driver.get("https://www.fitpeo.com/revenue-calculator")
    time.sleep(2)
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='accept-cookies']"))
    )
    cookie_button.click()
    see_how_it_works_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='See how it works']"))
    )
    see_how_it_works_button.click()

def scroll_to_slider_section(driver):
    slider_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='calculator__slider']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", slider_element)

def adjust_slider_and_text_field(driver):
    slider_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='range']"))
    )
    driver.execute_script("arguments[0].value = 560;", slider_element)
    text_field_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='calculator__input']"))
    )
    text_field_element.clear()
    text_field_element.send_keys("560")
    slider_value = float(slider_element.get_attribute("value"))
    if slider_value != 560:
        raise Exception("Slider value is not updated as expected")

def select_cpt_codes(driver):
    checkboxes = ["CPT-99091", "CPT-99453", "CPT-99454", "CPT-99474"]
    for code in checkboxes:
        checkbox_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//input[@id='{code}']"))
        )
        if not checkbox_element.is_selected():
            checkbox_element.click()

def validate_total_recurring_reimbursement(driver):
    expected_value = "$110,700"
    actual_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h3[text()='Total Recurring Reimbursement for all Patients Per Month:']//following-sibling::p"))
    ).text
    if actual_value != expected_value:
        raise Exception("Total recurring reimbursement value is not as expected")

def main():
    driver_path = 'C:/Users/INTEL/AppData/Local/Programs/Python/Python39/Scripts/chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        navigate_to_revenue_calculator(driver)
        scroll_to_slider_section(driver)
        adjust_slider_and_text_field(driver)
        select_cpt_codes(driver)
        validate_total_recurring_reimbursement(driver)
        print("Test case successfully completed!")
    except Exception as e:
        print(f"Test case failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
