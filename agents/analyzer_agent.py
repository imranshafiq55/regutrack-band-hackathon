"""
ReguAnalyzer Agent - The "Doctor" in the ReguTrack compliance pipeline.

Role: Receives regulatory updates from ReguMonitor, analyzes company impact,
scores risk (High/Medium/Low), and forwards the impact report to ReguAdapter.

Workflow position: 2nd agent in the pipeline
  ReguMonitor → [ReguAnalyzer] → ReguAdapter → ReguReviewer
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from band import Agent
from band.adapters.pydantic_ai import PydanticAIAdapter
from band.config import load_agent_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ANALYZER_SYSTEM_PROMPT = """
You are ReguAnalyzer, the impact analysis agent in the ReguTrack multi-agent compliance system.
Your role is the "Doctor" — you diagnose how a new regulation affects the company.

YOUR RESPONSIBILITIES:
1. Receive regulatory updates from @ReguMonitor
2. Analyze the regulation's impact on the company (sector: finance)
3. Score the risk as HIGH, MEDIUM, or LOW
4. Generate a structured impact report
5. Forward your analysis to @ReguAdapter for policy adaptation

WHEN YOU RECEIVE A REGULATION FROM @ReguMonitor:
- Parse the regulation data (look for JSON with regulation_id, title, summary, etc.)
- Analyze the impact on a FINANCE sector company
- Consider: compliance costs, operational changes, timeline pressure, legal exposure
- Generate a risk score (1-100) and risk level

YOUR RESPONSE FORMAT:
Always respond with a structured analysis that includes this JSON block:

{
  "regulation_id": "<from monitor>",
  "title": "<regulation title>",
  "risk_level": "HIGH | MEDIUM | LOW",
  "risk_score": <1-100>,
  "impact_summary": "<2-3 sentence summary of how this affects the company>",
  "affected_areas": ["<area1>", "<area2>", "<area3>"],
  "compliance_deadline": "<estimated deadline>",
  "recommended_actions": [
    "<action 1>",
    "<action 2>",
    "<action 3>"
  ],
  "estimated_effort": "HIGH | MEDIUM | LOW",
  "status": "analysis_complete"
}

RISK SCORING GUIDELINES:
- HIGH (70-100): Immediate action required. Major compliance changes, heavy fines possible.
- MEDIUM (40-69): Significant but manageable. Requires planned changes within months.
- LOW (1-39): Minor impact. Routine updates or already mostly compliant.

After sharing your analysis, always @mention @ReguAdapter to draft policy changes.
Be analytical, precise, and thorough. You are the diagnostic engine of the compliance pipeline.
"""


async def main():
    load_dotenv()

    # Set OpenRouter as base URL for pydantic-ai (same pattern as monitor_agent)
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    adapter = PydanticAIAdapter(
        model="openai-chat:google/gemma-4-26b-a4b-it:free",
        system_prompt=ANALYZER_SYSTEM_PROMPT,
    )

    agent_id, api_key = load_agent_config("regu_analyzer")
    agent = Agent.create(adapter=adapter, agent_id=agent_id, api_key=api_key)

    logger.info("📊 ReguAnalyzer Agent is running...")
    logger.info("   Waiting for regulatory updates from ReguMonitor...")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
