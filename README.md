# ai-lead-enrichment-prm
# AI Lead Enrichment & PRM Engine

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
- **HTML/CSS** — auto-generated visual dashboard

## Setup

1. Clone this repo
2. Install dependencies:
   ```
   pip install anthropic pandas openpyxl
   ```
3. Set your Anthropic API key as an environment variable:
   ```
   export ANTHROPIC_API_KEY="your-key-here"
   ```
4. Generate sample input data:
   ```
   python create_leads.py
   ```
5. Run the pipeline:
   ```
   python mitrex_demo.py
   ```

The script will process all leads in the input file, save an enriched Excel output, and automatically open a visual HTML dashboard in your browser.

## Notes

This was built as a proof of concept for a real-world use case: showing how a small business could plug AI directly into their sales pipeline with minimal infrastructure. In production, the input leads would come from a source like Apollo, Clay, or a CRM export rather than a static file — the rest of the pipeline would work unchanged.

## Author

Built by Thanikan Umagaran — [LinkedIn](https://www.linkedin.com/in/thanikan)
