import asyncio
import logging
import os
import json
from dotenv import load_dotenv
from band import Agent
from band.adapters.pydantic_ai import PydanticAIAdapter
from band.config import load_agent_config
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.scraper import scrape_eur_lex, scrape_sec_rss, get_mock_regulation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get real regulation data
def get_latest_regulation() -> str:
    logger.info("🔍 Scraping latest regulations...")
    regs = scrape_eur_lex()
    if not regs:
        regs = [get_mock_regulation()]
    reg = regs[0]
    return json.dumps(reg, indent=2)

LATEST_REG = get_latest_regulation()

MONITOR_SYSTEM_PROMPT = f"""
You are ReguMonitor, a regulatory monitoring agent in the ReguTrack compliance system.

You have just detected this new regulation from live sources:

{LATEST_REG}

Your responsibilities:
1. Report this regulation clearly to the room
2. Share the structured JSON data above
3. Always end your message by @mentioning @ReguAnalyzer to begin impact analysis

Be concise and professional. You are part of a 4-agent compliance pipeline.
"""

async def main():
    load_dotenv()

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    adapter = PydanticAIAdapter(
        model="openai-chat:google/gemma-4-31b-it:free",
        system_prompt=MONITOR_SYSTEM_PROMPT,
    )

    agent_id, api_key = load_agent_config("regu_monitor")
    agent = Agent.create(adapter=adapter, agent_id=agent_id, api_key=api_key)

    logger.info("🔍 ReguMonitor Agent is running...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())