import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_eur_lex() -> list[dict]:
    """Scrape EUR-Lex RSS for latest EU regulations"""
    url = "https://eur-lex.europa.eu/rss/rss-new-reg.xml"
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        items = soup.find_all("item")[:5]
        results = []
        for item in items:
            results.append({
                "regulation_id": f"REG-{datetime.now().strftime('%Y%m%d')}-{len(results)+1:03}",
                "source": "EUR-Lex",
                "title": item.find("title").text if item.find("title") else "Unknown",
                "summary": item.find("description").text[:300] if item.find("description") else "",
                "url": item.find("link").text if item.find("link") else "",
                "published_date": datetime.now().strftime("%Y-%m-%d"),
                "sector_tags": ["finance", "data_privacy"],
                "urgency": "MEDIUM",
                "status": "pending_analysis"
            })
        return results
    except Exception as e:
        return [get_mock_regulation()]

def scrape_sec_rss() -> list[dict]:
    """Scrape SEC RSS for latest financial regulations"""
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=&dateb=&owner=include&count=5&search_text=&output=atom"
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "ReguTrack/1.0"})
        soup = BeautifulSoup(r.content, "xml")
        entries = soup.find_all("entry")[:3]
        results = []
        for entry in entries:
            results.append({
                "regulation_id": f"SEC-{datetime.now().strftime('%Y%m%d')}-{len(results)+1:03}",
                "source": "SEC",
                "title": entry.find("title").text if entry.find("title") else "Unknown",
                "summary": entry.find("summary").text[:300] if entry.find("summary") else "",
                "url": entry.find("id").text if entry.find("id") else "",
                "published_date": datetime.now().strftime("%Y-%m-%d"),
                "sector_tags": ["finance", "securities"],
                "urgency": "HIGH",
                "status": "pending_analysis"
            })
        return results
    except Exception as e:
        return [get_mock_regulation()]

def get_mock_regulation() -> dict:
    """Fallback mock regulation for demo"""
    return {
        "regulation_id": "REG-2026-DEMO-001",
        "source": "EUR-Lex",
        "title": "EU AI Act Amendment 2026 - Financial Services",
        "summary": "New requirements for AI systems used in financial services. All AI models must be registered, audited, and approved by Q3 2026. Companies must maintain full audit trails.",
        "published_date": "2026-06-17",
        "sector_tags": ["finance", "AI", "data_privacy"],
        "urgency": "HIGH",
        "status": "pending_analysis"
    }