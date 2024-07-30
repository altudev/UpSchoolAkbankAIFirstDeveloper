import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

counter = 0
def find_titles(driver):
    global counter
    while True:
        # Navigate to "https://code-maze.com/"
        driver.get("https://code-maze.com/latest-posts-on-code-maze/")

        # Wait 2 seconds
        time.sleep(2)

        # Find <h2> elements with class "entry-title"
        titles = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title")

        if counter < 3:
                titles = []
                counter += 1

        if len(titles) > 0:
            return titles

        print("No titles found, retrying in 60 seconds...")
        # Wait 60 seconds before trying again
        time.sleep(8)

# Setup the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # Find the titles
    titles = find_titles(driver)

    # Print and save the data to a JSONL file
    with open("titles.jsonl", "w") as f:
        for title in titles:
            try:
                # Print the text of the <a> element
                title_text = title.find_element(By.CSS_SELECTOR, "a").text
                print(title_text)

                # Print the href attribute of the <a> element
                title_link = title.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                print(title_link)

                # Save the data to a JSONL file
                json_line = json.dumps({"title": title_text, "link": title_link})
                f.write(json_line + "\n")
            except Exception as e:
                print(f"Error processing title: {e}")
                continue

finally:
    # Close the browser after a short delay to see the result
    time.sleep(5)
    driver.quit()
