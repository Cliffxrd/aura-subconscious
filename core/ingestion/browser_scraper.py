import asyncio
import logging
from typing import Dict, Any, Optional

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger(__name__)

class BrowserScraper:
    """Interactive Playwright-based web scraper workflow for chat ingestion."""
    
    def __init__(self, headless: bool = True):
        self.active = False
        self.headless = headless
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright is not installed. BrowserScraper will be limited.")
        
    async def _scrape_impl(self, url: str, wait_selector: Optional[str] = None) -> Dict[str, Any]:
        """Internal asynchronous Playwright scraping logic."""
        if not PLAYWRIGHT_AVAILABLE:
            return {"status": "error", "message": "Playwright not installed"}
            
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Aura/BrowserScraper (Automated)"
            )
            page = await context.new_page()
            
            try:
                response = await page.goto(url, wait_until="networkidle", timeout=30000)
                if not response or not response.ok:
                    await browser.close()
                    return {"status": "error", "message": f"Failed to load {url}", "code": response.status if response else None}
                
                if wait_selector:
                    await page.wait_for_selector(wait_selector, timeout=10000)
                    
                html_content = await page.content()
                text_content = await page.evaluate("document.body.innerText")
                title = await page.title()
                
                return {
                    "status": "success", 
                    "url": url, 
                    "title": title,
                    "html_length": len(html_content),
                    "text_content": text_content[:5000] + ("..." if len(text_content) > 5000 else ""),
                    "full_html": html_content
                }
                
            except PlaywrightTimeoutError:
                return {"status": "error", "message": f"Timeout waiting for {url}"}
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                return {"status": "error", "message": str(e)}
            finally:
                await browser.close()

    def start_scraping(self, url: str, wait_selector: Optional[str] = None) -> Dict[str, Any]:
        """Synchronous wrapper around the async scraping workflow."""
        self.active = True
        try:
            return asyncio.run(self._scrape_impl(url, wait_selector))
        finally:
            self.active = False
