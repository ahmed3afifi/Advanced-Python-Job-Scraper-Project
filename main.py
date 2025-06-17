import logging
import sys
import os

# This allows running the script from the project root directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import utils
from src import config
from src.scraper import JobScraper

def main():
    """Main execution function."""
    utils.setup_logging()
    logging.info("--- Advanced Job Scraper Initialized ---")

    scraper_instance = None # Initialize to ensure it exists in finally block
    try:
        scraper_instance = JobScraper()
        scraped_data = scraper_instance.scrape_jobs()

        if scraped_data:
            logging.info(f"Saving {len(scraped_data)} job postings...")
            # Save to both CSV and JSON as configured
            utils.save_to_csv(scraped_data, config.OUTPUT_FILENAME_CSV)
            utils.save_to_json(scraped_data, config.OUTPUT_FILENAME_JSON)
            logging.info("Data saving complete.")
        else:
            logging.warning("No data was scraped. Output files will not be created or will be empty.")

    except Exception as e:
        logging.critical(f"An unhandled error occurred during the scraping process: {e}", exc_info=True)
        # Depending on the error (e.g., WebDriver setup failure), scraper_instance might be None

    finally:
        if scraper_instance:
            scraper_instance.close_driver()
        logging.info("--- Advanced Job Scraper Finished ---")

if __name__ == "__main__":
    # This allows the script to be run directly
    # To run from project root: python advanced_job_scraper/main.py
    # Or navigate into advanced_job_scraper and run: python main.py
    # Adjusting path assumes running from project root is common
    if os.path.basename(os.getcwd()) == "advanced_job_scraper":
         # If running from within the project dir, adjust path for config/utils
         sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
         # Need to re-import with adjusted path potentially, or structure differently
         # Simpler approach: Assume running from project root or handle imports inside functions
         pass # Keep imports as they are, assuming standard execution

    main()

