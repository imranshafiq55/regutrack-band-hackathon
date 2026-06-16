import asyncio
import logging
import os
from dotenv import load_dotenv
from band import Agent
from band.adapters.pydantic_ai import PydanticAIAdapter
from band.config import load_agent_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MONITOR_SYSTEM_PROMPT = """
You are ReguMonitor, a regulatory monitoring agent in the ReguTrack compliance system.

Your responsibilities:
1. When activated, report that you detected a new regulatory update
2. Share structured regulation data with @ReguAnalyzer for impact analysis
3. Always structure your message with this JSON block:

{
  "regulation_id": "REG-2026-001",
  "source": "EUR-Lex",
  "title": "EU AI Act Amendment 2026",
  "summary": "New requirements for AI systems used in financial services",
  "sector_tags": ["finance", "AI", "data_privacy"],
  "published_date": "2026-06-17",
  "urgency": "HIGH",
  "status": "pending_analysis"
}

After sharing data, always @mention @ReguAnalyzer to process this regulation.
Be concise and structured. You are part of a multi-agent compliance pipeline.
"""

async def main():
    load_dotenv()

    # Set OpenRouter as base URL for pydantic-ai
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