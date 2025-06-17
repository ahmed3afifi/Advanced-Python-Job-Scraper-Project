BASE_URL = "https://www.indeed.com/jobs"

# Search parameters
SEARCH_QUERY = "Python Developer"
LOCATION = "Remote"

# Number of pages to scrape
MAX_PAGES = 3

# Output file configuration
OUTPUT_DIR = "../data"
OUTPUT_FILENAME_CSV = "job_postings.csv"
OUTPUT_FILENAME_JSON = "job_postings.json"

# Logging configuration
LOG_DIR = "../logs"
LOG_FILENAME = "scraper.log"
LOG_LEVEL = "INFO" # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Selenium/WebDriver settings
# Path to your WebDriver executable (if not using webdriver-manager)
# WEBDRIVER_PATH = "/path/to/chromedriver"
# Set to True to run the browser in headless mode (without GUI)
HEADLESS_BROWSE = True
# Timeouts (in seconds)
PAGE_LOAD_TIMEOUT = 30
ELEMENT_WAIT_TIMEOUT = 10

# Delay between requests (in seconds) to avoid overwhelming the server
REQUEST_DELAY = 2
