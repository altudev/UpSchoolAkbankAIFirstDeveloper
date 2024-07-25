import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Setup the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

try:
    # Navigate to "https://code-maze.com/"
    driver.get("https://code-maze.com/latest-posts-on-code-maze/")

    # Wait 2 seconds
    time.sleep(2)

    # Find <h2> elements with class "entry-title"
    titles = driver.find_elements(By.CSS_SELECTOR, "h2.entry-title")

    # get the href value of the first <a> element in the <h2> element
    for title in titles:
        # Print the text of the <a> element
        print(title.find_element(By.CSS_SELECTOR, "a").text)

        # Print the href attribute of the <a> element
        print(title.find_element(By.CSS_SELECTOR, "a").get_attribute("href"))

        # Save the data to a JSONL file
        with open("titles.jsonl", "w") as f:
            for title in titles:
                title_text = title.find_element(By.CSS_SELECTOR, "a").text
                title_link = title.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                json_line = json.dumps({"title": title_text, "link": title_link})
                f.write(json_line + "\n")

finally:
    # Close the browser after a short delay to see the result
    time.sleep(5)
    driver.quit()
