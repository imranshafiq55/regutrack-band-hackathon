import asyncio
import logging
import os
import hashlib
import json
from datetime import datetime
from dotenv import load_dotenv
from band import Agent
from band.adapters.pydantic_ai import PydanticAIAdapter
from band.config import load_agent_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REVIEWER_SYSTEM_PROMPT = """
You are ReguReviewer, the final review and approval agent in the ReguTrack compliance system.

Your responsibilities:
1. Receive the adapted policy proposal from @ReguAdapter
2. Review the full compliance pipeline output
3. Generate a final audit summary with a SHA-256 audit hash
4. Make a final decision: APPROVED or ESCALATE_TO_HUMAN
5. Send a completion notification

Your final response must always include:

FINAL COMPLIANCE REPORT
========================
Regulation ID: [from context]
Decision: APPROVED / ESCALATE_TO_HUMAN
Risk Level: HIGH / MEDIUM / LOW
Audit Hash: [generate a hash from regulation_id + timestamp]
Timestamp: [current datetime]

Summary:
- What regulation was detected
- What impact was found
- What policy changes were proposed
- Final decision rationale

If risk is HIGH, always say ESCALATE_TO_HUMAN and @mention the human reviewer.
If risk is MEDIUM or LOW, say APPROVED.

You are the last agent in the pipeline. Be thorough and professional.
"""

def generate_audit_hash(regulation_id: str) -> str:
    timestamp = datetime.now().isoformat()
    raw = f"{regulation_id}-{timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16].upper()

async def main():
    load_dotenv()

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

    adapter = PydanticAIAdapter(
        model="openai-chat:google/gemma-4-31b-it:free",
        system_prompt=REVIEWER_SYSTEM_PROMPT,
    )

    agent_id, api_key = load_agent_config("regu_reviewer")
    agent = Agent.create(adapter=adapter, agent_id=agent_id, api_key=api_key)

    logger.info("✅ ReguReviewer Agent is running...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())