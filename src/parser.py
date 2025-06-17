import logging
from bs4 import BeautifulSoup
import re

# These might need adjustment based on the specific website structure and changes over time.

def parse_job_listings(html_content):
    """Parses the main job listings page to extract individual job links or basic info.

    Args:
        html_content (str): The HTML content of the search results page.

    Returns:
        list: A list of dictionaries, each containing basic info for a job found on the page.
              (e.g., title, company, location, summary snippet, URL)
    """
    soup = BeautifulSoup(html_content, \'html.parser\")
    job_cards = soup.find_all(\"div\", class_=re.compile(r\"job_\")) # Example selector, adjust as needed
    # Alternative: soup.select(\"[data-tn-component=\"jobHeader\"]\") or similar specific selectors

    jobs_data = []
    if not job_cards:
        # Try finding job cards using a more general approach if specific classes fail
        job_cards = soup.find_all(lambda tag: tag.name == \"div\" and tag.has_attr(\"class\") and any(\"job\" in cls for cls in tag[\"class\"])) 
        # Add more fallback selectors if necessary
        if not job_cards:
            logging.warning(\"Could not find job card elements using primary or secondary selectors.\")
            # Look for clickable links that might be jobs
            job_links = soup.find_all(\"a\", href=re.compile(r\"/rc/clk|/clk|/viewjob\", re.IGNORECASE))
            if job_links:
                logging.info(f\"Found {len(job_links)} potential job links as fallback.\")
                # Simplified extraction if only links are found
                for link in job_links:
                    job_title = link.get_text(strip=True) or \"N/A\"
                    job_url = link.get(\"href\")
                    # Attempt to construct absolute URL if relative
                    if job_url and not job_url.startswith(\"http\"):
                        # This needs the base URL from config or context, simplified here
                        job_url = f\"https://www.indeed.com{job_url}\" # Example, make dynamic
                    if job_url:
                        jobs_data.append({
                            \"title\": job_title,
                            \"company\": \"N/A\",
                            \"location\": \"N/A\",
                            \"summary\": \"N/A\",
                            \"date_posted\": \"N/A\",
                            \"url\": job_url
                        })
                return jobs_data
            else:
                logging.error(\"Failed to find any job card elements or potential job links.\")
                return []

    logging.info(f"Found {len(job_cards)} potential job card elements.")

    for card in job_cards:
        try:
            title_element = card.find(\"h2\", class_=re.compile(r\"title\", re.IGNORECASE)) or card.find(\"a\", attrs={\"data-jobid\": True})
            job_title = title_element.get_text(strip=True) if title_element else \"N/A\"

            company_element = card.find(\"span\", class_=re.compile(r\"company\", re.IGNORECASE))
            job_company = company_element.get_text(strip=True) if company_element else \"N/A\"

            location_element = card.find(\"div\", class_=re.compile(r\"location\", re.IGNORECASE)) or card.find(\"span\", class_=re.compile(r\"location\", re.IGNORECASE))
            job_location = location_element.get_text(strip=True) if location_element else \"N/A\"

            summary_element = card.find(\"div\", class_=re.compile(r\"summary\", re.IGNORECASE))
            job_summary = summary_element.get_text(strip=True) if summary_element else \"N/A\"

            date_element = card.find(\"span\", class_=re.compile(r\"date\", re.IGNORECASE))
            job_date = date_element.get_text(strip=True) if date_element else \"N/A\"

            url_element = card.find(\"a\", href=True)
            job_url = url_element[\"href\"] if url_element else \"N/A\"
            # Construct absolute URL if relative (Example for Indeed)
            if job_url.startswith(\"/\"):
                job_url = f\"https://www.indeed.com{job_url}\"

            if job_title != \"N/A\" and job_url != \"N/A\": # Basic validation
                jobs_data.append({
                    \"title\": job_title,
                    \"company\": job_company,
                    \"location\": job_location,
                    \"summary\": job_summary,
                    \"date_posted\": job_date,
                    \"url\": job_url
                })
            else:
                logging.debug(f\"Skipping card due to missing title or URL: {card.prettify()[:200]}...\")

        except Exception as e:
            logging.warning(f\"Error parsing a job card: {e}. Card content: {card.prettify()[:200]}...\")
            continue

    logging.info(f"Successfully parsed {len(jobs_data)} job listings from the page.")
    return jobs_data

def parse_job_details(html_content):
    """Parses the detailed job description page.

    Args:
        html_content (str): The HTML content of the job details page.

    Returns:
        dict: A dictionary containing detailed job information (e.g., full description).
              This can be expanded to extract more specific details if needed.
    """
    soup = BeautifulSoup(html_content, \'html.parser\")
    details = {}

    # Example: Extracting the full job description
    # Adjust selector based on the target website
    description_container = soup.find(\"div\", id=re.compile(r\"jobDescriptionText\", re.IGNORECASE)) or soup.find(\"div\", class_=re.compile(r\"description\", re.IGNORECASE))
    if description_container:
        details[\"full_description\"] = description_container.get_text(separator=\"\\n\", strip=True)
    else:
        details[\"full_description\"] = \"N/A\"
        logging.warning(\"Could not find job description container.\")

    # Add more parsing logic here to extract other details like:
    # - Salary information
    # - Job type (full-time, part-time)
    # - Specific requirements or qualifications
    # Example (highly site-specific):
    # salary_element = soup.find(\"span\", class_=\"salary-snippet\")
    # details[\"salary\"] = salary_element.get_text(strip=True) if salary_element else \"N/A\"

    logging.info(f"Parsed job details. Description length: {len(details.get(\"full_description\", \"\"))}")
    return details

def find_next_page_url(html_content, base_url):
    """Finds the URL for the next page of search results.

    Args:
        html_content (str): The HTML content of the current search results page.
        base_url (str): The base URL of the job site (e.g., https://www.indeed.com)

    Returns:
        str or None: The URL of the next page, or None if not found.
    """
    soup = BeautifulSoup(html_content, \'html.parser\")
    # Common patterns for \"Next\" links
    next_link = soup.find(\"a\", attrs={\"aria-label\": \"Next\"}) or \
                soup.find(\"a\", string=re.compile(r\"Next\", re.IGNORECASE)) or \
                soup.find(\"link\", rel=\"next\")

    if next_link and next_link.get(\"href\"):
        next_href = next_link[\"href\"]
        if next_href.startswith(\"/\"):
            # Ensure no double slashes if base_url ends with /
            next_url = f\"{base_url.rstrip(\"/\")}{next_href}\"
        elif next_href.startswith(\"http\"):
            next_url = next_href
        else:
            # Handle potentially relative paths differently if needed
            logging.warning(f\"Found potentially relative next page link: {next_href}. Attempting to join with base URL.\")
            next_url = f\"{base_url.rstrip(\"/\")}/{next_href.lstrip(\"/\")}\" # Basic joining

        logging.info(f"Found next page URL: {next_url}")
        return next_url
    else:
        logging.info(\"No next page link found.\")
        return None

