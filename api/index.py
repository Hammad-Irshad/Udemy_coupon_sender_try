from selenium import webdriver
import re
from http.server import BaseHTTPRequestHandler

def scrape_data(url):
    # Initialize a webdriver (e.g., Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get(url)

    # Wait for the page to load completely (you can adjust the time as needed)
    driver.implicitly_wait(10)

    # Wait for an additional 5 seconds
    time.sleep(5)

    # Get the content after JavaScript execution
    dynamic_content = driver.page_source

    # Close the browser
    driver.quit()

    # Process the content (similar to your existing code)
    matches = re.findall(r'<a.*?href=[\'"](.*?udemy.com/course.*?)["\']', dynamic_content)
    processed_data = '\n'.join(matches)

    return processed_data

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = "https://www.real.discount/udemy-coupon-code/"
        processed_data = scrape_data(url)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(processed_data.encode('utf-8'))

# Define the URL
url = "https://www.real.discount/udemy-coupon-code/"

# Create an instance of the RequestHandler
handler = RequestHandler()

# This part is specific to Vercel
def vercel_handler(request):
    # Trigger the scraping function when the function is invoked
    handler.do_GET()
    return {
        'statusCode': 200,
        'body': 'Scraping completed'
    }
