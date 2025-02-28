import os
from playwright.sync_api import sync_playwright

class WebToPDF:
    def __init__(self):
        self.playwright = sync_playwright().start()
        cache_dir = os.path.join(os.getcwd(), "playwright_cache")
        os.makedirs(cache_dir, exist_ok=True)
        self.browser = self.playwright.chromium.launch_persistent_context(
            user_data_dir=cache_dir,
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

    def save_page_as_pdf(self, url):
        page = None
        try:
            page = self.browser.new_page()
            print("[+] Processing the URL Please wait ...")
            page.goto(url, wait_until="networkidle", timeout=30000)

            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{output_dir}/{url.replace('https://', '').replace('/', '_')}.pdf"
            page.pdf(
                path=filename,
                format="A4",
                print_background=True
            )
            print(f"[✔] Print saved : {filename}")

        except Exception as e:
            print(f"[!] Error in processing {url}: {e}")
        finally:
            if page:
                page.close()

    def close_browser(self):
        try:
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            print(f"[!] Error in closing the browser {e}")

if __name__ == "__main__":
    input_url = input('[+] Please provide the URL you want : ')
    web2pdf = WebToPDF()
    urls = []
    urls.append(input_url)

    for url in urls:
        web2pdf.save_page_as_pdf(url)

    web2pdf.close_browser()