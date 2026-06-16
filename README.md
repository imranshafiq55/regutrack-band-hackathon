# ReguTrack 🛡️
### Multi-Agent Regulatory Intelligence & Compliance Orchestrator

Built for the **Band of Agents Hackathon** (June 12–19, 2026) on lablab.ai

---

## 🧠 What is ReguTrack?

ReguTrack is a multi-agent AI system that monitors regulatory changes (GDPR, EU AI Act, SEC rules, etc.) and automatically analyzes their impact on enterprises — using Band as the core agent coordination layer.

**Track:** Track 3 — Regulated & High-Stakes Workflows

---

## 🤖 Agent Architecture

| Agent | Role | Responsibility |
|---|---|---|
| 🔍 ReguMonitor | Watchman | Detects new regulatory updates, posts to Band room |
| 📊 ReguAnalyzer | Doctor | Analyzes company impact, scores risk (High/Medium/Low) |
| 📝 ReguAdapter | Lawyer | Proposes policy changes, generates updated draft documents |
| ✅ ReguReviewer | Manager | Reviews, approves, sends alerts, seals audit trail |

---

## 🔄 Workflow
New Regulation Detected

↓

ReguMonitor → posts to Band room

↓

ReguAnalyzer → impact report + risk score

↓

ReguAdapter → policy draft PDF

↓

ReguReviewer → approval + alert + audit hash

---

## 🏗️ Tech Stack

- **Agent Coordination:** Band SDK 1.0.0
- **LLM:** Google Gemma 4 31B via OpenRouter (free tier)
- **Language:** Python 3.12
- **Data Processing:** Pandas
- **Reports:** fpdf2 (PDF), openpyxl (Excel)
- **Dashboard:** Streamlit
- **Scraping:** BeautifulSoup4, Requests

---

## 🚀 Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/imranshafiq55/regutrack-band-hackathon.git
cd regutrack-band-hackathon
```

### 2. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Fill in your API keys
```

### 4. Configure Band agents
```bash
# Fill agent UUIDs and API keys in agent_config.yaml
```

### 5. Run agents (each in separate terminal)
```bash
python agents/monitor_agent.py
python agents/analyzer_agent.py
python agents/adapter_agent.py
python agents/reviewer_agent.py
```

---

## 📁 Project Structure
regutrack-band-hackathon/

├── agents/

│   ├── monitor_agent.py      # Regulatory monitoring

│   ├── analyzer_agent.py     # Impact analysis

│   ├── adapter_agent.py      # Policy adaptation

│   └── reviewer_agent.py     # Review & approval

├── tools/

│   ├── scraper.py            # RSS/web scraping

│   ├── pdf_generator.py      # PDF report generation

│   └── llm_client.py         # OpenRouter LLM calls

├── agent_config.yaml         # Band agent credentials

├── .env.example              # Environment template

├── requirements.txt

└── README.md

---

## 🏆 Hackathon

- **Event:** Band of Agents Hackathon — lablab.ai
- **Dates:** June 12–19, 2026
- **Team:** Imran Shafique
- **Submission:** lablab.ai