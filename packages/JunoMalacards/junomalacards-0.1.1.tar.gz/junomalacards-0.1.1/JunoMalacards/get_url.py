from DrissionPage import Chromium
from lxml import etree
import time


def extract_ncbi_links(target_url, output_file='url.txt'):
    """
    Extract all toc-item links from an NCBI page and save them to a file.

    Args:
        target_url (str): The URL of the NCBI page to scrape
        output_file (str): File to save the extracted links
    """
    print(f"Starting extraction from: {target_url}")

    # Initialize browser
    driver = Chromium()
    try:
        tab = driver.latest_tab

        # Load the target page
        print("Loading page...")
        tab.get(target_url)
        time.sleep(5)  # Wait for page to load

        # Get page HTML
        html = tab.run_js('return document.body.innerHTML;')
        tree = etree.HTML(html)

        # Extract all toc-item links
        print("Extracting links...")
        hrefs = tree.xpath('//a[contains(@class, "toc-item")]/@href')

        if not hrefs:
            print("Warning: No links found with the specified selector")
            return

        # Construct full URLs
        base_url = 'https://www.ncbi.nlm.nih.gov/'
        full_urls = [base_url + href if not href.startswith('http') else href
                     for href in hrefs]

        # Print results
        print(f"\nFound {len(full_urls)} links:")
        for url in full_urls[:5]:  # Print first 5 as sample
            print(f"  {url}")
        if len(full_urls) > 5:
            print(f"  ... and {len(full_urls) - 5} more")

        # Save to file
        print(f"\nSaving links to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(full_urls))

        print("Extraction completed successfully")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Ensure browser is closed
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    # Example usage
    target_url = 'https://www.ncbi.nlm.nih.gov/books/NBK1116/'
    extract_ncbi_links(target_url)