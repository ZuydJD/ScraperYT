from selenium import webdriver
from bs4 import BeautifulSoup
import time


def scrape_chat_users():
    url = input("Enter the popout chat URL: ")
    driver = webdriver.Chrome()
    driver.get(url)
    chat_users = set()

    # Wait for the chat to load and populate initially
    time.sleep(5)

    # Scroll to the bottom of the chat
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Scroll backwards in the chat
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    # Collect chat users' names
    last_print_time = time.time()
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for user in soup.select('.style-scope.yt-live-chat-author-chip'):
            username = user.text.strip()
            if username != "X":
                chat_users.add(username)

        current_time = time.time()

        # Check if 30 minutes have passed or Enter is pressed
        if current_time - last_print_time >= 1800 or input("Press 'Enter' to print chat users or 'Q' to exit: ").lower() == 'q':
            print("Chat users:")
            print("\n".join(chat_users))
            last_print_time = current_time

        # Scroll upwards to load previous chat messages
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(0.5)

        # Break the loop if reaching the top of the chat
        if driver.execute_script("return window.pageYOffset;") == 0:
            break

    driver.quit()
    return list(chat_users)


youtube_users = scrape_chat_users()
input("Press Enter to exit...")
