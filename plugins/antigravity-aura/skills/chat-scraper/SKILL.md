---
name: chat-scraper
description: Complete workflows for scraping and ingesting external Gemini web chats using Chrome DevTools MCP or Python ingestion scripts.
---

# Chat Scraper Workflow

This skill outlines how to ingest external AI conversations (e.g., Gemini web interface) into the Aura Chronicle.

## 1. Automated Web Scraping (Python Playwright)

If the user requests an automated sync of their recent web chats, utilize the Python ingestion engine:

```bash
python -m core.cli.main ingest --source browser
```
*Note: This utilizes `core/ingestion/browser_scraper.py` which must be properly configured with browser session cookies/auth.*

## 2. Manual Export Ingestion (JSON/Markdown)

If the user exports their Gemini chat history as a zip or raw JSON/MD files:
1. Place the raw export files into `Chronicle/raw_exports/`.
2. Run the chat importer:
   ```bash
   python -m core.cli.main import --path Chronicle/raw_exports/
   ```
3. The importer (`core/ingestion/raw_chat_importer.py`) will parse the JSON, extract the model and user steps, and generate standardized `XG###.md` transcripts in `Chronicle/chat_files/`.

## 3. Chrome DevTools MCP (Active Scraping)

If Antigravity needs to actively scrape a currently open browser window containing a chat:
1. Ensure Chrome is running with remote debugging enabled (`--remote-debugging-port=9222`).
2. Use the `chrome-devtools-mcp` tools:
   - Call `list_pages` to find the Gemini chat tab.
   - Call `evaluate_script` on that tab to extract the DOM elements containing the `.user-message` and `.model-message` texts.
3. Manually construct the standard transcript format and save it via `write_file` to `Chronicle/chat_files/`.

## 4. Post-Ingestion Processing

After any scraping workflow:
- The Heartbeat agent MUST run to summarize the new transcript and append the TL;DR to `Chronicle/chat_log.md`.
- Extract any notable tags and update `Context/Topics.md`.
