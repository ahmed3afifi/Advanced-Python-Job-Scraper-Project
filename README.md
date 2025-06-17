# Advanced-Python-Job-Scraper-Project

## Overview

This project is an advanced web scraper designed to extract job posting information from Indeed.com (or adaptable to other job boards). It systematically navigates search result pages, extracts key details for each job listing (title, company, location, summary, date posted, URL), and saves the data into structured formats (CSV and JSON). 

Built with Python, this scraper utilizes libraries like Selenium for handling dynamic web content and navigating pagination, and BeautifulSoup for robust HTML parsing. It incorporates best practices such as modular code structure, configuration management, comprehensive error handling, and logging, making it a suitable demonstration of advanced web scraping skills for a professional portfolio.

## Features

*   **Dynamic Content Handling**: Uses Selenium and WebDriver (managed by `webdriver-manager`) to interact with JavaScript-rendered pages and handle dynamically loaded content.
*   **Pagination**: Automatically navigates through multiple pages of search results based on configuration.
*   **Robust Parsing**: Employs BeautifulSoup4 with flexible selectors (including regex and fallbacks) to extract data from potentially complex and changing HTML structures.
*   **Structured Data Output**: Saves scraped data cleanly into both CSV and JSON formats using Pandas and the `json` library.
*   **Configuration Management**: Centralized configuration (`src/config.py`) for easy modification of search parameters (query, location), scraping depth (max pages), output paths, logging levels, and browser behavior (headless mode).
*   **Modular Code**: Organized into distinct modules (`scraper.py`, `parser.py`, `utils.py`, `config.py`, `main.py`) for clarity, maintainability, and reusability.
*   **Error Handling & Logging**: Implements `try-except` blocks for common scraping issues (e.g., timeouts, element not found) and logs activities, warnings, and errors to both console and a file (`logs/scraper.log`) for debugging and monitoring.
*   **Dependency Management**: Includes a `requirements.txt` file for straightforward setup of the necessary Python libraries.

## Technology Stack

*   **Language**: Python 3
*   **Web Interaction/Automation**: Selenium
*   **WebDriver Management**: webdriver-manager
*   **HTML Parsing**: BeautifulSoup4
*   **Data Handling**: Pandas
*   **Standard Libraries**: `logging`, `os`, `json`, `time`, `urllib.parse`

## Project Structure

```
advanced_job_scraper/
├── data/                 # Output directory for scraped data (CSV, JSON)
├── logs/                 # Output directory for log files
├── src/
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   ├── parser.py         # HTML parsing functions
│   ├── scraper.py        # Core scraping logic (Selenium)
│   ├── utils.py          # Utility functions (logging, file saving)
│   └── (WebDriver files) # Potentially downloaded by webdriver-manager
├── main.py               # Main entry point script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation (this file)
```

## Setup and Installation

1.  **Clone or Download**: Get the project code.
    ```bash
    # If using Git
    git clone <repository_url>
    cd advanced_job_scraper
    ```
    Or download and extract the ZIP file.

2.  **Create Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    # Activate the environment
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**: Ensure you have Python 3 and pip installed. Then run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install Selenium, webdriver-manager, BeautifulSoup4, Pandas, and requests.

4.  **Install Google Chrome**: `webdriver-manager` will automatically download the correct ChromeDriver, but you need to have Google Chrome browser installed on your system.

## Configuration

Modify the `src/config.py` file to customize the scraper's behavior:

*   `BASE_URL`: The base URL of the job board (default is Indeed).
*   `SEARCH_QUERY`: The job title or keywords to search for.
*   `LOCATION`: The desired job location.
*   `MAX_PAGES`: The maximum number of search result pages to scrape.
*   `OUTPUT_DIR`, `OUTPUT_FILENAME_CSV`, `OUTPUT_FILENAME_JSON`: Define where the output data files are saved.
*   `LOG_DIR`, `LOG_FILENAME`, `LOG_LEVEL`: Configure logging behavior.
*   `HEADLESS_BROWSE`: Set to `True` to run Chrome without a visible browser window (recommended for servers/automation), `False` to watch the browser operate.
*   `REQUEST_DELAY`: Time delay (in seconds) between page loads to be polite to the server.

## Usage

Navigate to the project's root directory (`advanced_job_scraper/`) in your terminal (ensure your virtual environment is activated) and run the main script:

```bash
python main.py
```

The scraper will start, initializing the WebDriver, navigating to the configured job board, performing the search, iterating through pages, parsing job listings, and saving the results.

*   **Output Data**: Check the `data/` directory for `job_postings.csv` and `job_postings.json` files containing the scraped information.
*   **Logs**: Check the `logs/` directory for `scraper.log` which contains detailed information about the scraping process, including any errors or warnings encountered.

## Code Explanation

*   **`main.py`**: Orchestrates the scraping process. It initializes logging, creates a `JobScraper` instance, calls the scraping method, saves the results using utility functions, and handles WebDriver cleanup.
*   **`scraper.py`**: Contains the `JobScraper` class. It manages the Selenium WebDriver setup, builds search URLs, controls the browser to navigate pages, retrieves page source, calls the parser, and handles pagination logic and basic error handling during navigation.
*   **`parser.py`**: Includes functions (`parse_job_listings`, `find_next_page_url`) that take HTML content as input and use BeautifulSoup to find and extract relevant data points (job title, company, etc.) and pagination links. It uses specific but adaptable selectors.
*   **`utils.py`**: Provides helper functions for common tasks like setting up the logging configuration (`setup_logging`) and saving the collected data to CSV (`save_to_csv`) and JSON (`save_to_json`) formats.
*   **`config.py`**: Acts as a central place for all configurable parameters, making it easy to adjust the scraper without modifying the core logic.

## Error Handling & Logging

The scraper incorporates `try-except` blocks to handle potential issues like page load timeouts, inability to find elements, or network errors. The `logging` module is configured in `utils.py` to record the scraper's progress and any issues encountered. Logs are outputted to both the console and a file (`logs/scraper.log`), with the level of detail configurable in `config.py`.

## Potential Improvements / Future Work

*   **Detailed Job Page Scraping**: Extend the parser and scraper to navigate into individual job posting URLs and extract the full job description or other details.
*   **Support for More Job Boards**: Refactor the parser and configuration to handle the different HTML structures and URL schemes of other websites (e.g., LinkedIn, Glassdoor).
*   **Database Integration**: Store scraped data in a database (e.g., SQLite, PostgreSQL) instead of flat files for better querying and management.
*   **Proxy Rotation / User-Agent Spoofing**: Implement techniques to avoid IP bans or detection when scraping at scale.
*   **GUI Interface**: Develop a simple graphical user interface (e.g., using Tkinter, PyQt) for easier configuration and execution.
*   **Advanced Anti-Scraping Bypass**: Incorporate more sophisticated methods to handle CAPTCHAs or advanced JavaScript challenges if encountered.
*   **Asynchronous Scraping**: Utilize libraries like `asyncio` and `aiohttp` or `httpx` for potentially faster scraping (though Selenium integration can be complex).



