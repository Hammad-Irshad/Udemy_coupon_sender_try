from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from selenium import webdriver
import time
import re
import os

# Define the URL
url = "https://www.real.discount/udemy-coupon-code/"

# Function to scrape and process the data
def scrape_data(url):
    # Initialize a webdriver (e.g., Chrome)
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load completely (you can adjust the time as needed)
    driver.implicitly_wait(10)

    # Wait for an additional 5 seconds
    time.sleep(5)

    # Get the content after JavaScript execution
    dynamic_content = driver.page_source

    # Save dynamic_content to a text file
    with open('text.txt', 'w', encoding='utf-8') as file:
        file.write(dynamic_content)

    # Close the browser
    driver.quit()

    # Extract links from html.txt and write to link.txt
    with open('text.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()

    matches = re.findall(r'<a.*?href=[\'"](.*?/offer/.*?)["\']', html_content)

    with open('link.txt', 'w', encoding='utf-8') as file:
        for match in matches:
            file.write(match + '\n')

    # Remove '/offer/`+ item[' from link.txt
    with open('link.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_links = [line.replace('/offer/`+ item[', '') for line in lines]

    with open('link.txt', 'w', encoding='utf-8') as file:
        file.writelines(cleaned_links)

    # Read links from link.txt
    with open('link.txt', 'r', encoding='utf-8') as file:
        links = file.readlines()

    all_content = ''  # Initialize all_content before the loop

    driver = webdriver.Chrome()

    for url in links:
        full_url = "https://www.real.discount/" + url.strip()
        driver.get(full_url)
        driver.implicitly_wait(10)
        time.sleep(3)
        dynamic_content = driver.page_source
        all_content += dynamic_content

    # Save all_content to a text file
    with open('final_content.txt', 'w', encoding='utf-8') as file:
        file.write(all_content + '\n')

    # Close the browser
    driver.quit()

    # Extract Udemy links
    with open('final_content.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()

    matches = re.findall(r'<a.*?href=[\'"](.*?udemy.com/course.*?)["\']', html_content)

    with open('udemy_links.txt', 'w', encoding='utf-8') as file:
        for match in matches:
            cleaned_match = re.sub(r'^.*https://www.udemy.com/course', 'https://www.udemy.com/course', match)
            file.write(cleaned_match + '\n')

# HTTP Request Handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        with open('udemy_links.txt', 'r', encoding='utf-8') as file:
            cleaned_match = file.read()
        self.wfile.write(cleaned_match.encode('utf-8'))

# Start the HTTP server
server_address = ('', 8000)
httpd = ThreadingHTTPServer(server_address, RequestHandler)

# Serve HTTP requests in a separate thread
import threading
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

# Keep the program running
while True:
    # Run the scraping function
    scrape_data(url)

    # Wait for 60 seconds before running again
    time.sleep(60)