from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://127.0.0.1:8000"  # তোমার Django সার্ভারের URL

# Browser open
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # Step 1: Go to homepage
    driver.get(BASE_URL)
    print("✅ Homepage loaded.")

    # Click on "Sign Up" link
    signup_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))
    )
    signup_link.click()
    print("✅ Signup page opened.")

    # Wait until username field appears
    try:
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
    except:
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )

    # ✅ Use your fixed credentials
    username = "rafa"
    password = "789"

    # Type credentials
    username_input.send_keys(username)
    print(f"Typing username: {username}")

    # Try password field (different Django templates can vary)
    try:
        password_input = driver.find_element(By.ID, "id_password1")
    except:
        try:
            password_input = driver.find_element(By.ID, "id_password")
        except:
            password_input = driver.find_element(By.NAME, "password")

    password_input.send_keys(password)

    # Try confirm password (if available)
    try:
        confirm_input = driver.find_element(By.ID, "id_password2")
        confirm_input.send_keys(password)
    except:
        pass  # some signup forms don’t need confirm password

    # Tick terms checkbox if exists
    try:
        driver.find_element(By.ID, "terms").click()
    except:
        pass  # ignore if no checkbox present

    # Submit the form
    try:
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    except:
        driver.find_element(By.XPATH, "//input[@type='submit']").click()

    print("✅ Signup form submitted.")

    # Wait a bit
    time.sleep(3)

    # Step 2: Go to login page
    driver.get(f"{BASE_URL}/login/")
    print("✅ Login page opened.")

    # Fill login form
    try:
        driver.find_element(By.ID, "id_username").send_keys(username)
    except:
        driver.find_element(By.ID, "username").send_keys(username)

    try:
        driver.find_element(By.ID, "id_password").send_keys(password)
    except:
        driver.find_element(By.ID, "password").send_keys(password)

    # Click login
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    print("✅ Login submitted.")

    time.sleep(3)

    # Step 3: Go to Report page
    driver.get(f"{BASE_URL}/report/")
    print("✅ Report page opened.")

    # Verify fields exist
    field_ids = ["id_name", "id_category", "id_location", "id_date_lost", "id_description"]
    for fid in field_ids:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, fid)))
    print("✅ All Report fields found.")

    print("\n🎉 Test completed successfully!")

except Exception as e:
    print("❌ Error:", e)

finally:
    time.sleep(3)
    driver.quit()
