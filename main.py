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
            print(f"[↺] Processing URL: {url}")
            page.goto(url, wait_until="networkidle", timeout=30000)

            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)

            # Extract page title
            page_title = page.title()
            words = page_title.split()[:10]  # Take the first 10 words
            clean_title = "_".join(words).replace("/", "_").replace("\\", "_")
            filename = f"{output_dir}/{clean_title}.pdf"

            # Save as PDF
            page.pdf(
                path=filename,
                format="A4",
                print_background=True
            )
            print(f"[✔] PDF saved: {filename}")

        except Exception as e:
            print(f"[!] Error processing {url}: {e}")
        finally:
            if page:
                page.close()

    def close_browser(self):
        try:
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            print(f"[!] Error closing the browser: {e}")

if __name__ == "__main__":
    web2pdf = WebToPDF()
    urls = []

    print("• Please enter your desired URL (and use 'exit' to start processing).")
    
    while True:
        url = input("[+] Enter a URL: ").strip()
        if url.lower() == 'exit':
            break
        if url:  # Ensure empty input is not added
            urls.append(url)

    if not urls:
        print("[x] No URLs provided. Exiting.")
        web2pdf.close_browser()
        exit()

    for url in urls:
        web2pdf.save_page_as_pdf(url)

    web2pdf.close_browser()
