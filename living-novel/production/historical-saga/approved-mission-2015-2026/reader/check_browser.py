"""Optional local Chromium smoke check; no service or network access required."""
import hashlib
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
page_file = HERE / "index.html"
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which("chromium"), headless=True,
                                args=["--no-sandbox"])
    for name, size in (("desktop", {"width": 1280, "height": 900}),
                       ("mobile", {"width": 390, "height": 844})):
        page = browser.new_page(viewport=size)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route("http://**/*", lambda route: route.abort())
        page.route("https://**/*", lambda route: route.abort())
        page.goto(page_file.as_uri(), wait_until="load")
        assert page.title() == "Commonwealth saga — draft reading room"
        assert page.locator("article").count() > 0
        overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        assert not overflow, f"Horizontal overflow on {name}"
        page.locator('nav a[href="#manuscript-1"]').click()
        assert page.url.endswith("#manuscript-1")
        page.locator('article a[href="#contents"]').first.click()
        assert page.url.endswith("#contents")
        assert errors == []
        results.append({"viewport": name, "size": size, "article_count": page.locator("article").count(),
                        "horizontal_overflow": overflow, "anchor_navigation": "PASS", "page_errors": errors})
        page.close()
    browser.close()
receipt = {"status": "TECHNICAL_BROWSER_SMOKE_PASS_NOT_EDITORIAL_ACCEPTANCE",
           "browser": "Installed Chromium via Playwright; local file; HTTP(S) blocked",
           "reader_sha256": hashlib.sha256(page_file.read_bytes()).hexdigest(),
           "checks": results,
           "limits": "No exhaustive accessibility, cross-browser, visual design or literary certification."}
(HERE / "BROWSER_CHECK.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
