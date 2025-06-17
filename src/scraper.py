# Main scraping logic for the Advanced Job Scraper

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.parse import urlencode

from . import config
from . import parser
from . import utils

class JobScraper:
    def __init__(self):
        """Initializes the JobScraper with WebDriver setup."""
        self.driver = self._setup_driver()
        self.all_jobs_data = []

    def _setup_driver(self):
        """Sets up the Selenium WebDriver."""
        logging.info("Setting up WebDriver...")
        chrome_options = Options()
        if config.HEADLESS_BROWSE:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox") # Important for running in restricted environments
        chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems
        # Optional: Add user agent to mimic a real browser
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        try:
            # Use webdriver-manager to automatically handle driver download/update
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            logging.info("WebDriver setup successful.")
            return driver
        except WebDriverException as e:
            logging.error(f"Failed to initialize WebDriver: {e}")
            # Consider adding fallback or specific error handling here
            raise # Re-raise the exception to stop execution if driver fails
        except Exception as e:
            logging.error(f"An unexpected error occurred during WebDriver setup: {e}")
            raise

    def _build_search_url(self, page_num=0):
        """Builds the search URL for Indeed (example)."""
        # Indeed uses 'q' for query, 'l' for location, 'start' for pagination (0, 10, 20...)
        params = {
            \"q\": config.SEARCH_QUERY,
            \"l\": config.LOCATION,
            \"start\": page_num * 10 # Indeed uses increments of 10
        }
        # Add more parameters as needed, e.g., radius, job type filters
        # params[\"radius\"] = \"50\" # Example: search within 50 miles
        # params[\"jt\"] = \"fulltime\" # Example: filter for full-time jobs

        return f\"{config.BASE_URL}?{urlencode(params)}\"

    def scrape_jobs(self):
        """Main function to scrape job listings across multiple pages."""
        logging.info(f"Starting job scraping for query: ", config.SEARCH_QUERY, f\" in location: ", config.LOCATION)

        current_page_num = 0
        while current_page_num < config.MAX_PAGES:
            page_url = self._build_search_url(current_page_num)
            logging.info(f"Scraping page {current_page_num + 1}: {page_url}")

            try:
                self.driver.get(page_url)
                # Optional: Add explicit waits here if needed for dynamic content
                # from selenium.webdriver.support.ui import WebDriverWait
                # from selenium.webdriver.support import expected_conditions as EC
                # from selenium.webdriver.common.by import By
                # wait = WebDriverWait(self.driver, config.ELEMENT_WAIT_TIMEOUT)
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, \"#resultsCol\"))) # Example wait condition

                time.sleep(config.REQUEST_DELAY) # Simple delay

                html_content = self.driver.page_source
                if not html_content:
                    logging.warning(f"Failed to retrieve HTML content for page {current_page_num + 1}.")
                    current_page_num += 1
                    continue

                page_jobs = parser.parse_job_listings(html_content)
                if not page_jobs:
                    logging.info(f"No jobs found on page {current_page_num + 1}. Stopping pagination or check selectors.")
                    # Decide whether to break or continue based on site behavior
                    # If a page reliably has no jobs when finished, we can break.
                    # If it might be an intermittent issue, continuing might be better.
                    break # Assuming no jobs means end of results for this example

                self.all_jobs_data.extend(page_jobs)
                logging.info(f"Found {len(page_jobs)} jobs on page {current_page_num + 1}. Total jobs found: {len(self.all_jobs_data)}")

                # Check for next page (optional, as we are using URL parameters for pagination)
                # next_page_url = parser.find_next_page_url(html_content, config.BASE_URL)
                # if not next_page_url or current_page_num >= config.MAX_PAGES - 1:
                #     logging.info(\"No more pages to scrape or max pages reached.\")
                #     break
                # else:
                #     current_page_num += 1 # Increment only if moving to next page via link click

                current_page_num += 1 # Increment page number for URL generation

            except TimeoutException:
                logging.warning(f"Page load timed out for {page_url}")
                # Optional: Implement retry logic here
                current_page_num += 1 # Move to next page attempt
                continue
            except WebDriverException as e:
                logging.error(f"WebDriver error on page {current_page_num + 1}: {e}")
                # Decide whether to stop or try to continue
                break # Stop on significant WebDriver errors
            except Exception as e:
                logging.error(f"An unexpected error occurred while scraping page {current_page_num + 1}: {e}")
                # Optional: Add more specific error handling
                current_page_num += 1 # Try next page
                continue

        logging.info(f"Scraping finished. Total jobs collected: {len(self.all_jobs_data)}")
        return self.all_jobs_data

    def close_driver(self):
        """Closes the Selenium WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
                logging.info("WebDriver closed successfully.")
            except Exception as e:
                logging.error(f"Error closing WebDriver: {e}")
            finally:
                self.driver = None


