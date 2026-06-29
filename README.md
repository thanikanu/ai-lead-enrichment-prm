# ai-lead-enrichment-prm
# AI Lead Enrichment & PRM Engine

A# AI Lead Enrichment & PRM Engine

A multi-step agentic pipeline built with the **Claude API** and **Python** that automates B2B lead enrichment, scoring, and outreach — turning a raw lead list into a fully qualified, CRM-ready dataset in seconds.

## What it does

Given a raw lead with just a company name, contact, and email, the pipeline runs through four sequential AI steps:

1. **Enrichment** — Claude researches and fills in firmographic data: industry, company size, estimated employees, and location.
2. **Scoring** — Each lead is scored 0–100 against a defined ideal customer profile and classified into a tier: Hot, Warm, or Cold.
3. **Assignment** — Leads are automatically routed to the appropriate sales rep based on their tier.
4. **Outreach generation** — Claude writes a personalized outreach email and a full email drip cadence (timing and messaging) tailored to the lead's tier and industry.

The pipeline outputs:
- A clean Excel file with every lead fully enriched and ready to import into a CRM
- A visual HTML dashboard summarizing all leads, scores, and outreach content at a glance

## Why this exists

Manual lead research and qualification typically takes 30–60 minutes per lead. This pipeline does it in seconds, using Claude as the reasoning layer instead of a human doing repetitive research and judgment calls.

## Tech stack

- **Claude API (Anthropic)** — enrichment, scoring, email generation, and cadence planning
- **Python** — pipeline orchestration
- **Pandas / OpenPyXL** — Excel input/output handling
- **python-dotenv** — environment variable management
- **HTML/CSS** — auto-generated visual dashboard

## Setup

### 1. Clone this repo

```
git clone https://github.com/your-username/ai-lead-enrichment-prm.git
cd ai-lead-enrichment-prm
```

### 2. Install dependencies

```
pip install anthropic pandas openpyxl python-dotenv
```

### 3. Create your `.env` file

Copy the provided template and rename it:

```
cp .env.example .env
```

Open the new `.env` file and fill in your own values:

```
ANTHROPIC_API_KEY=your-anthropic-api-key-here
DEMO_FOLDER=.
```

- **ANTHROPIC_API_KEY** — your personal API key from console.anthropic.com. Required for the pipeline to run.
- **DEMO_FOLDER** — the folder where input/output files are read from and saved to. Leave as `.` to use the current project folder, or set it to a full path (e.g. `/Users/yourname/Documents/leads-demo`) if you want files saved somewhere else.

Both `create_leads.py` and `mitrex_demo.py` read these two values automatically from this single `.env` file — there is nothing else to configure.

**Important:** never commit your real `.env` file to GitHub. It is already excluded via `.gitignore`.

### 4. Generate sample input data

```
python create_leads.py
```

This creates `mitrex_leads_input.xlsx` inside your `DEMO_FOLDER`, populated with five sample leads.

### 5. Run the pipeline

```
python mitrex_demo.py
```

This processes every lead in the input file, saves an enriched `mitrex_leads_output.xlsx`, and automatically opens a visual HTML dashboard (`mitrex_output.html`) in your browser.

## Customizing your own leads

To use your own leads instead of the sample data, either:
- Edit the `leads_data` dictionary inside `create_leads.py`, or
- Replace `mitrex_leads_input.xlsx` directly with your own spreadsheet, as long as it has the same column headers: `Company`, `Contact`, `Email`, `Notes`

## Notes

This was built as a proof of concept for a real-world use case: showing how a small business could plug AI directly into their sales pipeline with minimal infrastructure. In production, the input leads would come from a source like Apollo, Clay, or a CRM export rather than a static file — the rest of the pipeline would work unchanged.

## Author

Built by Thanikan Umagaran — LinkedIn: linkedin.com/in/thanikan
