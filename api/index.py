import os
from selenium import webdriver
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

def scrape_data(url):
    # Initialize a webdriver (e.g., Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load completely (you can adjust the time as needed)
    driver.implicitly_wait(10)

    # Get the content after JavaScript execution
    dynamic_content = driver.page_source

    # Close the browser
    driver.quit()

    # Process the content (similar to your existing code)
    # ...

    return processed_data

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://www.real.discount/udemy-coupon-code/"
        processed_data = scrape_data(url)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(processed_data.encode('utf-8'))

# Main function that will be executed by Vercel
def handler(request):
    # Start an HTTP server to handle incoming requests
    server_address = ('', 8000)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)

    # Serve HTTP requests in a separate thread
    import threading
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Scrape data
    url = "https://www.real.discount/udemy-coupon-code/"
    processed_data = scrape_data(url)

    # Close the HTTP server
    httpd.shutdown()

    return {
        'statusCode': 200,
        'body': processed_data
    }
