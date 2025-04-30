from DrissionPage import Chromium, ChromiumOptions
from lxml import etree
import time
from get_ip import get_ip
import requests


def is_proxy_working(ip, port):
    """Check if proxy is working by making a test request."""
    try:
        proxy = {"http": f"http://{ip}:{port}", "https": f"http://{ip}:{port}"}
        response = requests.get("http://ip.900cha.com/", proxies=proxy, timeout=10)
        return True
    except Exception:
        return False


def process_url(url, ip, port):
    """Process a single URL with the given proxy settings."""
    filename = url[len("https://www.malacards.org/card/"):]
    print(f"Processing: {filename}")

    co = ChromiumOptions()
    co.set_proxy(f"{ip}:{port}")
    driver = Chromium(co)

    try:
        tab = driver.latest_tab
        tab.get(url)

        # Initial delay only on first run
        if not hasattr(process_url, 'initial_delay_done'):
            time.sleep(16)
            process_url.initial_delay_done = True
        else:
            time.sleep(1.5)

        # Try to click all selectors
        selectors = [
            'x://select[@name="Genes_Related_length"]/option[4]',
            'x://select[@name="Phenotypes_Human_length"]/option[4]',
            'x://select[@name="Disorders_Related_length"]/option[4]',
        ]

        success_count = 0
        for selector in selectors:
            try:
                tab.ele(selector, timeout=1).click()
                success_count += 1
                time.sleep(0.8)
            except Exception:
                continue

        print(f"Successfully clicked {success_count} out of {len(selectors)} dropdowns")

        # Save the processed HTML
        html = tab.run_js('return document.body.innerHTML;')
        tree = etree.HTML(html)

        # Remove card navigation if present
        card = tree.xpath('//*[@id="card-nav"]')
        if card:
            card[0].getparent().remove(card[0])

        with open(f'result/{filename}.html', 'w', encoding='utf-8') as f:
            f.write(etree.tostring(tree, method='html', encoding='unicode'))

        return True

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False
    finally:
        driver.quit()


def dowload_html(filename:  str,is_proxy=False, proxy_ip=None, proxy_port=None,proxy_api=None):
    """

    :param filename: 文件路径
    :param is_proxy: 第一次爬虫是否需要代理，如果为False，那么proxy_ip 和 proxy_port就必须填
    :param proxy_ip: 代理ip
    :param proxy_port: 代理端口
    :param proxy_api: 提取代理的API(http/https)
    :return:
    """
    """Main function to process all URLs from the file."""
    # Initialize proxy
    if is_proxy:
        ip, port = get_ip(proxy_api)
    else:
        ip, port = proxy_ip, proxy_port
    if not is_proxy_working(ip, port):
        print("Initial proxy not working, getting new one...")
        ip, port = get_ip(proxy_api)

    processed_count = 0

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()

            if not url or url.startswith('#'):
                print(f"Skipping: {url}")
                continue

            max_retries = 3
            for attempt in range(max_retries):
                success = process_url(url, ip, port)
                if success:
                    processed_count += 1
                    break
                else:
                    print(f"Attempt {attempt + 1} failed for {url}")
                    if attempt < max_retries - 1:
                        print("Getting new proxy...")
                        ip, port = get_ip(proxy_api)
                        while not is_proxy_working(ip, port):
                            print("Proxy not working, trying another...")
                            ip, port = get_ip(proxy_api)
            else:
                print(f"Failed to process {url} after {max_retries} attempts")

            # Rotate proxy every 2 successful requests
            if processed_count > 0 and processed_count % 2 == 0:
                print("Rotating proxy...")
                ip, port = get_ip(proxy_api)
                while not is_proxy_working(ip, port):
                    print("New proxy not working, trying another...")
                    ip, port = get_ip(proxy_api)

    print(f"Processing complete. Total pages processed: {processed_count}")


if __name__ == "__main__":
    dowload_html()